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
assert text(home.select_one('#featured-event a[href="news.html#historical-recaps"]')) == 'Explore Past Charity Contest Recaps →'
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
        assert story.select_one('.recording-pending')
        assert 'https://youtu.be/U1bpogh_TXU' in (root/'docs/video-link-audit.md').read_text()
    else:
        assert [a['href'] for a in story.select('a')] == [a['href'] for a in old.select('a')], key
for year in [2024, 2025]:
    assert pages['news.html'].select_one(f'#historical-recaps a[href="#news-charity-{year}"]')
assert not pages['news.html'].select_one('#historical-recaps a[href*="2023"]'), 'No unconfirmed 2023 recap'

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
sessions_new = pages['programs.html'].select('.sessions li')
assert len(sessions_old) == len(sessions_new) == 9
# Session descriptions stay intact while date presentation, watch URLs/status may change.
for old, new in zip(sessions_old, sessions_new):
    description = ''.join(str(t) for t in old.find_all(string=True, recursive=False)).strip().rstrip('—').strip()
    assert description in text(new), description
for session in sessions_new:
    assert session.select_one('time[datetime]')
    if session.get('data-video-status') == 'needs-confirmation':
        assert session.select_one('.recording-pending') and not session.select('a'), session['id']
    for action in session.select('a'):
        assert '@MathTogetherCanada' not in action['href'], session['id']
assert pages['programs.html'].select_one('#livestream .livestream-channel a')['href'] == 'https://www.youtube.com/@MathTogetherCanada'

supporters = pages['get-involved.html'].select('.supporter-grid > a')
assert len(supporters) == 6
expected_urls = {'https://ttmath.ca/', 'https://www.citadel.com', 'https://www.janestreet.com/', 'https://wsdental.nextcard.ai/', 'http://www.hongdental2014.com/', 'https://blackbeltworld.ca/'}
assert {a['href'] for a in supporters} == expected_urls
for supporter in supporters:
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
print('PASS: local files/anchors, navigation, FAQ preservation, profile text/photos/positions, 17 News records and date precision, nine sessions, six supporters and homepage statistics.')
