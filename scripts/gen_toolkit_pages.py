# -*- coding: utf-8 -*-
# Генератор 4 страниц PDF Toolkit — уникальный контент, общий каркас
# Запуск: python gen_toolkit_pages.py  (в ~/Projects/pdf-merge)

PAGES = [
    dict(
        slug='split-pdf', tool='split', libs='pdf-lib',
        title='Split PDF — Extract Pages from PDF Online Free (No Upload)',
        desc='Split PDF files online for free. Extract specific pages or page ranges in your browser — files never leave your device. 100% private, no upload.',
        h1='Split PDF', h1b='In Your Browser',
        sub='Extract pages from a PDF instantly. No upload — your document never leaves your device.',
        howto='How to Split a PDF Online',
        steps=[
            ('Select PDF', 'Drag and drop or click to choose the PDF you want to split.'),
            ('Choose Pages', 'Type the pages or ranges to keep, e.g. 1-3, 5, 8-10.'),
            ('Download', 'Click Split and download a new PDF with only those pages.'),
        ],
        faqs=[
            ('How do I split a PDF into separate pages?',
             'Enter the page numbers or ranges you want to keep — for example "1-3, 5" — and click Split. The tool builds a new PDF containing exactly those pages, in order.'),
            ('Can I split a 500-page PDF?',
             'Yes. Splitting works entirely in your browser with pdf-lib, so there is no server limit. The only limit is your device memory — typical laptops handle several hundred pages easily.'),
            ('Is splitting a PDF safe here?',
             'Yes. Unlike online splitters that upload your file, this tool never sends your document anywhere. The PDF is processed by JavaScript inside your own browser tab.'),
            ('What is the difference between split and extract?',
             'Nothing in practice — both mean keeping only selected pages. This tool extracts the pages you list and discards the rest, producing a smaller PDF.'),
        ],
        body_extra='Type page ranges like <strong>1-3, 5, 8-10</strong> and get a new PDF with just those pages. Perfect for extracting a single contract section, one invoice, or a chapter from a long report.',
    ),
    dict(
        slug='compress-pdf', tool='compress', libs='pdf-lib + pdf.js',
        title='Compress PDF — Reduce PDF File Size Online Free (No Upload)',
        desc='Compress PDF files online for free. Reduce file size in your browser with 3 quality presets — no upload, no watermark, 100% private.',
        h1='Compress PDF', h1b='In Your Browser',
        sub='Shrink PDF file size without uploading. Choose quality — High, Medium or Low.',
        howto='How to Compress a PDF Online',
        steps=[
            ('Select PDF', 'Drag and drop the PDF you want to compress.'),
            ('Pick Quality', 'High keeps near-original clarity, Medium and Low give smaller files.'),
            ('Download', 'Click Compress and save the smaller PDF.'),
        ],
        faqs=[
            ('How much smaller will my PDF be?',
             'It depends on the content. Scanned documents and image-heavy PDFs often shrink 50-80%. Text-only PDFs may shrink less because they were already efficient.'),
            ('Why does compression rasterize pages?',
             'This tool renders each page to a JPEG image and rebuilds the PDF — the same approach used by most online compressors. Text stays readable at High quality, but is no longer selectable after compression.'),
            ('Is there a file size limit?',
             'The free plan handles files up to ~50 MB. Compression runs locally, so there is no server quota — the limit is your browser memory.'),
            ('Will compression add a watermark?',
             'No. Never. The output is a clean PDF with no watermarks, no branding and no hidden pages.'),
        ],
        body_extra='Three quality presets: <strong>High</strong> (recommended, keeps text crisp), <strong>Medium</strong> and <strong>Low</strong> for maximum size reduction.',
    ),
    dict(
        slug='rotate-pdf', tool='rotate', libs='pdf-lib',
        title='Rotate PDF — Turn PDF Pages Online Free (No Upload)',
        desc='Rotate PDF pages online for free — 90, 180 or 270 degrees. Fix sideways scans in your browser. No upload, 100% private.',
        h1='Rotate PDF', h1b='In Your Browser',
        sub='Turn pages 90°, 180° or 270°. Fix sideways scans without uploading anything.',
        howto='How to Rotate a PDF Online',
        steps=[
            ('Select PDF', 'Drag and drop the PDF with sideways pages.'),
            ('Pick Angle', 'Choose 90°, 180° or 270° and which pages to rotate (blank = all).'),
            ('Download', 'Click Rotate and save the corrected PDF.'),
        ],
        faqs=[
            ('How do I permanently rotate a PDF?',
             'Choose an angle and click Rotate. The change is saved into the PDF structure — it is not just a viewer setting, so every PDF reader will show the pages rotated correctly.'),
            ('Can I rotate only some pages?',
             'Yes. Leave the pages field blank to rotate the whole document, or type specific pages like "1, 3-5" to rotate only those.'),
            ('My scan is sideways — will this fix it?',
             'Yes, that is the most common use. Rotate 90° or 270° and the pages will display upright in every reader, on every device.'),
            ('Does rotating reduce quality?',
             'No. Rotation changes only the page orientation metadata — text, images and vectors stay exactly as they were.'),
        ],
        body_extra='Choose <strong>90°, 180° or 270°</strong> for all pages or just a selection. Rotation is written into the file itself — not a temporary viewer setting.',
    ),
    dict(
        slug='remove-pages', tool='remove', libs='pdf-lib',
        title='Remove Pages from PDF — Delete PDF Pages Online Free',
        desc='Delete pages from PDF online for free. Remove blank, confidential or unneeded pages in your browser. No upload, 100% private.',
        h1='Remove Pages from PDF', h1b='In Your Browser',
        sub='Delete the pages you don\'t need. No upload — processing happens on your device.',
        howto='How to Remove Pages from a PDF',
        steps=[
            ('Select PDF', 'Drag and drop the PDF you want to edit.'),
            ('List Pages to Delete', 'Type the page numbers or ranges to remove, e.g. 2, 5-7.'),
            ('Download', 'Click Remove and save the cleaned PDF.'),
        ],
        faqs=[
            ('How do I delete a page from a PDF?',
             'Type the page numbers you want gone — for example "2, 5-7" — and click Remove. Everything else stays in the original order.'),
            ('Can I remove blank pages automatically?',
             'Automatic blank-page detection is on the roadmap. For now, check the page numbers in any PDF viewer and list them manually.'),
            ('Is the removed page recoverable from the file?',
             'No. Deleted pages are not copied into the output document at all, so nothing recoverable remains — useful when removing confidential pages before sharing.'),
            ('What if I delete all pages?',
             'The tool refuses to delete every page — a PDF needs at least one. Remove all but one page if you need an almost-empty document.'),
        ],
        body_extra='List the pages to delete — <strong>2, 5-7</strong> — and get a clean document with everything else intact. Deleting confidential pages before emailing a PDF is the most common use.',
    ),
]

TPL = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <link rel="canonical" href="https://pdfmerge.dev/{slug}">
    <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E📄%3C/text%3E%3C/svg%3E">
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#000000">
    <link rel="apple-touch-icon" href="icon.svg">
    <link rel="stylesheet" href="css/style.css">
    {extra_scripts}
    <script type="application/ld+json">{howto_json}</script>
    <script type="application/ld+json">{faq_json}</script>
</head>
<body data-tool="{tool}">
    <div class="container">
        <header class="header">
            <a href="/" class="logo" style="text-decoration:none;color:inherit;">📄 PDFMerge</a>
            <div class="badge">Free • No Upload • Browser-Only</div>
        </header>

        <section class="hero">
            <h1>{h1} <span class="highlight">{h1b}</span></h1>
            <p class="subtitle">{sub}</p>
        </section>

        <section class="tool">
            <div class="drop-zone" id="dropZone">
                <div class="drop-icon">📁</div>
                <p class="drop-text">Drag & drop PDF files here</p>
                <p class="drop-sub">or <span class="link" id="filePicker">click to select</span> — batch up to 30 files with Pro</p>
                <input type="file" id="fileInput" multiple accept=".pdf" hidden>
            </div>

            <div class="file-list" id="fileList" style="display: none;">
                <div class="file-list-header">
                    <span>Files (<span id="fileCount">0</span>)</span>
                    <button class="btn-text" id="clearAll">Clear all</button>
                </div>
                <div class="files" id="files"></div>
            </div>

            <div id="toolOptions" class="tool-options"></div>

            <button class="btn-primary" id="runBtn" disabled>
                <span class="btn-icon">⬇️</span>
                {run_label}
            </button>

            <div class="progress" id="progress" style="display: none;">
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
                <p class="progress-text" id="progressText">Processing...</p>
            </div>

            <div class="counter" id="counter"></div>
        </section>

        <section class="about-text">
            <h2>About this tool</h2>
            <p>{body_extra}</p>
        </section>

        <section class="features">
            <h2>Why PDFMerge Tools?</h2>
            <div class="feature-grid">
                <div class="feature">
                    <div class="feature-icon">🔒</div>
                    <h3>100% Private</h3>
                    <p>Files never leave your browser. No server, no upload, no data collection.</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">⚡</div>
                    <h3>Instant</h3>
                    <p>No upload wait. Processing happens locally in seconds.</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">💰</div>
                    <h3>Free to Try</h3>
                    <p>5 free operations. $5 lifetime for unlimited, $9 for batch Pro.</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">📱</div>
                    <h3>Works Everywhere</h3>
                    <p>Any modern browser, any device. No installation.</p>
                </div>
            </div>
        </section>

        <section class="related">
            <h2>More PDF Tools</h2>
            <div class="related-grid">
                <a href="/" class="related-card">
                    <h3>Merge PDF</h3>
                    <p>Combine multiple PDFs into one file</p>
                </a>
                {related_cards}
            </div>
        </section>

        <section class="faq">
            <h2>Frequently Asked</h2>
            {faq_html}
        </section>

        <footer class="footer">
            <div class="footer-links">
                <a href="/">Merge PDF</a>
                <a href="split-pdf">Split PDF</a>
                <a href="compress-pdf">Compress PDF</a>
                <a href="rotate-pdf">Rotate PDF</a>
                <a href="remove-pages">Remove Pages</a>
            </div>
            <p>PDFMerge — Made for people who value privacy.</p>
            <p class="footer-small">Not affiliated with Adobe, Smallpdf, or iLovePDF.</p>
        </footer>
    </div>

    {scripts}
</body>
</html>'''

TOOL_LABEL = {'split': 'Split PDF & Download', 'compress': 'Compress & Download',
              'rotate': 'Rotate & Download', 'remove': 'Remove Pages & Download'}
TOOL_NAME = {'split': 'Split PDF', 'compress': 'Compress PDF', 'rotate': 'Rotate PDF', 'remove': 'Remove Pages'}

import json

for p in PAGES:
    slug, tool = p['slug'], p['tool']
    howto_json = json.dumps({
        '@context': 'https://schema.org', '@type': 'HowTo',
        'name': p['howto'],
        'totalTime': 'PT1M',
        'step': [{'@type': 'HowToStep', 'position': i + 1, 'name': n, 'text': t}
                 for i, (n, t) in enumerate(p['steps'])]
    }, ensure_ascii=False)
    faq_json = json.dumps({
        '@context': 'https://schema.org', '@type': 'FAQPage',
        'mainEntity': [{'@type': 'Question', 'name': q,
                        'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in p['faqs']]
    }, ensure_ascii=False)
    faq_html = ''.join(
        '<div class="faq-item"><h3>{}</h3><p>{}</p></div>'.format(q, a)
        for q, a in p['faqs'])

    others = [x for x in PAGES if x['slug'] != slug]
    related_cards = ''.join(
        '<a href="{}" class="related-card"><h3>{}</h3><p>{}</p></a>'.format(
            x['slug'], TOOL_NAME[x['tool']], x['sub'])
        for x in others)

    # pdf.js lazy only on compress; JSZip for batch; toolkit.js always
    if tool == 'compress':
        extra_scripts = '<script src="https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.min.js"></script>\n    <script>pdfjsLib.GlobalWorkerOptions.workerSrc="https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.worker.min.js";</script>'
    else:
        extra_scripts = ''
    scripts = '<script src="https://unpkg.com/pdf-lib@1.17.1/dist/pdf-lib.min.js"></script>\n    <script src="https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js"></script>\n    <script src="js/toolkit.js"></script>'

    html = TPL.format(
        title=p['title'], desc=p['desc'], slug=slug, tool=tool,
        h1=p['h1'], h1b=p['h1b'], sub=p['sub'],
        run_label=TOOL_LABEL[tool],
        howto_json=howto_json, faq_json=faq_json,
        faq_html=faq_html, related_cards=related_cards,
        body_extra=p['body_extra'], extra_scripts=extra_scripts, scripts=scripts)

    fname = slug + '.html' if slug != 'remove-pages' else 'remove-pages.html'
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    print('OK', fname, len(html), 'bytes')
print('Done')