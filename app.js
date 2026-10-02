/* Practical lab: Judge0 GCC C++ sandbox, not a Turbo C++ emulator. */
(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const lab = $('lab'), editor = $('editor'), input = $('stdin'), output = $('runOutput');
  let original = '', busy = false, previousFocus = null;
  const buttons = [...document.querySelectorAll('.open-lab')];
  const cards = [...document.querySelectorAll('details.card')];
  const base64 = (text) => btoa([...new TextEncoder().encode(text)].map(b => String.fromCharCode(b)).join(''));
  const unbase64 = (text) => new TextDecoder().decode(Uint8Array.from(atob(text), c => c.charCodeAt(0)));
  function adapt(code) {
    // Legacy Turbo C++ headers/streams are unavailable on GCC. This transforms only
    // the tutorial's header conventions; the editor still displays the original answer.
    return code.replace(/^\s*#include\s*<iostream\.h>/gm, '#include <iostream>\nusing namespace std;')
      .replace(/^\s*#include\s*<fstream\.h>/gm, '#include <fstream>\nusing namespace std;')
      .replace(/^\s*#include\s*<conio\.h>/gm, '')
      .replace(/\bclrscr\s*\(\s*\)\s*;/g, '')
      .replace(/\bgetch\s*\(\s*\)\s*;/g, '');
  }
  function open(button) {
    const pre = button?.closest('.answer')?.querySelector('pre code');
    previousFocus = button;
    original = pre?.textContent || '#include <iostream.h>\nint main() {\n    cout << "Hello, world!\\n";\n    return 0;\n}';
    editor.value = original;
    input.value = '';
    output.textContent = 'Ready to compile. Edit the answer or run it as shown.';
    $('labType').textContent = 'Turbo C++-style .CPP · online GCC C++ simulation';
    lab.hidden = false;
    document.body.style.overflow = 'hidden';
    editor.focus();
  }
  function close() {
    if (busy) return;
    lab.hidden = true;
    document.body.style.overflow = '';
    previousFocus?.focus();
  }
  buttons.forEach(button => button.addEventListener('click', () => open(button)));
  document.querySelectorAll('.open-blank-lab').forEach(button => button.addEventListener('click', () => open(button)));
  $('closeLab').addEventListener('click', close);
  lab.addEventListener('click', e => { if (e.target === lab) close(); });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && !lab.hidden) close();
    if (e.key === 'Tab' && !lab.hidden) {
      const els = [...lab.querySelectorAll('button,textarea')].filter(x => !x.disabled);
      const first = els[0], last = els[els.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });
  $('resetCode').addEventListener('click', () => { editor.value = original; editor.focus(); output.textContent = 'Original answer restored.'; });
  document.querySelectorAll('.practice-jump').forEach(link => link.addEventListener('click', event => {
    if (window.studyWorkspace) return;
    event.preventDefault();
    const match = link.dataset.match;
    const target = buttons.find(b => b.closest('.answer')?.querySelector('pre code')?.textContent.includes(match));
    if (target) { target.closest('details').open = true; setTimeout(() => open(target), 180); }
  }));
  async function compile() {
    if (busy) return;
    if (!editor.value.trim()) { output.textContent = 'Write a program before running.'; return; }
    if (editor.value.length > 12000 || input.value.length > 2000) { output.textContent = 'Code or input is too long for this study lab.'; return; }
    busy = true;
    $('runCode').disabled = true;
    output.textContent = 'Compiling and running in a remote sandbox…';
    try {
      const response = await fetch('https://ce.judge0.com/submissions?base64_encoded=true&wait=true', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({language_id: 52,
          source_code: base64(adapt(editor.value)), stdin: base64(input.value),
          compiler_options: '-std=c++98',
          cpu_time_limit: 2, wall_time_limit: 5, memory_limit: 128000})
      });
      if (!response.ok) throw Error('Runner returned HTTP ' + response.status);
      const result = await response.json();
      const text = ['compile_output', 'stderr', 'stdout', 'message']
        .map(key => result[key] ? `${key}:\n${unbase64(result[key])}` : '').filter(Boolean).join('\n\n');
      output.textContent = (result.status?.description || 'Finished') + '\n\n' + (text || '(no output)');
    } catch (err) {
      output.textContent = 'Runner unavailable or blocked by your connection. Your code remains in the editor. Try later or copy it to your local compiler.\n' + err.message;
    } finally { busy = false; $('runCode').disabled = false; }
  }
  $('runCode').addEventListener('click', compile);
  editor.addEventListener('keydown', e => {
    if (e.key === 'Tab') { e.preventDefault(); const a = editor.selectionStart, b = editor.selectionEnd; editor.setRangeText('    ', a, b, 'end'); }
  });
  // Progress is local to this browser only; no login or stored program text.
  const key = 'cs-halfyear-answered-v1';
  let done;
  try { done = new Set(JSON.parse(localStorage.getItem(key) || '[]')); } catch { done = new Set(); }
  function display() { $('studyProgress').textContent = `${done.size} / ${cards.length} answers opened on this device`; }
  cards.forEach((card, i) => card.addEventListener('toggle', () => {
    if (card.open) { done.add(i); try { localStorage.setItem(key, JSON.stringify([...done])); } catch {} display(); }
  }));
  $('resetProgress').addEventListener('click', () => { done.clear(); try { localStorage.removeItem(key); } catch {} display(); });
  display();
})();
