document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.report-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      const postId = btn.dataset.postId;
      if (!confirm('Rapòte pòs sa a?')) return;

      btn.disabled = true;
      try {
        const res = await fetch(`/p/${postId}/rapote/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCsrf(),
          },
          body: 'reason=offensive',
        });
        const data = await res.json();
        if (data.status === 'reported' || data.status === 'already_reported') {
          btn.style.color = 'var(--t-danger)';
          btn.title = 'Rapòte';
        }
      } catch {
        btn.disabled = false;
      }
    });
  });
});
