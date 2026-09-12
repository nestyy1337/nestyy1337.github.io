const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const source = name => fs.readFileSync(path.join(__dirname, '../static/js', name), 'utf8');

function themePage({ saved = null, dark = false, blocked = false } = {}) {
  const root = { dataset: {} };
  const events = {};
  const system = { matches: dark, addEventListener(_, fn) { this.change = fn; } };
  const styles = { '#syntax-light': {}, '#syntax-dark': {} };
  const label = {};
  const button = {
    hidden: true,
    setAttribute(_, value) { this.name = value; },
    querySelector() { return label; },
    addEventListener(_, fn) { this.click = fn; },
  };
  let loaded = false;
  const context = {
    document: {
      documentElement: root,
      querySelector: selector => styles[selector],
      querySelectorAll: () => loaded ? [button] : [],
      addEventListener: (name, fn) => events[name] = fn,
    },
    window: {
      matchMedia: () => system,
      addEventListener: (name, fn) => events[name] = fn,
    },
    localStorage: {
      getItem() { if (blocked) throw Error('blocked'); return saved; },
      setItem(_, value) { if (blocked) throw Error('blocked'); saved = value; },
    },
  };

  vm.runInNewContext(source('theme.js'), context);
  const initial = root.dataset.appearance;
  loaded = true;
  events.DOMContentLoaded();
  return { root, styles, button, system, events, initial, saved: () => saved };
}

test('theme follows system before a preference is saved', () => {
  const page = themePage({ dark: true });
  assert.equal(page.initial, 'dark');
  assert.equal(page.button.hidden, false);
  assert.equal(page.button.name, 'Switch to light mode');
  page.system.matches = false;
  page.system.change();
  assert.equal(page.root.dataset.appearance, 'light');
});

test('switch persists its choice, changes highlighting and ignores system changes', () => {
  const page = themePage();
  page.button.click();
  assert.equal(page.saved(), 'dark');
  assert.equal(page.button.name, 'Switch to light mode');
  assert.equal(page.styles['#syntax-dark'].media, 'all');
  assert.equal(page.styles['#syntax-light'].media, 'not all');
  page.system.change();
  assert.equal(page.root.dataset.appearance, 'dark');
  assert.equal(themePage({ saved: page.saved() }).initial, 'dark');
});

test('invalid values follow system, blocked storage still allows switching', () => {
  assert.equal(themePage({ saved: 'invalid', dark: true }).initial, 'dark');
  const page = themePage({ blocked: true });
  page.button.click();
  assert.equal(page.root.dataset.appearance, 'dark');
  assert.equal(page.saved(), null);
});

test('other tabs can update or clear the saved preference', () => {
  const page = themePage({ saved: 'dark' });
  page.events.storage({ key: 'site-appearance', newValue: 'light' });
  assert.equal(page.root.dataset.appearance, 'light');
  page.events.storage({ key: 'unrelated', newValue: 'dark' });
  assert.equal(page.root.dataset.appearance, 'light');
  page.events.storage({ key: null, newValue: null });
  page.system.matches = true;
  page.system.change();
  assert.equal(page.root.dataset.appearance, 'dark');
});

function pendulumPage({ previous = null, blocked = false, present = true, random = 0.25 } = {}) {
  const figure = { dataset: {}, setAttribute(_, value) { this.name = value; } };
  const context = {
    document: { querySelector: () => present ? figure : null },
    Math: { random: () => random },
    sessionStorage: {
      getItem() { if (blocked) throw Error('blocked'); return previous; },
      setItem(_, value) { if (blocked) throw Error('blocked'); previous = value; },
    },
  };
  vm.runInNewContext(source('pendulum.js'), context);
  return { figure, saved: previous };
}

test('pendulum alternates on new loads and gives the same mood to assistive technology', () => {
  const first = pendulumPage();
  const second = pendulumPage({ previous: first.saved });
  assert.equal(first.figure.dataset.mood, 'over');
  assert.match(first.figure.name, /it's so over/);
  assert.equal(second.figure.dataset.mood, 'back');
  assert.match(second.figure.name, /we're so back/);
  assert.equal(pendulumPage({ previous: second.saved }).saved, 'over');
});

test('pendulum handles blocked storage, invalid state and pages without a figure', () => {
  assert.equal(pendulumPage({ blocked: true }).figure.dataset.mood, 'over');
  assert.equal(pendulumPage({ previous: 'invalid', random: 0.75 }).saved, 'back');
  assert.equal(pendulumPage({ present: false }).saved, null);
});
