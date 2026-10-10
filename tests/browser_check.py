from playwright.sync_api import sync_playwright
from pathlib import Path
import json, os, shutil
out=Path(os.environ.get('SCREENSHOT_DIR', '/tmp/mathtogether-screenshots'));out.mkdir(parents=True, exist_ok=True)
results=[]
with sync_playwright() as p:
 executable = os.environ.get('CHROMIUM_PATH') or shutil.which('chromium')
 b=p.chromium.launch(executable_path=executable,headless=True)
 for width in [375,390,768,1440]:
  ctx=b.new_context(viewport={'width':width,'height':900},reduced_motion='reduce')
  page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  for name in ['index','programs','news','team','get-involved','faq']:
   page.goto('http://127.0.0.1:8000/'+name+'.html');page.wait_for_timeout(250)
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),(name,width,'overflow')
   assert [t.strip() for t in page.locator('header nav a').all_text_contents()]==['Home','Programs','News','Team','Get Involved','FAQ','Join Us']
   if width<1141:
    toggle=page.locator('.nav-toggle');assert toggle.is_visible()
    toggle.click();assert page.locator('#site-links').is_visible();assert toggle.get_attribute('aria-expanded')=='true'
    page.keyboard.press('Escape');assert toggle.get_attribute('aria-expanded')=='false'
    toggle.click();page.locator('#site-links a').first.click();assert page.locator('.nav-toggle').get_attribute('aria-expanded')=='false'
    page.goto('http://127.0.0.1:8000/'+name+'.html')
   if name=='index':
    assert page.locator('.home-proof + #about').count()==1
    photo=page.locator('.who-photo img')
    photo.scroll_into_view_if_needed()
    photo.evaluate('(e)=>e.loading="eager"')
    page.wait_for_function('document.querySelector(".who-photo img").naturalWidth > 0')
    assert photo.evaluate('(e)=>Math.abs(e.getBoundingClientRect().width/e.getBoundingClientRect().height-e.naturalWidth/e.naturalHeight)<0.001'), (width, 'Who We Are photograph cropped or stretched')
    page.evaluate('scrollTo(0,0)')
    assert page.locator('.stat-icon').count()==4
    assert page.locator('main > section').evaluate_all('(es)=>es.map(e=>e.id || e.classList[0]).join(",")') == 'home-hero,home-proof,about,featured-event,our-programs,latest-stories'
    assert page.locator('.home-programs .cards > article').count()==3
    assert page.locator('.home-story-card').count()==4
    assert not page.locator('.home-join, .two-col-callout').count()
    assert page.locator('.home-proof').evaluate('(e)=>e.getBoundingClientRect().height') < (150 if width <= 960 else 100)
    if width == 1440:
     assert page.locator('.home-story-card').evaluate_all('(es)=>new Set(es.map(e=>Math.round(e.getBoundingClientRect().top))).size')==1
    assert page.locator('.formula-lockup').evaluate('(e)=>e.scrollWidth<=e.clientWidth'),(width,'formula clipping')
    assert page.locator('.home-hero').evaluate('(e)=>getComputedStyle(e).paddingTop')=='0px'
   if name in ['programs','news','team','get-involved','faq']:
    assert page.locator('.page-hero-lede').evaluate('(e)=>Math.abs(e.getBoundingClientRect().width-e.closest(".page-hero-in").getBoundingClientRect().width)<1')
   if name=='programs':
    assert not page.locator('main > section .cta-in-simple').count()
    assert page.locator('#livestream .livestream-channel a').get_attribute('href')=='https://www.youtube.com/@MathTogetherCanada'
   if name=='get-involved':
    assert not page.locator('#involved .kicker, .hero-scribble, blockquote.pull').count()
    assert page.locator('#involved h2').evaluate('(e)=>parseFloat(getComputedStyle(e).fontSize)')>=34
   if name=='news':
    assert page.locator('.story').evaluate_all('(es)=>es.every(e=>e.firstElementChild.classList.contains("news-image"))')
    ratios=page.locator('.news-image').evaluate_all('(es)=>es.map(e=>e.clientWidth/e.clientHeight)')
    assert all(abs(r-16/9)<.02 for r in ratios),ratios
    heights=page.locator('.news-image').evaluate_all('(es)=>es.map(e=>e.clientHeight)');assert max(heights)-min(heights)<=1
    assert page.locator('.story > p a').evaluate_all('(es)=>es.every(a=>{const t=a.previousSibling; if(!t || t.nodeType!==Node.TEXT_NODE)return false; const r=document.createRange();r.selectNodeContents(t);const rects=Array.from(r.getClientRects()).filter(r=>r.width>0&&r.height>0);return getComputedStyle(a).display==="block"&&a.getBoundingClientRect().top>=Math.max(...rects.map(r=>r.bottom))+12;})')
    assert page.locator('.story summary').evaluate_all('(es)=>es.every(e=>parseFloat(getComputedStyle(e).marginTop)>=14)')
    page.locator('.story summary').first.click();assert page.locator('.story-dialog').is_visible();page.keyboard.press('Escape');assert not page.locator('.story-dialog').is_visible()
   if name=='team':
    assert page.locator('.team-grid').evaluate_all('(grids)=>grids.every(g=>{const cards=Array.from(g.children);const lastTop=cards[cards.length-1].getBoundingClientRect().top;const last=cards.filter(e=>Math.abs(e.getBoundingClientRect().top-lastTop)<1);const a=last[0].getBoundingClientRect(),z=last[last.length-1].getBoundingClientRect(),r=g.getBoundingClientRect();return Math.abs((a.left+z.right)/2-(r.left+r.right)/2)<2;})')
    m=page.locator('.member').first;m.focus();page.keyboard.press('Enter');assert m.get_attribute('aria-pressed')=='true';page.keyboard.press('Space');assert m.get_attribute('aria-pressed')=='false'
   if name=='faq':page.locator('.faq summary').first.click();assert page.locator('.faq').first.get_attribute('open') is not None
   if width in [390,1440] and name!='faq':
    page.locator('img[loading]').evaluate_all('(es)=>es.forEach(e=>e.loading="eager")')
    page.evaluate('document.activeElement.blur()')
    page.wait_for_function('Array.from(document.images).every(i=>i.complete)')
    page.screenshot(path=str(out/f'{name}-{width}.png'),full_page=True)
   results.append((name,width,'passed'))
  assert not errors,errors
  ctx.close()
 # Compatibility including deep bookmarks and JS-free fallback.
 page=b.new_page()
 for old,target in [('about.html','index.html#about'),('livestream.html','programs.html#livestream'),('support.html','get-involved.html#support'),('support.html#partners','get-involved.html#partners'),('index.html#news','news.html#news'),('index.html#faq','faq.html#faq')]:
  page.goto('http://127.0.0.1:8000/'+old);page.wait_for_url('**/'+target);assert page.locator('#'+target.split('#')[1]).count()==1
 ctx=b.new_context(java_script_enabled=False);page=ctx.new_page();page.goto('http://127.0.0.1:8000/about.html');assert page.locator('main a').get_attribute('href')=='index.html#about';ctx.close()
 b.close()
print(json.dumps(results));print('PASS: 24 page/viewport combinations, menu, formula, image ratios, news dialog, team keyboard, FAQ and legacy URLs; 10 screenshots')
