"""Exercise source-order independence, live updates and exact story deep links."""
from pathlib import Path
import shutil
from playwright.sync_api import sync_playwright

source = (Path(__file__).resolve().parents[1] / 'news.html').read_text()
base = 'http://127.0.0.1:8000/'
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=shutil.which('chromium'), headless=True)
    page = browser.new_page()
    page.goto(base + 'news.html')
    expected = page.locator('.story[data-date]').evaluate_all('(es)=>es.map(e=>({id:e.id,date:e.dataset.date,title:e.querySelector("h3").textContent.trim(),image:e.querySelector("img").getAttribute("src")})).sort((a,b)=>b.date.localeCompare(a.date)||a.id.localeCompare(b.id))')
    assert page.locator('.story[data-date]').evaluate_all('(es)=>es.map(e=>e.dataset.date)') == [s['date'] for s in expected]
    expected = page.locator('.story[data-date], .story[data-year]').evaluate_all('(es)=>es.map(e=>({id:e.id,date:e.dataset.date||null,year:e.dataset.year,title:e.querySelector("h3").textContent.trim(),image:e.querySelector("img").getAttribute("src")}))')
    page.goto(base)
    page.wait_for_function('document.querySelector("[data-latest-news]").getAttribute("aria-busy")==="false"')
    cards = page.locator('.home-story-card')
    assert cards.count() == 3
    assert cards.locator('h3').all_text_contents() == [s['title'] for s in expected[:3]]
    assert cards.locator('img').evaluate_all('(es)=>es.map(e=>e.getAttribute("src"))') == [s['image'] for s in expected[:3]]
    assert cards.locator('[data-year]').all_text_contents() == [s['year'] for s in expected[:3] if not s['date']]
    assert cards.locator('time').evaluate_all('(es)=>es.map(e=>e.dateTime)') == [s['date'] for s in expected[:3] if s['date']]
    assert cards.evaluate_all('(es)=>es.map(e=>e.getAttribute("href"))') == ['news.html#' + s['id'] for s in expected[:3]]
    for item in expected[:3]:
        page.goto(base + 'news.html#' + item['id'])
        if page.locator('#' + item['id'] + ' details').count():
            assert page.locator('.story-dialog').is_visible()
            assert page.locator('.story-dialog h3').inner_text().strip() == item['title']
        else:
            assert page.locator('#' + item['id']).evaluate('(e)=>{const r=e.getBoundingClientRect();return r.top<innerHeight && r.bottom>0;}')
            assert page.locator('#' + item['id'] + ' a').count() > 0
    page.goto(base + 'news.html#news-charity-2025')
    page.evaluate('location.hash="news-picnic-2026"')
    page.wait_for_function('document.querySelector(".story-dialog h3").textContent.includes("Picnic")')
    # Future dated item added only to the News response, not index.html; no explicit ID required.
    added = '''<article class="story" data-date="2027-01-02"><div class="news-image"><img src="assets/img/news-picnic.jpg" alt="Community event"></div><h3>New regression news</h3><p class="date">January 2, 2027</p><details><summary>Read the story</summary><p>A newly published article.</p></details></article>'''
    changed = source.replace('<div class="news-grid">', '<div class="news-grid">' + added)
    page.route('**/news.html', lambda route: route.fulfill(status=200, content_type='text/html', body=changed))
    page.goto(base)
    page.wait_for_selector('.home-story-card')
    assert page.locator('.home-story-card').count() == 3
    assert page.locator('.home-story-card h3').first.inner_text() == 'New regression news'
    new_link = page.locator('.home-story-card').first.get_attribute('href')
    page.goto(base + new_link)
    assert page.locator('.story-dialog h3').inner_text() == 'New regression news'
    page.unroute('**/news.html')
    # Reverse dated slots only; year-only slots retain their source order.
    page.goto(base + 'news.html')
    reversed_source = page.evaluate('''()=>{const g=document.querySelector('.news-grid');for(const year of ['2024','2025','2026']){const dated=Array.from(g.querySelectorAll(':scope > .story[data-date]')).filter(e=>e.dataset.date.startsWith(year));const markers=dated.map(e=>{const m=document.createElement('span');e.replaceWith(m);return m;});dated.reverse().forEach((e,i)=>markers[i].replaceWith(e));}return document.documentElement.outerHTML;}''')
    page.route('**/news.html', lambda route: route.fulfill(status=200, content_type='text/html', body=reversed_source))
    page.goto(base)
    page.wait_for_selector('.home-story-card')
    assert page.locator('.home-story-card').evaluate_all('(es)=>es.map(e=>e.getAttribute("href"))') == ['news.html#' + s['id'] for s in expected[:3]]
    page.unroute('**/news.html')
    page.goto(base + 'news.html')
    assert page.evaluate('''()=>{const root=document.createElement('div');root.innerHTML='<div class="news-grid"><article class="story" id="a" data-year="2025"><h3>A</h3></article><article class="story" id="b" data-year="2026"><h3>B</h3></article><article class="story" id="c" data-year="2026"><h3>C</h3></article><article class="story" id="d"><h3>D</h3></article></div>';return newsStories(root).map(e=>e.id).join(',')==='b,c,a,d';}''')
    # Reject invalid and incomplete dates, rather than rolling dates into the next month.
    page.goto(base + 'news.html')
    assert page.evaluate('''()=>['2026-02-30','2026-13-01','2026-09','',null].every(date=>{const s=document.createElement('article');if(date!==null)s.dataset.date=date;return newsDate(s)===null;})''')
    # Network failure remains understandable and retains a News-page link.
    page.route('**/news.html', lambda route: route.fulfill(status=503, body='Unavailable'))
    page.goto(base)
    page.wait_for_function('document.querySelector("[data-latest-news]").getAttribute("aria-busy")==="false"')
    assert page.locator('.latest-news-status').is_visible()
    assert page.locator('.home-latest-head a').get_attribute('href') == 'news.html#news'
    browser.close()
print('PASS: date sorting, three-item limit, original images/titles/dates, destinations, article/video deep links, source reordering, newer item without homepage edits, missing/invalid dates and fetch failure.')
