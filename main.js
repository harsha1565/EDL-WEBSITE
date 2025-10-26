const form = document.getElementById('uploadForm');
const img1 = document.getElementById('img1');
const img2 = document.getElementById('img2');
const preview1 = document.getElementById('preview1');
const preview2 = document.getElementById('preview2');
const results = document.getElementById('results');
const featuresDiv = document.getElementById('features');
const summaryDiv = document.getElementById('summary');

function preview(fileInput, imgEl) {
  const file = fileInput.files[0];
  if (!file) { imgEl.src = ''; return; }
  const reader = new FileReader();
  reader.onload = e => imgEl.src = e.target.result;
  reader.readAsDataURL(file);
}

img1.addEventListener('change', () => preview(img1, preview1));
img2.addEventListener('change', () => preview(img2, preview2));

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  if (!img1.files[0] || !img2.files[0]) return alert('Please select both images.');

  const data = new FormData();
  data.append('img1', img1.files[0]);
  data.append('img2', img2.files[0]);

  featuresDiv.innerHTML = 'Comparing...';
  summaryDiv.innerHTML = '';
  results.style.display = 'block';

  try {
    const resp = await fetch('/compare', { method: 'POST', body: data });
    if (!resp.ok) {
      const err = await resp.json();
      featuresDiv.innerHTML = `<div class="feature bad">Error: ${err.error || resp.statusText}</div>`;
      return;
    }
    const json = await resp.json();
    renderResults(json);
  } catch (err) {
    featuresDiv.innerHTML = `<div class="feature bad">Network error: ${err.message}</div>`;
  }
});

function renderResults(json) {
  const features = json.features || {};
  featuresDiv.innerHTML = '';
  Object.keys(features).forEach(k => {
    const val = features[k];
    const el = document.createElement('div');
    el.className = 'feature ' + (val === 0 ? 'good' : 'bad');
    el.textContent = `${k}: ${val === 0 ? 'Similar (0)' : 'Not similar (1)'}`;
    featuresDiv.appendChild(el);
  });
  summaryDiv.innerHTML = `<strong>Matched:</strong> ${json.matched_count} / 5<br><strong>Features matched:</strong> ${json.matched_features.join(', ')}`;
}
