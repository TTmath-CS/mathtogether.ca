# TTMath AI Workshop flyer

Source for the AI Workshop recruitment flyer, marked as an **in-person classroom
course**. US Letter (8.5 × 11 in), one page.

## Output

| File | What it is |
| --- | --- |
| `TTMath-AI-Workshop-flyer.pdf` | print-ready, 612 × 792 pt, no margins |
| `TTMath-AI-Workshop-flyer.png` | 2448 × 3168 px (288 dpi) for web and messaging |
| `flyer-print.html` | the flyer as one self-contained page — open it in a browser |

## Where the "classroom course" notation lives

1. A pill under the headline: `In-person classroom course · 8 weeks`
2. The **Class time** block: `In person · TTMath classroom`
3. The bottom band: "It's an **in-person** workshop that gives you the experience…"

## Editing

`body.html` holds the markup, `styles.css` the layout. The sheet is a fixed
816 × 1056 px box (96 px per inch), so keep the content inside it — the build
prints the bottom margin and warns if the content runs past the page.

```sh
python3 build.py          # regenerates flyer-print.html and Main.dc.html
npm i -g playwright       # if not already installed
node render.mjs           # re-renders the PDF and PNG, prints the fit metrics
```

`Main.dc.html` and `canvas.json` are the same flyer as a design canvas artboard.

Type is [Archivo](https://fonts.google.com/specimen/Archivo) (SIL Open Font
License 1.1), embedded in the page as a base64 woff2 so the PDF and PNG carry it.
