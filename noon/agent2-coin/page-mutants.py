"""page-mutants.py: break the page's own script on purpose, one fault at a time, build each broken page and run
the headless test on it. First a control: the true page must pass with all its assertions, or "caught" would
mean nothing (a test that cannot start also "fails").      python -I page-mutants.py
The test is run from ~/web, where playwright is."""
import os, json, shutil, subprocess, sys, re
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.join(HERE, 'mutants-page'); WEB = os.path.expanduser('~/web')
rd = lambda n: open(os.path.join(HERE, n), encoding='utf-8').read()
SRC = rd('page.src.html'); CORE = rd('pcore.js'); BEST = json.dumps(json.loads(rd('best.json')), separators=(',', ':'))
M = [
 ('tile-one-way-shows-greedy', "tile('tile-plain', costText(tp, L), false,", "tile('tile-plain', costText(tg, L), false,"),
 ('tile-worst-of-the-other-count', "'coins on average; ' + P.worst(S.plain) + ' at worst.", "'coins on average; ' + P.worst(S.both) + ' at worst."),
 ('tile-bound-of-the-other-count', "could cost less than ' + costText(P.bound(D, L, 'plain'), L) + '.');\n    else { n = cannot(S.plain);", "could cost less than ' + costText(P.bound(D, L, 'both'), L) + '.');\n    else { n = cannot(S.plain);"),
 ('tile-bound-for-one-coin-more', "var L = S.L, tp = P.total(S.plain), tg = P.total(S.greedy), tb = P.total(S.both), D = S.coins.length,", "var L = S.L, tp = P.total(S.plain), tg = P.total(S.greedy), tb = P.total(S.both), D = S.coins.length + 1,"),
 ('tile-greedy-judged-by-what-is-drawn', "pf === 0 ? 'Always the fewest coins, for every amount however large.' :", "fails.length === 0 ? 'Always the fewest coins, for every amount however large.' :"),
 ('tile-greedy-first-failure-is-last', "first at ' + fails[0] + ': ' + wayText(P.greedyWay(S.coins, fails[0]))", "first at ' + fails[fails.length - 1] + ': ' + wayText(P.greedyWay(S.coins, fails[0]))"),
 ('picture-both-line-is-one-way', "d = stepPath(L, function (i) { return fin(S.both[i]) ? S.both[i] : null; }, f.X, f.Y, 0);", "d = stepPath(L, function (i) { return fin(S.plain[i]) ? S.plain[i] : null; }, f.X, f.Y, 0);"),
 ('picture-one-place-to-the-right', "if (!open) { d += 'M' + (X(a + x0) - half).toFixed(2) + ',' + Y(v).toFixed(2); open = true; }\n      else d += 'V' + Y(v).toFixed(2);\n      d += 'H' + (X(a + x0) + half).toFixed(2);",
    "if (!open) { d += 'M' + (X(a + x0 + 1) - half).toFixed(2) + ',' + Y(v).toFixed(2); open = true; }\n      else d += 'V' + Y(v).toFixed(2);\n      d += 'H' + (X(a + x0 + 1) + half).toFixed(2);"),
 ('picture-no-gap-where-it-cannot', "if (v === null) { open = false; continue; }", "if (v === null) { continue; }"),
 ('picture-axis-labels-one-out', "svg.appendChild(el('text', { x: BOX.l - 6, y: py + 4, 'text-anchor': 'end' }, String(Math.round(v * 100) / 100)));", "svg.appendChild(el('text', { x: BOX.l - 6, y: py + 4, 'text-anchor': 'end' }, String(Math.round(v * 100) / 100 + 1)));"),
 ('picture-top-cut-off', "f = frame(svg, -0.5, L - 0.5, 0, top, 'amount', 'coins', true);", "f = frame(svg, -0.5, L - 0.5, 0, top - 1, 'amount', 'coins', true);"),
 ('picture-labels-run-off', "var BOX = { l: 44, r: 112, t: 26, b: 34, W: 1000, H: 300 };", "var BOX = { l: 44, r: 112, t: 26, b: 34, W: 1070, H: 300 };"),
 ('rings-at-the-fewest-count', "f.g.appendChild(el('circle', { cx: f.X(a).toFixed(2), cy: f.Y(S.greedy[a]).toFixed(2),", "f.g.appendChild(el('circle', { cx: f.X(a).toFixed(2), cy: f.Y(S.plain[a]).toFixed(2),"),
 ('rings-where-greedy-ties', "for (a = 0; a < L; a++) if (fin(S.greedy[a]) && fin(S.plain[a]) && S.greedy[a] > S.plain[a]) {", "for (a = 0; a < L; a++) if (fin(S.greedy[a]) && fin(S.plain[a]) && S.greedy[a] >= S.plain[a] && a % 7 === 3) {"),
 ('table-greedy-column-is-one-way', "'</td><td>' + c(S.greedy[a]) + '</td><td>' + c(S.both[a]) + '</td></tr>';", "'</td><td>' + c(S.plain[a]) + '</td><td>' + c(S.both[a]) + '</td></tr>';"),
 ('add-both-ways-tries-too-few', "S.addBoth = P.bestAdd(S.coins, S.L, 'both', 2 * S.L - 1);", "S.addBoth = P.bestAdd(S.coins, S.L, 'both', S.L - 1);"),
 ('add-one-way-is-greedy', "S.addPlain = P.bestAdd(S.coins, S.L, 'plain', S.L - 1);", "S.addPlain = P.bestAdd(S.coins, S.L, 'greedy', S.L - 1);"),
 ('add-cost-over-one-amount-fewer', "S.addPlain.forEach(function (e) { if (isFinite(e.total)) one[e.coin] = e.total / L; });", "S.addPlain.forEach(function (e) { if (isFinite(e.total)) one[e.coin] = e.total / (L - 1); });"),
 ('add-sentence-names-one-of-the-best', "function names(list) { return list.map(function (e) { return e.coin; }).join(' or '); }", "function names(list) { return String(list[0].coin); }"),
 ('add-rings-only-one-way', "    bb.forEach(function (e) { f.g.appendChild(el('circle', { cx: f.X(e.coin), cy: f.Y(e.total / L), r: 4.5, fill: '#1a1a19', stroke: '#f0efec', 'stroke-width': 1.5, 'class': 'bestmark' })); });\n", ""),
 ('add-button-takes-the-last-of-the-best', "$('addPlain').addEventListener('click', function () { var b = helping(S.addPlain, P.total(S.plain)); if (b.length) setCoinage(S.coins.concat([b[0].coin])", "$('addPlain').addEventListener('click', function () { var b = helping(S.addPlain, P.total(S.plain)); if (b.length) setCoinage(S.coins.concat([b[b.length - 1].coin])"),
 ('add-both-button-adds-the-one-way-coin', "$('addBoth').addEventListener('click', function () { var b = helping(S.addBoth, P.total(S.both));", "$('addBoth').addEventListener('click', function () { var b = helping(S.addPlain, P.total(S.plain));"),
 ('add-tooltip-one-way-for-large-coins', "(c <= L - 1 ? 'one way ' + (o === null", "(c <= 2 * L ? 'one way ' + (o === null"),
 ('add-coin-there-not-said', "if (S.coins.indexOf(c) >= 0) return 'A coin of <b>' + c + '</b> is already there.';\n    return 'With a coin", "return 'With a coin"),
 ('settle-handed-back-drawn-as-over', "(back.length ? '<span class=\"sep\"></span><span class=\"lab\">handed back</span>' + coinsHtml(back, 'back') : '')", "(back.length ? '<span class=\"sep\"></span><span class=\"lab\">handed back</span>' + coinsHtml(back, 'over') : '')"),
 ('settle-shows-eleven', "s = P.schemes(S.coins, a, 12, 3000000); shown = s.ways.length;", "s = P.schemes(S.coins, a, 11, 3000000); shown = s.ways.length;"),
 ('settle-gave-up-not-said', "(s.gaveUp ? 'more ways than I counted' : '<b>' + plural(s.total, 'way') + '</b>')", "('<b>' + plural(s.total, 'way') + '</b>')"),
 ('settle-greedy-row-hidden', "if (fin(p) && (!fin(g) || g > p)) h +=", "if (fin(p) && (!fin(g) || g > p + 1)) h +="),
 ('settle-draws-every-coin', "if (shown >= 40) return h +", "if (shown >= 4000) return h +"),
 ('settle-zero-draws-ways', "if (a === 0) { $('ways').innerHTML = '<div class=\"way\"><p class=\"k\">Nothing to settle: <b>no coins</b>.</p></div>'; return; }\n", ""),
 ('tooltip-speaks-of-greedy-always', "if (fin(g) && fin(p) && g > p) out.push('greedy <b>'", "if (fin(g) && fin(p) && g >= p) out.push('greedy <b>'"),
 ('tooltip-over-and-back-swapped', "var over = w.filter(function (e) { return e[1] > 0; }), back = w.filter(function (e) { return e[1] < 0; }).map(function (e) { return [e[0], -e[1]]; });\n    return (over.length",
    "var back = w.filter(function (e) { return e[1] > 0; }), over = w.filter(function (e) { return e[1] < 0; }).map(function (e) { return [e[0], -e[1]]; });\n    return (over.length"),
 ('tooltip-runs-off-the-figure', "tip.style.left = Math.max(4, Math.min(fig.width - tip.offsetWidth - 4, x + 12)) + 'px';\n    tip.style.top = (box.top - fig.top + 8) + 'px';\n    sayA(a);", "tip.style.left = (x + 12) + 'px';\n    tip.style.top = (box.top - fig.top + 8) + 'px';\n    sayA(a);"),
 ('click-one-amount-out', "A.addEventListener('click', function (e) { setAmount(amountAt(A, e, 0, S.L)); });", "A.addEventListener('click', function (e) { setAmount(amountAt(A, e, 0, S.L) + 1); });"),
 ('dotted-line-left-behind', "var pick = $('pickA'); if (pick && geoA) { pick.setAttribute('x1', geoA.f.X(a)); pick.setAttribute('x2', geoA.f.X(a)); }", ""),
 ('arrow-key-steps-two', "if (e.key === 'ArrowRight') { hoverA(Math.min(S.L - 1, a + 1)); e.preventDefault(); }", "if (e.key === 'ArrowRight') { hoverA(Math.min(S.L - 1, a + 2)); e.preventDefault(); }"),
 ('amount-not-brought-inside', "    if (S.amount > S.L - 1) S.amount = S.L - 1;\n  }\n  function cannot(t)", "  }\n  function cannot(t)"),
 ('read-takes-coins-too-large', "if (v < 1 || v > MAXCOIN) return", "if (v < 1) return"),
 ('read-takes-seventeen', "if (out.length > MAXCOINS) return", "if (out.length > MAXCOINS + 1) return"),
 ('read-keeps-repeats', "if (!seen[v]) { seen[v] = 1; out.push(v); }", "out.push(v);"),
 ('read-takes-any-range', "if (v < 2 || v > MAXL) return", "if (v < 1 || v > 9000) return"),
 ('notice-not-cleared', "    notice(''); redraw();\n", "    redraw();\n"),
 ('refused-entry-still-counted', "if (c.error) { notice(c.error); return; }", "if (c.error) { notice(c.error); c = { coins: [1] }; }"),
 ('listed-coinage-chosen-whatever-the-range', "PRESETS.forEach(function (p, i) { if (p.L === l.L && p.coins.join() === c.coins.join()) same = i; });", "PRESETS.forEach(function (p, i) { if (p.coins.join() === c.coins.join()) same = i; });"),
 ('best-table-cost-is-the-bound', "h += '<tr><td>' + D + '</td><td class=\"l\">' + btns(p) + '</td><td>' + costText(p.total, BEST.L) + '</td><td>' + costText(p.bound, BEST.L) + '</td>'", "h += '<tr><td>' + D + '</td><td class=\"l\">' + btns(p) + '</td><td>' + costText(p.bound, BEST.L) + '</td><td>' + costText(p.bound, BEST.L) + '</td>'"),
 ('best-table-keeps-the-range', "setCoinage(t.getAttribute('data-set').split(',').map(Number), BEST.L);", "setCoinage(t.getAttribute('data-set').split(',').map(Number), S.L);"),
 ('best-table-both-ways-bound-one-way', "(b ? '<td class=\"l\">' + btns(b) + '</td><td>' + costText(b.total, BEST.L) + '</td><td>' + costText(b.bound, BEST.L) + '</td>'", "(b ? '<td class=\"l\">' + btns(b) + '</td><td>' + costText(b.total, BEST.L) + '</td><td>' + costText(p.bound, BEST.L) + '</td>'"),
 ('table-button-does-not-open', "$(tab).className = 'tables' + (on ? ' on' : '');", "$(tab).className = 'tables';"),
 ('best-coin-named-though-it-helps-nothing', "return b.length && (!isFinite(now) || b[0].total < now) ? b : []; }", "return b; }"),
 ('no-coin-left-not-said', "else if (!S.addPlain.length) out.push('One way there is no coin left to try: every value up to ' + (L - 1) + ' is a coin already.');\n", ""),
 ('amount-box-not-put-back', "    $('amount').addEventListener('change', function () { $('amount').value = S.amount; });      /* an entry that is no amount is put back */\n", ""),
 ('first-makeable-coin-not-best', "return b.length && (!isFinite(now) || b[0].total < now) ? b : []; }", "return b.length && isFinite(now) && b[0].total < now ? b : []; }"),
 ('seventeenth-coin-offered', "$('addPlain').disabled = bp.length === 0 || S.coins.length >= MAXCOINS;", "$('addPlain').disabled = bp.length === 0;"),
]
def build(name, old, new):
    d = os.path.join(WORK, name); os.makedirs(d, exist_ok=True); s = SRC
    if old is not None:
        if s.count(old) != 1: raise SystemExit('mutant %s: pattern found %d times' % (name, s.count(old)))
        s = s.replace(old, new)
    open(os.path.join(d, 'change.html'), 'w', encoding='utf-8').write(s.replace('/*CORE*/', CORE).replace('/*BEST*/null', BEST))
    return d
def run(d):
    env = dict(os.environ, LD_LIBRARY_PATH=os.path.join(WEB, 'sysroot/usr/lib/x86_64-linux-gnu'))
    try:
        r = subprocess.run(['node', 'shot-change.js', os.path.join(d, 'change.html'), d, os.path.join(HERE, 'pcore.js')], cwd=WEB, env=env, capture_output=True, text=True, timeout=900)
    except subprocess.TimeoutExpired:
        return None, ['TIMEOUT']
    m = re.search(r'PAGE TEST: (\d+) assertions, (\d+) failed', r.stdout)
    return (m.groups() if m else None), [l[8:] for l in r.stdout.split('\n') if l.startswith('FAILED: ')] + ([] if m else [(r.stderr.strip().split('\n') or [''])[0][:160]])
if os.path.isdir(WORK): shutil.rmtree(WORK)
res, fails = run(build('CONTROL', None, None))
print('control (the true page): %s' % ('%s assertions, %s failed' % res if res else 'THE TEST DID NOT FINISH: ' + '; '.join(fails)))
if not res or res[1] != '0': sys.exit('the control does not pass; nothing below would mean anything')
dirs = [(name, build(name, old, new)) for name, old, new in M]
with ThreadPoolExecutor(max_workers=6) as ex: out = list(ex.map(lambda nd: (nd[0],) + run(nd[1]), dirs))
caught = 0; passed = []; crashed = []
for name, res, fails in out:
    if res is None: caught += 1; crashed.append(name); print('caught   %-40s the test could not finish: %s' % (name, (fails[0] if fails else '')[:120]))
    elif res[1] != '0': caught += 1; print('caught   %-40s by %s: %s' % (name, res[1], fails[0][:120]))
    else: passed.append(name); print('PASSED   %s' % name)
print('\n%d of %d broken pages caught (%d of them because the test could not finish: %s); passed: %s' % (caught, len(M), len(crashed), ', '.join(crashed) or 'none', ', '.join(passed) or 'none'))
