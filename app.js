var still = matchMedia('(prefers-reduced-motion: reduce)').matches;
var sky = document.querySelector('.sky-stage');
var coords = sky.querySelector('.coords');
var lastLegendName = '';

var formulas = [
  {
    title: 'Euler identity',
    formula: 'e^(iπ) + 1 = 0',
    formulaHtml: 'e<sup>iπ</sup> + 1 = 0',
    note: 'Five essential constants meeting in one line.'
  },
  {
    title: 'Pythagorean theorem',
    formula: 'a^2 + b^2 = c^2',
    formulaHtml: 'a<sup>2</sup> + b<sup>2</sup> = c<sup>2</sup>',
    note: 'The oldest right-triangle compass.'
  },
  {
    title: 'Cauchy-Schwarz',
    formula: '(Σa_i b_i)^2 ≤ (Σa_i^2)(Σb_i^2)',
    formulaHtml: '(<span class="sigma">Σ</span>a<sub>i</sub>b<sub>i</sub>)<sup>2</sup> ≤ ' +
      '(<span class="sigma">Σ</span>a<sub>i</sub><sup>2</sup>)(<span class="sigma">Σ</span>b<sub>i</sub><sup>2</sup>)',
    note: 'A quiet engine behind olympiad inequalities.'
  },
  {
    title: "Fermat's little theorem",
    formula: 'a^p ≡ a (mod p)',
    formulaHtml: 'a<sup>p</sup> ≡ a <span class="mod">(mod&nbsp;p)</span>',
    note: 'Prime numbers leaving a modular fingerprint.'
  },
  {
    title: 'Pascal identity',
    formula: 'C(n,k) = C(n-1,k-1) + C(n-1,k)',
    formulaHtml: '<span class="binom"><span>n</span><span>k</span></span> = ' +
      '<span class="binom"><span>n − 1</span><span>k − 1</span></span> + ' +
      '<span class="binom"><span>n − 1</span><span>k</span></span>',
    note: 'Combinations growing one row at a time.'
  },
  {
    title: 'Bayes theorem',
    formula: 'P(A|B) = P(B|A)P(A) / P(B)',
    formulaHtml: 'P(A|B) = <span class="math-frac"><span>P(B|A)P(A)</span><span>P(B)</span></span>',
    note: 'A rule for updating belief when evidence arrives.'
  },
  {
    title: 'Infinite primes',
    formula: 'There are infinitely many primes.',
    formulaHtml: '∀N ∈ ℕ, ∃ prime p &gt; N',
    note: 'Euclid made infinity feel inevitable.'
  },
  {
    title: 'Golden ratio',
    formula: 'φ = (1 + √5) / 2',
    formulaHtml: 'φ = <span class="math-frac"><span>1 + √5</span><span>2</span></span>',
    note: 'A recurrence, a spiral, and a proportion.'
  }
];

var conjectures = [
  {
    kicker: 'Open conjecture',
    title: 'Riemann hypothesis',
    formulaHtml: 'ζ(s) = 0 ⇒ Re(s) = <span class="math-frac"><span>1</span><span>2</span></span>',
    note: 'The hidden rhythm of prime numbers may sit on one critical line.'
  },
  {
    kicker: 'Open conjecture',
    title: 'Collatz conjecture',
    formulaHtml: 'n → <span class="piecewise"><span>n / 2</span><span>3n + 1</span></span> → 1 ?',
    note: 'A rule simple enough for middle school, still undefeated.'
  },
  {
    kicker: 'Open conjecture',
    title: 'Goldbach conjecture',
    formulaHtml: 'Every even n &gt; 2 = p + q',
    note: 'Can every even number split into two primes? We still do not know.'
  },
  {
    kicker: 'Open conjecture',
    title: 'Twin prime conjecture',
    formulaHtml: 'Infinitely many p where p + 2 is prime?',
    note: 'Prime pairs keep appearing; proving they never run out is another story.'
  },
  {
    kicker: 'Open conjecture',
    title: 'P vs NP',
    formulaHtml: 'P ?= NP',
    note: 'If solutions are easy to check, are they always easy to find?'
  },
  {
    kicker: 'Open conjecture',
    title: 'Birch and Swinnerton-Dyer',
    formulaHtml: 'rank E(ℚ) ↔ order of zero of L(E,s)',
    note: 'A bridge between rational points and the analytic behavior of elliptic curves.'
  }
];

var topics = [
  {
    kicker: 'Math world',
    title: 'Topology',
    formulaHtml: 'shape without measuring',
    note: 'Study what survives stretching, twisting, and continuous deformation.'
  },
  {
    kicker: 'Math world',
    title: 'Fractals and chaos',
    formulaHtml: 'z → z<sup>2</sup> + c',
    note: 'Tiny changes, infinite detail, and patterns that never quite settle.'
  },
  {
    kicker: 'Math world',
    title: 'Graph theory',
    formulaHtml: 'vertices + edges = networks',
    note: 'The math of routes, friendships, competitions, maps, and algorithms.'
  },
  {
    kicker: 'Math world',
    title: 'Modular arithmetic',
    formulaHtml: 'a ≡ b <span class="mod">(mod&nbsp;n)</span>',
    note: 'Clock math that powers contests, cryptography, and number theory.'
  },
  {
    kicker: 'Math world',
    title: 'Game theory',
    formulaHtml: 'strategy + incentives',
    note: 'A way to reason about choices when everyone else is thinking too.'
  },
  {
    kicker: 'Math world',
    title: 'Combinatorics',
    formulaHtml: 'count the impossible-looking set',
    note: 'Arrangements, invariants, clever counting, and olympiad problem magic.'
  }
];

var legends = [
  {
    name: 'Euclid',
    src: 'assets/img/legends/euclid.jpg',
    note: 'Wrote The Elements — 13 books that defined geometry and proof for 2,000+ years.'
  },
  {
    name: 'Pythagoras',
    src: 'assets/img/legends/pythagoras.jpg',
    note: 'The theorem linking right triangles to numbers; taught that number rules everything.'
  },
  {
    name: 'Archimedes',
    src: 'assets/img/mathematicians/archimedes.jpg',
    note: 'Nailed π between 3 10/71 and 3 1/7, law of the lever, buoyancy — antiquity at its peak.'
  },
  {
    name: 'René Descartes',
    src: 'assets/img/legends/descartes.jpg',
    note: 'Invented the Cartesian plane — the very grid this sky is drawn on.'
  },
  {
    name: 'Pierre de Fermat',
    src: 'assets/img/legends/fermat.jpg',
    note: 'Founded modern number theory; his Last Theorem took 358 years to prove.'
  },
  {
    name: 'Blaise Pascal',
    src: 'assets/img/legends/pascal.jpg',
    note: 'Pascal’s triangle, probability theory with Fermat, and a working calculator at 19.'
  },
  {
    name: 'Isaac Newton',
    src: 'assets/img/mathematicians/newton.jpg',
    note: 'Invented calculus, then used it to explain motion and gravity.'
  },
  {
    name: 'Gottfried Leibniz',
    src: 'assets/img/legends/leibniz.jpg',
    note: 'Co-invented calculus — the dy/dx and ∫ notation we still write today.'
  },
  {
    name: 'Leonhard Euler',
    src: 'assets/img/mathematicians/euler.jpg',
    note: 'Most prolific mathematician ever: e^iπ + 1 = 0, graph theory, 850+ works.'
  },
  {
    name: 'Carl Friedrich Gauss',
    src: 'assets/img/mathematicians/gauss.jpg',
    note: 'The "Prince of Mathematics": number theory, least squares, the Gaussian curve.'
  },
  {
    name: 'Évariste Galois',
    src: 'assets/img/legends/galois.jpg',
    note: 'Created group theory by age 20, settling when equations can be solved.'
  },
  {
    name: 'Bernhard Riemann',
    src: 'assets/img/legends/riemann.jpg',
    note: 'Riemann surfaces, the hypothesis on primes, and the geometry behind relativity.'
  },
  {
    name: 'Henri Poincaré',
    src: 'assets/img/legends/poincare.png',
    note: 'Founded topology and chaos theory; his conjecture stood for a century.'
  },
  {
    name: 'David Hilbert',
    src: 'assets/img/legends/hilbert.jpg',
    note: 'His 23 problems set the agenda for 20th-century mathematics.'
  },
  {
    name: 'Sofia Kovalevskaya',
    src: 'assets/img/legends/sofia-kovalevskaya.jpg',
    note: 'First woman to earn a math doctorate; Cauchy–Kovalevskaya theorem.'
  },
  {
    name: 'Srinivasa Ramanujan',
    src: 'assets/img/mathematicians/ramanujan.jpg',
    note: 'Self-taught genius: ~3,900 identities, partitions, and mock theta functions.'
  },
  {
    name: 'Emmy Noether',
    src: 'assets/img/mathematicians/noether.jpg',
    note: 'Noether’s theorem: every symmetry hides a conservation law.'
  },
  {
    name: 'Albert Einstein',
    src: 'assets/img/legends/einstein.jpg',
    note: 'General relativity — gravity explained as curved spacetime.'
  },
  {
    name: 'Galileo Galilei',
    src: 'assets/img/legends/galileo.jpg',
    note: '"The universe is written in the language of mathematics" — and he proved it.'
  },
  {
    name: 'Ada Lovelace',
    src: 'assets/img/mathematicians/lovelace.jpg',
    note: 'Wrote the first computer program — a century before computers existed.'
  },
  {
    name: 'Alan Turing',
    src: 'assets/img/mathematicians/turing.jpg',
    note: 'The Turing machine, breaking Enigma, and the test for machine minds.'
  },
  {
    name: 'John von Neumann',
    src: 'assets/img/legends/von-neumann.gif',
    note: 'Game theory, the stored-program computer, and the math of quantum mechanics.'
  },
  {
    name: 'Grace Hopper',
    src: 'assets/img/legends/grace-hopper.jpg',
    note: 'Built the first compiler and made programming speak English.'
  },
  {
    name: 'Katherine Johnson',
    src: 'assets/img/legends/katherine-johnson.jpg',
    note: 'Hand-computed NASA’s orbits for Mercury and Apollo 11.'
  },
  {
    name: 'Paul Erdős',
    src: 'assets/img/legends/erdos.jpg',
    note: '1,500+ papers with 500+ collaborators — math’s great connector.'
  },
  {
    name: 'Maryam Mirzakhani',
    src: 'assets/img/legends/mirzakhani.jpg',
    note: 'First woman to win the Fields Medal (2014), for the geometry of surfaces.'
  },
  {
    name: 'Terence Tao',
    src: 'assets/img/legends/tao.jpg',
    note: 'IMO gold at 13 — youngest ever — and the 2006 Fields Medal.'
  }
];

// Preload portraits so a legend appears instantly on unlock.
addEventListener('load', function () {
  legends.forEach(function (m) { new Image().src = m.src; });
});

function pick(list) {
  return list[Math.floor(Math.random() * list.length)];
}

function pickLegend() {
  var choices = legends.filter(function (m) {
    return m.name !== lastLegendName;
  });
  var item = pick(choices.length ? choices : legends);
  lastLegendName = item.name;
  return item;
}

function clamp(n, min, max) {
  return Math.max(min, Math.min(max, n));
}

// The two hero curves draw themselves on load.
document.querySelectorAll('.curve').forEach(function (p, i) {
  if (still) return;
  var L = p.getTotalLength();
  p.style.strokeDasharray = L;
  p.style.strokeDashoffset = L;
  p.style.transition = 'stroke-dashoffset 1.7s ease ' + (0.4 + i * 0.35) + 's';
  requestAnimationFrame(function () {
    requestAnimationFrame(function () { p.style.strokeDashoffset = 0; });
  });
});

// Sprinkle a night sky: varied sizes, warm and cool tints, a few bright standouts.
var tints = ['#ffffff', '#dbe6ff', '#fff3d9'];
for (var i = 0; i < 160; i++) {
  var s = document.createElement('span');
  s.className = 'star';
  var sz = 1 + Math.random() * 1.8;
  if (Math.random() < 0.06) sz = 2.8 + Math.random() * 1.2;
  s.style.cssText = 'left:' + (Math.random() * 100) + '%;top:' + (Math.random() * 92) +
    '%;width:' + sz + 'px;height:' + sz + 'px;background:' + tints[i % 3] +
    ';animation-duration:' + (1.6 + Math.random() * 5.5) + 's;animation-delay:-' +
    (Math.random() * 7) + 's';
  sky.insertBefore(s, sky.firstChild);
}

// Shooting stars: slow comets crossing the sky in straight random lines.
function meteorShower() {
  var W = sky.clientWidth, H = sky.clientHeight;
  var n = 1 + Math.floor(Math.random() * 2);
  for (var k = 0; k < n; k++) {
    var m = document.createElement('div');
    var fromLeft = Math.random() < 0.5;
    var x0 = fromLeft ? -30 : W + 30;
    var x1 = fromLeft ? W + 30 : -30;
    var y0 = 20 + Math.random() * H * 0.75;
    var y1 = 20 + Math.random() * H * 0.75;
    m.className = 'meteor';
    m.style.offsetPath = "path('M" + x0 + ' ' + y0 + ' L' + x1 + ' ' + y1 + "')";
    m.style.setProperty('--dur', (4.5 + Math.random() * 3) + 's');
    m.style.animationDelay = (Math.random() * 0.8) + 's';
    sky.appendChild(m);
    m.addEventListener('animationend', function (e) { e.target.remove(); });
  }
  setTimeout(meteorShower, 5000 + Math.random() * 9000);
}
if (!still) setTimeout(meteorShower, 1500);

// Live (x, y) readout: the panel is a real coordinate plane, 26px per unit.
sky.addEventListener('mousemove', function (e) {
  var r = sky.getBoundingClientRect();
  var x = ((e.clientX - r.left) / 26).toFixed(1);
  var y = ((r.bottom - e.clientY) / 26).toFixed(1);
  coords.textContent = '(x, y) = (' + x + ', ' + y + ')';
});

function showFormula(x, y, item) {
  var b = document.createElement('div');
  var star = document.createElement('span');
  var label = document.createElement('span');
  var title = document.createElement('b');
  var formula = document.createElement('em');

  b.className = 'spark-burst';
  b.style.left = x + 'px';
  b.style.top = y + 'px';
  star.className = 'spark-star';
  label.className = 'spark-formula';
  title.textContent = item.kicker ? item.kicker + ' · ' + item.title : item.title;
  formula.innerHTML = item.formulaHtml;
  label.appendChild(title);
  label.appendChild(formula);
  b.appendChild(star);
  b.appendChild(label);
  sky.appendChild(b);

  b.addEventListener('animationend', function () { b.remove(); });
  cap('.spark-burst', 4);
}

function showPortrait(x, y, item) {
  var card = document.createElement('div');
  var img = document.createElement('img');
  var name = document.createElement('b');
  var note = document.createElement('span');

  card.className = 'portrait-burst';
  card.style.left = x + 'px';
  card.style.top = y + 'px';
  img.src = item.src;
  img.alt = item.name + ' portrait';
  name.textContent = item.name;
  note.textContent = item.note;
  card.appendChild(img);
  card.appendChild(name);
  card.appendChild(note);

  function reveal() {
    sky.appendChild(card);
    cap('.portrait-burst', 3);
  }
  if (img.complete) reveal();
  else { img.onload = reveal; img.onerror = reveal; }

  card.addEventListener('animationend', function () { card.remove(); });
}

function cap(selector, limit) {
  var nodes = sky.querySelectorAll(selector);
  while (nodes.length > limit) {
    nodes[0].remove();
    nodes = sky.querySelectorAll(selector);
  }
}

function discover(px, py) {
  var r = sky.getBoundingClientRect();
  var safeX = clamp(px, 86, r.width - 86);
  var safeY = clamp(py, 70, r.height - 110);
  var roll = Math.random();
  var kind = roll < 0.3 ? 'portrait' : roll < 0.6 ? 'formula' :
    roll < 0.85 ? 'conjecture' : 'topic';
  var item = kind === 'portrait' ? pickLegend() :
    kind === 'formula' ? pick(formulas) :
    kind === 'conjecture' ? pick(conjectures) : pick(topics);

  if (kind === 'portrait') showPortrait(safeX, safeY, item);
  else showFormula(safeX, safeY, item);
}

sky.addEventListener('click', function (e) {
  var r = sky.getBoundingClientRect();
  discover(e.clientX - r.left, e.clientY - r.top);
});

sky.addEventListener('keydown', function (e) {
  if (e.key !== 'Enter' && e.key !== ' ') return;
  e.preventDefault();
  var r = sky.getBoundingClientRect();
  discover(90 + Math.random() * (r.width - 180), 80 + Math.random() * (r.height - 170));
});

// News stories open in a reading overlay instead of stretching the card.
var dlg = document.createElement('dialog');
dlg.className = 'story-dialog';
dlg.innerHTML = '<button class="dlg-close" aria-label="Close">×</button><div class="dlg-body"></div>';
document.body.appendChild(dlg);
var dlgBody = dlg.querySelector('.dlg-body');
dlg.querySelector('.dlg-close').addEventListener('click', function () { dlg.close(); });
dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });

document.querySelectorAll('.story').forEach(function (s) {
  var details = s.querySelector('details');
  if (!details) return;
  details.querySelector('summary').addEventListener('click', function (e) {
    e.preventDefault();
    dlgBody.innerHTML = '';
    ['img', 'h3', '.date'].forEach(function (sel) {
      var el = s.querySelector(sel);
      if (el) dlgBody.appendChild(el.cloneNode(true));
    });
    details.querySelectorAll('p').forEach(function (p) {
      dlgBody.appendChild(p.cloneNode(true));
    });
    dlg.showModal();
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
    details.querySelectorAll('p').forEach(function (p) { back.appendChild(p); });
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

  function turn() { m.classList.toggle('flipped'); }
  m.addEventListener('click', turn);
  m.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    e.preventDefault();
    turn();
  });
});

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
  'main section>h2, .section-lede, #about>p, blockquote, .cards article, ' +
  '.live-points li, h3.sub, .sessions, .story, .tier-label, .member, ' +
  '#involved p, #involved .cta-row, .faq');

document.querySelectorAll('.cards, .news-grid, .team-grid').forEach(function (g) {
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
