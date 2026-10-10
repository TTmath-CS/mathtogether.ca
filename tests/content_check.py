import sys,subprocess,re,json
from bs4 import BeautifulSoup as S
from pathlib import Path
from urllib.parse import urlsplit,unquote
root=Path(__file__).resolve().parents[1];pages={f.name:S(f.read_text(),'html.parser') for f in root.glob('*.html')}
errors=[]
for name,s in pages.items():
 ids=[t['id'] for t in s.select('[id]')]
 if len(ids)!=len(set(ids)):errors.append((name,'duplicate ID'))
 assert len(s.select('h1'))==1,(name,'h1 count')
 assert not re.search(r'>\s*id="',str(s)),name
 assert not s.select('.foot-links'),name
 for a in s.select('[href], [src]'):
  ref=a.get('href',a.get('src'));u=urlsplit(ref)
  if u.scheme or u.netloc:continue
  file=unquote(u.path) or name
  if not (root/file).is_file():errors.append((name,ref,'missing file'))
  elif u.fragment and file in pages and not pages[file].find(id=unquote(u.fragment)):errors.append((name,ref,'missing anchor'))
print('Internal file/anchor errors:',errors);assert not errors
assert len(pages['news.html'].select('.story'))==17
assert len(pages['team.html'].select('.member'))==16
assert len(pages['programs.html'].select('.sessions li'))==9
assert len(pages['index.html'].select('.home-destination'))==3
# Paragraph text and external links from original content must remain somewhere.
current=' '.join(' '.join(s.stripped_strings) for s in pages.values())
normalize=lambda t:re.sub(r'\s+',' ',t).strip()
current=normalize(current)
missing=[];external=set()
for name in pages:
 old=S(subprocess.check_output(['git','show','origin/main:'+name],cwd=root,text=True),'html.parser')
 for p in old.select('main p, .hero .lede'):
  text=normalize(p.get_text(' ',strip=True))
  if name != 'index.html' and text and text not in current:missing.append((name,text))
 for a in old.select('a[href]'):
  if urlsplit(a['href']).netloc:external.add(a['href'])
new_external={a['href'] for s in pages.values() for a in s.select('a[href]') if urlsplit(a['href']).netloc}
print('Missing external URLs:',external-new_external)
print('Missing original content paragraphs:',missing); assert not missing
assert not external-new_external
print('PASS: counts, internal links, anchors, navigation and external URL preservation')
