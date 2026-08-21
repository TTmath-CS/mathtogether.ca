# -*- coding: utf-8 -*-
"""Builds the flyer's self-contained print page and design-canvas artboard,
in English and Chinese, from body*.html + styles.css."""
import pathlib
from zh_text import ZH_CSS

d = pathlib.Path(__file__).parent
css = (d / 'styles.css').read_text()

def face(name, b64_path, weights='100 900'):
    b64 = (d / b64_path).read_text().strip()
    return (f"@font-face{{font-family:{name};font-style:normal;font-weight:{weights};"
            f"font-display:block;src:url(data:font/woff2;base64,{b64}) format('woff2');}}")

ARCHIVO = face('Archivo', 'fonts/archivo-latin.b64')
NOTO_SC = face("'Noto Sans SC'", 'fonts/noto-sans-sc-subset.b64')

EDITIONS = [
    dict(body='body.html', fonts=ARCHIVO, extra='', lang='en',
         page='flyer-print.html', artboard='Main.dc.html'),
    dict(body='body-zh.html', fonts=ARCHIVO + '\n' + NOTO_SC, extra=ZH_CSS, lang='zh-Hans',
         page='flyer-print-zh.html', artboard='Chinese.dc.html'),
]

for e in EDITIONS:
    body = (d / e['body']).read_text()
    sheet = e['fonts'] + '\n' + css + e['extra']

    (d / e['page']).write_text(f"""<!doctype html>
<html lang="{e['lang']}"><head><meta charset="utf-8">
<title>TTMath AI Workshop Flyer</title>
<style>
{sheet}
@page{{size:8.5in 11in;margin:0;}}
body{{display:flex;justify-content:center;align-items:flex-start;padding:22px 0;}}
.sheet{{box-shadow:0 10px 40px rgba(0,0,0,.35);}}
@media print{{
  body{{background:#fff;padding:0;display:block;}}
  .sheet{{box-shadow:none;}}
  *{{-webkit-print-color-adjust:exact;print-color-adjust:exact;}}
}}
</style></head>
<body>
{body}
</body></html>
""")

    (d / e['artboard']).write_text(f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  <style>
{sheet}
body{{background:var(--paper);}}
  </style>
</helmet>
{body}
</x-dc>
</body>
</html>
""")
    print('built', e['page'], (d / e['page']).stat().st_size, '/', e['artboard'])
