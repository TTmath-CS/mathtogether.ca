"""Static link integrity and targeted content-preservation checks for round 3."""
import json
import re
import subprocess
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlsplit
from bs4 import BeautifulSoup as S

root = Path(__file__).resolve().parents[1]
pages = {f.name: S(f.read_text(), 'html.parser') for f in root.glob('*.html')}
def original(name):
    return S(subprocess.check_output(['git', 'show', 'origin/main:' + name], cwd=root, text=True), 'html.parser')
def text(node):
    return re.sub(r'\s+', ' ', node.get_text(' ', strip=True)).strip()

errors = []
for name, soup in pages.items():
    ids = [t['id'] for t in soup.select('[id]')]
    assert len(ids) == len(set(ids)), (name, 'duplicate ID')
    assert len(soup.select('h1')) == 1, (name, 'h1 count')
    assert not soup.select('header nav a[href="faq.html"], header nav a[href="index.html#faq"]'), (name, 'FAQ navigation')
    assert [text(a) for a in soup.select('header nav a')] == ['Home', 'Programs', 'News', 'Team', 'Get Involved', 'Join Us'], name
    for a in soup.select('[href], [src]'):
        ref = a.get('href', a.get('src'))
        u = urlsplit(ref)
        if u.scheme or u.netloc:
            continue
        file = unquote(u.path) or name
        if not (root / file).is_file():
            errors.append((name, ref, 'missing file'))
        elif u.fragment and file in pages and not pages[file].find(id=unquote(u.fragment)):
            errors.append((name, ref, 'missing anchor'))
assert not errors, errors

home = pages['index.html']
assert len(home.select('.stat-icon')) == 4
assert text(home.select_one('.stat-copy strong')) == '850+'
assert text(home.select_one('.stat-copy span')) == 'Students Reached'
assert text(home.select_one('[data-supporter-count]')) == '6'
assert len(home.select('.home-programs .cards article')) == 3
assert not home.select('.home-story-card'), 'Homepage must derive news from news.html'
assert home.select_one('[data-latest-news]')
assert home.select_one('#featured-event a[href="news.html#news-charity-2026"]')
assert text(home.select_one('#featured-event .home-past-recaps summary')) == 'Explore Past Charity Contest Recaps →'
assert [text(p) for p in original('index.html').select('.about-body p')] == [text(p) for p in home.select('.about-body p')]
faq_old = original('faq.html').select('details.faq')
faq_new = home.select('#faq details.faq')
assert len(faq_old) == len(faq_new) == 5
assert [text(f) for f in faq_old] == [text(f) for f in faq_new], 'FAQ question/answer text changed'
assert [[a['href'] for a in f.select('a')] for f in faq_old] == [[a['href'] for a in f.select('a')] for f in faq_new]
assert pages['faq.html'].select_one('[data-legacy-target="index.html#faq"]')

news_old = {s['id']: s for s in original('news.html').select('.story')}
news_new = {s['id']: s for s in pages['news.html'].select('.story')}
assert news_old.keys() == news_new.keys() and len(news_new) == 17
for key, story in news_new.items():
    old = news_old[key]
    assert text(story.h3) == text(old.h3), key
    assert story.select_one('img')['src'] == old.select_one('img')['src'], key
    for attr in ['data-date', 'data-year', 'data-date-status']:
        assert story.get(attr) == old.get(attr), (key, attr, 'date precision changed')
    if story.get('data-date'):
        date.fromisoformat(story['data-date'])
    elif story.get('data-year'):
        assert re.fullmatch(r'\d{4}', story['data-year'])
        assert story.get('data-date-status') == 'year-only'
    else:
        assert story.get('data-date-status') == 'needs-confirmation'
    if key == 'news-summer-camp-voices':
        assert not story.select('a[href="https://youtu.be/U1bpogh_TXU"]'), 'Wrong quant interview video must not remain on summer camps'
        assert not story.select_one('.recording-pending')
        expected = ['JRGoP28tTjE', 'r3zC6nGIJXQ', '7tPu9H0FQ88', 'NdSrw3FwQCU', '9Lm0e-yhQgs']
        assert [a['href'] for a in story.select('a')] == ['https://www.youtube.com/watch?v='+video for video in expected]
        assert all(len(text(a)) > 10 for a in story.select('a'))
        assert 'https://youtu.be/U1bpogh_TXU' in (root/'docs/video-link-audit.md').read_text()
    elif key == 'news-interview-yingshan':
        assert [a['href'] for a in story.select('a')] == ['https://www.youtube.com/watch?v=Bkamz7QCS7I&t=5s', 'https://www.youtube.com/watch?v=gnG3twj-XNw']
        assert all(len(text(a)) > 10 for a in story.select('a'))
    else:
        assert [a['href'] for a in story.select('a')] == [a['href'] for a in old.select('a')], key
for year in [2024, 2025]:
    assert home.select_one(f'.home-past-recaps a[href="news.html#news-charity-{year}"]')
assert not pages['news.html'].select_one('#historical-recaps'), 'News keeps its original story-list layout'
assert not home.select_one('.home-past-recaps a[href*="2023"]'), 'No unconfirmed 2023 recap'

team_old = {text(m.h3): m for m in original('team.html').select('.member')}
team_new = {text(m.h3): m for m in pages['team.html'].select('.member')}
assert len(team_old) == len(team_new) == 16
updated = {'Perry Dai', 'Kaylyn Zhang', 'Prince Zhang'}
for name, old in team_old.items():
    new = team_new['Xuanyi(Prince) Zhang' if name == 'Prince Zhang' else name]
    assert new.select_one('img')['src'] == old.select_one('img')['src'], (name, 'photo')
    assert text(new.select_one('.role')) == text(old.select_one('.role')), (name, 'position')
    if name not in updated:
        assert str(old) == str(new), (name, 'unrequested profile change')
expected_bios = {
    'Perry Dai': [
        'Perry is passionate about mathematics, especially about creating opportunities for younger students to discover their own love of math. He is an IMO and USAMO gold medallist and a CMO silver medallist.',
        'Beyond mathematics, Perry enjoys exploring linguistics and economics, playing ultimate frisbee, and challenging himself with games like Tetris and SET. At Math Together Canada, he hopes to share his experiences and interests, inspire deeper engagement in math, and help create an inclusive, collaborative community.'
    ],
    'Kaylyn Zhang': [
        'Kaylyn is a passionate math student whose achievements include honourable mention and Olympiad bronze at Math Prize for Girls, CJMO bronze, and top 50 at ARML and HMMT November. She has also qualified for the APMO and attended the IMO summer training camp and Canada/USA Mathcamp in 2026.',
        'Outside of math, she has a third degree black belt in ITF Taekwondo. She hopes that through Math Together Canada, younger students will feel inspired to explore mathematics and have a welcoming community where they can learn and grow.'
    ],
    'Xuanyi(Prince) Zhang': [
        'A motivated math competitor, Prince hopes to foster that same curiosity and passion in younger students. He is a CJMO silver medallist and an individual 3rd place finisher at HMMT November.',
        "When he's not solving math problems, he is probably playing music or volleyball, all driven by an interest in exploring new areas. At Math Together Canada, Prince aims to share his enthusiasm for math by sparking interest in others and laying a strong foundation for their future learning and growth."
    ]
}
for name, expected in expected_bios.items():
    assert [text(p) for p in team_new[name].select('details p')] == expected, name

sessions_old = original('programs.html').select('.sessions li')
sessions_new = pages['programs.html'].select('.sessions > li')
assert len(sessions_old) == 9 and len(sessions_new) == 8
# Only the five sessions explicitly removed by the user may be removed.
removed_descriptions = [
    'Community discussion after the Math Kangaroo Contest, with CMO/CJMO qualifiers',
    'Interactive Q&A session: your burning questions, answered by math experts',
    'Complete breakdown of the 2024 AMC10A Contest',
    'Complete breakdown of the 2025 Fermat Contest',
    'Waterloo Pascal & Fermat solutions, before official answers are out',
]
retained_descriptions = []
for old in sessions_old:
    description = ''.join(str(t) for t in old.find_all(string=True, recursive=False)).strip().rstrip('—').strip()
    if description not in removed_descriptions:
        retained_descriptions.append(description)
assert len(retained_descriptions) == 4
for description in retained_descriptions:
    assert any(description in text(session) for session in sessions_new), description
for removed in removed_descriptions:
    assert removed not in text(pages['programs.html'])
assert not pages['programs.html'].select('#session-kangaroo-2025, #session-questions-2025, #session-amc10a-2024, #session-waterloo-2025, #session-fermat-2025, .sessions .recording-pending')
for session in sessions_new:
    assert session.select_one('time[datetime]')
    assert session.select('a'), session['id']
    for action in session.select('a'):
        assert '@MathTogetherCanada' not in action['href'], session['id']
        assert action.get('target') == '_blank'
        assert {'noopener', 'noreferrer'} <= set(action.get('rel', []))
        assert text(action) in action.get('aria-label', text(action)), session['id']
        u = urlsplit(action['href'])
        assert (u.netloc == 'youtu.be' and u.path.strip('/')) or (u.netloc in {'youtube.com', 'www.youtube.com'} and u.path == '/watch' and 'v=' in u.query), action['href']
expected_comc = ['9343O-spIAI', '24KYT2FrM_Q', 'WeVz3kbnq4U', 'kObBbe_cfIE']
expected_amc10 = ['WFVfabjtnb4', 'GCJ6smMF7io', '2AHhJ-EjRn4', 'quRP3FsrB6k', 'TiIWCAKGZQg', 'VqWHUufAXvs']
assert [a['href'] for a in pages['programs.html'].select('#session-comc-2025 a')] == ['https://www.youtube.com/watch?v='+video for video in expected_comc]
assert [a['href'] for a in pages['programs.html'].select('#session-amc10-2025 a')] == ['https://www.youtube.com/watch?v='+video for video in expected_amc10]
new_sessions = {
    'session-cayley-2026': ['v-AzSSLHm98', 'UXjvfT29EQA', 'V7MscLlK4pI'],
    'session-galois-2026': ['3QLrRolXlAw'],
    'session-fryer-2026': ['waVmtYh56_M'],
    'session-pascal-2026': ['CUvSTc-RhGc'],
}
for session_id, videos in new_sessions.items():
    session = pages['programs.html'].select_one('#'+session_id)
    assert session is not None, session_id
    assert [a['href'] for a in session.select('a')] == ['https://www.youtube.com/watch?v='+video for video in videos]
    assert session.select_one('time')['datetime'] == '2026-08', 'The owner supplied August 2026 for these recordings'
    assert text(session.select_one('time')) == 'Aug 2026'
urls = [a['href'] for session in sessions_new for a in session.select('a')]
assert len(urls) == len(set(urls)), 'Duplicate recording destinations'
expected_amc12 = ['nXs682bcsNQ', 'MeyLmhwl-FA', 'PeSHSVGMpNI']
assert [a['href'] for a in pages['programs.html'].select('#session-amc12-2025 a')] == ['https://www.youtube.com/watch?v='+video for video in expected_amc12]
assert len(pages['programs.html'].select('#session-comc-2025 a')) == 4
assert len(pages['programs.html'].select('#session-amc10-2025 a')) == 6
assert pages['programs.html'].select_one('#livestream .livestream-channel a')['href'] == 'https://www.youtube.com/@MathTogetherCanada'

supporters = pages['get-involved.html'].select('.supporter-grid > a')
assert len(supporters) == 6
expected_urls = {'https://ttmath.ca/', 'https://www.citadel.com', 'https://www.janestreet.com/', 'https://wsdental.nextcard.ai/', 'http://www.hongdental2014.com/', 'https://blackbeltworld.ca/'}
assert {a['href'] for a in supporters} == expected_urls
for supporter in supporters:
    assert len(supporter.select('img')) == 1, 'All supplied supporter logos must be displayed'
    assert supporter.get('target') == '_blank'
    assert {'noopener', 'noreferrer'} <= set(supporter.get('rel', []))
    assert text(supporter) or supporter.get('aria-label')
    for image in supporter.select('img'):
        assert image.get('alt')
assert 'Supporters are listed alphabetically, with no ranking implied.' in text(pages['get-involved.html'])
assert not pages['get-involved.html'].select('.sponsor .rank, .sponsor .role')
data = json.loads((root / 'data/supporters.json').read_text())
ordered = sorted(data, key=lambda s:s['sort_name'].casefold())
assert [s['data-supporter-id'] for s in supporters] == [s['id'] for s in ordered]
assert len({s['id'] for s in data}) == 6
subprocess.run(['python3', 'scripts/render_supporters.py', '--check'], cwd=root, check=True)
print('PASS: local files/anchors, navigation, FAQ preservation, profile text/photos/positions, 17 News records and date precision, eight confirmed sessions, six supporters and homepage statistics.')
