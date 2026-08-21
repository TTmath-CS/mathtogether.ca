# TTMath AI Workshop flyer

Source for the AI Workshop recruitment flyer, marked as an **in-person classroom
course**, in English and Simplified Chinese. US Letter (8.5 × 11 in), one page each.

## Output

| File | What it is |
| --- | --- |
| `TTMath-AI-Workshop-flyer.pdf` / `-zh.pdf` | print-ready, 612 × 792 pt, no margins |
| `TTMath-AI-Workshop-flyer.png` / `-zh.png` | 2448 × 3168 px (288 dpi) for web and messaging |
| `flyer-print.html` / `flyer-print-zh.html` | each flyer as one self-contained page — open it in a browser |

## Where the "classroom course" notation lives

1. A pill under the headline — `In-person classroom course · 8 weeks` / `线下教室课 · 共 8 次课`
2. The **Class time** block — `In person · TTMath classroom` / `线下上课 · TTMath 教室`
3. The bottom band — "It's an **in-person** workshop that…" / "这是一次**线下**工作坊，…"

## Editing

`body.html` holds the English markup and `styles.css` the layout, shared by both
editions. The Chinese edition is generated: `zh_text.py` maps every English string
to its Chinese counterpart and carries the CJK typography overrides (larger
reading sizes, looser leading), and `make-zh.py` applies that map to `body.html`.
So **edit `body.html` for anything structural** and re-run the chain — `make-zh.py`
fails loudly if an English string it translates has drifted.

```sh
python3 make-zh.py        # body.html -> body-zh.html (+ zh-chars.txt)
python3 build.py          # -> flyer-print*.html and the .dc.html artboards
node render.mjs           # -> both PDFs and PNGs; prints each page's bottom margin
```

`render.mjs` needs Playwright (`npm i -g playwright`). It reports the gap between
the last band and the page edge for each edition — keep it above ~12 px, that is
the check that nothing has overflowed the sheet.

The sheet is a fixed 816 × 1056 px box (96 px per inch), so 12 pt type is 16 px.
CJK text wraps at any character, so the Chinese copy carries explicit `<br>`
breaks where automatic wrapping would split a word; re-check them after editing.

`Main.dc.html`, `Chinese.dc.html` and `canvas.json` are the same two flyers as
design-canvas artboards.

## Fonts

Both are embedded in the pages as base64 woff2 so the PDFs and PNGs carry them.

- Latin: [Archivo](https://fonts.google.com/specimen/Archivo) (SIL OFL 1.1), latin subset.
- Chinese: [Noto Sans SC](https://fonts.google.com/noto/specimen/Noto+Sans+SC) (SIL OFL 1.1),
  subset to just the glyphs this flyer uses (64 KB instead of several MB). To
  refresh it after a copy change, feed `zh-chars.txt` to the Google Fonts API:

  ```sh
  curl -G -A "Mozilla/5.0 (X11; Linux x86_64) Chrome/124.0.0.0" \
    "https://fonts.googleapis.com/css2" \
    --data-urlencode "family=Noto Sans SC:wght@400;500;700;900" \
    --data-urlencode "text=$(cat zh-chars.txt)"
  # then download the woff2 it points at, base64 it into fonts/noto-sans-sc-subset.b64
  ```
