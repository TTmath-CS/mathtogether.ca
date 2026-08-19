// support.html is a plain page — no coordinate sky — so it takes just the two
// behaviours from app.js that the shared stylesheet expects: the y-axis scroll
// ruler and the on-scroll reveal.

// The fixed y-axis ruler tracks scroll depth.
var marker = document.querySelector('.yaxis .marker');
function ruler() {
  var max = document.documentElement.scrollHeight - innerHeight;
  var p = max > 0 ? scrollY / max : 0;
  var track = marker.parentElement.clientHeight - 12;
  marker.style.top = p * track + 'px';
  marker.setAttribute('data-v', Math.round(p * 100));
}
addEventListener('scroll', function () { requestAnimationFrame(ruler); }, { passive: true });
ruler();

// Fade blocks in on scroll, grid items staggered.
var items = document.querySelectorAll(
  'main section>h2, .section-lede, blockquote, .sponsor, ' +
  '.live-points li, #join p, #join .cta-row');

document.querySelectorAll('.sponsor-grid').forEach(function (g) {
  [].forEach.call(g.children, function (c, i) { c.dataset.d = Math.min(i, 5) * 80; });
});

var io = new IntersectionObserver(function (es) {
  es.forEach(function (e) {
    if (!e.isIntersecting) return;
    e.target.style.transitionDelay = (e.target.dataset.d || 0) + 'ms';
    e.target.classList.add('in');
    io.unobserve(e.target);
  });
}, { threshold: 0.1 });

items.forEach(function (el) { el.classList.add('reveal'); io.observe(el); });

// Count the hero stats up from zero.
var still = matchMedia('(prefers-reduced-motion: reduce)').matches;
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
