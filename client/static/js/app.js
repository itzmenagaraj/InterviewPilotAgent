/* ── File Upload ──────────────────────────────────────── */
const dropZone      = document.getElementById('dropZone');
const fileInput     = document.getElementById('fileInput');
const fileList      = document.getElementById('fileList');
const fileListItems = document.getElementById('fileListItems');
const indexBtn      = document.getElementById('indexBtn');

let selectedFiles = [];

dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
});

['dragleave', 'dragend'].forEach((evt) =>
    dropZone.addEventListener(evt, () => dropZone.classList.remove('drag-over'))
);

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    setFiles([...e.dataTransfer.files].filter(isAllowed));
});

fileInput.addEventListener('change', () => {
    setFiles([...fileInput.files].filter(isAllowed));
});

function isAllowed(file) {
    return /\.(pdf|txt)$/i.test(file.name);
}

function setFiles(files) {
    selectedFiles = files;
    const hasFiles = files.length > 0;
    indexBtn.disabled = !hasFiles;

    if (!hasFiles) {
        fileList.classList.add('d-none');
        return;
    }

    fileListItems.innerHTML = files.map((f) => `
        <li class="list-group-item d-flex justify-content-between align-items-center">
            <span><i class="bi bi-file-earmark-text me-2"></i>${escHtml(f.name)}</span>
            <span class="badge bg-secondary rounded-pill">${fmtSize(f.size)}</span>
        </li>
    `).join('');
    fileList.classList.remove('d-none');
}

function fmtSize(bytes) {
    if (bytes < 1024)        return `${bytes} B`;
    if (bytes < 1_048_576)   return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / 1_048_576).toFixed(1)} MB`;
}

indexBtn.addEventListener('click', async () => {
    if (!selectedFiles.length) return;

    const formData = new FormData();
    selectedFiles.forEach((f) => formData.append('files', f));

    setBtnLoading(indexBtn, true, 'Indexing\u2026');
    hideAlert('uploadAlert');

    try {
        const data = await apiFetch(`${API_BASE_URL}/api/documents/upload`, { method: 'POST', body: formData });
        showAlert('uploadAlert', 'success', `Indexed ${data.chunks_indexed} chunks successfully.`);
        setFiles([]);
        fileInput.value = '';
    } catch (err) {
        showAlert('uploadAlert', 'danger', err.message);
    } finally {
        setBtnLoading(indexBtn, false);
        indexBtn.innerHTML = '<i class="bi bi-database-add me-1"></i>Index Documents';
        indexBtn.disabled = !selectedFiles.length;
    }
});

/* ── Ask Question ─────────────────────────────────────── */
const questionInput = document.getElementById('questionInput');
const askBtn        = document.getElementById('askBtn');

questionInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') askBtn.click(); });

askBtn.addEventListener('click', async () => {
    const question = questionInput.value.trim();
    if (!question) return;

    setLoading('answer', true);
    hideAlert('askAlert');
    document.getElementById('answerResult').classList.add('d-none');

    try {
        const data = await apiFetch(`${API_BASE_URL}/api/qa/answer`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question }),
        });
        document.getElementById('answerContent').innerHTML = marked.parse(data.answer);
        renderSources('answerSources', 'answerSourcesList', data.sources);
        document.getElementById('answerResult').classList.remove('d-none');
    } catch (err) {
        showAlert('askAlert', 'danger', err.message);
    } finally {
        setLoading('answer', false);
    }
});

/* ── Generate Q&A ─────────────────────────────────────── */
const generateBtn = document.getElementById('generateBtn');

generateBtn.addEventListener('click', async () => {
    const topic      = document.getElementById('topicInput').value.trim();
    const difficulty = document.getElementById('difficultySelect').value;
    const count      = parseInt(document.getElementById('countInput').value, 10);

    if (!topic) {
        showAlert('generateAlert', 'danger', 'Please enter a topic.');
        return;
    }

    setLoading('generate', true);
    hideAlert('generateAlert');
    document.getElementById('generateResult').classList.add('d-none');

    try {
        const data = await apiFetch(`${API_BASE_URL}/api/qa/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic, difficulty, count }),
        });
        document.getElementById('generateContent').innerHTML = marked.parse(data.result);
        renderSources('generateSources', 'generateSourcesList', data.sources);
        document.getElementById('generateResult').classList.remove('d-none');
    } catch (err) {
        showAlert('generateAlert', 'danger', err.message);
    } finally {
        setLoading('generate', false);
    }
});

/* ── Shared Helpers ───────────────────────────────────── */
async function apiFetch(url, options) {
    const res  = await fetch(url, options);
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
    return data;
}

function setLoading(section, loading) {
    const isAsk   = section === 'answer';
    const spinner = document.getElementById(isAsk ? 'answerSpinner'   : 'generateSpinner');
    const btn     = document.getElementById(isAsk ? 'askBtn'          : 'generateBtn');
    spinner.classList.toggle('d-none', !loading);
    btn.disabled = loading;
    if (loading) setBtnLoading(btn, true, isAsk ? 'Thinking\u2026' : 'Generating\u2026');
    else btn.innerHTML = isAsk
        ? '<i class="bi bi-send me-1"></i>Ask'
        : '<i class="bi bi-stars me-1"></i>Generate';
}

function setBtnLoading(btn, loading, label = '') {
    if (loading) {
        btn.dataset.originalHtml = btn.innerHTML;
        btn.innerHTML = `<span class="spinner-border spinner-border-sm me-1"></span>${label}`;
        btn.disabled  = true;
    } else {
        btn.innerHTML = btn.dataset.originalHtml || btn.innerHTML;
        btn.disabled  = false;
    }
}

function renderSources(containerId, listId, sources) {
    const container = document.getElementById(containerId);
    const list      = document.getElementById(listId);
    if (sources && sources.length) {
        list.innerHTML = sources.map((s) => `<li>${escHtml(s)}</li>`).join('');
        container.classList.remove('d-none');
    } else {
        container.classList.add('d-none');
    }
}

function showAlert(id, type, message) {
    const el = document.getElementById(id);
    el.className = `alert alert-${type}`;
    el.textContent = message;
    el.classList.remove('d-none');
}

function hideAlert(id) {
    document.getElementById(id).classList.add('d-none');
}

function escHtml(str) {
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}
