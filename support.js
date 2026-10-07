// support.html has no stories or team cards, so it takes just the behaviours
// from app.js that the shared stylesheet expects: the mobile menu, the
// on-scroll reveal and the stat count-up.
var still = matchMedia('(prefers-reduced-motion: reduce)').matches;

// Mobile menu: the nav links collapse behind a toggle on narrow screens.
var toggle = document.querySelector('.nav-toggle');
var links = document.getElementById('site-links');
toggle.addEventListener('click', function () {
  var open = links.classList.toggle('open');
  toggle.setAttribute('aria-expanded', open);
});
links.addEventListener('click', function (e) {
  if (e.target.tagName !== 'A') return;
  links.classList.remove('open');
  toggle.setAttribute('aria-expanded', 'false');
});

// Fade blocks in on scroll, grid items staggered.
var items = document.querySelectorAll(
  '.section-head, .sponsor, .live-points li, blockquote, .cta-copy');

document.querySelectorAll('.sponsor-grid, .live-points').forEach(function (g) {
  [].forEach.call(g.children, function (c, i) { c.dataset.d = Math.min(i, 5) * 80; });
});

if (!still && 'IntersectionObserver' in window) {
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.style.transitionDelay = (e.target.dataset.d || 0) + 'ms';
      e.target.classList.add('in');
      io.unobserve(e.target);
    });
  }, { threshold: 0.1 });
  items.forEach(function (el) { el.classList.add('reveal'); io.observe(el); });
}

// Count the hero stats up from zero.
document.querySelectorAll('.stats b').forEach(function (b) {
  var m = b.textContent.match(/^([^0-9]*)([\d,]+)(.*)$/);
  if (!m || still) return;
  var end = +m[2].replace(/,/g, ''), t0 = null;
  function step(ts) {
    if (!t0) t0 = ts;
    var p = Math.min((ts - t0) / 900, 1), e = 1 - Math.pow(1 - p, 3);
    b.textContent = m[1] + Math.round(end * e).toLocaleString('en-CA') + m[3];
    if (p < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
});
