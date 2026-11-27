"""Second stage of the coin page's remake: the script.   python -I remake2.py   (reads out27/stage1.html, writes page.src.html)"""
H = '/home/agent2/coin/'
if __name__ == '__main__':
    s = open(H + 'out27/stage1.html', encoding='utf8').read()
    def rep(a, b, count=1):
        global s
        assert s.count(a) == count, (a[:90], s.count(a)); s = s.replace(a, b)
    def between(a, b, new):
        global s
        i = s.index(a); j = s.index(b, i); assert s.count(a) == 1, a; s = s[:i] + new + s[j:]
    rep('<label>The coins of <select id="preset"></select></label>', '<label>Choose coins <select id="preset"></select></label>')
    between("  var PRESETS = [", "  var MAXCOIN = 5000", """  var PRESETS = [
    { name: 'United States: 1, 5, 10, 25', coins: [1, 5, 10, 25], L: 100 },
    { name: "Shallit's: 1, 5, 18, 25", coins: [1, 5, 18, 25], L: 100 },
    { name: 'the euro: 1, 2, 5, 10, 20, 50, 100, 200', coins: [1, 2, 5, 10, 20, 50, 100, 200], L: 100 },
    { name: 'United States with 50 and 100', coins: [1, 5, 10, 25, 50, 100], L: 100 },
    { name: 'Britain before 1971, in pence', coins: [1, 3, 6, 12, 24, 30], L: 240 },
    { name: 'Canada, to 5 dollars', coins: [1, 5, 10, 25, 100, 200], L: 500 },
    { name: 'powers of two', coins: [1, 2, 4, 8, 16, 32, 64], L: 100 },
    { name: 'powers of three', coins: [1, 3, 9, 27, 81], L: 100 },
    { name: 'best three with change: 16, 19, 21', coins: [16, 19, 21], L: 100 },
    { name: 'a best four with change: 19, 20, 23, 32', coins: [19, 20, 23, 32], L: 100 },
    { name: 'best five, fewest coins: 1, 5, 16, 23, 33', coins: [1, 5, 16, 23, 33], L: 100 }
  ];
""")
    rep("amount: 38, plain: null, greedy: null, both: null, addPlain: null, addBoth: null, hoverA: -1, hoverB: -1, notice: '' };",
        "amount: 24, plain: null, greedy: null, both: null, addPlain: null, addBoth: null, hoverA: -1, hoverB: -1, pickB: -1, notice: '' };")
    rep("    if (S.amount > S.L - 1) S.amount = S.L - 1;\n  }", "    if (S.amount > S.L - 1) S.amount = S.L - 1;\n    S.pickB = -1;\n  }")
    between("  function drawTiles() {", "  /* ---------- drawing helpers ---------- */", """  function drawTiles() {
    var L = S.L, tp = P.total(S.plain), tg = P.total(S.greedy), tb = P.total(S.both), has1 = S.coins[0] === 1, fails, pf, n;
    $('capA').textContent = 'The coins for each amount from 0 to ' + (L - 1);
    if (isFinite(tp)) tile('tile-plain', costText(tp, L), false, 'coins on average; ' + P.worst(S.plain) + ' at worst.');
    else { n = cannot(S.plain); tile('tile-plain', 'cannot make ' + plural(n, 'amount'), true, 'of the ' + (L - 1) + ' from 1 to ' + (L - 1) + (has1 ? '.' : ': there is no coin of 1.')); }
    if (!has1) {
      n = cannot(S.greedy);
      tile('tile-greedy', 'gets stuck at ' + plural(n, 'amount'), true, 'Without a coin of 1 the cashier cannot finish every amount.');
    } else {
      fails = P.greedyFails(S.coins, L); pf = P.pearson(S.coins);
      tile('tile-greedy', costText(tg, L), false, pf === 0 ? 'With these coins the cashier never takes more than the fewest, however large the amount.' :
        (fails.length ? 'More than the fewest for ' + plural(fails.length, 'amount') + ' here, first at ' + fails[0] + ': ' + wayText(P.greedyWay(S.coins, fails[0])) + ' against ' + wayText(P.plainWay(S.coins, fails[0])) + '.' :
          'The fewest for every amount here, but not for ' + pf + ': ' + wayText(P.greedyWay(S.coins, pf)) + ' against ' + wayText(P.plainWay(S.coins, pf)) + '.'));
    }
    if (isFinite(tb)) tile('tile-both', costText(tb, L), false, 'coins changing hands on average; ' + P.worst(S.both) + ' at worst.');
    else { n = cannot(S.both); tile('tile-both', 'cannot make ' + plural(n, 'amount'), true, 'even with change: every coin is a multiple of ' + S.coins.reduce(P.gcd) + '.'); }
  }

""")
    between("  var BOX = { l: 44", "  /* a stepped line through", """  /* The pictures are drawn at the size they are shown, so that their lettering is the size it says: on a narrow screen
     the frame is narrower and the names at the right-hand end of the lines are left to the legend beneath. */
  var BOX = { l: 44, r: 112, t: 26, b: 34, W: 1000, H: 300 };
  function fit() {
    var w = Math.round($('chartA').getBoundingClientRect().width) || 1000, narrow = w < 620;
    BOX = { W: Math.max(260, w), H: narrow ? 250 : 300, l: narrow ? 30 : 44, r: narrow ? 10 : 128, t: 26, b: 34, narrow: narrow };
  }
  function frame(svg, x0, x1, y0, y1, xlabel, ylabel, yInt) {
    var g, v, st, px, py;
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    svg.setAttribute('viewBox', '0 0 ' + BOX.W + ' ' + BOX.H);
    function X(x) { return BOX.l + (x - x0) / (x1 - x0) * (BOX.W - BOX.l - BOX.r); }
    function Y(y) { return BOX.H - BOX.b - (y - y0) / (y1 - y0) * (BOX.H - BOX.t - BOX.b); }
    st = niceStep(y1 - y0, 5); if (yInt && st < 1) st = 1;
    for (v = Math.ceil(y0 / st - 1e-9) * st; v <= y1 + 1e-9; v += st) {
      py = Y(v);
      svg.appendChild(el('line', { x1: BOX.l, x2: BOX.W - BOX.r, y1: py, y2: py, stroke: '#2c2c2a', 'stroke-width': 1 }));
      svg.appendChild(el('text', { x: BOX.l - 6, y: py + 4, 'text-anchor': 'end' }, String(Math.round(v * 100) / 100)));
    }
    st = niceStep(x1 - x0, BOX.narrow ? 5 : 10); if (st < 1) st = 1;
    for (v = Math.ceil(x0 / st) * st; v <= x1 + 1e-9; v += st) {
      px = X(v);
      svg.appendChild(el('line', { x1: px, x2: px, y1: BOX.H - BOX.b, y2: BOX.H - BOX.b + 4, stroke: '#383835', 'stroke-width': 1 }));
      svg.appendChild(el('text', { x: px, y: BOX.H - BOX.b + 17, 'text-anchor': 'middle' }, String(v)));
    }
    svg.appendChild(el('line', { x1: BOX.l, x2: BOX.W - BOX.r, y1: BOX.H - BOX.b, y2: BOX.H - BOX.b, stroke: '#383835', 'stroke-width': 1 }));
    svg.appendChild(el('text', { x: (BOX.l + BOX.W - BOX.r) / 2, y: BOX.H - 3, 'text-anchor': 'middle' }, xlabel));
    svg.appendChild(el('text', { x: 2, y: 12, 'text-anchor': 'start' }, ylabel));
    g = el('g', {}); svg.appendChild(g);
    return { X: X, Y: Y, g: g };
  }
""")
    between("  function endLabels(svg, items) {", "  function lastFinite(t)", """  function endLabels(svg, items) {           /* direct labels at the right, kept apart; on a narrow screen the legend does it */
    if (BOX.narrow) return;
    items = items.filter(function (i) { return i.y !== null; }).sort(function (p, q) { return p.y - q.y; });
    for (var i = 1; i < items.length; i++) if (items[i].y - items[i - 1].y < 15) items[i].y = items[i - 1].y + 15;
    items.forEach(function (it) {
      svg.appendChild(el('line', { x1: BOX.W - BOX.r + 6, x2: BOX.W - BOX.r + 16, y1: it.y, y2: it.y, stroke: it.color, 'stroke-width': 2.5 }));
      svg.appendChild(el('text', { x: BOX.W - BOX.r + 20, y: it.y + 4, 'text-anchor': 'start' }, it.text));
    });
  }
""")
    between("  function drawA() {", "  function hoverA(a, evt) {", """  function drawA() {
    var svg = $('chartA'), L = S.L, top = 1, a, f, d, fails, per;
    for (a = 0; a < L; a++) { if (fin(S.plain[a]) && S.plain[a] > top) top = S.plain[a]; if (fin(S.both[a]) && S.both[a] > top) top = S.both[a]; if (fin(S.greedy[a]) && S.greedy[a] > top) top = S.greedy[a]; }
    f = frame(svg, -0.5, L - 0.5, 0, top, 'amount', 'coins', true); geoA = { f: f, top: top }; per = f.X(1) - f.X(0);      /* pixels to an amount */
    d = stepPath(L, function (i) { return fin(S.plain[i]) ? S.plain[i] : null; }, f.X, f.Y, 0);
    f.g.appendChild(el('path', { d: d, fill: 'none', stroke: '#3987e5', 'stroke-width': per >= 7 ? 4.5 : per >= 4 ? 3.5 : 2.5, 'stroke-linejoin': 'round', id: 'lineA-plain' }));
    d = stepPath(L, function (i) { return fin(S.both[i]) ? S.both[i] : null; }, f.X, f.Y, 0);
    f.g.appendChild(el('path', { d: d, fill: 'none', stroke: '#d95926', 'stroke-width': per >= 4 ? 2 : 1.2, 'stroke-linejoin': 'round', id: 'lineA-both' }));
    fails = 0;
    for (a = 0; a < L; a++) if (fin(S.greedy[a]) && fin(S.plain[a]) && S.greedy[a] > S.plain[a]) {
      fails++;
      f.g.appendChild(el('circle', { cx: f.X(a).toFixed(2), cy: f.Y(S.greedy[a]).toFixed(2), r: per >= 7 ? 4 : per >= 2.5 ? 3 : 2.5, fill: '#1a1a19', stroke: '#f0efec', 'stroke-width': 1.5, 'class': 'failmark' }));
    }
    endLabels(svg, [
      { y: lastFinite(S.plain) === null ? null : f.Y(lastFinite(S.plain)), color: '#3987e5', text: 'fewest coins' },
      { y: lastFinite(S.both) === null ? null : f.Y(lastFinite(S.both)), color: '#d95926', text: 'with change' }]);
    f.g.appendChild(el('line', { id: 'crossA', x1: 0, x2: 0, y1: BOX.t, y2: BOX.H - BOX.b, stroke: '#c3c2b7', 'stroke-width': 1, visibility: 'hidden' }));
    f.g.appendChild(el('line', { id: 'pickA', x1: f.X(S.amount), x2: f.X(S.amount), y1: BOX.t, y2: BOX.H - BOX.b, stroke: '#898781', 'stroke-width': 1, 'stroke-dasharray': '2 3' }));
    svg.setAttribute('aria-label', 'Number of coins for each amount from 0 to ' + (L - 1) + ', with the fewest coins and with change' + (fails ? '; the cashier\\'s way takes more at ' + plural(fails, 'amount') : ''));
    sayA(S.amount);
    fillTableA();
  }
  function describe(a) {
    var p = S.plain[a], g = S.greedy[a], b = S.both[a], out = [], s;
    out.push(fin(p) ? 'fewest coins <b>' + p + '</b>' + (a > 0 ? ' (' + esc(wayText(P.plainWay(S.coins, a))) + ')' : '') : 'paid exactly: cannot be made');
    if (fin(g) && fin(p) && g > p) out.push('the cashier\\'s way <b>' + g + '</b> (' + esc(wayText(P.greedyWay(S.coins, a))) + ')');
    else if (!fin(g) && fin(p)) out.push('the cashier gets stuck');
    if (fin(b)) {
      s = a > 0 ? P.schemes(S.coins, a, 1, 200000) : null;
      out.push('with change <b>' + b + '</b>' + (s && s.ways.length ? ' (' + esc(schemeText(s.ways[0])) + ')' : ''));
    } else out.push('with change: cannot be made');
    return out;
  }
  function sayA(a) { $('sayA').innerHTML = 'Amount <b>' + a + '</b>: ' + describe(a).join('; ') + '.' + (a === S.amount ? '' : ' Tap the picture to pay it above.'); }
""")
    between("  function fillTableA() {", "  /* ---------- picture B", """  function fillTableA() {
    var h = '<table><tr><th>amount</th><th>fewest coins</th><th>the cashier\\'s way</th><th>with change</th></tr>', a;
    function c(v) { return fin(v) ? v : 'cannot'; }
    for (a = 0; a < S.L; a++) h += '<tr><td>' + a + '</td><td>' + c(S.plain[a]) + '</td><td>' + c(S.greedy[a]) + '</td><td>' + c(S.both[a]) + '</td></tr>';
    $('tabA').innerHTML = h + '</table>';
  }

""")
    open(H + 'out27/stage2a.html', 'w', encoding='utf8').write(s); print('stage 2a:', len(s))
