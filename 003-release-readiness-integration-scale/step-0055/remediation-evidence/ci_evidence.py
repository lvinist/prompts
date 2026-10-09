"""Read exact-head GitHub CI evidence without exposing credentials."""
import json
import pathlib
import subprocess
import urllib.request
import zipfile
import io
import re

ROOT = pathlib.Path(__file__).parent
APP = ROOT.parents[1] / 'Code' / 'mine-flow-app'
API = 'https://api.github.com/repos/lvinist/mine-flow-app'


def get(url, token=None):
    """Fetch GitHub metadata or artifacts; never print headers or tokens."""
    headers = {'User-Agent': 'mine-flow-step55-verification', 'Accept': 'application/vnd.github+json'}
    if token:
        headers['Authorization'] = 'Bearer ' + token
    class NoAuthRedirect(urllib.request.HTTPRedirectHandler):
        """Avoid forwarding GitHub credentials to the signed artifact host."""
        def redirect_request(self, req, fp, code, msg, hdrs, newurl):
            redirected = super().redirect_request(req, fp, code, msg, hdrs, newurl)
            if redirected and urllib.parse.urlparse(newurl).hostname != 'api.github.com':
                redirected.remove_header('Authorization')
            return redirected
    return urllib.request.build_opener(NoAuthRedirect).open(urllib.request.Request(url, headers=headers), timeout=90).read()


def main():
    """Save metadata, sanitized logs, and real screenshots for latest head run."""
    sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=APP, text=True).strip()
    runs = json.loads(get(API + '/actions/runs?head_sha=' + sha + '&per_page=30'))
    candidates = [r for r in runs['workflow_runs'] if r['name'] == 'ci']
    assert candidates, 'No exact-head CI run'
    run = candidates[0]
    folder = ROOT / ('ci-' + str(run['id']))
    folder.mkdir(exist_ok=True)
    jobs = json.loads(get(API + '/actions/runs/' + str(run['id']) + '/jobs?per_page=100'))
    artifacts = json.loads(get(API + '/actions/runs/' + str(run['id']) + '/artifacts?per_page=100'))
    for name, data in [('run', run), ('jobs', jobs), ('artifacts', artifacts)]:
        (folder / (name + '.json')).write_text(json.dumps(data, indent=2), encoding='utf-8')
    print(json.dumps({'run': run['id'], 'head': run['head_sha'], 'jobs': [{'id': j['id'], 'name': j['name'], 'conclusion': j['conclusion'], 'failed_steps': [s['name'] for s in j['steps'] if s['conclusion'] == 'failure']} for j in jobs['jobs']]}, indent=2))
    cred = subprocess.run(['git', 'credential', 'fill'], input='protocol=https\nhost=github.com\n\n', capture_output=True, text=True, check=True)
    fields = dict(line.split('=', 1) for line in cred.stdout.splitlines() if '=' in line)
    token = fields.get('password')
    assert token, 'No saved GitHub API credential'
    for a in artifacts['artifacts']:
        if a['name'] not in ['web-e2e-driver-log', 'android-e2e-log', 'android-screenshots'] or a['expired']:
            continue
        blob = get(a['archive_download_url'], token)
        dest = folder / a['name']
        dest.mkdir(exist_ok=True)
        with zipfile.ZipFile(io.BytesIO(blob)) as z:
            for entry in z.infolist():
                if entry.is_dir():
                    continue
                safe = pathlib.Path(entry.filename)
                assert not safe.is_absolute() and '..' not in safe.parts
                target = dest / safe
                target.parent.mkdir(parents=True, exist_ok=True)
                content = z.read(entry)
                if safe.suffix != '.png':
                    text = content.decode('utf-8', errors='replace')
                    text = re.sub(r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+', '[REDACTED_JWT]', text)
                    content = text.encode('utf-8')
                target.write_bytes(content)
        print('Saved', a['name'], 'files', sum(1 for p in dest.rglob('*') if p.is_file()))
    android = next(j for j in jobs['jobs'] if j['name'] == 'E2E Tests (Android)')
    raw = get(API + '/actions/jobs/' + str(android['id']) + '/logs', token).decode('utf-8', errors='replace')
    raw = re.sub(r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+', '[REDACTED_JWT]', raw)
    (folder / 'android-job.log').write_text(raw, encoding='utf-8')
    print('Evidence directory:', folder)


if __name__ == '__main__':
    main()
