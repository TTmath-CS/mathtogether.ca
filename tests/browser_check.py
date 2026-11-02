from playwright.sync_api import sync_playwright
from pathlib import Path
import json, os, shutil
out=Path(os.environ.get('SCREENSHOT_DIR', '/tmp/mathtogether-screenshots'));out.mkdir(parents=True, exist_ok=True)
names=os.environ.get('TEST_PAGES', 'index,programs,news,team,get-involved').split(',')
assert names and set(names)<=set(['index','programs','news','team','get-involved'])
results=[]
with sync_playwright() as p:
 executable = os.environ.get('CHROMIUM_PATH') or shutil.which('chromium')
 b=p.chromium.launch(executable_path=executable,headless=True)
 for width in [375,390,768,1440]:
  ctx=b.new_context(viewport={'width':width,'height':900},reduced_motion='reduce')
  page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  for name in names:
   page.goto('http://127.0.0.1:8000/'+name+'.html');page.wait_for_timeout(250)
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),(name,width,'overflow')
   assert [t.strip() for t in page.locator('header nav a').all_text_contents()]==['Home','Programs','News','Team','Get Involved','Join Us']
   if width<1141:
    toggle=page.locator('.nav-toggle');assert toggle.is_visible()
    toggle.click();assert page.locator('#site-links').is_visible();assert toggle.get_attribute('aria-expanded')=='true'
    page.keyboard.press('Escape');assert toggle.get_attribute('aria-expanded')=='false'
    toggle.click();page.locator('#site-links a').first.click();assert page.locator('.nav-toggle').get_attribute('aria-expanded')=='false'
    page.goto('http://127.0.0.1:8000/'+name+'.html')
   if name=='index':
    assert page.locator('.home-proof + #about').count()==1
    photo=page.locator('.who-photo img')
    assert photo.get_attribute('src') == 'assets/img/leadership-event.jpg'
    photo.scroll_into_view_if_needed()
    photo.evaluate('(e)=>e.loading="eager"')
    page.wait_for_function('document.querySelector(".who-photo img").naturalWidth > 0')
    assert photo.evaluate('(e)=>Math.abs(e.getBoundingClientRect().width/e.getBoundingClientRect().height-e.naturalWidth/e.naturalHeight)<0.001'), (width, 'Who We Are photograph cropped or stretched')
    page.evaluate('scrollTo(0,0)')
    assert page.locator('.stat-icon').count()==4
    assert page.locator('.stat-copy').evaluate_all('''(es)=>es.every(e=>{const rect=q=>{const r=document.createRange();r.selectNodeContents(e.querySelector(q));return r.getBoundingClientRect();};const n=rect('strong'),l=rect('span');return Math.abs((n.left+n.right)/2-(l.left+l.right)/2)<=1 && n.bottom<=l.top+1;})'''), (width,'Statistic numbers must be centered directly above their labels')
    assert page.locator('#faq').evaluate('''(e)=>Math.abs(e.getBoundingClientRect().left-document.querySelector('.home-latest .wrap').getBoundingClientRect().left)<=1'''), (width,'FAQ left edge')
    assert page.locator('#faq h2').evaluate('''(e)=>{const r=document.createRange();r.selectNodeContents(e);const ref=document.createRange();ref.selectNodeContents(document.querySelector('.home-latest-head h2'));return Math.abs(r.getBoundingClientRect().left-ref.getBoundingClientRect().left)<=1 && getComputedStyle(e).textAlign==='left';}'''), (width,'FAQ heading left alignment')
    assert page.locator('.stat-copy').first.inner_text().splitlines()==['850+', 'Students Reached']
    assert page.locator('[data-supporter-count]').inner_text().strip()=='6'
    assert page.locator('#featured-event a[href="news.html#news-charity-2026"]').count()==1
    recaps=page.locator('#featured-event .home-past-recaps')
    assert recaps.locator('summary').inner_text().strip()=='Explore Past Charity Contest Recaps →'
    recaps.locator('summary').focus();page.keyboard.press('Enter');assert recaps.get_attribute('open') is not None
    assert recaps.locator('a').count()==2
    page.keyboard.press('Space');assert recaps.get_attribute('open') is None
    assert page.locator('#faq details').count()==5
    summary=page.locator('#faq summary').first
    summary.focus();page.keyboard.press('Enter');assert page.locator('#faq details').first.get_attribute('open') is not None
    page.keyboard.press('Space');assert page.locator('#faq details').first.get_attribute('open') is None
    page.evaluate('scrollTo(0,0)')
    assert page.locator('main > section').evaluate_all('(es)=>es.map(e=>e.id || e.classList[0]).join(",")') == 'home-hero,home-proof,about,featured-event,our-programs,latest-stories,faq'
    assert page.locator('.home-programs .cards > article').count()==3
    page.wait_for_function('document.querySelector("[data-latest-news]").getAttribute("aria-busy")==="false"')
    assert page.locator('.home-story-card').count()==3
    assert page.locator('.home-latest-head .home-kicker').inner_text().strip().upper()=='LATEST NEWS'
    assert page.locator('.home-latest-head .home-kicker').evaluate('(e)=>getComputedStyle(e).textTransform')=='uppercase'
    assert page.locator('.home-latest-head h2').inner_text().strip()=='Our Community in Action.'
    assert not page.locator('.home-join, .two-col-callout').count()
    assert page.locator('.home-proof').evaluate('(e)=>e.getBoundingClientRect().height') < (150 if width <= 960 else 100)
    if width in [375,390]:
     assert page.locator('#about').evaluate('''(s)=>{const r=q=>s.querySelector(q).getBoundingClientRect();return r('.about-head').bottom<=r('.who-photo').top && r('.who-photo').bottom<=r('.about-body').top;}''')
     assert page.locator('#featured-event').evaluate('''(s)=>{const r=q=>s.querySelector(q).getBoundingClientRect();return r('.home-kicker').bottom<=r('h2').top && r('h2').bottom<=r('.home-feature-media').top && r('.home-feature-media').bottom<=r('.event-date').top;}''')
    if width == 1440:
     assert page.locator('.home-story-card').evaluate_all('(es)=>new Set(es.map(e=>Math.round(e.getBoundingClientRect().top))).size')==1
    assert page.locator('.formula-lockup').evaluate('(e)=>e.scrollWidth<=e.clientWidth'),(width,'formula clipping')
    assert page.locator('.home-hero').evaluate('(e)=>getComputedStyle(e).paddingTop')=='0px'
   if name in ['programs','news','team','get-involved']:
    assert page.locator('.page-hero-lede').evaluate('(e)=>Math.abs(e.getBoundingClientRect().width-e.closest(".page-hero-in").getBoundingClientRect().width)<1')
   if name=='programs':
    assert page.locator('.sessions > li').count()==9
    assert page.locator('#session-comc-2025 a').count()==4
    assert page.locator('#session-amc10-2025 a').count()==6
    assert page.locator('#session-amc12-2025 a').count()==3
    assert page.locator('#session-fermat-2025 a').count()==2
    assert page.locator('#session-cayley-2026 a').count()==3
    for session_id in ['session-galois-2026','session-fryer-2026','session-pascal-2026']:
     assert page.locator('#'+session_id+' a').count()==1
    assert page.locator('.sessions a').evaluate_all('(es)=>es.every(a=>a.target==="_blank"&&a.rel.includes("noopener")&&a.rel.includes("noreferrer"))')
    assert page.locator('#session-charity-2026 .session-content').evaluate('''(e)=>{const ranges=Array.from(e.childNodes).filter(n=>n.nodeType===Node.TEXT_NODE&&n.textContent.trim()).flatMap(n=>{const r=document.createRange();r.selectNodeContents(n);return Array.from(r.getClientRects());}).filter(r=>r.width>0&&r.height>0);return ranges.length>0&&e.querySelector('a').getBoundingClientRect().top>=Math.max(...ranges.map(r=>r.bottom));}'''), (width,'Charity recording link must start below its description')
    assert not page.locator('#session-kangaroo-2025, #session-questions-2025, #session-amc10a-2024, #session-waterloo-2025, .sessions .recording-pending').count()
    assert page.locator('.sessions a').evaluate_all('(es)=>es.every(a=>!a.href.includes("@MathTogetherCanada"))')
    assert page.locator('.session-content a').evaluate_all('(es)=>es.every(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.left>=0&&r.right<=innerWidth;} )')

    assert not page.locator('#programs .section-head > .section-lede, #livestream .section-lede').count()
    assert not page.locator('main > section .cta-in-simple').count()
    assert page.locator('#livestream .livestream-channel a').get_attribute('href')=='https://www.youtube.com/@MathTogetherCanada'
   if name=='get-involved':
    assert page.locator('.involved-heart').is_visible()
    grid=page.locator('.supporter-grid')
    assert grid.locator('a').count()==6
    assert grid.locator('img').count()==grid.locator('a').count(), 'Every supporter has an original logo'
    assert page.get_by_text('Supporters are listed alphabetically, with no ranking implied.',exact=True).count()==1
    assert grid.locator('a').evaluate_all('(es)=>es.every(a=>a.target==="_blank"&&a.rel.includes("noopener")&&a.rel.includes("noreferrer"))')
    assert grid.locator('.supporter-logo').evaluate_all('(es)=>{const rs=es.map(e=>e.getBoundingClientRect());return rs.every(r=>Math.abs(r.width-rs[0].width)<1&&Math.abs(r.height-rs[0].height)<1);}')
    grid.scroll_into_view_if_needed()
    grid.locator('img').evaluate_all('(es)=>es.forEach(e=>e.loading="eager")')
    page.wait_for_function('Array.from(document.querySelectorAll(".supporter-grid img")).every(e=>e.complete&&e.naturalWidth>0)')
    assert grid.locator('img').evaluate_all('(es)=>es.every(e=>{const r=e.getBoundingClientRect();return e.complete&&e.naturalWidth>0&&getComputedStyle(e).objectFit==="contain"&&Math.abs((r.width/r.height)/(e.naturalWidth/e.naturalHeight)-1)<0.01;})')
    if width in [375,390,768,1440]:
     columns=grid.locator('a').evaluate_all('(es)=>{const top=es[0].getBoundingClientRect().top;return es.filter(e=>Math.abs(e.getBoundingClientRect().top-top)<1).length;}')
     assert columns==(3 if width>600 else 2),(width,'supporter columns',columns)
    assert not page.locator('.sponsor .rank').count()
    assert not page.locator('#involved .kicker, .hero-scribble, blockquote.pull').count()
    assert page.locator('#involved h2').evaluate('(e)=>parseFloat(getComputedStyle(e).fontSize)')>=34
   if name=='news':
    assert not page.locator('#historical-recaps').count()
    assert page.locator('#news-summer-camp-voices details a').count()==5
    assert page.locator('#news-interview-yingshan a').count()==2
    page.locator('#news-summer-camp-voices summary').click()
    page.locator('.story-dialog').wait_for(state='visible')
    assert page.locator('.story-dialog a').count()==5
    assert page.locator('.story-dialog').evaluate('(e)=>e.scrollWidth<=e.clientWidth')
    assert page.locator('.story-dialog a').evaluate_all('(es)=>es.every(a=>a.textContent.trim().length>10)')
    page.keyboard.press('Escape')
    page.locator('#news-interview-yingshan').scroll_into_view_if_needed()
    assert page.locator('#news-interview-yingshan a').evaluate_all('(es)=>es.every(a=>{const r=a.getBoundingClientRect();return a.textContent.trim().length>10&&r.width>0&&r.left>=0&&r.right<=innerWidth;} )')
    for year in [2024,2025]:
     expected_title=page.locator(f'#news-charity-{year} h3').inner_text()
     page.goto(f'http://127.0.0.1:8000/news.html#news-charity-{year}')
     page.locator('.story-dialog').wait_for(state='visible')
     assert page.locator('.story-dialog h3').inner_text()==expected_title
     assert str(year) in page.locator('.story-dialog .date').inner_text()
     page.keyboard.press('Escape')
    assert page.locator('.story').evaluate_all('(es)=>es.every(e=>e.firstElementChild.classList.contains("news-image"))')
    ratios=page.locator('.news-image').evaluate_all('(es)=>es.map(e=>e.clientWidth/e.clientHeight)')
    assert all(abs(r-16/9)<.02 for r in ratios),ratios
    heights=page.locator('.news-image').evaluate_all('(es)=>es.map(e=>e.clientHeight)');assert max(heights)-min(heights)<=1
    assert page.locator('.story > p a').evaluate_all('(es)=>es.every(a=>{const t=a.previousSibling; if(!t || t.nodeType!==Node.TEXT_NODE)return false; const r=document.createRange();r.selectNodeContents(t);const rects=Array.from(r.getClientRects()).filter(r=>r.width>0&&r.height>0);return getComputedStyle(a).display==="block"&&a.getBoundingClientRect().top>=Math.max(...rects.map(r=>r.bottom))+12;})')
    assert page.locator('.story summary').evaluate_all('(es)=>es.every(e=>parseFloat(getComputedStyle(e).marginTop)>=14)')
    page.locator('.story summary').first.click();assert page.locator('.story-dialog').is_visible();page.keyboard.press('Escape');assert not page.locator('.story-dialog').is_visible()
   if name=='team':
    assert page.locator('.team-grid-five').count()==2
    if width==1440:
     assert page.locator('.team-grid-five').evaluate_all('''(gs)=>gs.every(g=>{const rs=Array.from(g.children).map(e=>e.getBoundingClientRect());return rs.length===5 && rs[0].top===rs[2].top && rs[3].top===rs[4].top && rs[3].top>rs[0].top && rs.every(r=>Math.abs(r.width-rs[0].width)<1);})''')
    assert page.locator('.team-grid').evaluate_all('(grids)=>grids.every(g=>{const cards=Array.from(g.children);const lastTop=cards[cards.length-1].getBoundingClientRect().top;const last=cards.filter(e=>Math.abs(e.getBoundingClientRect().top-lastTop)<1);const a=last[0].getBoundingClientRect(),z=last[last.length-1].getBoundingClientRect(),r=g.getBoundingClientRect();return Math.abs((a.left+z.right)/2-(r.left+r.right)/2)<2;})')
    for person in ['Perry Dai','Kaylyn Zhang','Xuanyi(Prince) Zhang']:
     card=page.locator('.member').filter(has=page.locator('.front h3',has_text=person))
     card.focus();page.keyboard.press('Enter');assert card.get_attribute('aria-pressed')=='true'
     assert card.locator('.back p').count()==2
     assert card.locator('.back').evaluate('(e)=>getComputedStyle(e).overflowY')=='auto'
     page.keyboard.press('End')
     assert card.locator('.back').evaluate('(e)=>e.scrollHeight<=e.clientHeight||e.scrollTop>0')
     page.keyboard.press('Space');assert card.get_attribute('aria-pressed')=='false'
    m=page.locator('.member').first;m.focus();page.keyboard.press('Enter');assert m.get_attribute('aria-pressed')=='true';page.keyboard.press('Space');assert m.get_attribute('aria-pressed')=='false'
   if width in [390,1440]:
    page.locator('img[loading]').evaluate_all('(es)=>es.forEach(e=>e.loading="eager")')
    page.evaluate('document.activeElement.blur()')
    page.wait_for_function('Array.from(document.images).every(i=>i.complete)')
    page.evaluate('scrollTo(0,0)')
    page.wait_for_function('scrollY===0')
    page.screenshot(path=str(out/f'{name}-{width}.png'),full_page=True)
   results.append((name,width,'passed'))
  assert not errors,errors
  ctx.close()
 if 'index' in names:
  # FAQ redirects land at the visible section after asynchronous Latest News renders.
  ctx=b.new_context(viewport={'width':390,'height':900},reduced_motion='reduce');page=ctx.new_page()
  for url in ['faq.html','faq.html#faq','index.html#faq']:
   page.goto('http://127.0.0.1:8000/'+url);page.wait_for_url('**/index.html#faq')
   page.wait_for_function('document.querySelector("[data-latest-news]").getAttribute("aria-busy")==="false"')
   page.wait_for_function('(()=>{const r=document.querySelector("#faq").getBoundingClientRect();return r.top<innerHeight&&r.bottom>0;})()')
  ctx.close()
  # Compatibility including deep bookmarks and JS-free fallback.
  page=b.new_page()
  for old,target in [('about.html','index.html#about'),('livestream.html','programs.html#livestream'),('support.html','get-involved.html#support'),('support.html#partners','get-involved.html#partners'),('index.html#news','news.html#news'),('faq.html','index.html#faq'),('faq.html#faq','index.html#faq'),('index.html#faq','index.html#faq')]:
   page.goto('http://127.0.0.1:8000/'+old);page.wait_for_url('**/'+target);assert page.locator('#'+target.split('#')[1]).count()==1
  ctx=b.new_context(java_script_enabled=False);page=ctx.new_page();page.goto('http://127.0.0.1:8000/about.html');assert page.locator('main a').get_attribute('href')=='index.html#about';page.goto('http://127.0.0.1:8000/faq.html');page.wait_for_url('**/index.html#faq');assert page.locator('#faq details').count()==5;ctx.close()
 b.close()
print(json.dumps(results));print(f'PASS: {len(results)} page/viewport combinations for {names}; {len(names)*2} screenshots. Full-page checks also exercise FAQ and legacy URLs when index is selected.')
