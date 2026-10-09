"""Re-run committed RISK-0025 regression in a fresh localhost-only cluster."""
from pathlib import Path
import os
import subprocess

app = Path('D:/AppDev/mine_flow/Code/mine-flow-app')
scratch = Path('C:/Users/Alpxalpha/AppData/Local/hermes/cache/scratch/step55-security-resume')
scratch.mkdir(exist_ok=True)
bin_dir = Path('C:/Program Files/PostgreSQL/17/bin')
data = scratch / 'pgdata'
log = scratch / 'verification.log'


def run(exe, *args, expected=0):
    """Run a local tool, persist actual output, and enforce its expected status."""
    if exe == 'pg_ctl':
        # A detached Windows postgres can inherit PIPE handles and prevent EOF.
        with (scratch / 'pg_ctl.log').open('a', encoding='utf-8') as handle:
            result = subprocess.run([str(bin_dir / (exe + '.exe')), *map(str, args)], cwd=app, stdout=handle, stderr=handle, timeout=60, text=True)
        result.stdout = result.stderr = ''
    else:
        result = subprocess.run([str(bin_dir / (exe + '.exe')), *map(str, args)], cwd=app, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=120)
    with log.open('a', encoding='utf-8') as out:
        out.write(f'\nCOMMAND {exe} {args}\nEXIT {result.returncode}\n{result.stdout}{result.stderr}')
    print(exe, 'exit', result.returncode)
    if result.returncode != expected:
        print((result.stdout + result.stderr)[-2500:])
        raise RuntimeError(f'{exe} expected {expected}, got {result.returncode}')
    return result


run('initdb', '-D', data, '-U', 'step55_verify', '-A', 'trust', '--encoding=UTF8', '--no-locale')
run('pg_ctl', '-D', data, '-l', scratch / 'postgres.log', '-o', '-h 127.0.0.1 -p 55456', '-w', 'start')
base = ['-X', '-h', '127.0.0.1', '-p', '55456', '-U', 'step55_verify', '-d', 'postgres', '-v', 'ON_ERROR_STOP=1']
try:
    run('psql', *base, '-f', app.parents[1] / 'Upcoming Prompts/step55-remediation/bootstrap_local.sql')
    migration = app / 'supabase/migrations/20261004000001_step_55_user_profile_permissions.sql'
    for path in sorted((app / 'supabase/migrations').glob('*.sql')):
        if path != migration:
            run('psql', *base, '-f', path)
    red = run('psql', *base, '-f', app / 'supabase/tests/user_profile_permissions.sql', expected=3)
    assert 'REGRESSION: crew can self-promote to supervisor' in red.stderr
    run('psql', *base, '-f', migration)
    green = run('psql', *base, '-f', app / 'supabase/tests/user_profile_permissions.sql')
    assert 'PASS: 20 protected-field updates rejected' in green.stderr
    assert 'PASS: trusted server administration preserved' in green.stderr
    check = run('psql', *base, '-At', '-c', "select count(*) from public.users where email like 'step55-%@example.invalid';")
    assert check.stdout.strip() == '0'
    print('RED exploit reproduced; GREEN permissions passed; rollback verified. Evidence:', log)
finally:
    run('pg_ctl', '-D', data, '-m', 'fast', '-w', 'stop')
