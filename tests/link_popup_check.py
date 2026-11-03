"""Exercise real new-tab navigation while preserving the source page."""
import os
import shutil
from urllib.parse import urlsplit, parse_qs

from playwright.sync_api import sync_playwright


BASE = 'http://127.0.0.1:8000/'
checks = []


def route_request(route):
    """Keep site requests real and replace external destinations with a stub."""
    if urlsplit(route.request.url).netloc == urlsplit(BASE).netloc:
        route.continue_()
    elif route.request.resource_type == 'document':
        route.fulfill(status=200, content_type='text/html', body='<title>External destination</title><p>External destination</p>')
    else:
        route.fulfill(status=200, body='')


def assert_new_tab_links(page):
    assert page.locator('a[href]:not(.skip-link)').evaluate_all('''anchors => anchors.every(a =>
        a.target === '_blank' && a.relList.contains('noopener') && a.relList.contains('noreferrer'))''')


def open_link(source, link, label, width):
    """Return the new page, leaving its caller responsible for closing it."""
    before = source.url
    expected = link.evaluate('(a) => a.href')
    with source.context.expect_page() as created:
        link.click()
    opened = created.value
    opened.wait_for_url(expected)
    opened.wait_for_load_state('domcontentloaded')
    assert source.url == before, (width, label, 'source page navigated')
    assert opened.evaluate('window.opener === null'), (width, label, 'opener exposed')
    if urlsplit(expected).netloc == urlsplit(BASE).netloc:
        if urlsplit(expected).path.endswith('/read.html'):
            opened.wait_for_function('document.querySelector("#reader-story").getAttribute("aria-busy") === "false"')
            assert opened.locator('#reader-content > *').count(), (width, label, 'reader failed')
            assert not opened.locator('header, nav, footer, .news-grid').count(), (width, label, 'News UI present')
            assert parse_qs(urlsplit(expected).query).get('story'), (width, label, 'missing story')
        story_id = urlsplit(expected).fragment
        story = opened.locator(f'.story[id="{story_id}"]') if story_id else None
        if story is not None and story.count() and story.locator('details').count():
            opened.locator('.story-dialog').wait_for(state='visible')
            assert opened.locator('.story-dialog h3').inner_text().strip() == story.locator('h3').inner_text().strip()
    checks.append((width, label))
    return opened


def click_and_close(page, selector, label, width):
    opened = open_link(page, page.locator(selector), label, width)
    opened.close()


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium'), headless=True)
    for width in [375, 1440]:
        context = browser.new_context(viewport={'width': width, 'height': 900}, reduced_motion='reduce')
        context.route('**/*', route_request)
        page = context.new_page()
        page.goto(BASE + 'index.html')
        page.wait_for_function('document.querySelector("[data-latest-news]").getAttribute("aria-busy") === "false"')
        assert_new_tab_links(page)

        # The accessibility skip link intentionally stays within the current tab.
        count = len(context.pages)
        page.locator('.skip-link').focus()
        page.keyboard.press('Enter')
        assert page.url == BASE + 'index.html#main-content'
        assert len(context.pages) == count
        page.goto(BASE + 'index.html')
        page.wait_for_selector('.home-story-card')

        click_and_close(page, '#featured-event a[href="read.html?story=news-charity-2026"]', '2026 event recap', width)
        before = page.url
        page.locator('.home-past-recaps summary').click()
        assert page.locator('.home-past-recaps').get_attribute('open') is not None
        assert page.url == before and len(context.pages) == 1
        for year in [2025, 2024]:
            click_and_close(page, f'.home-past-recaps a[href="read.html?story=news-charity-{year}"]', f'{year} historical recap', width)
        for index in range(3):
            popup = open_link(page, page.locator('.home-programs article a').nth(index), f'homepage program {index + 1}', width)
            popup.close()
        for index in range(3):
            popup = open_link(page, page.locator('.home-story-card').nth(index), f'Latest News {index + 1}', width)
            popup.close()

        for selector, label in [('header nav a[href="programs.html"]', 'internal navigation'), ('header nav a.join', 'external Join Us')]:
            if width < 1141:
                page.locator('.nav-toggle').click()
            click_and_close(page, selector, label, width)
        click_and_close(page, '.home-btn-secondary', 'homepage YouTube', width)

        page.goto(BASE + 'programs.html')
        assert_new_tab_links(page)
        click_and_close(page, '.sessions > li:first-child a', 'Watch recording', width)

        page.goto(BASE + 'get-involved.html')
        assert_new_tab_links(page)
        click_and_close(page, '.supporter-grid a:first-child', 'supporter website', width)

        page.goto(BASE + 'news.html')
        assert_new_tab_links(page)
        camp = page.locator('#news-summer-camp-voices .story-read-link')
        opened = open_link(page, camp, 'Read the story', width)
        assert_new_tab_links(opened)
        video = open_link(opened, opened.locator('.story-dialog a').first, 'video from reading dialog', width)
        video.close()
        opened.close()
        assert len(context.pages) == 1
        context.close()
    browser.close()

print(f'PASS: {len(checks)} real popup navigations at 375/1440px, correct destinations, retained source URLs, safe opener isolation, and same-tab skip links.')
