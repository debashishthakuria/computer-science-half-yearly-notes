/* Navigation, topic completion and search; lesson content remains in the HTML. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const sections = [...document.querySelectorAll('.study-main > section')];
  const links = [...document.querySelectorAll('#studyNav a[data-route]')];
  const ids = ['home', ...sections.map(s => s.id)];
  const key = 'cs-halfyear-topics-v2';
  let completed;
  try { completed = new Set(JSON.parse(localStorage.getItem(key) || '[]').filter(x => ids.includes(x))); }
  catch { completed = new Set(); }
  let lastFocus = null;
  function save() { try { localStorage.setItem(key, JSON.stringify([...completed])); } catch {} }
  function update() {
    document.querySelectorAll('.mark-done').forEach(button => {
      const yes = completed.has(button.dataset.section);
      button.setAttribute('aria-pressed', String(yes));
      button.textContent = yes ? '✓ Studied · tap to undo' : 'Mark this topic studied';
    });
    const count = completed.size, total = sections.length;
    $('progressFill').style.width = `${(count / total) * 100}%`;
    $('progressLabel').textContent = `${count} of ${total} topics studied`;
    const next = sections.find(s => !completed.has(s.id)) || sections[0];
    const name = links.find(a => a.dataset.route === next.id)?.textContent || next.id;
    $('nextTitle').textContent = count === total ? 'All topics marked studied' : name;
    $('nextDescription').textContent = count === total ? 'Review your weak areas or test yourself again.' : 'Open this topic, study its examples, then mark it complete.';
    $('continueLink').href = '#' + (count === total ? 'questions' : next.id);
    $('continueLink').textContent = count === total ? 'Test yourself again →' : 'Continue studying →';
  }
  document.querySelectorAll('.mark-done').forEach(button => button.addEventListener('click', () => {
    const id = button.dataset.section;
    completed.has(id) ? completed.delete(id) : completed.add(id);
    save(); update();
  }));
  function route() {
    const id = location.hash.slice(1) || 'home';
    const target = ids.includes(id) ? id : 'home';
    const leaving = document.activeElement;
    const isInternal = leaving && leaving.closest && leaving.closest('.study-main');
    document.querySelectorAll('.study-main > header, .study-main > section').forEach(s => {
      s.classList.toggle('is-active', s.id === target);
      s.setAttribute('aria-hidden', String(s.id !== target));
    });
    links.forEach(a => {
      if (a.dataset.route === target) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });
    $('studyNav').classList.remove('is-open');
    $('navToggle').setAttribute('aria-expanded', 'false');
    if (isInternal && !leaving.closest('#' + target)) {
      const heading = document.querySelector('#' + target + ' h1, #' + target + ' h2');
      if (heading) { heading.tabIndex = -1; heading.focus({preventScroll:true}); }
    }
    window.scrollTo(0, 0);
    document.title = (target === 'home' ? 'Computer Science · Study workspace' :
      (links.find(a => a.dataset.route === target)?.textContent || target) + ' · Computer Science');
  }
  $('navToggle').addEventListener('click', () => {
    const opened = $('studyNav').classList.toggle('is-open');
    $('navToggle').setAttribute('aria-expanded', String(opened));
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && $('studyNav').classList.contains('is-open')) {
      $('studyNav').classList.remove('is-open'); $('navToggle').setAttribute('aria-expanded', 'false'); $('navToggle').focus();
    }
  });
  document.addEventListener('click', e => {
    if (e.target.closest('#studyNav,#navToggle')) return;
    if ($('studyNav').classList.contains('is-open')) {
      $('studyNav').classList.remove('is-open'); $('navToggle').setAttribute('aria-expanded', 'false');
    }
  });
  const searchable = sections.flatMap(s => {
    const topic = links.find(a => a.dataset.route === s.id)?.textContent || s.id;
    const cards = [...s.querySelectorAll('details.card')];
    return [{id:s.id, title:topic, summary:'Open the whole topic', card:null},
      ...cards.map((card,i) => ({id:s.id,title:card.querySelector('summary')?.textContent.trim() || topic,
        summary:topic,card:i}))];
  });
  const results = $('searchResults'), search = $('lessonSearch');
  search.addEventListener('input', () => {
    results.replaceChildren();
    const q = search.value.trim().toLowerCase();
    if (q.length < 2) return;
    const found = searchable.filter(x => (x.title + ' ' + x.summary).toLowerCase().includes(q)).slice(0, 8);
    if (!found.length) { results.textContent = 'No matches. Try a shorter keyword.'; return; }
    found.forEach(item => {
      const button = document.createElement('button'); button.type='button';
      const strong = document.createElement('strong'), small = document.createElement('small');
      strong.textContent = item.title; small.textContent = item.summary;
      button.append(strong,small);
      button.addEventListener('click', () => {
        location.hash = '#' + item.id;
        route();
        if (item.card !== null) {
          const card = sections.find(s => s.id === item.id).querySelectorAll('details.card')[item.card];
          card.open = true;
          card.scrollIntoView({block:'center',behavior:'smooth'});
          card.querySelector('summary')?.focus();
        }
      });
      results.append(button);
    });
  });
  // Existing question links route into a hidden topic; reveal the destination first.
  document.querySelectorAll('.practice-jump').forEach(link => link.addEventListener('click', e => {
    e.preventDefault();
    e.stopImmediatePropagation();
    const match = link.dataset.match;
    const target = [...document.querySelectorAll('.open-lab')].find(b =>
      b.closest('.answer')?.querySelector('pre code')?.textContent.includes(match));
    if (!target) return;
    location.hash = '#' + target.closest('section').id;
    route();
    target.closest('details').open = true;
    target.click();
  }, true));
  window.studyWorkspace = true;
  window.addEventListener('hashchange', route);
  update(); route();
})();
