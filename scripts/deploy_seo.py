#!/usr/bin/env python3
"""deploy_seo.py — деплой проекта pdf-merge в makszoom/pdf-merge (GitHub Pages, корень).

Заменяет прежний ad-hoc deploy.py, который знал только index.html + css + js
(до PDF Toolkit v2 с пятью инструментами) и деплоил всё без разбора.

Логика: сравниваем содержимое после нормализации переводов строк — сравнение
по git-blob SHA на Windows бесполезно (локально CRLF, в репозитории LF).

  python scripts/deploy_seo.py --dry-run   # показать, что уйдёт
  python scripts/deploy_seo.py             # задеплоить изменённое
  python scripts/deploy_seo.py --all       # задеплоить всё
"""
import base64
import os
import sys

import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = os.path.join(os.path.expanduser('~'), 'Projects', 'csvtojson', '.env')
OWNER, REPO, BRANCH = 'makszoom', 'pdf-merge', 'main'

# что публикуем: только файлы сайта. backup-* папки и test*.pdf сюда не входят.
FILES = [
    'index.html', 'merge-pdf.html', 'split-pdf.html', 'compress-pdf.html',
    'rotate-pdf.html', 'remove-pages.html', 'privacy.html',
    'sitemap.xml', 'robots.txt', 'manifest.json', 'icon.svg', 'CNAME',
    'css/style.css', 'js/app.js',
]


def token():
    with open(ENV, encoding='utf-8') as f:
        for line in f:
            if line.startswith('GITHUB_TOKEN='):
                return line.split('=', 1)[1].strip()
    raise SystemExit('GITHUB_TOKEN не найден в ' + ENV)


def norm(b):
    return b.replace(b'\r\n', b'\n')


def main():
    dry = '--dry-run' in sys.argv
    force = '--all' in sys.argv
    H = {'Authorization': f'Bearer {token()}', 'Accept': 'application/vnd.github+json'}

    todo = []
    for name in FILES:
        path = os.path.join(ROOT, name)
        if not os.path.exists(path):
            print(f'  [!] нет файла {name}')
            continue
        local = open(path, 'rb').read()
        r = requests.get(f'https://api.github.com/repos/{OWNER}/{REPO}/contents/{name}',
                         headers=H, params={'ref': BRANCH}, timeout=25)
        if r.status_code == 404:
            todo.append((name, local, None))
            continue
        if r.status_code != 200:
            print(f'  [!] {name}: GET {r.status_code}')
            continue
        remote = base64.b64decode(r.json()['content'])
        if force or norm(local) != norm(remote):
            todo.append((name, local, r.json()['sha']))

    print(f'файлов в списке: {len(FILES)} | к деплою: {len(todo)}')
    for name, local, sha in todo:
        print(f'  {"НОВЫЙ   " if sha is None else "ИЗМЕНЁН "} {name} ({len(local)} b)')
    if dry:
        return 0
    if not todo:
        print('нечего деплоить — файлы совпадают с репозиторием')
        return 0

    ok = 0
    for name, local, sha in todo:
        body = {'message': f'seo: {name}', 'content': base64.b64encode(local).decode('ascii'),
                'branch': BRANCH}
        if sha:
            body['sha'] = sha
        r = requests.put(f'https://api.github.com/repos/{OWNER}/{REPO}/contents/{name}',
                         headers=H, json=body, timeout=40)
        print(f'  [{"OK " if r.status_code in (200, 201) else "ERR"}] {name} {r.status_code}')
        if r.status_code in (200, 201):
            ok += 1
        else:
            print('       ', str(r.json().get('message'))[:150])
    print(f'\nзадеплоено {ok} из {len(todo)}')
    return 0 if ok == len(todo) else 1


if __name__ == '__main__':
    sys.exit(main())
