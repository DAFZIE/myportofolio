(() => {
    const form = document.getElementById('education-detail-form');
    if (!form) return;
    const button = form.querySelector('button[type="submit"]');
    const status = document.getElementById('education-save-status');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        if (button.disabled) return;
        button.disabled = true;
        status.textContent = 'Menyimpan...';
        try {
            const fields = new FormData(form);
            const payload = Object.fromEntries(
                ['title', 'description', 'level', 'started_at', 'ended_at']
                    .map(name => [name, fields.get(name)])
            );
            payload.ended_at = payload.ended_at || null;
            const response = await fetch(form.dataset.apiUrl, {
                method: form.dataset.apiMethod,
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/json',
                    'X-CSRFToken': fields.get('csrfmiddlewaretoken'),
                },
                body: JSON.stringify(payload),
            });
            const data = await response.json().catch(() => ({}));
            if (!response.ok) {
                const messages = Object.entries(data).flatMap(([field, errors]) =>
                    (Array.isArray(errors) ? errors : [errors])
                        .filter(value => typeof value === 'string')
                        .map(value => field === 'detail' ? value : `${field}: ${value}`)
                );
                throw new Error(messages.join(' ') || `Permintaan gagal (HTTP ${response.status}).`);
            }
            // Use the server's cleaned text without interpreting it as HTML.
            for (const name of ['title', 'description', 'level']) {
                form.elements.namedItem(name).value = data[name];
            }
            // A second save after creating an item updates that same item.
            if (form.dataset.apiMethod === 'POST') {
                form.dataset.apiUrl += `${encodeURIComponent(data.id)}/`;
                form.dataset.apiMethod = 'PATCH';
            }
            status.textContent = 'Education berhasil disimpan.';
            showToast('Berhasil', status.textContent, 'success');
        } catch (error) {
            status.textContent = 'Perubahan belum tersimpan.';
            showToast('Gagal menyimpan Education', error.message, 'error');
        } finally {
            button.disabled = false;
        }
    });
})();
