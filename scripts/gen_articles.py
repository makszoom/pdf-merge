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
    dict(
        slug='merge-pdf-without-adobe',
        title='Merge PDF Without Adobe: What Works Instead',
        desc=('Adobe Reader cannot merge and Acrobat needs a paid plan. The free options on Windows, Mac and in the '
              'browser, and the jobs where Acrobat still earns its price.'),
        h1='Merge PDF Without Adobe',
        h1b='What Works Instead',
        sub='Why the free Reader cannot merge, what is built into each system, and the cases where paying Adobe is still the right call.',
        sections=[
            ('The Reader trap',
             ['Adobe Acrobat Reader is free, and it will not combine two PDFs. The menu item exists in some builds '
              'and does nothing useful without a subscription, which is where a lot of people give up and assume '
              'merging is a paid feature everywhere.',
              'Merging lives in Acrobat Standard and Acrobat Pro, both subscription products. If you already pay for '
              'Acrobat at work, use it. If you need to merge four invoices once, paying a monthly fee is a poor trade.']),
            ('What is already on the machine',
             ['On macOS, Preview merges PDFs with no extra software. Open the first document, show the sidebar, drag '
              'the rest in, then save. It handles a few dozen files before the thumbnail dragging becomes tedious.',
              'On Windows there is no built-in merger. Printing to Microsoft Print to PDF creates one file per print '
              'job, so it cannot combine documents. The usual answer is PDFsam Basic, free and open source, which asks '
              'for Java first. LibreOffice Draw opens PDFs and can export a merged file, but it treats a PDF as an '
              'editable drawing, and complicated layouts will shift.']),
            ('Merging in the browser',
             ['A browser tool avoids the install and the subscription. The page loads once and then does the merge in '
              'the tab, so the documents stay on your machine.',
              '<a class="cta-inline" href="/">Merge a PDF in the browser, free</a>',
              'This is the shortest path on a locked-down laptop or a Chromebook. It is not a replacement for Acrobat '
              'when the job involves more than combining files, and the next section is about exactly that.']),
            ('Where Acrobat is genuinely better',
             ['Three jobs come to mind, and no browser tool I know of does them well. Optical character recognition on '
              'a scanned document: Acrobat reads the text layer and makes it searchable, which a browser tab cannot '
              'match for large files. Fillable forms and digital signatures: Acrobat handles certificate-based signing '
              'and form fields that other tools flatten or drop. PDF/A and accessibility remediation: if you submit to '
              'a court, a regulator or an archive with format requirements, Acrobat validates against the profile.',
              'If your work is one of those, the subscription is not the problem to solve. If your work is combining '
              'documents, you are paying for a printing press to staple two pages together.']),
            ('The short comparison',
             ['<table><thead><tr><th>Option</th><th>Cost</th><th>Works offline</th><th>Good for</th></tr></thead><tbody>'
              '<tr><td>Acrobat Pro</td><td>Subscription</td><td>Yes</td><td>OCR, forms, signing, PDF/A</td></tr>'
              '<tr><td>Preview on Mac</td><td>Free, built in</td><td>Yes</td><td>A few files, quick jobs</td></tr>'
              '<tr><td>PDFsam Basic</td><td>Free, open source</td><td>Yes</td><td>Many files, splitting, rotation</td></tr>'
              '<tr><td>Browser tool</td><td>Free tier, then paid once</td><td>After first load</td><td>No install, file stays local</td></tr>'
              '</tbody></table>']),
        ],
        faqs=[
            ('Can Adobe Acrobat Reader merge PDF files for free?',
             'No. Acrobat Reader opens and annotates PDFs, but combining files requires Acrobat Standard or Pro, both '
             'paid subscriptions.'),
            ('What is the easiest free way to merge PDFs on Windows?',
             'Install PDFsam Basic, which is free and open source, or use a browser tool that needs no install. Windows '
             'itself has no built-in merger.'),
            ('Can I merge PDFs on Mac without paying?',
             'Yes. Preview is built into macOS and merges files: open the first PDF, show the sidebar, drag the other '
             'documents into it, then save.'),
            ('Does merging in the browser lose quality?',
             'No. The pages are copied into a new document rather than re-rendered, so text stays selectable and images '
             'keep their original resolution.'),
            ('When should I pay for Acrobat instead?',
             'When the job needs OCR on scans, fillable forms, certificate-based signatures, or PDF/A compliance for a '
             'court or archive. For simply combining documents, a free tool does the same thing.'),
        ],
    ),
    dict(
        slug='compress-pdf-offline',
        title='Compress PDF Offline: Mac, Windows and Android',
        desc=('How to shrink a PDF without uploading it, what each system gives you for free, and the catch that makes '
              'browser compressors lose the text layer.'),
        h1='Compress PDF Offline',
        h1b='Without Uploading It',
        sub='Two different compression methods, the built-in option on a Mac, what Windows makes you install, and the price a browser compressor pays.',
        sections=[
            ('Two methods, and only one keeps the text',
             ['Compressors work in one of two ways and the difference decides whether your document survives intact.',
              'The first method rewrites the file structure: it removes duplicate objects, drops unused fonts, '
              'downsamples oversized images and recompresses streams. The text layer stays exactly as it was. Acrobat '
              'and Ghostscript both do this, and so do the command line tools on Linux.',
              'The second method renders each page to an image and builds a new PDF from those images. Compression '
              'ratios look impressive, but the text is gone. It is a picture of text now, so you cannot select it, '
              'search it, or copy a number out of an invoice.']),
            ('On a Mac',
             ['Preview compresses through the Quartz filter. Open the PDF, choose File then Export, pick "Reduce File '
              'Size" from the Quartz filter dropdown and save. It keeps the text layer and works offline. The reduction '
              'is modest compared with what a rasterizing tool reports, which is the trade you want for a document you '
              'still need to read.',
              'For more control, ColorSync Utility lets you build a custom filter with a specific image resolution. It '
              'is a fiddly dialog, and worth it only if you compress the same kind of document regularly.']),
            ('On Windows',
             ['Windows has nothing built in. There is no system dialog that shrinks a PDF. Two practical options: '
              'Ghostscript, which is free and runs from the command line, and PDFsam Enhanced, which is paid. Ghostscript '
              'with the -dPDFSETTINGS=/ebook flag gets a text layer and reasonable image quality, and it takes about '
              'thirty seconds to learn.']),
            ('On Android',
             ['Most Android "PDF compressor" apps upload the file to a server, because phone CPUs are slow at this. '
              'Read the permissions and the privacy policy before installing one. A browser compressor avoids the app '
              'install and keeps the file on the device, at the cost of speed on large documents.']),
            ('What a browser compressor does here',
             ['PDFMerge compresses by rendering pages, which is the same approach most online compressors use. That '
              'means the output is smaller and the text layer is lost. If you need the text to stay selectable, use the '
              'Mac Export route or Ghostscript instead, and treat this tool as the option for scans and image-heavy '
              'documents.',
              '<a class="cta-inline" href="compress-pdf">Compress a PDF in the browser</a>',
              'Being straight about that matters more than the compression ratio. A PDF whose text you cannot search '
              'has failed at the thing a PDF is for.']),
        ],
        faqs=[
            ('How do I compress a PDF offline on a Mac?',
             'Open it in Preview, choose File then Export, and select "Reduce File Size" in the Quartz filter dropdown. '
             'It works without an internet connection and keeps the text selectable.'),
            ('Is there a built-in PDF compressor in Windows?',
             'No. Windows has no system tool for shrinking PDFs. Ghostscript is the free option, and the command '
             'line flag -dPDFSETTINGS=/ebook gives a sensible balance.'),
            ('Why is the text not selectable after compression?',
             'Because that compressor rebuilt the pages as images. It is the same method most online compressors use, '
             'and it trades the text layer for a smaller file. Structural compressors such as Ghostscript keep the text.'),
            ('How much smaller will my PDF get?',
             'Scanned and image-heavy documents often drop by half or more. A text-only PDF is already efficient, so '
             'expect little gain without rasterizing it.'),
            ('Does compressing offline produce the same result as online?',
             'The output depends on the method, not on where it runs. A rasterizing compressor gives the same result in '
             'a browser tab as on a server. The difference is that the file never leaves your machine.'),
        ],
    ),
    dict(
        slug='pdf-merge-no-signup',
        title='PDF Merge With No Sign-Up: What Needs an Account',
        desc=('Which PDF mergers ask for an account and what they want it for. What still works without registering, '
              'and when creating one is actually worth it.'),
        h1='Merge PDFs With No Sign-Up',
        h1b='And What the Account Is Really For',
        sub='Why free tools ask for an email, what you give up by refusing, and the mergers that work without any account at all.',
        sections=[
            ('Why a merger wants your email',
             ['Three reasons, and they are not equally honest. The first is billing: a tool with a paid tier needs an '
              'identity to attach it to. The second is usage limits: an account is how a free allowance gets counted, '
              'so you get five merges a month instead of five ever. The third is marketing, where the account exists so '
              'there is an address to email later.',
              'None of these is sinister, and none of them is about merging files. That is the part worth noticing: the '
              'account is there for the business, not for the task.']),
            ('What you give up by refusing',
             ['Usually: a file history, batch jobs above a small limit, and cloud storage for the results. If you merge '
              'one document a month, none of that matters. If you process invoices weekly, the batch limit is the real '
              'cost, and the account starts to look reasonable.',
              'You also lose the ability to complain. Support channels tend to require a login, which is fair enough.']),
            ('Working without an account',
             ['<strong>System tools.</strong> Preview on macOS merges with no account because there is nobody to ask. '
              'PDFsam Basic on Windows and Linux is the same: a download, not a registration.',
              '<strong>Browser tools.</strong> A page that runs the merge in the tab has no reason to know who you are. '
              'PDFMerge takes that position: five merges free, no email, no account, and a one-time $5 if you want '
              'unlimited. There is no login screen to skip because there is no login.',
              '<a class="cta-inline" href="/">Try it without signing up</a>',
              '<strong>Command line.</strong> qpdf and pdftk merge files locally and have never asked anyone for an '
              'address.']),
            ('When the account is worth it',
             ['If the tool does something a free one does not, the account is the price of that feature rather than a '
              'toll. Smallpdf and iLovePDF both handle conversions and OCR that a local tool will not, and both want an '
              'account for the paid tier. That is a normal trade.',
              'The bad version is a site that requires registration to merge two files and offers nothing a browser tab '
              'cannot do. Those exist in numbers, and they are the reason the phrase "no sign up" gets searched at all.']),
            ('The comparison',
             ['<table><thead><tr><th>Tool</th><th>Account</th><th>Limit without paying</th></tr></thead><tbody>'
              '<tr><td>Preview (macOS)</td><td>None</td><td>None, it is part of the system</td></tr>'
              '<tr><td>PDFsam Basic</td><td>None</td><td>None</td></tr>'
              '<tr><td>PDFMerge</td><td>None</td><td>5 merges, then $5 once</td></tr>'
              '<tr><td>Smallpdf</td><td>Required for paid features</td><td>2 documents a day</td></tr>'
              '<tr><td>iLovePDF</td><td>Required for paid features</td><td>Daily task limits</td></tr>'
              '</tbody></table>']),
        ],
        faqs=[
            ('Can I merge PDFs without creating an account?',
             'Yes. Preview on macOS and PDFsam Basic on Windows need no account. Browser tools that process the file '
             'locally also have no reason to ask, since there is nothing to bill per user.'),
            ('Why do free PDF tools require registration?',
             'Usually to count a usage allowance or to have an address to market to. Registration rarely has anything '
             'to do with the merge itself.'),
            ('Is it safe to give my email to a PDF site?',
             'Consider what the site does with files first. A site that uploads documents keeps a copy, and an email '
             'links that activity to a person. A site that processes locally has less to link.'),
            ('What is the difference between no sign-up and no upload?',
             'Sign-up is about identity, upload is about where the file goes. A tool can skip the account and still '
             'upload your document, and plenty do. Check the network tab, not the marketing.'),
            ('Do I lose quality by merging without an account?',
             'No. The account has no effect on the output. A merge copies pages into a new document, so quality is '
             'identical whether you registered or not.'),
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

# Статьи ссылаются друг на друга, а не на инструменты: перекрёстные ссылки внутри
# кластера помогают Google связать материалы по теме и держат посетителя на сайте.
GUIDES = [
    ('merge-pdf-offline', 'Merge PDF Offline', 'Windows, Mac and browser options compared.'),
    ('merge-pdf-without-uploading', 'Merge Without Uploading', 'How to check any merger before you drop a file.'),
    ('merge-pdf-without-adobe', 'Merge Without Adobe', 'What works instead, and where Acrobat still wins.'),
    ('compress-pdf-offline', 'Compress PDF Offline', 'Two methods, and which one keeps the text.'),
    ('pdf-merge-no-signup', 'No Sign-Up Merging', 'What the account is really for.'),
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
        for slug, name, text in [(s, n, t) for s, n, t in GUIDES if s != art['slug']])

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
