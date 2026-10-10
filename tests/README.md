# Redesign regression checks

The website still requires no build or runtime packages. These optional development checks use Python dependencies listed in `requirements.txt`.

Install them in a virtual environment: `python3 -m pip install -r tests/requirements.txt`. Install Playwright Chromium with `python3 -m playwright install chromium`, or use an existing Chromium via `CHROMIUM_PATH`.

From the repository root:

```sh
python3 tests/content_check.py
node --check app.js
node --check support.js
```

`content_check.py` compares the original content and external links against `origin/main`; fetch that reference before running it. It verifies all local file/fragment links, IDs, preserved content and news/team/session counts. Approved replacement of homepage navigation cards is excluded from paragraph preservation.

Start the site in a separate terminal:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Then run:

```sh
python3 tests/browser_check.py
```

This checks all six primary pages at 375, 390, 768 and 1440 pixels, menu actions, formula fit, image containers and placement, keyboard team interactions, news dialogs, FAQ and legacy URLs. Ten screenshots are saved outside the checkout to `/tmp/mathtogether-screenshots`; override with `SCREENSHOT_DIR`.

During redesign, HTML was also checked with html-validate's recommended rules (format-only exceptions and inline styles allowed), CSS parsed with css-tree, and WCAG A/AA checked with axe-core on all six primary pages at 390 and 1440 pixels. These tools are optional and do not change the website's static publishing workflow. Automated accessibility checks supplement, rather than replace, human review.
