// One local preference. Reading and navigation still work without this script.
(() => {
  const root = document.documentElement;
  const storageKey = 'site-appearance';
  const system = window.matchMedia('(prefers-color-scheme: dark)');
  const valid = value => value === 'light' || value === 'dark';
  let preference;
  try {
    preference = localStorage.getItem(storageKey);
  } catch { }

  function render() {
    const appearance = valid(preference) ? preference : system.matches ? 'dark' : 'light';
    root.dataset.appearance = appearance;
    document.querySelector('#syntax-light').media = appearance === 'light' ? 'all' : 'not all';
    document.querySelector('#syntax-dark').media = appearance === 'dark' ? 'all' : 'not all';

    const next = appearance === 'dark' ? 'light' : 'dark';
    for (const button of document.querySelectorAll('[data-theme-toggle]')) {
      button.setAttribute('aria-label', `Switch to ${next} mode`);
      button.querySelector('[data-theme-label]').textContent = next === 'light' ? 'Light' : 'Dark';
    }
  }

  render();

  document.addEventListener('DOMContentLoaded', () => {
    for (const button of document.querySelectorAll('[data-theme-toggle]')) {
      button.addEventListener('click', () => {
        preference = root.dataset.appearance === 'dark' ? 'light' : 'dark';
        try {
          localStorage.setItem(storageKey, preference);
        } catch { }

        render();
      });
      button.hidden = false;
    }

    render();
  });

  system.addEventListener('change', () => {
    if (!valid(preference)) render();
  });

  window.addEventListener('storage', event => {
    if (event.key === storageKey || event.key === null) {
      preference = event.newValue;
      render();
    }
  });
})();
