// PDFMerge — Core Application

const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const filePicker = document.getElementById('filePicker');
const fileList = document.getElementById('fileList');
const filesEl = document.getElementById('files');
const fileCount = document.getElementById('fileCount');
const mergeBtn = document.getElementById('mergeBtn');
const clearAll = document.getElementById('clearAll');
const progress = document.getElementById('progress');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const counter = document.getElementById('counter');
const mergesLeft = document.getElementById('mergesLeft');
const paywallModal = document.getElementById('paywallModal');
const payBtn = document.getElementById('payBtn');

let files = [];
const MAX_FREE_MERGES = 5;

// Counter functions
function getMergesUsed() {
    return parseInt(localStorage.getItem('pdfmerge_merges_used') || '0');
}

function incrementMergesUsed() {
    const current = getMergesUsed();
    localStorage.setItem('pdfmerge_merges_used', String(current + 1));
    updateCounter();
}

function isUnlocked() {
    return localStorage.getItem('pdfmerge_unlocked') === 'true';
}

function updateCounter() {
    if (isUnlocked()) {
        counter.innerHTML = '<strong>Unlimited</strong> merges';
        return;
    }
    const used = getMergesUsed();
    const left = Math.max(0, MAX_FREE_MERGES - used);
    mergesLeft.textContent = String(left);
    if (left === 0) {
        counter.innerHTML = 'Free limit reached. <a href="#" id="unlockLink" style="color:#000;text-decoration:underline;">Unlock for $5</a>';
        const link = document.getElementById('unlockLink');
        if (link) link.addEventListener('click', (e) => { e.preventDefault(); showPaywall(); });
    }
}

// Drag & Drop
dropZone.addEventListener('click', () => fileInput.click());
filePicker.addEventListener('click', (e) => { e.stopPropagation(); fileInput.click(); });
fileInput.addEventListener('change', (e) => handleFiles(e.target.files));

dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('dragover'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    handleFiles(e.dataTransfer.files);
});

// File handling
function handleFiles(fileList) {
    const pdfs = Array.from(fileList).filter(f => f.type === 'application/pdf' || f.name.toLowerCase().endsWith('.pdf'));
    if (pdfs.length === 0) { alert('Please select PDF files only.'); return; }
    files = [...files, ...pdfs];
    renderFiles();
    mergeBtn.disabled = files.length < 2;
}

function renderFiles() {
    if (files.length === 0) {
        fileList.style.display = 'none';
        mergeBtn.disabled = true;
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
    // Add remove listeners
    filesEl.querySelectorAll('.file-remove').forEach(btn => {
        btn.addEventListener('click', () => removeFile(parseInt(btn.dataset.index)));
    });
    mergeBtn.disabled = files.length < 2;
}

function removeFile(index) {
    files.splice(index, 1);
    renderFiles();
}

clearAll.addEventListener('click', () => {
    files = [];
    renderFiles();
    fileInput.value = '';
});

// Merge
mergeBtn.addEventListener('click', async () => {
    if (files.length < 2) return;
    if (!isUnlocked() && getMergesUsed() >= MAX_FREE_MERGES) {
        showPaywall();
        return;
    }
    try {
        progress.style.display = 'block';
        mergeBtn.disabled = true;
        progressFill.style.width = '10%';
        progressText.textContent = 'Reading PDF files...';

        const { PDFDocument } = PDFLib;
        const mergedPdf = await PDFDocument.create();

        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            const arrayBuffer = await file.arrayBuffer();
            const pdf = await PDFDocument.load(arrayBuffer);
            const copiedPages = await mergedPdf.copyPages(pdf, pdf.getPageIndices());
            copiedPages.forEach(page => mergedPdf.addPage(page));
            const pct = 10 + Math.round(((i + 1) / files.length) * 70);
            progressFill.style.width = pct + '%';
            progressText.textContent = 'Merging ' + (i + 1) + ' of ' + files.length + '...';
        }

        progressFill.style.width = '90%';
        progressText.textContent = 'Generating PDF...';
        const mergedBytes = await mergedPdf.save();
        const blob = new Blob([mergedBytes], { type: 'application/pdf' });

        progressFill.style.width = '100%';
        progressText.textContent = 'Done!';

        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'merged.pdf';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        if (!isUnlocked()) incrementMergesUsed();

        setTimeout(() => {
            progress.style.display = 'none';
            mergeBtn.disabled = false;
            progressFill.style.width = '0%';
            files = [];
            renderFiles();
            fileInput.value = '';
        }, 2000);
    } catch (err) {
        console.error(err);
        progressText.textContent = 'Error: ' + (err.message || 'Could not merge PDFs. Files may be corrupted or password-protected.');
        mergeBtn.disabled = false;
    }
});

// Paywall
function showPaywall() { paywallModal.style.display = 'flex'; }
paywallModal.addEventListener('click', (e) => { if (e.target === paywallModal) paywallModal.style.display = 'none'; });
payBtn.addEventListener('click', () => {
    const address = 'YOUR_TRC20_ADDRESS';
    alert('Send 5 USDT (TRC-20) to:\n' + address + '\n\nThen paste your TXID to unlock.');
    if (confirm('Developer: unlock now?')) {
        localStorage.setItem('pdfmerge_unlocked', 'true');
        paywallModal.style.display = 'none';
        updateCounter();
        alert('Unlocked! You now have unlimited merges.');
    }
});

// Helpers
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

// Init
updateCounter();
console.log('PDFMerge loaded. PDFLib available:', typeof PDFLib !== 'undefined');
