"""Render supporter cards and organization counts from data/supporters.json.

Run after changing supporter data; --check detects stale committed output.
Uses only the Python standard library. No browser JavaScript is required.
"""
from pathlib import Path
from html import escape
import argparse
import json
import re

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check', action='store_true')
args = parser.parse_args()
supporters = json.loads((ROOT / 'data/supporters.json').read_text())
assert len({s['id'] for s in supporters}) == len(supporters), 'Duplicate organization ID'
assert len({s['url'] for s in supporters}) == len(supporters), 'Duplicate organization URL'
supporters.sort(key=lambda s: s['sort_name'].casefold())
cards = ['     <div class="supporter-grid" role="group" aria-label="Supporter websites">']
for supporter in supporters:
    name = escape(supporter['name'])
    url = escape(supporter['url'], quote=True)
    cards.append(f'      <a class="supporter-card" data-supporter-id="{supporter["id"]}" href="{url}" target="_blank" rel="noopener noreferrer" aria-label="Visit {name} (opens in a new tab)">')
    cards.append('       <span class="supporter-logo">')
    if supporter.get('logo'):
        logo = escape(supporter['logo'], quote=True)
        assert (ROOT / supporter['logo']).is_file(), f'Missing logo: {logo}'
        cards.append(f'        <img src="{logo}" alt="{name} logo" loading="lazy"/>')
    else:
        cards.append(f'        <span class="supporter-wordmark">{name}</span>')
    cards.append('       </span>')
    cards.append('      </a>')
cards.append('     </div>')
cards.append('     <details class="supporter-stories">')
cards.append('      <summary>How our supporters help</summary>')
for supporter in supporters:
    if supporter.get('description'):
        cards.append(f'      <p><strong>{escape(supporter["name"])}</strong> — {escape(supporter["description"])}</p>')
cards.append('     </details>')
generated = '\n'.join(cards)
stale = []
for filename in ['get-involved.html', 'index.html']:
    path = ROOT / filename
    old = path.read_text()
    updated = old
    if filename == 'get-involved.html':
        updated, matches = re.subn(r'(?<=<!-- BEGIN GENERATED SUPPORTERS -->)\n.*?(?=     <!-- END GENERATED SUPPORTERS -->)', '\n' + generated + '\n', updated, flags=re.S)
        assert matches == 1, 'Missing or duplicate supporter output markers'
    updated = re.sub(r'<(strong|b)([^>]*\bdata-supporter-count(?:\s*=\s*[\'\"][^\'\"]*[\'\"])?[^>]*)>.*?</\1>', lambda match: f'<{match[1]}{match[2]}>{len(supporters)}</{match[1]}>', updated, flags=re.S)
    if updated != old:
        stale.append(filename)
        if not args.check:
            path.write_text(updated)
if args.check and stale:
    raise SystemExit('Run python3 scripts/render_supporters.py: stale ' + ', '.join(stale))
print(f'{len(supporters)} distinct supporters; alphabetical grid and counts {"checked" if args.check else "rendered"}.')
