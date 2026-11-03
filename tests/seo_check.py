"""Validate metadata, canonical routes and local social image assets before review."""
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from xml.etree import ElementTree as ET
import json
from PIL import Image
root=Path(__file__).resolve().parents[1]
main=['index.html','programs.html','news.html','team.html','get-involved.html']
titles=set();descriptions=set()
for p in root.glob('*.html'):
 s=BeautifulSoup(p.read_text(),'html.parser'); head=s.head
 title=head.title.get_text(strip=True);description=head.select_one('meta[name=description]')['content']
 assert title not in titles,p; titles.add(title)
 assert description not in descriptions,p; descriptions.add(description)
 canon=head.select('link[rel=canonical]');assert len(canon)==1,p
 assert canon[0]['href'].startswith('https://mathtogether.ca/'),p
 for prop in ['og:title','og:description','og:image','og:url','og:type']:
  assert len(head.select(f'meta[property="{prop}"]'))==1,(p,prop)
 assert head.select_one('meta[property="og:title"]')['content']==title,p
 assert head.select_one('meta[property="og:description"]')['content']==description,p
 assert head.select_one('meta[property="og:url"]')['content']==canon[0]['href'],p
 assert head.select_one('meta[name="twitter:card"]')['content']=='summary_large_image',p
 for selector in ['meta[property="og:image"]','meta[property="og:image:secure_url"]','meta[name="twitter:image"]']:
  u=head.select_one(selector)['content'];assert u.startswith('https://mathtogether.ca/'),(p,u)
  local=root/urlparse(u).path.lstrip('/'); assert local.is_file(),local
  with Image.open(local) as im: assert im.width>=1200,(local,im.size)
 for script in head.select('script[type="application/ld+json"]'): json.loads(script.string)
 if p.name not in main: assert head.select_one('meta[name=robots]')['content']=='noindex, follow',p
 assert head.select_one('link[rel=icon]')['href']=='assets/img/logo-badge.png',p
urls=[n.text for n in ET.parse(root/'sitemap.xml').findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
assert len(urls)==5 and len(set(urls))==5
for u in urls:
 assert u.startswith('https://mathtogether.ca/') and not urlparse(u).fragment,u
 local=root/(urlparse(u).path.lstrip('/') or 'index.html');assert local.is_file(),u
 s=BeautifulSoup(local.read_text(),'html.parser');assert s.select_one('link[rel=canonical]')['href']==u,u
 assert not s.select_one('meta[name=robots]'),u
assert 'Sitemap: https://mathtogether.ca/sitemap.xml' in (root/'robots.txt').read_text()
print(f'PASS: {len(titles)} unique titles/descriptions, canonical/OG/Twitter metadata, favicon, JSON-LD, image files/dimensions, five sitemap URLs, robots.')
