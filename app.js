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

// news.html is the only source of homepage news; never infer a date from its position.
function newsDate(story) {
  var date = story.getAttribute('data-date') || '';
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) return null;
  var parsed = new Date(date + 'T00:00:00Z');
  if (isNaN(parsed.getTime()) || parsed.toISOString().slice(0, 10) !== date) return null;
  return date;
}

function newsYear(story) {
  var date = newsDate(story);
  if (date) return date.slice(0, 4);
  var year = story.getAttribute('data-year') || '';
  return /^\d{4}$/.test(year) && Number(year) > 0 ? year : null;
}

function newsStories(root) {
  var stories = Array.from(root.querySelectorAll('.news-grid > .story'));
  // A deterministic title-derived ID also lets a newly added story link correctly.
  stories.forEach(function (story) {
    if (!story.id) {
      var title = story.querySelector('h3').textContent.trim();
      var hash = 2166136261;
      for (var i = 0; i < title.length; i++) hash = Math.imul(hash ^ title.charCodeAt(i), 16777619);
      story.id = 'news-' + (hash >>> 0).toString(16);
    }
  });
  var missing = stories.filter(function (story) { return !newsDate(story); });
  if (missing.length) console.warn('News exact dates not specified:', missing.map(function (story) { return story.querySelector('h3').textContent.trim(); }));
  // Group by known year. Within each year, sort the precisely dated entries
  // into their dated slots; year-only entries keep their source left-to-right slots.
  // This gives a transitive order without inventing a month/day for year-only news.
  var years = new Map();
  var unknown = [];
  stories.forEach(function (story) {
    var year = newsYear(story);
    if (!year) { unknown.push(story); return; }
    if (!years.has(year)) years.set(year, []);
    years.get(year).push(story);
  });
  var sorted = [];
  Array.from(years.keys()).sort().reverse().forEach(function (year) {
    var group = years.get(year);
    var dated = group.filter(function (story) { return newsDate(story); }).sort(function (a, b) {
      var aDate = newsDate(a), bDate = newsDate(b);
      return aDate !== bDate ? (aDate > bDate ? -1 : 1) : a.id.localeCompare(b.id);
    });
    var next = 0;
    group.forEach(function (story) { sorted.push(newsDate(story) ? dated[next++] : story); });
  });
  return sorted.concat(unknown);
}

var newsGrid = document.querySelector('.news-grid');
if (newsGrid) newsStories(document).forEach(function (story) { newsGrid.appendChild(story); });

var latestGrid = document.querySelector('[data-latest-news]');
if (latestGrid) {
  var latestStatus = document.querySelector('.latest-news-status');
  fetch('news.html', { cache: 'no-cache' }).then(function (response) {
    if (!response.ok) throw new Error('News request failed');
    return response.text();
  }).then(function (html) {
    var source = new DOMParser().parseFromString(html, 'text/html');
    var stories = newsStories(source).filter(function (s) { return newsYear(s); }).slice(0, 3);
    if (!stories.length) throw new Error('No news with a known year available');
    stories.forEach(function (story) {
      var card = document.createElement('a');
      card.className = 'home-story-card';
      card.href = 'news.html#' + encodeURIComponent(story.id);
      var frame = document.createElement('div');
      frame.className = 'news-image';
      var image = story.querySelector('.news-image img').cloneNode(true);
      frame.appendChild(image);
      var heading = document.createElement('h3');
      heading.textContent = story.querySelector('h3').textContent.trim();
      var preciseDate = newsDate(story);
      var date = document.createElement(preciseDate ? 'time' : 'span');
      date.className = 'date';
      if (preciseDate) {
        date.dateTime = preciseDate;
        date.textContent = new Intl.DateTimeFormat('en-CA', { year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC' }).format(new Date(preciseDate + 'T00:00:00Z'));
      } else {
        date.dataset.year = newsYear(story);
        date.textContent = newsYear(story);
      }
      card.appendChild(frame);
      card.appendChild(heading);
      card.appendChild(date);
      latestGrid.appendChild(card);
    });
    latestStatus.hidden = true;
  }).catch(function () {
    latestStatus.textContent = 'Latest news is currently unavailable. Please visit the News page.';
  }).finally(function () { latestGrid.setAttribute('aria-busy', 'false'); });
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
  if (!details) return;
  if (typeof dlg.showModal !== 'function') { details.open = true; return; }
  dlgBody.innerHTML = '';
  ['img', 'h3', '.date'].forEach(function (sel) {
    var el = s.querySelector(sel);
    if (el) dlgBody.appendChild(el.cloneNode(true));
  });
  details.querySelectorAll('p:not(.story-preview)').forEach(function (p) {
    dlgBody.appendChild(p.cloneNode(true));
  });
  dlg.setAttribute('aria-label', s.querySelector('h3').textContent.trim());
  if (!dlg.open) dlg.showModal();
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

// Exact story bookmarks open their reading dialog; video-only stories remain visible
// with their existing video link. Back/Forward and in-page bookmark changes work too.
function openLinkedStory() {
  var id;
  try { id = decodeURIComponent(location.hash.slice(1)); } catch (e) { return; }
  var story = document.getElementById(id);
  if (!story || !story.matches('.news-grid > .story')) return;
  story.scrollIntoView({ block: 'start' });
  if (story.querySelector('details')) openStory(story);
  else if (dlg.open) dlg.close();
}
window.addEventListener('hashchange', openLinkedStory);
openLinkedStory();

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
