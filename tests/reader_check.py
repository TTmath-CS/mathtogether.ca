"""Check content-only browser windows, source preservation, and reader failures."""
import os
import re
import shutil
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from bs4 import BeautifulSoup
from playwright.sync_api import Error, sync_playwright

BASE = 'http://127.0.0.1:8000/'
SOURCE = (Path(__file__).resolve().parents[1] / 'news.html').read_text()
NEWS = BeautifulSoup(SOURCE, 'html.parser')
checks = []


def normalized(value):
    return re.sub(r'\s+', ' ', value).strip()


def isolated_requests(route):
    """Exercise real local site files without requesting third-party services."""
    if urlsplit(route.request.url).netloc == urlsplit(BASE).netloc:
        route.continue_()
    elif route.request.resource_type == 'document':
        route.fulfill(status=200, content_type='text/html', body='<title>Video test fixture</title>')
    else:
        route.fulfill(status=200, body='')


def ready(page):
    page.wait_for_function('document.querySelector("#reader-story").getAttribute("aria-busy") === "false"')


def content_only(page):
    assert page.locator('header, nav, footer, .news-grid, .story-dialog').count() == 0
    assert page.locator('main').count() == 1
    assert page.locator('h1').count() == 1
    assert page.locator('#reader-close').is_visible()
    assert page.locator('#reader-close').get_attribute('type') == 'button'
    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'Reader overflows horizontally'
    assert urlsplit(page.url).path == '/read.html', 'Reader navigated to a full page'


def assert_story(page, story_id):
    story = NEWS.find(id=story_id)
    assert story is not None
    ready(page)
    content_only(page)
    title = normalized(story.h3.get_text())
    assert normalized(page.locator('#reader-title').text_content()) == title
    assert page.title() == title + ' — Math Together Canada'
    assert page.locator('#reader-status').is_hidden()
    assert page.locator('#reader-retry').is_hidden()
    details = story.find('details', recursive=False)
    if details:
        nodes = [node for node in details.find_all(recursive=False) if node.name != 'summary']
    else:
        nodes = [node for node in story.find_all(recursive=False)
                 if (node.name == 'p' and not {'date', 'story-preview'} & set(node.get('class', [])))
                 or 'story-video-links' in node.get('class', [])]
    expected_text = normalized(' '.join(node.get_text() for node in nodes))
    assert normalized(page.locator('.reader-body').text_content()) == expected_text, story_id
    assert page.locator('.reader-body img').evaluate_all('(images) => images.map(i => i.getAttribute("src"))') == [image['src'] for node in nodes for image in node.select('img')]
    assert page.locator('.reader-body a[href]').evaluate_all('(links) => links.map(a => a.getAttribute("href"))') == [link['href'] for node in nodes for link in node.select('a[href]')]
    assert page.locator('.reader-body a[href]').evaluate_all('''links => links.every(a =>
        a.target === '_blank' && a.relList.contains('noopener') && a.relList.contains('noreferrer'))''')
    date = story.find(class_='date', recursive=False)
    if date:
        assert normalized(page.locator('.reader-date').text_content()) == normalized(date.get_text())
        assert page.locator('.reader-date time').evaluate_all('(times) => times.map(t => t.getAttribute("datetime"))') == [time['datetime'] for time in date.select('time[datetime]')]
    if details:
        assert page.locator('.reader-cover').get_attribute('src') == story.select_one('.news-image img')['src']
    elif story.select('a[href*="youtu"]'):
        assert page.locator('.reader-video iframe').count() > 0, 'Video-only story needs its player'
        assert page.locator('.reader-cover').count() == 0, 'Video player should replace the duplicate poster'
    for frame in page.locator('.reader-video iframe').all():
        url = urlsplit(frame.get_attribute('src'))
        assert url.scheme == 'https' and url.netloc == 'www.youtube-nocookie.com'
        assert re.fullmatch('/embed/[A-Za-z0-9_-]{11}', url.path)
        assert 'autoplay' not in parse_qs(url.query)
        assert frame.get_attribute('title')
        assert frame.get_attribute('allowfullscreen') is not None


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium'), headless=True)
    for width in [375, 390, 768, 1440]:
        context = browser.new_context(viewport={'width': width, 'height': 900}, reduced_motion='reduce')
        context.route('**/*', isolated_requests)
        home = context.new_page()
        home.goto(BASE + 'index.html')
        home.wait_for_selector('.home-story-card')
        home.locator('.home-past-recaps summary').click()
        links = home.locator('#featured-event a[href^="read.html?story="], .home-story-card')
        assert links.count() == 6, 'Featured, both past recaps, and all three community stories need content windows'
        for index in range(links.count()):
            link = links.nth(index)
            link.scroll_into_view_if_needed()
            original_url, original_scroll = home.url, home.evaluate('scrollY')
            destination = link.get_attribute('href')
            story_id = parse_qs(urlsplit(destination).query)['story'][0]
            with context.expect_page() as opened:
                link.click()
            reader = opened.value
            reader.wait_for_url(BASE + destination)
            reader.set_viewport_size({'width': width, 'height': 900})
            assert_story(reader, story_id)
            assert home.url == original_url
            assert abs(home.evaluate('scrollY') - original_scroll) <= 1, (width, story_id, 'Home scrolled')
            assert reader.evaluate('window.opener === null'), 'Reader must not expose the homepage opener'
            with reader.expect_event('close'):
                try:
                    if index % 2:
                        reader.keyboard.press('Escape')
                    else:
                        reader.locator('#reader-close').click()
                except Error:
                    # Chromium may close the script-opened window before the
                    # input dispatch reports success to Playwright.
                    if not reader.is_closed():
                        raise
            assert len(context.pages) == 1
            checks.append((width, story_id))
        context.close()

    # An unknown/missing ID stays in the focused reader with a useful status.
    context = browser.new_context(viewport={'width': 390, 'height': 844}, reduced_motion='reduce')
    context.route('**/*', isolated_requests)
    page = context.new_page()
    for query in ['', '?story=not-a-real-story', '?story=main-content']:
        page.goto(BASE + 'read.html' + query)
        ready(page)
        content_only(page)
        assert page.locator('#reader-title').inner_text() == 'Story unavailable'
        assert page.locator('#reader-status').is_visible()
        assert page.locator('#reader-status').inner_text()
        assert page.locator('#reader-retry').is_visible()
        assert page.locator('#reader-content').text_content() == ''

    # A transient fetch failure can be retried without a redirect or stale body.
    attempts = []
    def fail_once(route):
        attempts.append(route.request.url)
        if len(attempts) == 1:
            route.fulfill(status=503, body='Temporarily unavailable')
        else:
            route.continue_()
    context.route('**/news.html', fail_once)
    page.goto(BASE + 'read.html?story=news-charity-2025')
    ready(page)
    assert page.locator('#reader-title').inner_text() == 'Story unavailable'
    page.locator('#reader-retry').click()
    assert_story(page, 'news-charity-2025')
    assert len(attempts) == 2, 'Exactly one fetch per initial load or retry'
    context.unroute('**/news.html', fail_once)

    # Preserve structured article content and links; embed only exact video URLs.
    fixture = '''<article class="story" id="news-reader-fixture"><div class="news-image"><img src="assets/img/news-picnic.jpg" alt="Community"></div><h3>Reader fixture</h3><p class="date"><time datetime="2025-05">May 2025</time></p><details><summary>Read</summary><p>First paragraph.</p><h2>Full content</h2><ul><li>First item</li><li>Second item</li></ul><p><a href="https://www.youtube.com/watch?v=Bkamz7QCS7I&amp;t=5s">Approved video</a></p><p><a href="https://youtu.be/gnG3twj-XNw">Second video</a></p><p><a href="https://www.youtube.com/watch?v=Bkamz7QCS7I">Duplicate video</a></p><p><a href="https://www.youtube.com/@MathTogetherCanada">Channel</a></p><p><a href="https://www.youtube.com.evil.example/watch?v=Bkamz7QCS7I">Lookalike host</a></p><p><a href="https://www.youtube.com/watch?v=short">Malformed ID</a></p><p><a href="http://www.youtube.com/watch?v=Bkamz7QCS7I">Non-HTTPS video</a></p></details></article>'''
    changed = SOURCE.replace('<div class="news-grid">', '<div class="news-grid">' + fixture)
    context.route('**/news.html', lambda route: route.fulfill(status=200, content_type='text/html', body=changed))
    page.goto(BASE + 'read.html?story=news-reader-fixture')
    ready(page)
    content_only(page)
    assert page.locator('#reader-title').inner_text() == 'Reader fixture'
    assert page.locator('.reader-body h2').inner_text() == 'Full content'
    assert page.locator('.reader-body li').all_text_contents() == ['First item', 'Second item']
    assert page.locator('.reader-body a').count() == 7, 'Original Watch links must remain available'
    assert page.locator('.reader-video iframe').evaluate_all('(frames) => frames.map(f => f.getAttribute("src"))') == ['https://www.youtube-nocookie.com/embed/Bkamz7QCS7I?start=5', 'https://www.youtube-nocookie.com/embed/gnG3twj-XNw']
    assert page.locator('.reader-date time').get_attribute('datetime') == '2025-05'
    context.close()
    browser.close()

print(f'PASS: {len(checks)} content-only popup windows at 375/390/768/1440px, full source content/dates, unchanged homepage URLs/scroll, opener isolation, Close/Escape, video URL validation, and failure/retry handling.')
