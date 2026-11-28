"""remake7.py -- the seventh stage of the gasket page's remake: what the referee's reading found (referee27/reading-report.md).
It changes page.src.html in place, from out27/page.src.stage6.html.txt to out27/page.src.stage7.html.txt.     python -I out27/remake7.py
  a. The first sentence said "Squares are lit in orange" whatever was lit: its second half now follows the menu of lights.
  b. The sentence under the swap button spoke of "the two largest orange circles" of a picture that may be magnified: it now says what
     is true of the gasket in any view.
  c. "N circles drawn" counted circles of which nothing was in the picture (the circle round the rest when its edge is out of view;
     circles whose bounding square only touches the view): the count, the count of lit circles and the table now take a circle only if
     some of it is in the picture.
  d. Third panel, the kind with two pairs of fourth-power forms: the pair the circles show to be ruled out is now counted with the
     families ruled out, and marked.
  e. Four numbers that satisfy the equation with every sign turned (4, -5, -20, -21) were told that they do not satisfy it.
  f. "come to an end" in the second caption is "seem to come to an end": the paper conjectures it.
  g. "For twenty years the guess was": the guess was first made in 2003 and revised in 2011.
  h. The lists are the same as those in the authors' own files, which their paper names; the paper is cited with its arXiv number.
  i. "rules out no family of squares" beside "no number in it is a fourth power": the sentence now names the four forms it means.
  and from "what have I not thought of": a word for a visitor whose browser runs no script; "Looking through the circles" before a look."""
import os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); P = os.path.join(HERE, 'page.src.html')
def rep(s, a, b, n=1):
    assert s.count(a) == n, (s.count(a), a[:90]); return s.replace(a, b)
def main():
    s = open(P, encoding='utf-8').read()
    assert s == open(os.path.join(HERE, 'out27', 'page.src.stage6.html.txt'), encoding='utf-8').read(), 'page.src.html is not stage 6'
    # a. the first sentence, and a word for a browser without script
    s = rep(s, '  <p class="sub" id="lead">The smaller a circle, the bigger its number. Squares are lit in orange.</p>\n',
               '  <p class="sub" id="lead">The smaller a circle, the bigger its number. <span id="leadlit"></span></p>\n'
               '  <noscript><p class="sub">This page draws its pictures with a script, and the script is off or has not loaded. Without it there is nothing here to see or to press; what is below is only the words.</p></noscript>\n')
    s = rep(s, '</style>\n</head>', '</style>\n<noscript><style>figure, h2.fig { display: none; }</style></noscript>\n</head>')
    s = rep(s, '<h2>The numbers that never come</h2>', '<h2 class="fig">The numbers that never come</h2>')
    s = rep(s, '<h2>Any gasket</h2>', '<h2 class="fig">Any gasket</h2>')
    s = rep(s, "    $('hiName').textContent = words; var mag = view.s / base();", "    $('hiName').textContent = words; var mag = view.s / base(), ll = litLead(); if ($('leadlit').textContent !== ll) $('leadlit').textContent = ll;")
    s = rep(s, "  function draw() {\n", "  function litLead() { var h = $('hi').value; return h === 'none' ? 'Nothing is lit now.' : (h === '1' ? 'Squares' : h === 'five' ? 'Multiples of 5' : h === 'q' ? 'Fourth powers, and 4, 9 or 36 times one,' : 'Numbers that are ' + hiWords()) + ' are lit in orange.'; }      /* the second half of the page's first sentence */\n"
               "  // Is anything of this circle in the picture?  For a circle of the gasket: its disc meets the picture.  For the circle round the rest: its edge does.\n"
               "  function seen(c) { var b = c[0], r = view.s / Math.abs(b), dx = Math.abs(c[3] / b * view.s), dy = Math.abs(c[4] / b * view.s), qx, qy; if (b < 0) return (dx + W / 2) * (dx + W / 2) + (dy + H / 2) * (dy + H / 2) >= r * r; qx = Math.max(dx - W / 2, 0); qy = Math.max(dy - H / 2, 0); return qx * qx + qy * qy <= r * r; }\n"
               "  function draw() {\n")
    # on a screen held sideways (360 high) the picture, 240 high, ran off the first screen: its floor is now 200
    s = rep(s, "Math.round(Math.min(w, Math.max(240, window.innerHeight * 0.62)))", "Math.round(Math.min(w, Math.max(200, window.innerHeight * 0.62)))")
    # b. the sentences under the swap button
    s = rep(s, "h = 'Here squares turn up: the two largest orange circles are marked 36 (6 \\u00d7 6).';", "h = 'Squares turn up in this gasket: the smallest is 36 (6 \\u00d7 6), on two circles.';")
    s = rep(s, "That was proved in 2023, against what had been believed for twenty years.';", "That was proved in 2023, against a guess first made twenty years before.';")
    # c. only circles of which something is in the picture are counted
    s = rep(s, "if (b > 0 && test && test(b)) lit++; if (b > 0 && at2 && at2[0] > 30", "if (b > 0 && test && test(b) && seen(c)) lit++; if (b > 0 && at2 && at2[0] > 30")
    s = rep(s, "if (b > 0 && test && test(b)) { lit++; g.fillStyle = '#d95926';", "if (b > 0 && test && test(b)) { if (seen(c)) lit++; g.fillStyle = '#d95926';")
    s = rep(s, "var ncirc = drawn.filter(function (c) { return c[0] !== 0; }).length;", "var ncirc = drawn.filter(function (c) { return c[0] !== 0 && seen(c); }).length;                 /* the program hands over every circle whose bounding square meets the view: some of those have nothing in the picture */")
    s = rep(s, "function gtable() { var rows = drawn.filter(function (c) { return c[0] > 0; })", "function gtable() { var rows = drawn.filter(function (c) { return c[0] > 0 && seen(c); })")
    # d. the third panel: the pair of fourth-power forms that the circles show to be ruled out is counted with the families
    s = rep(s, "miss = G.missing(rootq, N, en); spor = miss.filter(function (v) { return !G.inFamily(v, fam); });\n", "miss = G.missing(rootq, N, en);\n")
    s = rep(s, "'it finds none of them up to ' + group(N) + '. '; }\n",
               "'it finds none of them up to ' + group(N) + '. '; }\n"
               "    var q4 = t.quartic && t.k !== 1 ? (may.length ? [9, 36] : no.length ? [1, 4] : []) : [], ruled = function (v) { return G.inFamily(v, fam) || q4.some(function (u) { var w = v / u, r4 = Math.round(Math.sqrt(Math.sqrt(w))); return v % u === 0 && r4 * r4 * r4 * r4 === w; }); };\n"
               "    spor = miss.filter(function (v) { return !ruled(v); });                 /* for the kind with two pairs of fourth-power forms, the pair the circles show to be ruled out is counted with the families, and marked */\n")
    s = rep(s, "numbers that pass the test are missing' + (fam.length ? ', ' + group(miss.length - spor.length) + ' of them in the famil' + (fam.length > 1 ? 'ies' : 'y') + ' ruled out", "numbers that pass the test are missing' + (fam.length + q4.length ? ', ' + group(miss.length - spor.length) + ' of them in the famil' + (fam.length + q4.length > 1 ? 'ies' : 'y') + ' ruled out")
    s = rep(s, "list = miss.slice(0, 600).map(function (v) { return G.inFamily(v, fam) ? '<b>' + group(v) + '</b>' : group(v); })", "list = miss.slice(0, 600).map(function (v) { return ruled(v) ? '<b>' + group(v) + '</b>' : group(v); })")
    # e. four numbers with every sign turned
    s = rep(s, "    if (q.some(function (x) { return Math.abs(x) > 1e6; }) || !G.isDescartes(q)) { $('tsay').innerHTML = 'Those four do not satisfy Descartes’s equation' + (q.some(function (x) { return Math.abs(x) > 1e6; }) ? ' (or are too large for this page)' : '') + ', so they are not the numbers of four circles that all touch. Try −11, 21, 24, 28 or −6, 11, 14, 15.'; return; }\n",
               "    var big = q.some(function (x) { return Math.abs(x) > 1e6; }), s4 = q[0] + q[1] + q[2] + q[3], eq = !big && s4 * s4 === 2 * (q[0] * q[0] + q[1] * q[1] + q[2] * q[2] + q[3] * q[3]);                 /* the equation as the caption prints it; four circles need a sum above nought as well */\n"
               "    if (big || !G.isDescartes(q)) { $('tsay').innerHTML = eq && s4 < 0 ? 'Those four satisfy the equation, but with every sign the wrong way round: of four circles that touch, at most one has a minus. Try ' + q.map(function (x) { return x > 0 ? '−' + x : String(-x); }).join(', ') + '.' : eq ? 'Four noughts are not four circles. Try −11, 21, 24, 28 or −6, 11, 14, 15.' :\n"
               "      'Those four do not satisfy Descartes’s equation' + (big ? ' (or are too large for this page)' : '') + ', so they are not the numbers of four circles that all touch. Try −11, 21, 24, 28 or −6, 11, 14, 15.'; return; }\n")
    # f, g, h. the caption, the history, the notes
    s = rep(s, "The rest (<b>blue</b>) come to an end: past the last blue mark,", "The rest (<b>blue</b>) seem to come to an end: past the last blue mark,")
    s = rep(s, "<p>For twenty years the guess was that every number that passes the test turns up, once the numbers are large enough. In 2023 four mathematicians", "<p>The guess, first made in 2003 and revised in 2011, was that every number that passes the test turns up, once the numbers are large enough. In 2023 four mathematicians")
    s = rep(s, "(Annals of Mathematics 200, 2024). The conjecture they overturned", "(Annals of Mathematics 200, 2024; arXiv 2307.02749). The conjecture they overturned")
    s = rep(s, "and are the same, number for number, as the lists the paper's authors have published.", "and are the same, number for number, as the lists in the authors' own files, which their paper names.")
    s = rep(s, "(the authors looked at least a hundred times further)", "(the authors looked at least a hundred times further, by their paper as it stands on arXiv)")
    # i. which families the theorem does not rule out
    s = rep(s, "'The theorem of 2023 rules out no family of squares in it.'", "'The theorem of 2023 does not rule out the squares in it, nor twice, three times or six times a square.'")
    s = rep(s, "'The paper’s theorem rules out no family of squares in it. '", "'The paper’s theorem does not rule out the squares in it, nor twice, three times or six times a square. '")
    # a look says that it is looking: a million takes a second at a desk and several on a phone
    s = rep(s, "  $('try').addEventListener('click', look); $('quad').addEventListener('keydown', function (e) { if (e.key === 'Enter') look(); });",
               "  function lookSoon() { $('tsay').textContent = 'Looking through the circles\\u2026'; $('show').disabled = true; setTimeout(look, 30); }      /* the words are painted before the work begins */\n"
               "  $('try').addEventListener('click', lookSoon); $('quad').addEventListener('keydown', function (e) { if (e.key === 'Enter') lookSoon(); });")
    open(P, 'w', encoding='utf-8').write(s); open(os.path.join(HERE, 'out27', 'page.src.stage7.html.txt'), 'w', encoding='utf-8').write(s)
    print('page.src.html: stage 7,', len(s), 'characters')
if __name__ == '__main__':
    main()
