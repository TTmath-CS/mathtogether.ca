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
    assert page.locator('.formula-lockup').evaluate('(e)=>e.scrollWidth<=e.clientWidth'),(width,'formula clipping')
    assert page.locator('.home-hero').evaluate('(e)=>getComputedStyle(e).paddingTop')=='0px'
   if name=='news':
    assert page.locator('.story').evaluate_all('(es)=>es.every(e=>e.firstElementChild.classList.contains("news-image"))')
    ratios=page.locator('.news-image').evaluate_all('(es)=>es.map(e=>e.clientWidth/e.clientHeight)')
    assert all(abs(r-16/9)<.02 for r in ratios),ratios
    heights=page.locator('.news-image').evaluate_all('(es)=>es.map(e=>e.clientHeight)');assert max(heights)-min(heights)<=1
    page.locator('.story summary').first.click();assert page.locator('.story-dialog').is_visible();page.keyboard.press('Escape');assert not page.locator('.story-dialog').is_visible()
   if name=='team':
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
