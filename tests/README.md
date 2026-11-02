# Website regression checks

The website requires no build or runtime packages. These optional checks use Python development dependencies in `requirements.txt`.

Install them in a virtual environment with `python3 -m pip install -r tests/requirements.txt`. Install Playwright Chromium with `python3 -m playwright install chromium`, or set `CHROMIUM_PATH` to an existing Chromium executable.

From the repository root:

```sh
python3 tests/content_check.py
python3 tests/seo_check.py
python3 scripts/render_supporters.py --check
node --check app.js
node --check support.js
```

`content_check.py` compares content against the fixed pre-round-3 snapshot `c0f98861a1978cc51f1f9540e3e53728d5742e93` (merged PR #20). This keeps preservation checks valid after round 3 is merged into `main`; ensure that commit exists in a shallow checkout before running it. It checks local files and anchors, primary navigation, exact FAQ questions/answers, exact replacement biographies, the other 13 unchanged profiles, preserved photos/positions, all 17 News records and precise date metadata, four retained session descriptions and four new 2026 contest sessions (five older sessions removed with user authorization), alphabetized supporters and homepage statistics. Approved biography, supporter, date presentation and video link changes are checked separately from preservation.

`seo_check.py` checks unique titles/descriptions, canonical URLs, Open Graph and Twitter metadata, existing social image files/dimensions, JSON-LD syntax, legacy `noindex` metadata, sitemap URLs and robots.txt. It does not claim a production preview crawl occurred.

Start the site in a separate terminal:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Then run:

```sh
python3 tests/browser_check.py
python3 tests/latest_news_check.py
python3 tests/link_popup_check.py
```

Browser checks cover five primary pages at 375, 390, 768 and 1440 pixels, including horizontal overflow, navigation controls, homepage layout, centered statistic values, left-aligned FAQ, keyboard FAQ accordion behavior, historical recap links and dialogs, equal supporter containers and responsive column counts, team flip-card keyboard behavior and scrollable biographies, photographs, News links, legacy redirects and FAQ without JavaScript. Use `TEST_PAGES=programs python3 tests/browser_check.py` for a targeted Programs rerun. Ten desktop/mobile screenshots are saved outside the checkout to `/tmp/mathtogether-screenshots`; override with `SCREENSHOT_DIR`.

Latest News is generated from `news.html`; see [maintenance and unresolved dates](../docs/news-maintenance.md). The news-specific check covers exact-date sorting independently of source order, year-only source-order fallback, known display months without fabricated sorting precision, date validation, a three-item limit, newer additions without homepage changes, deep links and fetch failure. Visible homepage dates use abbreviated English month-year while retaining machine-readable precision.

All nine raw HTML pages and rendered/generated links are checked for secure new-tab navigation, with the skip link retaining its same-page behavior. `link_popup_check.py` clicks representative homepage CTAs, program cards, news cards, navigation, supporter and reading links at 375/1440px; it checks the new destination and unchanged source page. External destinations are mocked for this behavior test. FAQ, menus, team controls and JavaScript-free News details remain inline controls.

External destination availability, physical phones, Safari, and platform-specific social preview caches need separate verification. Automated accessibility checks supplement human review.
