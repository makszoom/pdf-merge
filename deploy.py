import requests
import base64
import re

# Extract token from existing plainqr git config (per skill: github-auth -> pat-token-discovery)
config_path = r'C:\Users\MiniPC\Projects\plainqr\.git\config'
with open(config_path, 'r') as f:
    s = f.read()

m = re.search(r'https://[^/]+:([^@]+)@github\.com', s)
if not m:
    raise ValueError('Token not found in git config')
TOKEN = m.group(1)

OWNER = 'makszoom'
REPO = 'pdf-merge'
BRANCH = 'main'

headers = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

# Step 1: Ensure repo exists
repo_url = f'https://api.github.com/repos/{OWNER}/{REPO}'
r = requests.get(repo_url, headers=headers)
print(f'Repo check: {r.status_code}')

if r.status_code == 404:
    create_url = 'https://api.github.com/user/repos'
    payload = {
        'name': REPO,
        'description': 'Browser-side PDF merger — 100% client-side, no upload',
        'private': False,
        'auto_init': True
    }
    r2 = requests.post(create_url, headers=headers, json=payload)
    print(f'Create repo: {r2.status_code}')
    if r2.status_code not in (201, 200):
        print('ERROR:', r2.json())
        exit(1)
else:
    print('Repo already exists')

# Step 2: Deploy files
FILES = {
    'index.html': r'C:\Users\MiniPC\Projects\pdf-merge\index.html',
    'css/style.css': r'C:\Users\MiniPC\Projects\pdf-merge\css\style.css',
    'js/app.js': r'C:\Users\MiniPC\Projects\pdf-merge\js\app.js',
}

base_url = f'https://api.github.com/repos/{OWNER}/{REPO}/contents'

for repo_path, local_path in FILES.items():
    print(f'\nDeploying: {repo_path}')
    
    url = f'{base_url}/{repo_path}?ref={BRANCH}'
    r = requests.get(url, headers=headers)
    sha = r.json().get('sha') if r.status_code == 200 else None
    
    with open(local_path, 'r', encoding='utf-8') as f:
        content_b64 = base64.b64encode(f.read().encode('utf-8')).decode('utf-8')
    
    payload = {
        'message': f'Deploy {repo_path}',
        'content': content_b64,
        'sha': sha,
        'branch': BRANCH
    }
    
    r = requests.put(url, headers=headers, json=payload)
    status = 'OK' if r.status_code in (200, 201) else f'FAIL {r.status_code}: {r.json()}'
    print(f'  Result: {status}')

print('\n✅ Deploy complete!')
print(f'URL: https://{OWNER}.github.io/{REPO}/')
print('Wait 1-2 minutes for GitHub Pages cache.')
