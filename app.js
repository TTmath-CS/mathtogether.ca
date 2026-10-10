var still = matchMedia('(prefers-reduced-motion: reduce)').matches;

// Mobile menu: the nav links collapse behind a toggle on narrow screens.
var toggle = document.querySelector('.nav-toggle');
var links = document.getElementById('site-links');
if (toggle && links) {
  function closeMenu(returnFocus) {
    links.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open navigation');
    if (returnFocus) toggle.focus();
  }
  toggle.addEventListener('click', function () {
    var open = links.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  });
  links.addEventListener('click', function (e) {
    if (e.target.closest('a')) closeMenu(false);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && links.classList.contains('open')) closeMenu(true);
  });
  matchMedia('(min-width: 1141px)').addEventListener('change', function () { closeMenu(false); });
}

// Small compatibility map for old static-page URLs and homepage bookmarks.
var legacy = document.querySelector('[data-legacy-target]');
if (legacy) {
  var target = legacy.dataset.legacyTarget;
  if (location.pathname.endsWith('/support.html')) {
    var supportAnchors = ['partners', 'how', 'join', 'contact'];
    if (supportAnchors.indexOf(location.hash.slice(1)) !== -1) target = 'get-involved.html' + location.hash;
  }
  location.replace(target);
} else if (location.pathname.endsWith('/index.html') || location.pathname.endsWith('/')) {
  var oldSections = {programs: 'programs.html#programs', livestream: 'programs.html#livestream', news: 'news.html#news', team: 'team.html#team', involved: 'get-involved.html#involved', faq: 'faq.html#faq', supporters: 'get-involved.html#support'};
  if (oldSections[location.hash.slice(1)]) location.replace(oldSections[location.hash.slice(1)]);
}

// News stories open in a reading overlay instead of stretching the card.
var dlg = document.createElement('dialog');
dlg.className = 'story-dialog';
dlg.setAttribute('aria-label', 'News story');
dlg.innerHTML = '<button class="dlg-close" aria-label="Close">×</button><div class="dlg-body"></div>';
document.body.appendChild(dlg);
var dlgBody = dlg.querySelector('.dlg-body');
dlg.querySelector('.dlg-close').addEventListener('click', function () { dlg.close(); });
dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });

function openStory(s) {
  var details = s.querySelector('details');
  dlgBody.innerHTML = '';
  ['img', 'h3', '.date'].forEach(function (sel) {
    var el = s.querySelector(sel);
    if (el) dlgBody.appendChild(el.cloneNode(true));
  });
  details.querySelectorAll('p:not(.story-preview)').forEach(function (p) {
    dlgBody.appendChild(p.cloneNode(true));
  });
  dlg.showModal();
}

document.querySelectorAll('.story').forEach(function (s) {
  var details = s.querySelector('details');
  if (!details) return;
  details.querySelector('summary').addEventListener('click', function (e) {
    if (!dlg.showModal) return;
    e.preventDefault();
    openStory(s);
  });
});

// The featured event's button opens its full story in the same overlay.
document.querySelectorAll('[data-open-story]').forEach(function (a) {
  var s = document.getElementById(a.getAttribute('data-open-story'));
  if (!s || !s.querySelector('details')) return;
  a.addEventListener('click', function (e) {
    if (!dlg.showModal) return;
    e.preventDefault();
    openStory(s);
  });
});

// Team cards flip like award medals: person on the front, bio on the back.
document.querySelectorAll('.member').forEach(function (m) {
  var flip = document.createElement('div');
  var front = document.createElement('div');
  var back = document.createElement('div');
  var title = document.createElement('h3');
  var details = m.querySelector('details');

  flip.className = 'flip';
  front.className = 'face front';
  back.className = 'face back';
  title.textContent = m.querySelector('h3').textContent;
  back.appendChild(title);

  if (details) {
    details.querySelectorAll('p:not(.story-preview)').forEach(function (p) { back.appendChild(p); });
    details.remove();
  } else {
    var soon = document.createElement('p');
    soon.textContent = 'Bio coming soon.';
    back.appendChild(soon);
  }

  while (m.firstChild) front.appendChild(m.firstChild);
  var hint = document.createElement('p');
  hint.className = 'flip-hint';
  hint.textContent = 'tap for bio';
  front.appendChild(hint);

  flip.appendChild(front);
  flip.appendChild(back);
  m.appendChild(flip);
  m.setAttribute('tabindex', '0');
  m.setAttribute('role', 'button');
  m.setAttribute('aria-pressed', 'false');
  m.setAttribute('aria-label', title.textContent + ': show biography');

  function turn() {
    var flipped = m.classList.toggle('flipped');
    m.setAttribute('aria-pressed', String(flipped));
    m.setAttribute('aria-label', title.textContent + (flipped ? ': show photograph' : ': show biography'));
    front.setAttribute('aria-hidden', String(flipped));
    back.setAttribute('aria-hidden', String(!flipped));
  }
  back.setAttribute('aria-hidden', 'true');
  m.addEventListener('click', turn);
  m.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    e.preventDefault();
    turn();
  });
});

// Fade blocks in on scroll, grid items staggered.
var items = document.querySelectorAll(
  '.section-head, .featured-photo, .featured-copy, .about-body, .cards article, ' +
  '.live-points li, h3.sub, .sessions, .story, .tier-label, .member, ' +
  '.quote-band blockquote, .cta-copy, .support-strip, .faq');

document.querySelectorAll('.cards, .news-grid, .team-grid, .live-points').forEach(function (g) {
  [].forEach.call(g.children, function (c, i) { c.dataset.d = Math.min(i % 4, 3) * 80; });
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
