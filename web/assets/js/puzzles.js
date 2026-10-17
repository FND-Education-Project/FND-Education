/* Progressive enhancement: retain the complete download list until data is ready. */
(() => {
  'use strict';
  const root = document.getElementById('puzzle-browser');
  if (!root) return;
  const moduleSelect = document.getElementById('puzzle-module');
  const lessonSelect = document.getElementById('puzzle-lesson');
  const previous = document.getElementById('puzzle-previous');
  const next = document.getElementById('puzzle-next');
  const tabs = Array.from(root.querySelectorAll('[data-collection]'));
  let catalog;
  let collection = 'crosswords';
  let selected;
  const items = () => catalog.items.filter(item => item.collection === collection);
  /* Catalog paths stay on this site, including installations beneath a base URL. */
  const localURL = path => {
    if (typeof path !== 'string' || !path.startsWith('/') || path.startsWith('//')) {
      throw new Error('Invalid puzzle asset path');
    }
    return root.dataset.base.replace(/\/$/, '') + path;
  };
  const option = (value, label) => new Option(label, String(value));
  const address = (kind, id) => {
    const url = new URL(location.href);
    url.search = '';
    url.hash = '';
    url.searchParams.set('collection', kind);
    if (id) url.searchParams.set('puzzle', id);
    return url;
  };
  /* Render from trusted catalog data using DOM text APIs, never HTML interpolation. */
  function render(push = false) {
    const available = items();
    const moduleIds = [...new Set(available.map(item => item.module))];
    moduleSelect.replaceChildren(...moduleIds.map(id => option(id, `Module ${id}: ${catalog.modules[id]}`)));
    moduleSelect.value = String(selected.module);
    lessonSelect.replaceChildren(...available.filter(item => item.module === selected.module).map(item =>
      option(item.id, item.lesson ? `Lesson ${item.lesson}: ${item.title}` : item.title)));
    lessonSelect.value = selected.id;
    tabs.forEach(tab => {
      const kind = tab.dataset.collection;
      const counterpart = catalog.items.find(item => item.collection === kind && item.id === selected.id);
      tab.href = address(kind, counterpart ? selected.id : null).href;
      if (kind === collection) tab.setAttribute('aria-current', 'page');
      else tab.removeAttribute('aria-current');
    });
    document.getElementById('puzzle-title').textContent = selected.lesson ? `Lesson ${selected.lesson}: ${selected.title}` : selected.title;
    const preview = document.getElementById('puzzle-preview');
    preview.src = localURL(selected.image);
    preview.alt = collection === 'crosswords' ? `Blank crossword grid for ${selected.title}` : `Colouring page preview for ${selected.title}`;
    const downloads = document.getElementById('puzzle-downloads');
    const labels = collection === 'crosswords' ? ['Easy', 'Normal', 'Answer key'] : ['Open printable PDF'];
    downloads.replaceChildren(...labels.filter(label => selected.downloads[label]).map(label => {
      const link = document.createElement('a');
      link.href = localURL(selected.downloads[label]);
      link.textContent = label;
      link.target = '_blank';
      link.rel = 'noopener';
      link.setAttribute('aria-label', `${label} PDF for ${selected.title} (opens in a new tab)`);
      return link;
    }));
    const course = document.getElementById('puzzle-course');
    course.href = localURL(selected.course);
    course.textContent = selected.lesson ? 'Read this lesson' : 'Read this module';
    document.getElementById('puzzle-help').textContent = collection === 'crosswords'
      ? 'Easy includes a word bank. Easy and Normal are fillable PDFs. All PDFs open in a new tab.'
      : 'Open the PDF to print. Choose landscape orientation and fit to page. PDFs open in a new tab.';
    const index = available.indexOf(selected);
    previous.disabled = index === 0;
    next.disabled = index === available.length - 1;
    document.getElementById('puzzle-status').textContent = `${collection === 'crosswords' ? 'Crossword' : 'Colouring page'} ${index + 1} of ${available.length}`;
    if (push) history.pushState(null, '', address(collection, selected.id));
  }
  /* Restore shared links and browser Back/Forward; old collection anchors still work. */
  function restore() {
    const params = new URLSearchParams(location.search);
    collection = params.get('collection') === 'colouring' || (!params.has('collection') && location.hash === '#colouring-pages') ? 'colouring' : 'crosswords';
    const aliases = {'#what-is-fnd':'lesson-1','#biopsychosocial-what':'lesson-2','#recovery':'lesson-3','#available-capacity':'lesson-4','#positive-signs':'lesson-5','#tests-and-coexisting-conditions':'lesson-6','#module-1-review-crossword':'module-1-review'};
    selected = items().find(item => item.id === (params.get('puzzle') || aliases[location.hash])) || items()[0];
    render();
  }
  fetch(root.dataset.catalog).then(response => {
    if (!response.ok) throw new Error(`Puzzle catalog HTTP ${response.status}`);
    return response.json();
  }).then(data => {
    catalog = data;
    if (!catalog.items?.length || !catalog.modules) throw new Error('Empty puzzle catalog');
    /* Validate every URL before hiding the fallback, avoiding partially working controls. */
    catalog.items.forEach(item => [item.image, item.course, ...Object.values(item.downloads)].forEach(localURL));
    restore();
    moduleSelect.addEventListener('change', () => {
      selected = items().find(item => String(item.module) === moduleSelect.value);
      render(true);
    });
    lessonSelect.addEventListener('change', () => {
      selected = items().find(item => item.id === lessonSelect.value);
      render(true);
    });
    [previous, next].forEach((button, direction) => button.addEventListener('click', () => {
      selected = items()[items().indexOf(selected) + (direction ? 1 : -1)];
      render(true);
    }));
    tabs.forEach(tab => tab.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      collection = tab.dataset.collection;
      selected = items().find(item => item.id === selected.id) || items()[0];
      render(true);
    }));
    window.addEventListener('popstate', restore);
    window.addEventListener('hashchange', restore);
    document.getElementById('puzzle-fallback').hidden = true;
    root.hidden = false;
  }).catch(error => {
    /* Downloads stay visible on failure; no visitor information is sent anywhere. */
    console.warn('Puzzle selector unavailable; showing download list.', error.message);
  });
})();
