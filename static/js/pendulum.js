// Alternate the joke on new homepage loads in this tab. No animation or requests.
(() => {
  const figure = document.querySelector('.pendulum');
  if (!figure) return;

  let mood = Math.random() < 0.5 ? 'over' : 'back';
  try {
    const previous = sessionStorage.getItem('site-pendulum');
    if (previous === 'over' || previous === 'back') {
      mood = previous === 'over' ? 'back' : 'over';
    }
    sessionStorage.setItem('site-pendulum', mood);
  } catch {
    // Blocked storage leaves a random choice for this load.
  }

  figure.dataset.mood = mood;
  figure.setAttribute('aria-label', `Industry sentiment, a joke: ${mood === 'over' ? "it's so over" : "we're so back"}`);
})();
