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
  text wordmarks until their original image files can be imported. The owner
  supplied logo previews in chat, but no readable attachment files or file IDs
  were exposed to this execution environment.
  These are text treatments, not reconstructed or unofficial logos.

The new supporter destinations were supplied by the site owner. On 2026-11-02,
the official [Jane Street website](https://www.janestreet.com/) and
[BLACK BELT WORLD website](https://blackbeltworld.ca/) were readable. The title of
[小月牙医's supplied website](https://wsdental.nextcard.ai/) identifies it as
Woodbine-Steeles Dental Clinic, so it is sorted under W. The supplied
[Dr Hong Dental HTTP website](http://www.hongdental2014.com/) could not be fetched
by the verification browser; the owner-supplied URL is preserved without guessing
an HTTPS replacement. The owner subsequently confirmed that the supplied HTTP
website is valid; its URL remains unchanged. No third-party directory logo was substituted.

## 需要补充的素材

四家机构的 logo 预览已收到，但本执行环境没有可读取的原图文件。请将原始 PNG、JPG
或 SVG 通过文件/ZIP 附件上传，或上传至 `feat/website-round-3` 分支的
`assets/img/sponsors/` 目录。目前保留文字标识和全部官网链接；志鸿牙医 HTTP 官网已获用户确认有效。
