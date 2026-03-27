function getCsrf() {
  return document.cookie.split(';')
    .find(c => c.trim().startsWith('csrftoken='))
    ?.split('=')[1] ?? '';
}

async function handleVote(btn) {
  const postId = btn.dataset.postId;
  const value = parseInt(btn.dataset.value);
  const scoreEl = btn.querySelector('.vote-score');

  // Optimistic update
  const prevScore = parseInt(scoreEl.textContent);
  const wasActive = btn.classList.contains('active');
  btn.classList.toggle('active');
  scoreEl.textContent = wasActive ? prevScore - value : prevScore + value;
  btn.disabled = true;

  try {
    const res = await fetch(`/p/${postId}/vote/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': getCsrf(),
      },
      body: `value=${value}`,
    });

    if (res.status === 403) {
      // Non connecté — rediriger vers login
      window.location.href = '/accounts/login/';
      return;
    }

    const data = await res.json();
    // Sync avec la vraie valeur du serveur
    scoreEl.textContent = data.score;
    btn.classList.toggle('active', data.user_voted === value);

  } catch {
    // Rollback si erreur réseau
    scoreEl.textContent = prevScore;
    btn.classList.toggle('active', wasActive);
  } finally {
    btn.disabled = false;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.vote-btn').forEach(btn => {
    btn.addEventListener('click', () => handleVote(btn));
  });
});
