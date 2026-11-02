# SEO and sharing review — Round 3

All metadata uses the production origin `https://mathtogether.ca`. The five content pages have distinct titles and descriptions, canonical URLs, Open Graph metadata, Twitter/X `summary_large_image` metadata, and page JSON-LD. The homepage also describes the existing Math Together Canada organization and website. Existing square `assets/img/logo-badge.png` is used as the PNG favicon.

`robots.txt` points to `https://mathtogether.ca/sitemap.xml`. The sitemap lists the five canonical content URLs, without duplicate legacy routes, hashes, or invented last-modified dates. Legacy About, Livestream, Support and FAQ routes use destination canonicals and `noindex, follow`; crawlers can still follow their compatibility links. The redirect pages remain crawlable so the noindex instruction is visible.

## Sharing image and approval

Every page currently uses the existing, approved photograph:

`https://mathtogether.ca/assets/img/leadership-event.jpg`

It is an existing 1706 × 1279 JPEG. Open Graph includes its real dimensions, JPEG type, HTTPS URL and descriptive alternative text. Twitter/X uses the same HTTPS URL. The source file exists, decodes correctly and is large enough for large-image sharing; platforms may crop it differently because it is not 1.91:1.

A separate proposed 1200 × 630 brand cover was generated using the existing Math Together Canada logo, site colors and branding. The proposal is supplied for review in chat and stays outside the committed/published website. **It is not referenced by any metadata, uploaded to the repository, or published.** After explicit image approval, the approved file can replace the existing-photo fallback in a subsequent change. The generated logo treatment should also be checked during image approval.

## Validation and practical limits

Local validation checks all nine pages for unique titles and descriptions; canonical/Open Graph agreement; required Open Graph and Twitter/X fields; production-domain HTTPS URLs; existing, decodable image files and correct dimensions; valid JSON-LD; and sitemap paths that exist and match their page canonicals. The sitemap contains exactly the five primary pages.

The existing production homepage is readable through the web search tool and contains the approved leadership photograph. Direct image requests through that tool were unavailable. A separate HTTPS HEAD request was blocked by the execution environment's destination policy (`CONNECT 403`), so a live origin HTTP status/content type for the image cannot be certified here. This is an environment access limitation, not a confirmed failure at mathtogether.ca. Local HTTP image responses and browser rendering can be checked in the review checkout. New metadata and the new sitemap remain unserved in production until the PR is approved, merged and deployed.

WhatsApp, WeChat and other messaging apps use their own crawlers, caches and image-cropping rules; some cache a URL's earlier preview for a long time. A local review server cannot reproduce their public crawls. Instagram does not consistently generate normal clickable link previews in feed posts or captions; in-app and direct-message behavior varies. Twitter/X and Facebook inspection tools also require an accessible public URL. No platform preview is guaranteed by static metadata validation. After an approved deployment, re-fetch the public canonical URLs and image without authentication, then check previews in the actual apps or official sharing inspection tools where available. Do not publish the proposed cover merely to test it.
