// PDFMerge Toolkit — Split / Compress / Rotate / Remove Pages
// Reuses: style.css classes, pdf-lib (loaded per-page), paywall from app.js patterns
// Storage keys shared with index.html: pdfmerge_merges_used (single ops),
//   pdfmerge_unlocked ($5 unlimited single), pdfmerge_unlocked_pro ($9 batch)

(function () {
    'use strict';

    // ── Which tool is this page? ──
    // Each page sets <body data-tool="split|compress|rotate|remove">
    const TOOL = document.body.dataset.tool;
    if (!TOOL) return; // not a toolkit page

    const MAX_FREE_OPS = 5;
    const FREE_MAX_FILES = 1;
    const PRO_MAX_FILES = 30;

    // ── Elements (same IDs as index.html patterns) ──
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const filePicker = document.getElementById('filePicker');
    const fileList = document.getElementById('fileList');
    const filesEl = document.getElementById('files');
    const fileCount = document.getElementById('fileCount');
    const runBtn = document.getElementById('runBtn');
    const clearAll = document.getElementById('clearAll');
    const progress = document.getElementById('progress');
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    const counter = document.getElementById('counter');
    const optsEl = document.getElementById('toolOptions');

    let files = [];

    // ── Quota (shared with merge tool) ──
    function getOpsUsed() {
        return parseInt(localStorage.getItem('pdfmerge_merges_used') || '0');
    }
    function incrementOpsUsed() {
        localStorage.setItem('pdfmerge_merges_used', String(getOpsUsed() + 1));
    }
    function isUnlocked() {
        return localStorage.getItem('pdfmerge_unlocked') === 'true';
    }
    function isPro() {
        return localStorage.getItem('pdfmerge_unlocked_pro') === 'true';
    }
    function maxFiles() {
        return isPro() ? PRO_MAX_FILES : FREE_MAX_FILES;
    }
    function updateCounter() {
        if (!counter) return;
        if (isPro()) { counter.innerHTML = '<strong>Pro</strong> — batch up to ' + PRO_MAX_FILES + ' files'; return; }
        if (isUnlocked()) { counter.innerHTML = '<strong>Unlimited</strong> single-file operations'; return; }
        const left = Math.max(0, MAX_FREE_OPS - getOpsUsed());
        counter.innerHTML = 'Free operations left: <strong>' + left + '</strong>/5 — ' +
            '<a href="/#paywall" style="color:#000;text-decoration:underline;">Unlock $5</a> or <a href="/#paywall" style="color:#000;text-decoration:underline;">Pro $9</a>';
    }

    // ── Drag & Drop (mirrors index.html) ──
    dropZone.addEventListener('click', () => fileInput.click());
    filePicker.addEventListener('click', (e) => { e.stopPropagation(); fileInput.click(); });
    fileInput.addEventListener('change', (e) => addFiles(e.target.files));
    dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('dragover'); });
    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        addFiles(e.dataTransfer.files);
    });

    function addFiles(list) {
        const pdfs = Array.from(list).filter(f => f.type === 'application/pdf' || f.name.toLowerCase().endsWith('.pdf'));
        if (pdfs.length === 0) { alert('Please select PDF files only.'); return; }
        const cap = maxFiles();
        if (files.length + pdfs.length > cap) {
            const extra = files.length + pdfs.length - cap;
            files = [...files, ...pdfs.slice(0, Math.max(0, cap - files.length))];
            alert(extra > 0
                ? (isPro() ? 'Batch limit is ' + PRO_MAX_FILES + ' files.' : 'Free plan processes 1 file at a time. Batch (up to ' + PRO_MAX_FILES + ') is part of Pro — $9 lifetime.')
                : '');
        } else {
            files = [...files, ...pdfs];
        }
        renderFiles();
    }

    function renderFiles() {
        if (files.length === 0) {
            fileList.style.display = 'none';
            runBtn.disabled = true;
            return;
        }
        fileList.style.display = 'block';
        fileCount.textContent = String(files.length);
        filesEl.innerHTML = files.map((file, i) =>
            '<div class="file-item">' +
            '<span class="file-icon">📄</span>' +
            '<span class="file-name">' + escapeHtml(file.name) + '</span>' +
            '<span class="file-size">' + formatSize(file.size) + '</span>' +
            '<button class="file-remove" data-index="' + i + '">✕</button>' +
            '</div>'
        ).join('');
        filesEl.querySelectorAll('.file-remove').forEach(btn => {
            btn.addEventListener('click', () => { files.splice(parseInt(btn.dataset.index), 1); renderFiles(); });
        });
        runBtn.disabled = false;
    }

    clearAll.addEventListener('click', () => { files = []; renderFiles(); fileInput.value = ''; });

    // ── Tool-specific options UI ──
    function buildOptions() {
        if (!optsEl) return '';
        if (TOOL === 'split') {
            return '<label class="opt-label">Pages to keep (e.g. 1-3, 5, 8-10)</label>' +
                '<input type="text" id="optRanges" placeholder="1-3, 5, 8-10" class="opt-input">';
        }
        if (TOOL === 'rotate') {
            return '<label class="opt-label">Rotation</label>' +
                '<div class="opt-row">' +
                '<label><input type="radio" name="optAngle" value="90" checked> 90° clockwise</label>' +
                '<label><input type="radio" name="optAngle" value="180"> 180°</label>' +
                '<label><input type="radio" name="optAngle" value="270"> 90° counter-clockwise</label>' +
                '</div>' +
                '<label class="opt-label">Pages (blank = all), e.g. 1, 3-5</label>' +
                '<input type="text" id="optPages" placeholder="all pages" class="opt-input">';
        }
        if (TOOL === 'remove') {
            return '<label class="opt-label">Pages to DELETE (e.g. 2, 5-7)</label>' +
                '<input type="text" id="optRemove" placeholder="2, 5-7" class="opt-input">';
        }
        if (TOOL === 'compress') {
            return '<label class="opt-label">Quality</label>' +
                '<div class="opt-row">' +
                '<label><input type="radio" name="optQ" value="0.8" checked> High (recommended)</label>' +
                '<label><input type="radio" name="optQ" value="0.5"> Medium (smaller)</label>' +
                '<label><input type="radio" name="optQ" value="0.3"> Low (smallest)</label>' +
                '</div>';
        }
        return '';
    }

    if (optsEl) optsEl.innerHTML = buildOptions();

    function parseRanges(spec, pageCount) {
        // "1-3, 5, 8-10" → [0,1,2,4,7,8,9]
        const set = new Set();
        spec.split(',').forEach(part => {
            part = part.trim();
            if (!part) return;
            const m = part.match(/^(\d+)(?:-(\d+))?$/);
            if (!m) return;
            let a = parseInt(m[1], 10), b = m[2] ? parseInt(m[2], 10) : a;
            for (let p = Math.min(a, b); p <= Math.max(a, b); p++) {
                if (p >= 1 && p <= pageCount) set.add(p - 1);
            }
        });
        return [...set].sort((x, y) => x - y);
    }

    // ── Core operations (pdf-lib; compress uses pdf.js if present) ──
    async function opSplit(file, opts) {
        const { PDFDocument } = PDFLib;
        const src = await PDFDocument.load(await file.arrayBuffer());
        const total = src.getPageCount();
        const keep = parseRanges(opts.ranges || '', total);
        if (keep.length === 0) throw new Error('No valid pages in range. This PDF has ' + total + ' pages.');
        const out = await PDFDocument.create();
        const copied = await out.copyPages(src, keep);
        copied.forEach(p => out.addPage(p));
        return { bytes: await out.save(), name: baseName(file.name) + '-split.pdf' };
    }

    async function opRotate(file, opts) {
        const { PDFDocument, degrees } = PDFLib;
        const src = await PDFDocument.load(await file.arrayBuffer());
        const total = src.getPageCount();
        const targets = new Set(opts.pages ? parseRanges(opts.pages, total) : src.getPageIndices());
        src.getPages().forEach((page, i) => {
            if (targets.has(i)) {
                const current = page.getRotation().angle || 0;
                page.setRotation(degrees((current + opts.angle) % 360));
            }
        });
        return { bytes: await src.save(), name: baseName(file.name) + '-rotated.pdf' };
    }

    async function opRemove(file, opts) {
        const { PDFDocument } = PDFLib;
        const src = await PDFDocument.load(await file.arrayBuffer());
        const total = src.getPageCount();
        const removeSet = new Set(parseRanges(opts.remove || '', total));
        if (removeSet.size === 0) throw new Error('No valid pages to delete. This PDF has ' + total + ' pages.');
        if (removeSet.size >= total) throw new Error('Cannot delete every page.');
        const keep = src.getPageIndices().filter(i => !removeSet.has(i));
        const out = await PDFDocument.create();
        const copied = await out.copyPages(src, keep);
        copied.forEach(p => out.addPage(p));
        return { bytes: await out.save(), name: baseName(file.name) + '-edited.pdf' };
    }

    async function opCompress(file, opts) {
        if (typeof pdfjsLib === 'undefined') throw new Error('PDF renderer failed to load. Check your connection and reload.');
        const quality = parseFloat(opts.quality || '0.8');
        const pdf = await pdfjsLib.getDocument({ data: await file.arrayBuffer() }).promise;
        const { PDFDocument } = PDFLib;
        const out = await PDFDocument.create();
        for (let i = 1; i <= pdf.numPages; i++) {
            const page = await pdf.getPage(i);
            const viewport = page.getViewport({ scale: 1.5 });
            const canvas = document.createElement('canvas');
            canvas.width = viewport.width; canvas.height = viewport.height;
            await page.render({ canvasContext: canvas.getContext('2d'), viewport }).promise;
            const dataUrl = canvas.toDataURL('image/jpeg', quality);
            const jpg = await fetch(dataUrl).then(r => r.arrayBuffer());
            const img = await out.embedJpg(jpg);
            const p = out.addPage([img.width, img.height]);
            p.drawImage(img, { x: 0, y: 0, width: img.width, height: img.height });
            progressFill.style.width = Math.round((i / pdf.numPages) * 80) + '%';
            progressText.textContent = 'Compressing page ' + i + ' of ' + pdf.numPages + '...';
        }
        return { bytes: await out.save(), name: baseName(file.name) + '-compressed.pdf' };
    }

    function baseName(name) {
        return name.replace(/\.pdf$/i, '');
    }

    // ── Runner ──
    runBtn.addEventListener('click', async () => {
        if (files.length === 0) return;
        if (!isUnlocked() && !isPro() && getOpsUsed() >= MAX_FREE_OPS) {
            window.location.href = '/#paywall';
            return;
        }
        const opts = {};
        if (TOOL === 'split') opts.ranges = (document.getElementById('optRanges') || {}).value || '';
        if (TOOL === 'rotate') {
            opts.angle = parseInt((document.querySelector('input[name=optAngle]:checked') || { value: '90' }).value, 10);
            opts.pages = (document.getElementById('optPages') || {}).value || '';
        }
        if (TOOL === 'remove') opts.remove = (document.getElementById('optRemove') || {}).value || '';
        if (TOOL === 'compress') opts.quality = (document.querySelector('input[name=optQ]:checked') || { value: '0.8' }).value;

        runBtn.disabled = true;
        progress.style.display = 'block';
        progressFill.style.width = '10%';
        progressText.textContent = 'Reading PDF...';

        const results = [];
        try {
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                let res;
                if (TOOL === 'split') res = await opSplit(file, opts);
                else if (TOOL === 'rotate') res = await opRotate(file, opts);
                else if (TOOL === 'remove') res = await opRemove(file, opts);
                else if (TOOL === 'compress') res = await opCompress(file, opts);
                results.push(res);
                const pct = 10 + Math.round(((i + 1) / files.length) * 80);
                progressFill.style.width = pct + '%';
                progressText.textContent = 'Processing ' + (i + 1) + ' of ' + files.length + '...';
            }

            // single file → direct download; batch → ZIP via JSZip (Pro)
            if (results.length === 1) {
                saveBlob(new Blob([results[0].bytes], { type: 'application/pdf' }), results[0].name);
            } else {
                const zip = new JSZip();
                results.forEach(r => zip.file(r.name, r.bytes));
                const blob = await zip.generateAsync({ type: 'blob' });
                saveBlob(blob, 'pdfmerge-' + TOOL + '-batch.zip');
            }

            progressFill.style.width = '100%';
            progressText.textContent = 'Done!';
            if (!isUnlocked() && !isPro()) incrementOpsUsed();
            updateCounter();

            setTimeout(() => {
                progress.style.display = 'none';
                progressFill.style.width = '0%';
                runBtn.disabled = files.length === 0;
            }, 2000);
        } catch (err) {
            console.error(err);
            progressText.textContent = 'Error: ' + (err.message || 'Operation failed. The PDF may be corrupted or password-protected.');
            runBtn.disabled = false;
        }
    });

    function saveBlob(blob, name) {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url; a.download = name;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    // ── Helpers ──
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    function formatSize(bytes) {
        if (!bytes) return '0 B';
        const k = 1024, sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
    }

    updateCounter();
    console.log('PDFMerge toolkit loaded: ' + TOOL);
})();