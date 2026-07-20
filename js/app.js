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
            '<button class="file-move-up" data-index="' + i + '" title="Move up"' + (i === 0 ? ' disabled' : '') + '>↑</button>' +
            '<button class="file-move-down" data-index="' + i + '" title="Move down"' + (i === files.length - 1 ? ' disabled' : '') + '>↓</button>' +
            '<button class="file-remove" data-index="' + i + '">✕</button>' +
        '</div>'
    ).join('');
    // Add move up listeners
    filesEl.querySelectorAll('.file-move-up').forEach(btn => {
        btn.addEventListener('click', () => moveUp(parseInt(btn.dataset.index)));
    });
    // Add move down listeners
    filesEl.querySelectorAll('.file-move-down').forEach(btn => {
        btn.addEventListener('click', () => moveDown(parseInt(btn.dataset.index)));
    });
    // Add remove listeners
    filesEl.querySelectorAll('.file-remove').forEach(btn => {
        btn.addEventListener('click', () => removeFile(parseInt(btn.dataset.index)));
    });
    mergeBtn.disabled = files.length < 2;
}

function moveUp(index) {
    if (index <= 0) return;
    [files[index - 1], files[index]] = [files[index], files[index - 1]];
    renderFiles();
}

function moveDown(index) {
    if (index >= files.length - 1) return;
    [files[index], files[index + 1]] = [files[index + 1], files[index]];
    renderFiles();
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

// ═══════ Payment Configuration ═══════
const PAYMENT_CONFIG = {
    WORKER_URL: 'https://pdfmerge-payment.makszoom85.workers.dev',
    TRC20_ADDRESS: 'TCQTHvLP1ZctspY8UEgsWjy8xqe5tUTtFc',
    PRICE: 5
};

// Payment elements
const paymentClose = document.getElementById('paymentClose');
const copyBtn = document.getElementById('copyBtn');
const txidInput = document.getElementById('txidInput');
const verifyBtn = document.getElementById('verifyBtn');
const paymentStatus = document.getElementById('paymentStatus');

// Paywall
function showPaywall() { paywallModal.style.display = 'flex'; }
function closePaywall() { paywallModal.style.display = 'none'; }

paywallModal.addEventListener('click', (e) => { if (e.target === paywallModal) closePaywall(); });
if (paymentClose) paymentClose.addEventListener('click', closePaywall);

// Copy address
if (copyBtn) {
    copyBtn.addEventListener('click', async () => {
        try {
            await navigator.clipboard.writeText(PAYMENT_CONFIG.TRC20_ADDRESS);
            copyBtn.textContent = '✓ Copied';
            copyBtn.classList.add('copied');
            setTimeout(() => {
                copyBtn.textContent = 'Copy';
                copyBtn.classList.remove('copied');
            }, 2000);
        } catch (e) {
            // Fallback
            const addrInput = document.getElementById('paymentAddress');
            addrInput.select();
            document.execCommand('copy');
            copyBtn.textContent = '✓ Copied';
            copyBtn.classList.add('copied');
            setTimeout(() => {
                copyBtn.textContent = 'Copy';
                copyBtn.classList.remove('copied');
            }, 2000);
        }
    });
}

// Verify payment
if (verifyBtn) {
    verifyBtn.addEventListener('click', async () => {
        const txId = txidInput.value.trim();

        if (!txId) {
            showStatus('Please paste your TXID first.', 'error');
            return;
        }

        if (!/^[a-fA-F0-9]{64}$/.test(txId)) {
            showStatus('Invalid TXID format. Must be 64 hex characters.', 'error');
            return;
        }

        // Loading state
        verifyBtn.disabled = true;
        verifyBtn.textContent = 'Verifying...';
        showStatus('<span class="payment-spinner"></span>Verifying transaction on blockchain...', 'loading');

        try {
            const response = await fetch(PAYMENT_CONFIG.WORKER_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ txId })
            });

            const data = await response.json();

            if (data.verified) {
                // Success — unlock!
                localStorage.setItem('pdfmerge_unlocked', 'true');
                showStatus('✅ Payment verified! Unlimited merges activated.', 'success');
                verifyBtn.textContent = '✓ Unlocked';

                setTimeout(() => {
                    closePaywall();
                    updateCounter();
                    // Reset button for future
                    verifyBtn.disabled = false;
                    verifyBtn.textContent = 'Verify';
                    txidInput.value = '';
                    paymentStatus.innerHTML = '';
                }, 2500);
            } else {
                // Error from worker
                showStatus('❌ ' + (data.message || 'Verification failed.'), 'error');
                verifyBtn.disabled = false;
                verifyBtn.textContent = 'Verify';
            }
        } catch (err) {
            showStatus('❌ Network error. Check your connection and try again.', 'error');
            verifyBtn.disabled = false;
            verifyBtn.textContent = 'Verify';
        }
    });
}

// Allow Enter key in TXID field
if (txidInput) {
    txidInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            verifyBtn.click();
        }
    });
}

function showStatus(message, type) {
    paymentStatus.className = 'payment-status ' + type;
    paymentStatus.innerHTML = message;
}

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
