import requests
import base64
import re

config_path = r'C:\Users\MiniPC\Projects\plainqr\.git\config'
with open(config_path, 'r') as f:
    s = f.read()
m = re.search(r'https://[^/]+:([^@]+)@github\.com', s)
TOKEN = m.group(1)

OWNER = 'makszoom'
REPO = 'pdf-merge'
BRANCH = 'main'
headers = {'Authorization': f'token {TOKEN}', 'Accept': 'application/vnd.github.v3+json'}
base_url = f'https://api.github.com/repos/{OWNER}/{REPO}/contents'

FILES = {
    'js/app.js': r'C:\Users\MiniPC\Projects\pdf-merge\js\app.js',
    'css/style.css': r'C:\Users\MiniPC\Projects\pdf-merge\css\style.css',
}

for repo_path, local_path in FILES.items():
    print(f'Deploying: {repo_path}')
    url = f'{base_url}/{repo_path}?ref={BRANCH}'
    r = requests.get(url, headers=headers)
    sha = r.json().get('sha') if r.status_code == 200 else None
    with open(local_path, 'r', encoding='utf-8') as f:
        content_b64 = base64.b64encode(f.read().encode('utf-8')).decode('utf-8')
    payload = {'message': f'Add drag-to-reorder arrows: {repo_path}', 'content': content_b64, 'sha': sha, 'branch': BRANCH}
    r = requests.put(url, headers=headers, json=payload)
    print(f'  Result: {"OK" if r.status_code in (200, 201) else f"FAIL {r.status_code}"}')

print('\n✅ Deployed! Test: https://makszoom.github.io/pdf-merge/')
