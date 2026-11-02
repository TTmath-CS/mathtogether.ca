# Link behavior

All destination links open a new browser tab/window, preserving the original
page. This covers navigation and brand links, calls to action, homepage program
cards, featured and historical recaps, generated Latest News cards, article
reading actions, social/video links and supporter websites.

Static anchors specify `target="_blank"` and `rel="noopener noreferrer"`.
Accessible labels or descriptions announce the new tab. The shared
`setNewTabLink` helper applies the same behavior to generated links. URLs,
article IDs, video question ranges and machine-readable dates are unchanged.

News reading actions progressively become native anchors to their existing
`news.html#article-id` destinations. The destination tab opens the reading
dialog. With JavaScript disabled, the original details/summary reading fallback
remains available. Skip-to-content links move focus in the current document;
FAQ, historical-recap disclosure, menu and team-card controls remain in-page
interactions.

The former “How our supporters help” section, its generator output, styles and
unused description data are removed. The six supporter organizations, original
logos, Chinese caption, equal-size grid, order, counts and website URLs remain.

Validation includes all nine pages' static links, five main pages at four
viewport widths, Latest News regressions, JavaScript-free fallbacks and actual
popup navigation with original-page URLs preserved. External destinations are
mocked only for popup tests; internal pages and article dialogs load from the
real local site.
