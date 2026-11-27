"""Third stage of the coin page's remake: the coin to add, the rings, the best sets, the handlers.   python -I remake3.py
(reads out27/stage2a.html, writes page.src.html)"""
H = '/home/agent2/coin/'
if __name__ == '__main__':
    s = open(H + 'out27/stage2a.html', encoding='utf8').read()
    def rep(a, b, count=1):
        global s
        assert s.count(a) == count, (a[:90], s.count(a)); s = s.replace(a, b)
    def between(a, b, new):
        global s
        assert s.count(a) == 1, a; i = s.index(a); j = s.index(b, i); s = s[:i] + new + s[j:]
    rep(" + (a === S.amount ? '' : ' Tap the picture to pay it above.'); }", "; }")
    between("  function drawB() {", "  function hoverB(c) {", """  function drawB() {
    var svg = $('chartB'), L = S.L, n = 2 * L - 1, one = new Array(n + 1), two = new Array(n + 1), i, lo = Infinity, hi = -Infinity, f, d, tp = P.total(S.plain), tb = P.total(S.both), bp, bb, labels = [], full = S.coins.length >= MAXCOINS;
    for (i = 0; i <= n; i++) { one[i] = null; two[i] = null; }
    S.addPlain.forEach(function (e) { if (isFinite(e.total)) one[e.coin] = e.total / L; });
    S.addBoth.forEach(function (e) { if (isFinite(e.total)) two[e.coin] = e.total / L; });
    for (i = 1; i <= n; i++) { [one[i], two[i]].forEach(function (v) { if (v !== null) { if (v < lo) lo = v; if (v > hi) hi = v; } }); }
    if (isFinite(tp)) { hi = Math.max(hi, tp / L); lo = Math.min(lo, tp / L); } if (isFinite(tb)) { hi = Math.max(hi, tb / L); lo = Math.min(lo, tb / L); }
    if (!isFinite(lo)) { lo = 0; hi = 1; }
    if (hi - lo < 0.5) hi = lo + 0.5;
    lo = Math.max(0, lo - (hi - lo) * 0.12); hi = hi + (hi - lo) * 0.04;
    f = frame(svg, 0.5, n + 0.5, lo, hi, 'value of the new coin', 'average', false); geoB = { f: f, n: n, one: one, two: two };
    if (isFinite(tp)) f.g.appendChild(el('line', { x1: BOX.l, x2: BOX.W - BOX.r, y1: f.Y(tp / L), y2: f.Y(tp / L), stroke: '#898781', 'stroke-width': 1.5, 'stroke-dasharray': '4 3' }));
    if (isFinite(tb)) f.g.appendChild(el('line', { x1: BOX.l, x2: BOX.W - BOX.r, y1: f.Y(tb / L), y2: f.Y(tb / L), stroke: '#898781', 'stroke-width': 1.5, 'stroke-dasharray': '4 3' }));
    d = stepPath(n, function (k) { return one[k + 1]; }, f.X, f.Y, 1);
    f.g.appendChild(el('path', { d: d, fill: 'none', stroke: '#3987e5', 'stroke-width': 2, 'stroke-linejoin': 'round', id: 'lineB-plain' }));
    d = stepPath(n, function (k) { return two[k + 1]; }, f.X, f.Y, 1);
    f.g.appendChild(el('path', { d: d, fill: 'none', stroke: '#d95926', 'stroke-width': 2, 'stroke-linejoin': 'round', id: 'lineB-both' }));
    bp = helping(S.addPlain, tp); bb = helping(S.addBoth, tb);
    bp.forEach(function (e) { f.g.appendChild(el('circle', { cx: f.X(e.coin), cy: f.Y(e.total / L), r: 4.5, fill: '#1a1a19', stroke: '#f0efec', 'stroke-width': 1.5, 'class': 'bestmark' })); });
    bb.forEach(function (e) { f.g.appendChild(el('circle', { cx: f.X(e.coin), cy: f.Y(e.total / L), r: 4.5, fill: '#1a1a19', stroke: '#f0efec', 'stroke-width': 1.5, 'class': 'bestmark' })); });
    if (isFinite(tp)) labels.push({ y: f.Y(tp / L), color: '#3987e5', text: 'fewest coins now' });
    if (isFinite(tb)) labels.push({ y: f.Y(tb / L), color: '#d95926', text: 'with change now' });
    endLabels(svg, labels);
    f.g.appendChild(el('line', { id: 'crossB', x1: 0, x2: 0, y1: BOX.t, y2: BOX.H - BOX.b, stroke: '#c3c2b7', 'stroke-width': 1, visibility: 'hidden' }));
    f.g.appendChild(el('line', { id: 'pickB', x1: 0, x2: 0, y1: BOX.t, y2: BOX.H - BOX.b, stroke: '#898781', 'stroke-width': 1, 'stroke-dasharray': '2 3', visibility: 'hidden' }));
    $('addPlain').disabled = bp.length === 0 || full; $('addBoth').disabled = bb.length === 0 || full;
    sayB(-1);
    fillTableB();
  }
  /* "4 or 9 or 24"; of a long list the first four and how many more */
  function names(list) { var c = list.map(function (e) { return e.coin; }); return c.length <= 5 ? c.join(' or ') : c.slice(0, 4).join(', ') + ' or any of ' + (c.length - 4) + ' others'; }
  function summaryB() {
    var L = S.L, tp = P.total(S.plain), tb = P.total(S.both), bp = helping(S.addPlain, tp), bb = helping(S.addBoth, tb), out = [];
    if (S.coins.length >= MAXCOINS) out.push('There are ' + MAXCOINS + ' coins, which is as many as this page takes, so no more can be added.');
    if (bp.length) out.push('For the fewest coins the best coin to add is <b>' + names(bp) + '</b>, bringing the average ' + (isFinite(tp) ? 'from ' + costText(tp, L) + ' ' : '') + 'to <b>' + costText(bp[0].total, L) + '</b>.');
    else if (!S.addPlain.length) out.push('For the fewest coins there is no coin left to try: every value up to ' + (L - 1) + ' is a coin already.');
    else if (isFinite(tp)) out.push('For the fewest coins no single coin lowers the average of ' + costText(tp, L) + '.');
    else out.push('Paid exactly, no single coin lets every amount be made.');
    if (bb.length) out.push('With change it is <b>' + names(bb) + '</b>, ' + (isFinite(tb) ? 'from ' + costText(tb, L) + ' ' : '') + 'to <b>' + costText(bb[0].total, L) + '</b>.');
    else if (!S.addBoth.length) out.push('With change there is no coin left to try.');
    else if (isFinite(tb)) out.push('With change no single coin up to ' + (2 * L - 1) + ' lowers the average of ' + costText(tb, L) + '.');
    else out.push('With change no single coin up to ' + (2 * L - 1) + ' lets every amount be made.');
    return out.join(' ');
  }
  function coinLine(c) {
    var L = S.L, o = geoB.one[c], t = geoB.two[c];
    if (S.coins.indexOf(c) >= 0) return 'A coin of <b>' + c + '</b> is already there.';
    return 'With a coin of <b>' + c + '</b> added: ' + (c <= L - 1 ? 'fewest coins ' + (o === null ? 'cannot make every amount' : '<b>' + costText(Math.round(o * L), L) + '</b>') + '; ' : '') +
      'with change ' + (t === null ? 'cannot make every amount' : '<b>' + costText(Math.round(t * L), L) + '</b>') + '.';
  }
  function sayB(c) { $('sayB').innerHTML = c < 1 ? summaryB() : coinLine(c) + ' ' + summaryB(); }
  function pickB(c) {                                  /* a tap on the picture keeps its coin's line under the picture */
    var pick = $('pickB'); S.pickB = c;
    if (pick) { if (c < 1) pick.setAttribute('visibility', 'hidden'); else { pick.setAttribute('x1', geoB.f.X(c)); pick.setAttribute('x2', geoB.f.X(c)); pick.setAttribute('visibility', 'visible'); } }
    sayB(c);
  }
""")
    rep("    if (c < 1) { cross.setAttribute('visibility', 'hidden'); tip.style.display = 'none'; sayB(-1); return; }", "    if (c < 1) { cross.setAttribute('visibility', 'hidden'); tip.style.display = 'none'; sayB(S.pickB); return; }")
    between("  function fillTableB() {", "  /* ---------- settle an amount", """  function fillTableB() {
    var L = S.L, h = '<table><tr><th>new coin</th><th>fewest coins</th><th>with change</th></tr>', c, o, t;
    for (c = 1; c <= geoB.n; c++) {
      if (S.coins.indexOf(c) >= 0) continue;
      o = geoB.one[c]; t = geoB.two[c];
      h += '<tr><td>' + c + '</td><td>' + (c > L - 1 ? '' : o === null ? 'cannot' : costText(Math.round(o * L), L)) + '</td><td>' + (t === null ? 'cannot' : costText(Math.round(t * L), L)) + '</td></tr>';
    }
    $('tabB').innerHTML = h + '</table>';
  }

""")
    between("  function drawWays() {", "  /* ---------- the table of best sets", """  function drawWays() {
    var a = S.amount, h = '', p = S.plain[a], g = S.greedy[a], b = S.both[a], s, i, w, over, back, shown;
    $('amount').value = a; $('amount').max = S.L - 1; $('amountR').max = S.L - 1; $('amountR').value = a;
    if (a === 0) { $('ways').innerHTML = '<div class="way"><p class="k">Nothing to pay: <b>no coins</b>.</p></div>'; return; }
    h += '<div class="way" id="way-plain"><p class="k">Fewest coins: ' + (fin(p) ? '<b>' + plural(p, 'coin') + '</b>' : '<b>cannot be paid exactly</b> with these coins') + '</p>' +
      (fin(p) ? '<div class="row">' + coinsHtml(P.plainWay(S.coins, a), 'over') + '</div>' : '') + '</div>';
    if (fin(p) && (!fin(g) || g > p)) h += '<div class="way" id="way-greedy"><p class="k">The cashier\\'s way, the largest coin that fits each time: ' + (fin(g) ? '<b>' + plural(g, 'coin') + '</b>, ' + (g - p) + ' more than need be' : '<b>gets stuck</b>') + '</p>' +
      (fin(g) ? '<div class="row">' + coinsHtml(P.greedyWay(S.coins, a), 'over') + '</div>' : '') + '</div>';
    else if (fin(p)) h += '<div class="way" id="way-greedy"><p class="k">The cashier\\'s way, the largest coin that fits each time: <b>the same count</b></p></div>';
    if (!fin(b)) h += '<div class="way" id="way-both"><p class="k">With change: <b>cannot be paid</b> even so</p></div>';
    else {
      s = P.schemes(S.coins, a, 12, 3000000); shown = s.ways.length;
      h += '<div class="way" id="way-both"><p class="k">With change: <b>' + plural(b, 'coin') + '</b> ' + (b === 1 ? 'changes' : 'change') + ' hands' +
        (s.gaveUp ? ' (there are more ways of doing it than I counted' : s.total === 1 ? '' : ' (it can be done in <b>' + s.total + '</b> ways') + (s.total > shown || s.gaveUp ? '; the first ' + shown + ' are shown)' : s.total === 1 ? '' : ')') + '</p>';
      for (i = 0; i < shown; i++) {
        w = s.ways[i]; over = w.filter(function (e) { return e[1] > 0; }); back = w.filter(function (e) { return e[1] < 0; }).map(function (e) { return [e[0], -e[1]]; });
        h += '<div class="row scheme">' + (over.length ? '<span class="grp"><span class="lab">handed over</span>' + coinsHtml(over, 'over') + '</span>' : '') +
          (back.length ? '<span class="grp"><span class="lab">handed back</span>' + coinsHtml(back, 'back') + '</span>' : '') + '</div>';
      }
      h += '</div>';
    }
    $('ways').innerHTML = h;
    var pick = $('pickA'); if (pick && geoA) { pick.setAttribute('x1', geoA.f.X(a)); pick.setAttribute('x2', geoA.f.X(a)); }
  }

""")
    between("  function drawBest() {", "  /* ---------- putting it together", """  function drawBest() {
    var head = '<tr><th>coins</th><th class="l">the best sets</th><th>average</th><th>least possible</th></tr>', hp = head, hb = head, D, p, b;
    function btns(r) { return r.sets.map(function (s) { return '<button class="setbtn" data-set="' + s.join(',') + '">' + s.join(', ') + '</button>'; }).join(''); }
    for (D = 1; D <= BEST.plain.length; D++) {
      p = BEST.plain[D - 1]; b = BEST.both[D - 1];
      hp += '<tr><td>' + D + '</td><td class="l">' + btns(p) + '</td><td>' + costText(p.total, BEST.L) + '</td><td>' + costText(p.bound, BEST.L) + '</td></tr>';
      hb += '<tr><td>' + D + '</td>' + (b ? '<td class="l">' + btns(b) + '</td><td>' + costText(b.total, BEST.L) + '</td><td>' + costText(b.bound, BEST.L) + '</td>' : '<td class="l">not searched</td><td></td><td>' + costText(P.bound(D, BEST.L, 'both'), BEST.L) + '</td>') + '</tr>';
    }
    $('best-plain').innerHTML = hp; $('best-both').innerHTML = hb;
  }

""")
    between("  function notice(msg) {", "  init();", """  function notice(msg) { S.notice = msg; var n = $('notice'); n.textContent = msg; n.className = 'notice' + (msg ? ' on' : ''); }
  function redraw() { compute(); fit(); drawTiles(); drawA(); drawWays(); drawB(); }
  function setCoinage(coins, L, keepPreset) {
    S.coins = coins.slice(); S.L = L;
    $('coins').value = coins.join(', '); $('L').value = L;
    if (!keepPreset) $('preset').value = 'own';
    notice(''); $('addedSay').textContent = ''; $('amountSay').textContent = ''; redraw();
  }
  function matchPreset() {
    var same = -1;
    PRESETS.forEach(function (p, i) { if (p.L === S.L && p.coins.join() === S.coins.join()) same = i; });
    $('preset').value = same >= 0 ? String(same) : 'own';
  }
  function still() { return ' The page still shows the coins ' + S.coins.join(', ') + (S.L === 100 ? '' : ' for amounts below ' + S.L) + '.'; }      /* what is typed has not been taken */
  function apply() {
    var c = readCoins($('coins').value), l = readL($('L').value);
    if (c.error) { notice(c.error + still()); return; }
    if (l.error) { notice(l.error + still()); return; }
    setCoinage(c.coins, l.L, true); matchPreset();
  }
  function setAmount(a) {
    if (!(a >= 0)) a = 0; if (a > S.L - 1) a = S.L - 1;
    S.amount = Math.floor(a); $('amountSay').textContent = ''; drawWays(); if (S.hoverA < 0) sayA(S.amount);
  }
  /* What a visitor has a finger on stays under the finger while the page above it changes its length. */
  function steady(elem, change) { var y = elem.getBoundingClientRect().top; change(); window.scrollBy(0, elem.getBoundingClientRect().top - y); }
  function addBest(list, now, which, btn) {
    var b = helping(list, now), before = now, L = S.L, coin, after;
    if (!b.length) return;
    coin = b[0].coin; after = b[0].total;
    steady(btn, function () { setCoinage(S.coins.concat([coin]).sort(function (x, y) { return x - y; }), L); matchPreset(); });
    $('addedSay').innerHTML = 'Added a <b>' + coin + '</b>. The coins are now ' + S.coins.join(', ') + ', and the average ' + which + ' ' + (isFinite(before) ? 'has gone from ' + costText(before, L) + ' to ' : 'is ') + '<b>' + costText(after, L) + '</b>.';
  }
  function init() {
    var sel = $('preset');
    PRESETS.forEach(function (p, i) { var o = document.createElement('option'); o.value = String(i); o.textContent = p.name; sel.appendChild(o); });
    var own = document.createElement('option'); own.value = 'own'; own.textContent = 'your own'; sel.appendChild(own);
    sel.addEventListener('change', function () { if (sel.value !== 'own') { var p = PRESETS[Number(sel.value)]; setCoinage(p.coins, p.L, true); } });
    $('apply').addEventListener('click', apply);
    $('coins').addEventListener('keydown', function (e) { if (e.key === 'Enter') apply(); });
    $('L').addEventListener('keydown', function (e) { if (e.key === 'Enter') apply(); });
    $('L').addEventListener('change', apply);
    $('amount').addEventListener('input', function () { if (/^\\d+$/.test($('amount').value)) setAmount(Number($('amount').value)); });
    $('amount').addEventListener('change', function () {                                    /* an entry that is no amount is put back, and the page says so */
      var typed = $('amount').value;
      if (String(typed) !== String(S.amount)) $('amountSay').textContent = (typed === '' ? 'That' : '"' + typed + '"') + ' is not a whole number from 0 to ' + (S.L - 1) + ': the amount is still ' + S.amount + '.';
      $('amount').value = S.amount;
    });
    $('amountR').addEventListener('input', function () { setAmount(Number($('amountR').value)); });
    var A = $('chartA'), B = $('chartB');
    A.addEventListener('pointermove', function (e) { if (e.pointerType === 'mouse') hoverA(amountAt(A, e, 0, S.L), e); });
    A.addEventListener('pointerleave', function () { hoverA(-1); });
    A.addEventListener('click', function (e) { var a = amountAt(A, e, 0, S.L); hoverA(-1); steady(A, function () { setAmount(a); }); });
    A.addEventListener('keydown', function (e) {
      var a = S.hoverA < 0 ? S.amount : S.hoverA;
      if (e.key === 'ArrowRight') { hoverA(Math.min(S.L - 1, a + 1)); e.preventDefault(); }
      else if (e.key === 'ArrowLeft') { hoverA(Math.max(0, a - 1)); e.preventDefault(); }
      else if (e.key === 'Enter' || e.key === ' ') { setAmount(a); e.preventDefault(); }
      else if (e.key === 'Escape') hoverA(-1);
    });
    A.addEventListener('blur', function () { hoverA(-1); });
    B.addEventListener('pointermove', function (e) { if (e.pointerType === 'mouse') hoverB(amountAt(B, e, 1, geoB.n)); });
    B.addEventListener('pointerleave', function () { hoverB(-1); });
    B.addEventListener('click', function (e) { hoverB(-1); pickB(amountAt(B, e, 1, geoB.n)); });
    B.addEventListener('keydown', function (e) {
      var c = S.hoverB < 1 ? (S.pickB < 1 ? 1 : S.pickB) : S.hoverB;
      if (e.key === 'ArrowRight') { hoverB(S.hoverB < 1 && S.pickB < 1 ? 1 : Math.min(geoB.n, c + 1)); e.preventDefault(); }
      else if (e.key === 'ArrowLeft') { hoverB(Math.max(1, c - 1)); e.preventDefault(); }
      else if (e.key === 'Enter' || e.key === ' ') { pickB(c); e.preventDefault(); }
      else if (e.key === 'Escape') hoverB(-1);
    });
    B.addEventListener('blur', function () { hoverB(-1); });
    function toggle(btn, tab) { $(btn).addEventListener('click', function () { var on = $(btn).getAttribute('aria-pressed') !== 'true'; $(btn).setAttribute('aria-pressed', on ? 'true' : 'false'); $(btn).textContent = on ? 'Hide the table' : 'Show the table'; $(tab).className = 'tables' + (on ? ' on' : ''); }); }
    toggle('tA', 'tabA'); toggle('tB', 'tabB');
    $('addPlain').addEventListener('click', function () { addBest(S.addPlain, P.total(S.plain), 'with the fewest coins', $('addPlain')); });
    $('addBoth').addEventListener('click', function () { addBest(S.addBoth, P.total(S.both), 'with change', $('addBoth')); });
    $('fig4').addEventListener('click', function (e) {
      var t = e.target; if (t && t.getAttribute && t.getAttribute('data-set')) { setCoinage(t.getAttribute('data-set').split(',').map(Number), BEST.L); matchPreset(); $('fig0').scrollIntoView({ block: 'start' }); }
    });
    [].forEach.call(document.querySelectorAll('button.inline'), function (b) { b.addEventListener('click', function () { steady(b, function () { setCoinage(b.getAttribute('data-set').split(',').map(Number), 100); matchPreset(); }); }); });
    var waiting = null, wide = 0;                                                             /* the pictures are drawn again when their width changes */
    window.addEventListener('resize', function () { clearTimeout(waiting); waiting = setTimeout(function () { var w = Math.round($('chartA').getBoundingClientRect().width); if (w !== wide) { wide = w; fit(); drawA(); drawB(); } }, 120); });
    drawBest();
    $('preset').value = '0';
    setCoinage(PRESETS[0].coins, PRESETS[0].L, true);
    wide = Math.round($('chartA').getBoundingClientRect().width);
  }
""")
    open(H + 'page.src.html', 'w', encoding='utf8').write(s); print('page.src.html written:', len(s))
