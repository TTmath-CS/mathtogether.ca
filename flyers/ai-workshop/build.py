import pathlib
d = pathlib.Path('.')
font = (d/'fonts/archivo-latin.b64').read_text().strip()
css  = (d/'styles.css').read_text()
body = (d/'body.html').read_text()

font_face = ("@font-face{font-family:Archivo;font-style:normal;font-weight:100 900;font-display:block;"
             "src:url(data:font/woff2;base64,%s) format('woff2');}" % font)

print_html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>TTMath AI Workshop Flyer</title>
<style>
{font_face}
@page{{size:8.5in 11in;margin:0;}}
{css}
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
"""
(d/'flyer-print.html').write_text(print_html)

dc = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  <style>
{font_face}
{css}
body{{background:var(--paper);}}
  </style>
</helmet>
{body}
</x-dc>
</body>
</html>
"""
(d/'Main.dc.html').write_text(dc)
print('built flyer-print.html', (d/'flyer-print.html').stat().st_size, 'and Main.dc.html', (d/'Main.dc.html').stat().st_size)
