// Fork's own driving of the coordinator's page (read-only): node drive.js PAGE.html OUTDIR
'use strict';
const { chromium } = require('playwright'); const path = require('path');
const F = 360000n; const bmod = (a, m) => ((a % m) + m) % m; const bgcd = (a, b) => { while (b) { [a, b] = [b, a % b]; } return a < 0n ? -a : a; };
function theory(A, I) { const a = bmod(BigInt(A), F), i = bmod(BigInt(I), F); let q = 1n, p = 0n; if (i !== 0n) { const g = bgcd(i, F); q = F / g; p = i / g; }
  const TT = (q * a + 180000n * p * (q - 1n)) % F; if (TT === 0n) return { home: false, q: Number(q) }; return { home: true, q: Number(q), steps: Number(q * (F / bgcd(TT, F))) }; }
function lit(A, I, cap) { const FF = 360000, K = 2 * Math.PI / FF; const a0 = ((A % FF) + FF) % FF, inc = ((I % FF) + FF) % FF; let ang = a0, h = 0, x = 0, y = 0, home = 0, there = 0;
  for (let k = 1; k <= cap; k++) { x += Math.sin(h * K); y += Math.cos(h * K); h = (h + ang) % FF; ang = (ang + inc) % FF; if (Math.hypot(x, y) < 1e-9) { if (!there) there = k; if (h === 0 && ang === a0) { home = k; break; } } }
  return { home, there, x, y }; }
const th1000 = s => { const m = /^\s*([+-]?)(\d+)(?:\.(\d*))?\s*$/.exec(s); if (!m) return null; const v = Math.round(parseFloat(m[2] + '.' + (m[3] || '0')) * 1000); return m[1] === '-' ? -v : v; };
(async () => {
  const page = path.resolve(process.argv[2]), out = path.resolve(process.argv[3]);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1000, height: 1500 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + page); await p.waitForTimeout(500);
  const state = (pg) => (pg || p).evaluate(() => window.INSPISTATE());
  const typed = async (a, i, pg) => { await (pg || p).fill('#angle', a); await (pg || p).fill('#inc', i); };
  const once = async (pg) => { await (pg || p).selectOption('#pace', 'once'); await (pg || p).click('#go'); await (pg || p).waitForTimeout(150); return state(pg); };
  // what is really on the field canvas: dark line box, rust pixels in a 3 px band at the canvas edge, count of round rust dots is not attempted
  const px = (pg) => (pg || p).evaluate(() => { const c = document.getElementById('field'), d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let line = 0, x0 = 1e9, x1 = -1, y0 = 1e9, y1 = -1, edgeRust = 0, edgeDark = 0, rust = 0;
    for (let y = 0; y < c.height; y++) for (let x = 0; x < c.width; x++) { const i = 4 * (y * c.width + x), r = d[i], g = d[i + 1], bl = d[i + 2], a = d[i + 3]; const edge = x < 3 || y < 3 || x >= c.width - 3 || y >= c.height - 3;
      if (a > 90 && r < 100 && g < 90 && bl < 90) { line++; if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; if (edge) edgeDark++; }
      if (a > 40 && r > 130 && g < 110 && bl < 85) { rust++; if (edge) edgeRust++; } }
    return { line, x0, x1, y0, y1, w: c.width, h: c.height, edgeRust, edgeDark, rust }; });
  const guideOver = s => { const g = s.guide, v = s.view; if (!g || g.kind !== 'circle') return null; return Math.max(0 - (v.ox + v.k * (g.cx - g.r)), (v.ox + v.k * (g.cx + g.r)) - s.W, 0 - (v.oy - v.k * (g.cy + g.r)), (v.oy - v.k * (g.cy - g.r)) - s.H); };
  const log = (...a) => console.log(...a);
  // ---- A. turtles of my choosing, all at once
  const list = [['2', '20'], ['10', '20'], ['0', '7'], ['112', '135'], ['22', '135'], ['30', '180'], ['25', '210'], ['155', '2'], ['0', '180'], ['180', '180'], ['4', '8'], ['359', '359'], ['0', '1'], ['1', '1'],
    ['22.5', '45'], ['0.5', '1'], ['2', '22.5'], ['0', '0.1'], ['0', '0.333'], ['0.1', '0'], ['0.05', '180'], ['179.999', '0.002'], ['0', '0.001'], ['0.001', '0'], ['3.5', '7'], ['0', '0.036'], ['0.009', '0.018'],
    ['-10', '-20'], ['10', '-20'], ['-2', '20'], ['999999', '999999.999'], ['100000', '100000'], ['0', '0'], ['90', '0'], ['360', '0'], ['0', '360'], ['90', '360'], ['72', '0'], ['144', '0'],
    ['.5', '20'], ['−5', '20'], ['1234567', '20'], ['1e9', '20'], ['', '20'], ['5.', '+20'], ['2', '3600020']];
  let wrong = 0;
  for (const [a, i] of list) { await typed(a, i); const s0 = await state(); if (!s0.valid) { log('A.', JSON.stringify([a, i]), 'REFUSED | say:', s0.say, '| go disabled:', await p.isDisabled('#go')); continue; }
    const s = await once(), pix = await px(), A = th1000(a), I = th1000(i), th = theory(A, I); let verdict = [];
    if (th.home) { if (!s.say.includes('it comes home after ' + th.steps.toLocaleString('en-US') + ' steps')) verdict.push('FORECAST WRONG'); if (th.steps <= 20000) { const l = lit(A, I, th.steps); if (l.home !== th.steps || !s.report.startsWith('Step ' + th.steps.toLocaleString('en-US') + ': home.')) verdict.push('REPORT WRONG'); if (l.there < l.home && !s.report.includes('first at step ' + l.there.toLocaleString('en-US'))) verdict.push('EARLIER VISIT NOT AS MINE (' + l.there + ')'); if (!(l.there < l.home) && s.report.includes('stood on its starting point before')) verdict.push('EARLIER VISIT CLAIMED'); } else { const l = lit(A, I, 20000); if (l.home || !s.report.includes('it has not been home yet')) verdict.push('CAP REPORT WRONG'); } }
    else { if (!s.say.includes('it never comes home')) verdict.push('FORECAST WRONG'); const laps = Math.floor(s.total / th.q), l = lit(A, I, laps * th.q), d = Math.hypot(l.x, l.y); if (laps >= 1 && (!s.report.includes('it is ' + d.toFixed(3) + ' steps from its start') || Math.abs(d - laps * Math.sqrt(th.q)) > 1e-6)) verdict.push('DISTANCE WRONG (mine ' + d.toFixed(3) + ')'); if (l.home) verdict.push('MY WALK CAME HOME'); }
    const over = guideOver(s); const nl = Math.floor(s.total / s.forecast.q);
    if (s.report.includes('The dots') && s.dots === 0) verdict.push('SAYS DOTS, DREW NONE');
    if (over !== null && over > 1) verdict.push('DASHED CIRCLE ' + over.toFixed(0) + ' px OUTSIDE CANVAS (edge rust px ' + pix.edgeRust + ')');
    if (pix.edgeDark) verdict.push('LINE TOUCHES CANVAS EDGE');
    if (s.fails.length) verdict.push('PAGE FAILS: ' + s.fails.join(';'));
    if (verdict.length) wrong++;
    log('A.', JSON.stringify([a, i]), '| theory', JSON.stringify(th), '| total', s.total, 'home', s.home, 'there', s.there, 'dots', s.dots, 'laps drawn', nl, 'guide', s.guide ? s.guide.kind : null, '| line box x', pix.x0, pix.x1, 'y', pix.y0, pix.y1, 'of', pix.w, pix.h, '\n     SAY: ' + s.say + '\n     REPORT: ' + s.report + '\n     VERDICT: ' + (verdict.length ? verdict.join(' / ') : 'agrees with my programs')); }
  log('A. turtles with something wrong:', wrong, '; script errors:', errs.length, errs.join(' | ').slice(0, 300));
  await typed('25', '210'); await once(); await p.locator('.stage').screenshot({ path: path.join(out, 'mine-25-210-circle.png') });
  await typed('0.1', '0'); await once(); await p.locator('.stage').screenshot({ path: path.join(out, 'mine-0.1-0-nodots.png') });
  // ---- B. states
  await typed('2', '20'); await p.selectOption('#pace', 'slow'); await p.click('#go'); await p.waitForTimeout(700); let s = await state(); log('B1. slow, 0.7 s after Go:', s.running, s.drawn, s.report);
  await p.fill('#inc', '21'); s = await state(); log('B1. number changed while walking:', 'running', s.running, 'drawn', s.drawn, 'I', s.I, '| report:', s.report, '| say:', s.say.slice(0, 70)); await p.waitForTimeout(500); s = await state(); log('B1. half a second later: drawn', s.drawn, 'running', s.running);
  await typed('0', '7'); await p.selectOption('#pace', 'quick'); await p.click('#go'); await p.waitForTimeout(1000); const g1 = await state(); await p.click('#go'); await p.waitForTimeout(300); const g2 = await state(); await p.waitForTimeout(1000); const g3 = await state();
  log('B2. Go twice (720 steps at 120 a second): after 1 s drawn', g1.drawn, '; 0.3 s after second Go drawn', g2.drawn, 'goes', g2.goes, '; 1 s later drawn', g3.drawn, '(about 156 if the pace is not doubled)');
  await p.waitForTimeout(5200); s = await state(); let pix = await px(); log('B2. at the end: done', s.done, 'drawn', s.drawn, 'dots', s.dots, '| report:', s.report, '| line pixels', pix.line);
  const full = await (async () => { await once(); return (await px()).line; })(); log('B2. dark pixels after Go twice', pix.line, 'and after a clean all-at-once', full);
  await typed('2', '20'); await p.selectOption('#pace', 'slow'); await p.click('#go'); await p.waitForTimeout(700);
  { const bx = await p.locator('#map').boundingBox(); await p.locator('#map').scrollIntoViewIfNeeded(); const bx2 = await p.locator('#map').boundingBox(); await p.mouse.click(bx2.x + (40 - 1 + 0.5) / 359 * bx2.width, bx2.y + (359 - 30 + 0.5) / 360 * bx2.height); await p.waitForTimeout(1000); s = await state();
    log('B3. map clicked while it walks (slow): A', s.A, 'I', s.I, 'running', s.running, 'drawn', s.drawn, '(about 5 if one walk is running)', 'goes', s.goes, '| report:', s.report, '| say:', s.say.slice(0, 80)); await p.waitForTimeout(1000); s = await state(); log('B3. one second later drawn', s.drawn, '(about 10)'); }
  await typed('112', '135'); await p.selectOption('#pace', 'quick'); await p.click('#go'); await p.waitForTimeout(1500); const r1 = await state(), p1 = await px(); await p.setViewportSize({ width: 500, height: 900 }); await p.waitForTimeout(300); const r2 = await state(), p2 = await px();
  log('B4. resize while walking: before: drawn', r1.drawn, 'canvas', p1.w, p1.h, 'dark px', p1.line, '; after: running', r2.running, 'drawn', r2.drawn, 'canvas', p2.w, p2.h, 'dark px', p2.line, 'line box x', p2.x0, p2.x1, 'y', p2.y0, p2.y1, 'edge dark', p2.edgeDark);
  await p.waitForTimeout(5500); s = await state(); pix = await px(); const lay = await p.evaluate(() => ({ sw: document.documentElement.scrollWidth, iw: window.innerWidth }));
  log('B4. at the end: done', s.done, 'drawn', s.drawn, 'dots', s.dots, 'fails', s.fails.length, 'guide over', guideOver(s), 'edge rust', pix.edgeRust, 'edge dark', pix.edgeDark, 'page', lay.sw, 'of', lay.iw, '| report:', s.report);
  await p.setViewportSize({ width: 1000, height: 1500 }); await p.waitForTimeout(300);
  // ---- C. a narrow screen
  const ph = await b.newPage({ viewport: { width: 320, height: 700 }, deviceScaleFactor: 2 }); await ph.goto('file://' + page); await ph.waitForTimeout(400);
  for (const [a, i] of [['10', '20'], ['112', '135'], ['25', '210'], ['312', '144'], ['0', '0'], ['999999', '999999.999']]) { await typed(a, i, ph); const st = await once(ph), pk = await px(ph);
    const lay2 = await ph.evaluate(() => { const r = id => document.getElementById(id).getBoundingClientRect(); const ids = ['say', 'report', 'field', 'map', 'presets', 'angle', 'inc', 'go', 'pace']; let right = 0, worst = ''; for (const id of ids) { const x = r(id).right; if (x > right) { right = x; worst = id; } } const say = document.getElementById('say'); return { sw: document.documentElement.scrollWidth, iw: window.innerWidth, right, worst, sayOverflow: say.scrollWidth > say.clientWidth, mapw: r('map').width, maph: r('map').height }; });
    log('C. 320 px:', JSON.stringify([a, i]), 'page', lay2.sw, 'of', lay2.iw, 'rightmost', lay2.worst, lay2.right.toFixed(1), 'say overflows', lay2.sayOverflow, 'map', lay2.mapw.toFixed(0), 'x', lay2.maph.toFixed(0), '| canvas', pk.w, pk.h, 'line box x', pk.x0, pk.x1, 'y', pk.y0, pk.y1, 'edge dark', pk.edgeDark, 'edge rust', pk.edgeRust, 'guide over', guideOver(st), '| report:', st.report.slice(0, 90)); }
  await typed('25', '210', ph); await once(ph); await ph.screenshot({ path: path.join(out, 'mine-phone-25-210.png'), fullPage: false });
  log('script errors in all of this:', errs.length, errs.join(' | ').slice(0, 300));
  await b.close();
})().catch(e => { console.log('DRIVE STOPPED: ' + String(e).slice(0, 400)); process.exit(2); });
