# -*- coding: utf-8 -*-
"""Generates body-zh.html from body.html so both editions stay in sync."""
import pathlib, re
from zh_text import REPLACEMENTS

d = pathlib.Path(__file__).parent
s = (d / 'body.html').read_text()
missing = [a for a, _ in REPLACEMENTS if a not in s]
if missing:
    raise SystemExit('these English strings are no longer in body.html:\n  ' + '\n  '.join(missing))
for a, b in REPLACEMENTS:
    s = s.replace(a, b)
(d / 'body-zh.html').write_text(s)

chars = sorted(set(re.sub(r'[\x00-\x7f]', '', re.sub(r'<[^>]+>', '', s))))
(d / 'zh-chars.txt').write_text(''.join(chars))
print(f'body-zh.html written ({len(chars)} non-ascii glyphs -> zh-chars.txt)')
