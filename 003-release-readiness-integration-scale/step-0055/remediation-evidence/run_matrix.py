"""Serialize STEP-55 matrix runs with secret-safe logs and real exit codes."""
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import threading

ROOT = Path(__file__).parent
APP = ROOT.parents[1] / 'Code' / 'mine-flow-app'


def main():
    """Run only the chosen target; scrub credentials before writing any output."""
    platform, label = sys.argv[1:3]
    values = {}
    for line in (APP / '.env').read_text(encoding='utf-8').splitlines():
        if '=' in line and not line.lstrip().startswith('#'):
            key, value = line.split('=', 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    allowed = ['SUPABASE_URL', 'SUPABASE_ANON_KEY', 'GOOGLE_DRIVE_CLIENT_ID', 'TEST_USER_EMAIL', 'TEST_USER_PASSWORD', 'TEST_SUPERVISOR_EMAIL', 'TEST_SUPERVISOR_PASSWORD', 'TEST_FOREMAN_EMAIL', 'TEST_FOREMAN_PASSWORD', 'TEST_CREW_EMAIL', 'TEST_CREW_PASSWORD']
    assert 'rpdnonpivoyhghzolyzv.supabase.co' in values.get('SUPABASE_URL', ''), 'Unexpected target; owner approved only named test project'
    assert all(values.get(k) for k in allowed[:2] + ['TEST_USER_EMAIL', 'TEST_USER_PASSWORD']), 'Required test defines absent'
    dest = ROOT / label
    dest.mkdir(exist_ok=False)
    env = dict(os.environ, SCREENSHOT_DESTINATION_DIR=str(dest))
    cmd = [shutil.which('flutter'), 'drive', '--no-pub', '--driver=test_driver/integration_test.dart', '--target=integration_test/design_review_capture_test.dart', '-d', 'web-server' if platform == 'web' else 'emulator-5554']
    if platform == 'web':
        cmd += ['--browser-name=chrome']
    cmd += ['--dart-define=APP_ENV=staging'] + ['--dart-define=' + k + '=' + values[k] for k in allowed if values.get(k)]
    secrets = [v for k, v in values.items() if len(v) > 6 and any(t in k for t in ['KEY', 'PASSWORD', 'TOKEN'])]
    all_values = sorted([v for v in values.values() if len(v) > 6], key=len, reverse=True)
    proc = subprocess.Popen(cmd, cwd=APP, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
    timed_out = []
    def stop():
        """Kill only this runner's process tree on bounded timeout."""
        timed_out.append(True)
        subprocess.run(['taskkill', '/PID', str(proc.pid), '/T', '/F'], capture_output=True)
    timer = threading.Timer(1000, stop)
    timer.start()
    secret_leak = False
    try:
        with (ROOT / (label + '.log')).open('w', encoding='utf-8', newline='\n') as log:
            for raw in proc.stdout:
                leaked = any(secret in raw for secret in secrets)
                safe = raw
                for value in all_values:
                    safe = safe.replace(value, '[REDACTED_CONFIG]')
                safe = re.sub(r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+', '[REDACTED_JWT]', safe)
                safe = re.sub(r'[A-Za-z0-9_.+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}', '[REDACTED_EMAIL]', safe)
                log.write(safe)
                log.flush()
                if leaked:
                    secret_leak = True
                    stop()
                    break
            code = proc.wait(timeout=60)
    finally:
        timer.cancel()
    artifacts = []
    for p in sorted(dest.glob('*.png')):
        b = p.read_bytes()
        valid = len(b) > 68 and b[:8] == b'\x89PNG\r\n\x1a\n'
        w, h = struct.unpack('>II', b[16:24]) if valid else (0, 0)
        artifacts.append({'file': p.name, 'bytes': len(b), 'width': w, 'height': h, 'valid': valid and w > 1 and h > 1})
    summary = {'platform': platform, 'target': 'integration_test/design_review_capture_test.dart', 'exit': code, 'timed_out': bool(timed_out), 'secret_leak_stopped': secret_leak, 'expected': 73 if platform == 'web' else 25, 'artifacts': artifacts}
    (ROOT / (label + '.json')).write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in summary.items() if k != 'artifacts'}, indent=2))
    print('Valid PNGs:', sum(a['valid'] for a in artifacts), 'artifact directory:', dest)
    sys.exit(code if code else (1 if secret_leak or len(artifacts) != summary['expected'] else 0))


if __name__ == '__main__':
    main()
