# -*- coding: utf-8 -*-
"""Генератор контентных статей для pdfmerge.dev.

Темы выбраны по Suggest (спрос подтверждён):
  merge pdf offline       — 10 подсказок (windows, mac, free, tool, app)
  merge pdf without uploading — 3 подсказки + "how to merge pdf files without uploading"
  pdf merge no signup     — 5 подсказок

Правила текста (скилл humanizer): без em dash, без "testament/pivotal/landscape",
без rule-of-three, без bold-заголовков в списках, sentence case в заголовках,
без риторических вопросов с немедленным ответом. Честно про то, где конкуренты лучше.

Запуск: python scripts/gen_articles.py
"""
import json
import os

TOOL_NAME = {
    'merge': 'Merge PDF', 'split': 'Split PDF', 'compress': 'Compress PDF',
    'rotate': 'Rotate PDF', 'remove': 'Remove Pages',
}

ARTICLES = [
    dict(
        slug='merge-pdf-offline',
        title='Merge PDF Offline: Windows, Mac and Browser',
        desc=('What offline really means for merging PDFs, the built-in Windows and Mac options, '
              'and how to merge without sending the file anywhere.'),
        h1='Merge PDF Offline',
        h1b='Without Sending the File Anywhere',
        sub='Three different meanings of "offline", the built-in options on each system, and what actually works when there is no internet.',
        sections=[
            ('What "offline" means, and why it matters',
             ['People use the word in three ways and the difference is not academic. It can mean the tool '
              'needs no internet at all, which is what a desktop application gives you. It can mean the file '
              'is never transmitted, which is what a browser tool can give you while still using the network '
              'to load its own code. Or it can mean nothing except "no account", which is how a lot of online '
              'mergers use the word.',
              'The distinction decides who can see your documents. A merger that uploads the file keeps a copy '
              'at least for the length of the request, and the privacy policy says how long after that. A merger '
              'that runs in your browser tab has nothing to keep.']),
            ('Merging PDFs on Windows without internet',
             ['Windows has no built-in PDF merger. Printing to "Microsoft Print to PDF" does not merge anything, '
              'it writes one document at a time, so the trick of printing several files into a single queue does '
              'not work the way people hope.',
              'What does work: PDFsam Basic, which is free and open source, and LibreOffice Draw, which opens '
              'PDFs as editable pages. PDFsam asks you to install Java first, which is a step people either accept '
              'or find irritating. LibreOffice is a large download and importing a PDF into Draw can shift the '
              'layout of a complicated document.']),
            ('Merging PDFs on a Mac',
             ['Preview is already installed and it merges PDFs without an internet connection. Open the first '
              'file, show the sidebar thumbnails, drag the other files into that sidebar, then save. It handles '
              'a handful of documents well.',
              'Preview gets awkward above roughly twenty files or with very large scans, and it gives you no way '
              'to reorder pages across documents except by dragging thumbnails one at a time.']),
            ('Merging in the browser, with the file staying put',
             ['A browser tool sits between the two options above. It needs the internet once, to load the page and '
              'its libraries, and then does the work in the tab. Nothing is transmitted. If you open the page and '
              'then disconnect the network, the merge still runs.',
              '<a class="cta-inline" href="/">Open PDFMerge, free and no signup</a>',
              'That middle position is useful on a work laptop where you cannot install software, or on a borrowed '
              'machine where you do not want to leave a file behind. It is not useful on a plane, because the page '
              'still has to load at least once.']),
            ('Which option fits which situation',
             ['<table><thead><tr><th>Situation</th><th>Best fit</th><th>The catch</th></tr></thead><tbody>'
              '<tr><td>No internet at all, many files</td><td>PDFsam Basic</td><td>Needs Java installed</td></tr>'
              '<tr><td>Mac, a few files</td><td>Preview</td><td>Reordering pages across documents is slow</td></tr>'
              '<tr><td>Work laptop, cannot install anything</td><td>Browser merger</td><td>Page must load once</td></tr>'
              '<tr><td>Confidential scans, one-off job</td><td>Browser merger</td><td>Confirm it does not upload first</td></tr>'
              '</tbody></table>',
              'If the machine is yours and you merge files every week, a desktop tool is the better habit. If you '
              'merge a document once a month on equipment you do not control, the browser is simpler, provided you '
              'check that it really does keep the file local.']),
        ],
        faqs=[
            ('Can I merge PDFs with no internet connection?',
             'Only if the tool is already on the machine. A browser merger needs the internet once to load the page, '
             'then works without it until you close the tab. Desktop applications like PDFsam Basic work with no '
             'connection at all.'),
            ('Does Windows have a built-in PDF merger?',
             'No. Printing to Microsoft Print to PDF creates one PDF per print job, so it cannot combine several '
             'documents into one. You need a separate application for that.'),
            ('How do I merge PDFs on a Mac without extra software?',
             'Use Preview. Open the first PDF, show the thumbnail sidebar, drag the other files into it, then save. '
             'It is free, built into macOS, and works offline.'),
            ('Is a browser merger really offline?',
             'It does the work locally, which means the file is never transmitted, but the page itself loads from a '
             'web server at least once. Check it by opening the page, disconnecting the network, and running a merge. '
             'If it still works, the file is not being uploaded.'),
            ('Which is the safest way to merge confidential PDFs?',
             'The one where the document never leaves your control. That means a desktop application with no network '
             'access, or a browser tool you have verified does not upload. A server-based merger is the weakest option '
             'because the file is transmitted and stored, even briefly.'),
        ],
    ),
    dict(
        slug='merge-pdf-without-uploading',
        title='How to Merge PDF Files Without Uploading Them',
        desc=('Most free PDF mergers send your file to a server. How to check any tool before you drop a document, '
              'and three ways to merge that keep the file on your machine.'),
        h1='How to merge PDF files',
        h1b='Without Uploading Them',
        sub='A thirty-second check that tells you whether a merger uploads your document, and three ways to merge that do not.',
        sections=[
            ('What an upload actually involves',
             ['When a merger uploads a file, three things happen before you see a result. The document is copied over '
              'the network, written to temporary storage on a server you do not control, and processed there. The '
              'output then travels back to you.',
              'How long the copy survives depends on the operator. Some services delete it within an hour, some keep '
              'it for a day, and a few keep files longer for debugging or training. The privacy policy is the only '
              'place this is written down, and most people never open it before dropping a bank statement into a '
              'web form.']),
            ('The thirty-second check',
             ['You do not have to trust the marketing. Open the tool, press F12 or right-click and choose Inspect, '
              'then switch to the Network tab. Drop a small test PDF and watch the requests.',
              'If a request appears with your file in it, usually a POST to something like /upload or /convert, the '
              'document left your machine. If the only requests are the page itself, its fonts and its scripts, the '
              'work happened locally. This takes half a minute and works on any merger, including this one.',
              'Two weaker signals: the page keeps working if you disconnect the network after loading it, and the '
              'file size stays the same in the network panel because nothing was transferred.']),
            ('Three ways that keep the file local',
             ['<strong>Desktop software.</strong> PDFsam Basic on Windows and Linux, Preview on macOS. Nothing is '
              'transmitted because there is no transmission step. PDFsam needs Java installed; Preview is already there.',
              '<strong>A browser tab.</strong> Load the page once, then merge with the file never leaving the tab. '
              'Works on machines where you cannot install anything.',
              '<strong>Command line.</strong> If you are comfortable in a terminal, tools like qpdf and pdftk combine '
              'files locally with one command. No interface, no waiting, no upload.']),
            ('Merging here',
             ['PDFMerge runs the merge in your browser. There is no upload endpoint, so there is nothing to check on '
              'the Network tab except the page and its libraries. You can confirm it the same way you would confirm '
              'any other tool, which is the point.',
              '<a class="cta-inline" href="/">Merge a PDF in the browser</a>',
              'It is free for five merges, then a one-time $5 unlocks unlimited use. No account, no email. If you '
              'merge once a year, the free allowance covers you and the payment never comes up.']),
            ('When an upload is the right choice',
             ['Uploading is not always wrong. If the file is a public document, if you are on a phone with no local '
              'tools, or if the task needs server hardware such as heavy optical character recognition, a server-side '
              'tool is simply better equipped. Adobe and Smallpdf handle OCR and conversion formats that a browser '
              'tab cannot.',
              'The rule worth keeping is narrower than "never upload". It is: know which one you are doing. Most people '
              'assume the merge happens locally because the button says free, and that assumption is what gets a '
              'confidential scan stored on someone else\'s disk.']),
        ],
        faqs=[
            ('How can I tell if a PDF merger uploads my file?',
             'Open the browser developer tools, go to the Network tab, and drop a test file. A POST request carrying '
             'the file means it was uploaded. If only the page, fonts and scripts load, the work happened in the tab.'),
            ('Is it safe to merge PDFs online?',
             'It depends entirely on whether the site uploads. A tool that processes the file in the browser is as '
             'safe as software on your own machine. A tool that uploads stores a copy on a server, and how long it '
             'stays there is up to the operator.'),
            ('Do free PDF mergers keep my files?',
             'Many do, at least temporarily. The retention period is in the privacy policy; common answers range '
             'from one hour to a day, and some services keep files longer. A browser-side merger has nothing to '
             'retain because the file never arrives.'),
            ('Can I merge PDFs on a phone without uploading?',
             'Yes, through a browser tool that processes locally, since mobile browsers can run the same JavaScript '
             'as a desktop. Apps that merge on the device also work, but check the permissions they request.'),
            ('What is the difference between browser-side and server-side merging?',
             'Browser-side means the code runs on your machine and the file stays there. Server-side means the file '
             'travels to a computer you do not control, gets processed, and comes back. The result looks identical, '
             'which is why the distinction is easy to miss.'),
        ],
    ),
]

TPL = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E📄%3C/text%3E%3C/svg%3E">
    <link rel="manifest" href="manifest.json">
    <link rel="canonical" href="https://pdfmerge.dev/{slug}">
    <meta property="og:url" content="https://pdfmerge.dev/{slug}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:type" content="article">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="theme-color" content="#000000">
    <link rel="stylesheet" href="css/style.css">
    <script type="application/ld+json">
{howto_json}
    </script>
    <script type="application/ld+json">
{faq_json}
    </script>
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="logo">📄 PDFMerge</div>
            <div class="badge">Free • No Upload • Browser-Only</div>
        </header>

        <section class="hero">
            <h1>{h1}<br><span class="highlight">{h1b}</span></h1>
            <p class="subtitle">{sub}</p>
            <a class="cta-inline" href="/" style="margin-top:22px">Merge a PDF free, no signup</a>
        </section>

        <section class="seo-content">
{body}
        </section>

        <section class="faq">
            <h2>Frequently Asked Questions</h2>
{faq_html}
        </section>

        <section class="related">
            <h2>Other PDF tools</h2>
            <div class="related-grid">
{related_cards}
            </div>
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
            <p class="footer-small">Not affiliated with Adobe, Smallpdf, or iLovePDF. Last checked 14 November 2026.</p>
        </footer>
    </div>
</body>
</html>
'''

RELATED = [
    ('merge-pdf', 'Merge PDF', 'Combine several documents into one file.'),
    ('split-pdf', 'Split PDF', 'Extract pages or page ranges.'),
    ('compress-pdf', 'Compress PDF', 'Reduce file size with three presets.'),
    ('rotate-pdf', 'Rotate PDF', 'Fix sideways scans, 90 to 270 degrees.'),
    ('remove-pages', 'Remove Pages', 'Delete pages you do not need.'),
]


def build(art):
    body_parts = []
    for heading, paras in art['sections']:
        body_parts.append('            <h2>{}</h2>'.format(heading))
        for p in paras:
            if p.startswith('<table') or p.startswith('<a class='):
                body_parts.append('            <p>{}</p>'.format(p))
            else:
                body_parts.append('            <p>{}</p>'.format(p))
    body = '\n'.join(body_parts)

    faq_html = '\n'.join(
        '            <div class="faq-item">\n                <h3>{}</h3>\n                <p>{}</p>\n            </div>'.format(q, a)
        for q, a in art['faqs'])

    cards = '\n'.join(
        '                <a href="{}" class="related-card"><h3>{}</h3><p>{}</p></a>'.format(slug, name, text)
        for slug, name, text in RELATED)

    # HowTo собираем из инструкций внутри секций: берём шаги из первой секции-инструкции, если есть
    howto = {
        '@context': 'https://schema.org', '@type': 'Article',
        'headline': art['title'],
        'description': art['desc'],
        'url': 'https://pdfmerge.dev/' + art['slug'],
        'datePublished': '2026-11-14',
        'dateModified': '2026-11-14',
        'author': {'@type': 'Organization', 'name': 'PDFMerge'},
        'publisher': {'@type': 'Organization', 'name': 'PDFMerge'},
    }
    faq_json = {
        '@context': 'https://schema.org', '@type': 'FAQPage',
        'mainEntity': [{'@type': 'Question', 'name': q,
                        'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in art['faqs']],
    }

    return TPL.format(
        title=art['title'], desc=art['desc'], slug=art['slug'],
        h1=art['h1'], h1b=art['h1b'], sub=art['sub'], body=body,
        howto_json=json.dumps(howto, ensure_ascii=False, indent=2),
        faq_json=json.dumps(faq_json, ensure_ascii=False, indent=2),
        faq_html=faq_html, related_cards=cards)


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for art in ARTICLES:
        html = build(art)
        path = os.path.join(root, art['slug'] + '.html')
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(html)
        print('OK {} ({} байт, {} слов в title)'.format(art['slug'] + '.html', len(html), len(art['title'])))
    print('Готово')


if __name__ == '__main__':
    main()
