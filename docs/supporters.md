# Supporter maintenance and assets

`data/supporters.json` is the shared source for the six confirmed organizations.
The grid is generated as static HTML, so it remains available without JavaScript.
Run `python3 scripts/render_supporters.py` after editing the data. This updates
the grid in `get-involved.html` and every `data-supporter-count` value on that page
and the homepage. Run with `--check` to detect stale output without writing files.
Only add confirmed, distinct organizations; use one entry per organization.

The `sort_name` value uses the official English name, case-insensitively, or
pinyin when the organization has no confirmed English name. Display names retain
the Chinese names supplied by the site owner.

## Logo sources

- Citadel and TTmath use the existing repository artwork, unaltered.
- Jane Street, BLACK BELT WORLD, 志鸿牙医 / Dr Hong Dental, and 小月牙医 use the
  original PNGs supplied by the site owner in `logos.zip`. The four files were
  copied byte-for-byte without cropping, redrawing, or reencoding.

| ZIP entry | Repository asset | Original dimensions |
|---|---|---|
| `Jane Street.png` | `assets/img/sponsors/jane-street.png` | 2968 × 1238 |
| `小月牙医.png` | `assets/img/sponsors/woodbine-steeles-dental.png` | 3840 × 2160 |
| `志鸿牙医.png` | `assets/img/sponsors/dr-hong-dental.png` | 198 × 86 |
| `black world belt.png` | `assets/img/sponsors/black-belt-world.png` | 263 × 45 |

Every logo uses the same 112px-tall container and retains its original aspect
ratio, including transparent margins. BLACK BELT WORLD's original white lettering
has a dark CSS backing for contrast. This changes only the container background;
the image remains unaltered and there is no sponsorship tier or ranking.

The new supporter destinations were supplied by the site owner. On 2026-11-02,
the official [Jane Street website](https://www.janestreet.com/) and
[BLACK BELT WORLD website](https://blackbeltworld.ca/) were readable. The title of
[小月牙医's supplied website](https://wsdental.nextcard.ai/) identifies it as
Woodbine-Steeles Dental Clinic, so it is sorted under W. The supplied
[Dr Hong Dental HTTP website](http://www.hongdental2014.com/) could not be fetched
by the verification browser; the owner-supplied URL is preserved without guessing
an HTTPS replacement. The owner subsequently confirmed that the supplied HTTP
website is valid; its URL remains unchanged. No third-party directory logo was substituted.

## 素材状态

四家新增机构的原始 logo 已从用户提供的 ZIP 接入，现六家支持者均展示原始 logo。
所有官网链接保持不变；志鸿牙医 HTTP 官网已获用户确认有效。无需再补充支持者 logo。
