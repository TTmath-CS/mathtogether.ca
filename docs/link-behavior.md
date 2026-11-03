# Link behavior

All destination links open a new browser tab/window, preserving the original
page. This covers navigation and brand links, calls to action, homepage program
cards, featured and historical recaps, generated Latest News cards, article
reading actions, social/video links and supporter websites.

Static anchors specify `target="_blank"` and `rel="noopener noreferrer"`.
Accessible labels or descriptions announce the new tab or window. The shared
`setNewTabLink` helper applies the same behavior to generated links. URLs,
article IDs, video question ranges and machine-readable dates are unchanged.

The homepage featured recap, 2024/2025 recap links and all three generated
“Our Community in Action” cards use `read.html?story=<existing-story-id>`.
An ordinary click or keyboard activation requests an independent browser popup
with `noopener,noreferrer`; it leaves the homepage URL, scroll and controls
unchanged. Modified clicks and middle clicks retain native link behavior.
Browsers, particularly mobile browsers, ultimately control whether a requested
popup appears as a separate window or tab.

The reader fetches the original story from `news.html`, displaying its full
article, date and images without News navigation, footer or story grid. Verified
individual YouTube URLs produce privacy-enhanced players without autoplay;
original Watch links remain available. Close window and Escape close a
script-opened reader. Loading failures show an in-window retry rather than
redirecting to News. The reader is `noindex, follow`, canonicalizes to News,
and stays outside the sitemap. With JavaScript disabled it offers a News link.

News reading actions progressively become native anchors to their existing
`news.html#article-id` destinations. The destination tab opens the reading
dialog. With JavaScript disabled, the original details/summary reading fallback
remains available. Skip-to-content links move focus in the current document;
FAQ, historical-recap disclosure, menu and team-card controls remain in-page
interactions.

The former “How our supporters help” section, its generator output, styles and
unused description data are removed. The six supporter organizations, original
logos, Chinese caption, equal-size grid, counts and website URLs remain.
TTmath is pinned first at the owner's request; the other five keep their
alphabetical order. The alphabetical-order note is removed.

Validation includes all ten pages' static links, five main pages at four
viewport widths, Latest News regressions, JavaScript-free fallbacks and actual
popup navigation with original-page URLs preserved. External destinations are
mocked only for popup tests; internal pages and article dialogs load from the
real local site. Reader tests also cover full content preservation, video-only
stories, safe YouTube URL matching, error/retry and window closing.
