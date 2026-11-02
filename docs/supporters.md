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
- Jane Street, BLACK BELT WORLD, 志鸿牙医 / Dr Hong Dental, and 小月牙医 use plain
  text wordmarks pending original logo files and confirmation of suitable use.
  These are text treatments, not reconstructed or unofficial logos.

The new supporter destinations were supplied by the site owner. On 2026-11-02,
the official [Jane Street website](https://www.janestreet.com/) and
[BLACK BELT WORLD website](https://blackbeltworld.ca/) were readable. The title of
[小月牙医's supplied website](https://wsdental.nextcard.ai/) identifies it as
Woodbine-Steeles Dental Clinic, so it is sorted under W. The supplied
[Dr Hong Dental HTTP website](http://www.hongdental2014.com/) could not be fetched
by the verification browser; the owner-supplied URL is preserved without guessing
an HTTPS replacement. No third-party directory logo was substituted.

## 需要补充的素材

请提供 Jane Street、小月牙医（Woodbine-Steeles Dental Clinic）、志鸿牙医 / Dr Hong Dental、
BLACK BELT WORLD 的原始徽标文件（建议透明背景 SVG 或 PNG），并确认可用于支持者展示。
目前已使用简洁的文字标识，保留所有官网链接。志鸿牙医的官网在本次验证时未能加载，
请确认所提供的 HTTP 链接仍然有效。
