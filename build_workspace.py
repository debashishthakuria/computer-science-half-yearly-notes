"""Reframe generated revision content into a navigable study workspace.
Runs after build.py and writes index.html; the lesson source remains build.py/base.html.
"""
from pathlib import Path
from html.parser import HTMLParser
import re

ROOT = Path(__file__).parent
page = (ROOT / 'index.html').read_text(encoding='utf-8')
# The original builder is the content source. This second stage owns the product shell.
page = re.sub(r'<style>.*?</style>', '<link rel="stylesheet" href="study.css">', page, count=1, flags=re.S)
page = page.replace('<div class="top"><div class="wrap">', '<div class="top"><div class="wrap">', 1)
page = page.replace('<span class="tag">Separate half-yearly revision page</span>', '<span class="tag">Your personal revision workspace · HS final year</span><button type="button" class="mobile-nav-toggle" id="navToggle" aria-expanded="false" aria-controls="studyNav">Topics</button>', 1)
page = page.replace('<main class="wrap" id="top">', '<div class="site-layout"><aside id="studyNav" class="nav" aria-label="Study sections"></aside><main class="study-main" id="top">', 1)
page = re.sub(r'<nav class="nav" aria-label="Jump to topic">.*?</nav>', '', page, count=1)
page = page.replace('</main><footer>', '</main></div><footer>', 1)
# The opening caution and exact closing credit from the published guide remain untouched.

NAV = [
    ('map', 'Overview'), ('concepts', 'Key concepts'), ('turbo', 'Turbo C++ setup'),
    ('oop', 'Object-oriented C++'), ('cppprograms', 'C++ programs'), ('dbms', 'Database concepts'),
    ('networks', 'Networks'), ('sql', 'SQL foundations'), ('commands', 'SQL commands'),
    ('practice', 'SQL practice'), ('topics', 'Your PDF topic list'), ('wider', 'Other board units'),
    ('questions', 'Exam-style questions'), ('recap', 'Quick revision'),
    ('corrections', 'Corrections'), ('sources', 'Sources & scope')
]
sections = re.findall(r'<section id="([\w-]+)"', page)
assert set(sections) == {sid for sid, _ in NAV}, (sections, NAV)

def nav_group(label, ids):
    return '<div class="nav-label">' + label + '</div>' + ''.join('<a href="#' + sid + '" data-route="' + sid + '">' + name + '</a>' for sid, name in NAV if sid in ids)

nav = (nav_group('Start', ['map', 'concepts', 'recap']) +
       nav_group('Learn & code', ['turbo', 'oop', 'cppprograms', 'dbms']) +
       nav_group('From your notes', ['networks', 'sql', 'commands', 'practice', 'topics']) +
       nav_group('Test yourself', ['questions', 'wider']) +
       nav_group('Reference', ['corrections', 'sources']))
page = page.replace('<aside id="studyNav" class="nav" aria-label="Study sections"></aside>',
                    '<aside id="studyNav" class="nav" aria-label="Study sections">' + nav + '</aside>')

old_header = '<header><h1>Computer Science<br>revision guide</h1><p>Important concepts first, then flowcharts, Turbo C++-style programs, detailed notes and answered ASSEB-style practice. Your common-question PDF remains in the guide below.</p></header>'
new_header = '''<header id="home" class="is-active"><div class="home-lede"><p class="eyebrow">A focused way to prepare</p><h1>Computer Science,<br>made easier to study.</h1><p class="home-intro">Learn one topic at a time. Read the idea, trace a worked example, try the code, then check yourself. Your supplied notes and the official full-year syllabus are kept distinct.</p></div>
<div class="home-status"><div class="progress-line" aria-hidden="true"><span id="progressFill"></span></div><strong id="progressLabel">Your study progress</strong></div>
<div class="home-grid"><article class="home-panel"><p class="eyebrow">Recommended next</p><h2 id="nextTitle">Start with the study map</h2><p id="nextDescription">Know what is high priority for the half-yearly and what needs teacher confirmation.</p><a class="home-action" id="continueLink" href="#map">Continue studying →</a></article>
<article class="home-panel"><p class="eyebrow">Practice C++ directly</p><h2>Open the coding window</h2><p>Start with a working Turbo C++-style answer, edit it, add input and run it. This uses an online GCC C++ simulation, not the Turbo C++ compiler.</p><a class="home-action" href="#cppprograms">Choose a C++ program →</a><button type="button" class="home-action open-blank-lab">Open blank C++ editor →</button></article>
<article class="home-panel"><p class="eyebrow">Use your time well</p><h2>Choose a study mode</h2><div class="home-links"><a href="#concepts">Learn concepts</a><a href="#oop">Work through C++</a><a href="#questions">Test yourself</a><a href="#recap">Revise quickly</a></div><p style="margin-top:15px">Every C++ example has an editable practice button. Program questions open their worked answer in the editor.</p></article>
<article class="home-panel wide"><p class="eyebrow">Find exactly what you need</p><h2>Search the guide</h2><div class="search-wrap"><input id="lessonSearch" type="search" placeholder="Try: constructor, topology, SQL, stack…" aria-label="Search study topics"></div><div id="searchResults" class="search-results" aria-live="polite"></div></article>
</div><p class="small" style="margin-top:22px">Important: the local half-yearly chapter list has not been independently confirmed. Question styles here are original practice, not official or guaranteed predictions.</p></header>'''
assert old_header in page
page = page.replace(old_header, new_header, 1)

# Cards remain native <details> controls, but each unit becomes a separate screen.
for n, (sid, label) in enumerate(NAV, 1):
    key = '<section id="' + sid + '">'
    assert key in page, key
    next_sid, next_name = NAV[(n) % len(NAV)]
    prev_sid, prev_name = NAV[(n-2) % len(NAV)]
    top = '<div class="section-top"><div><p class="section-kicker">Study guide / ' + ('Practice' if sid in ('questions','practice','cppprograms') else 'Learn') + '</p></div><span class="section-number">' + str(n).zfill(2) + ' / ' + str(len(NAV)) + '</span></div>'
    meta = '<div class="section-meta"><button type="button" class="mark-done" data-section="' + sid + '" aria-pressed="false">Mark this topic studied</button><a href="#home" class="quick-link">Back to home</a>' + ('<button type="button" class="open-blank-lab">Open blank C++ editor</button>' if sid in ('oop', 'cppprograms', 'questions') else '') + '</div>'
    page = page.replace(key, key + top, 1)
    # place controls after the section's first subtitle (or first heading when no subtitle)
    start = page.index(key)
    end = page.index('</section>', start)
    block = page[start:end]
    if '<p class="sub">' in block:
        block = re.sub(r'(<p class="sub">.*?</p>)', r'\1' + meta, block, count=1, flags=re.S)
    else:
        block = re.sub(r'(</h2>)', r'\1' + meta, block, count=1)
    page = page[:start] + block + page[end:]
    end = page.index('</section>', start)
    bottom = '<div class="section-bottom"><a class="jump-next jump-prev" href="#' + prev_sid + '">← ' + prev_name + '</a><a class="jump-next" href="#' + next_sid + '">' + next_name + ' →</a></div>'
    page = page[:end] + bottom + page[end:]

# Correct a formerly overconfident source label: no school-issued scope was supplied.
page = page.replace('the existing study plan names <strong>OOP in C++ and DBMS/SQL</strong> for this half-yearly.', 'the existing personal study plan names <strong>OOP in C++ and DBMS/SQL</strong> for this half-yearly, but is not a school-issued syllabus.')
page = page.replace('Beyond the confirmed focus', 'Beyond the study-plan focus')
page = page.replace('Other board units', 'Other full-year units')
page = page.replace('<script src="app.js" defer></script>', '<script src="app.js" defer></script><script src="workspace.js" defer></script>')
page = page.replace('</head>', '<style>.home-action.open-blank-lab{border:0;margin-top:10px;margin-left:0;display:inline-block;min-height:44px}.section-meta .open-blank-lab{background:var(--accent);color:#fff;border:0;border-radius:8px;padding:8px 12px;font-weight:700}#home .home-panel .open-blank-lab:hover,.section-meta .open-blank-lab:hover{background:var(--accent-deep)}</style></head>', 1)
(ROOT / 'index.html').write_text(page, encoding='utf-8')
print('workspace:', len(NAV), 'topic screens,', page.count('class="open-lab"'), 'practice links')
