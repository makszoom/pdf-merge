# -*- coding: utf-8 -*-
# 4 дубликата-лендинга → meta-refresh redirect на /merge-pdf
# (GitHub Pages не поддерживает серверные 301; meta-refresh + canonical признаны Google)

REDIRECTS = {
    'combine-pdf.html': 'merge-pdf',
    'pdf-merger-online.html': 'merge-pdf',
    'merge-pdf-files.html': 'merge-pdf',
    'join-pdf.html': 'merge-pdf',
}

TPL = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Merge PDF — Combine Multiple PDFs into One File Online</title>
    <meta name="robots" content="noindex, follow">
    <link rel="canonical" href="https://pdfmerge.dev/{target}">
    <meta http-equiv="refresh" content="0; url=https://pdfmerge.dev/{target}">
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="container">
        <section class="hero" style="padding-top:80px;">
            <h1>This page has moved</h1>
            <p class="subtitle">Redirecting to <a href="/{target}">/{target}</a>...</p>
            <p><a class="btn-primary" style="display:inline-block;text-decoration:none;margin-top:16px;" href="/{target}">Go to {label} →</a></p>
        </section>
    </div>
</body>
</html>'''

for fname, target in REDIRECTS.items():
    label = target.replace('-', ' ').title()
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(TPL.format(target=target, label=label))
    print('OK', fname, '->', target)
print('Done')