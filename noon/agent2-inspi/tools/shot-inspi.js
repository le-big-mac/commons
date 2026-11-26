// Headless checks of the turtle page.   usage: node shot-inspi.js PAGE.html OUTDIR CORE.js TABLE.json
// TABLE.json is made by table.py in Python, by walking; nothing in it comes from core.js.
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
const fails = []; let asserts = 0, fullLine = 0, browser = null;
(async () => {
  const page = path.resolve(process.argv[2]), out = path.resolve(process.argv[3]), T = require(path.resolve(process.argv[4])), table = JSON.parse(fs.readFileSync(path.resolve(process.argv[5]), 'utf8'));
  const U = T.UNIT, WIDEST = 83.594568, NARROWEST = 1.931852;          // from score.out (Python, every pair that could matter measured)
  const b = await chromium.launch(); browser = b;
  const p = await b.newPage({ viewport: { width: 1000, height: 1500 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + page); await p.waitForTimeout(500);
  const must = (cond, what, detail) => { asserts++; if (!cond) fails.push(what); console.log((cond ? 'ok   ' : 'FAIL ') + what + (detail ? '   [' + detail + ']' : '')); };
  const state = (pg) => (pg || p).evaluate(() => window.INSPISTATE());
  const typed = async (a, i) => { await p.fill('#angle', a); await p.fill('#inc', i); };
  const once = async () => { await p.selectOption('#pace', 'once'); await p.click('#go'); await p.waitForTimeout(120); return state(); };
  // what is drawn on the field: the dark line, the rust marks, and where they are
  const ink = (pg) => (pg || p).evaluate(() => { const c = document.getElementById('field'), d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let line = 0, rust = 0, x0 = 1e9, x1 = -1, y0 = 1e9, y1 = -1;
    for (let y = 0; y < c.height; y++) for (let x = 0; x < c.width; x++) { const i = 4 * (y * c.width + x), r = d[i], g = d[i + 1], bl = d[i + 2], a = d[i + 3];
      if (a > 90 && r < 100 && g < 90 && bl < 90) { line++; if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
      if (a > 150 && r > 130 && g < 110 && bl < 85 && r - g > 60) rust++; }
    return { line, rust, x0, x1, y0, y1, w: c.width, h: c.height }; });
  const rustNear = (x, y, rad, pg) => (pg || p).evaluate(([x, y, rad]) => { const c = document.getElementById('field'), X = Math.round(x), Y = Math.round(y), d = c.getContext('2d').getImageData(X - rad, Y - rad, 2 * rad + 1, 2 * rad + 1).data; let n = 0;
    for (let i = 0; i < d.length; i += 4) if (d[i + 3] > 150 && d[i] > 130 && d[i + 1] < 110 && d[i + 2] < 85) n++; return n; }, [x, y, rad]);
  const dashNear = (x, y, rad) => p.evaluate(([x, y, rad]) => { const c = document.getElementById('field'), X = Math.round(x), Y = Math.round(y), d = c.getContext('2d').getImageData(X - rad, Y - rad, 2 * rad + 1, 2 * rad + 1).data; let n = 0;
    for (let i = 0; i < d.length; i += 4) if (d[i + 3] > 40 && d[i] > 130 && d[i + 1] < 110 && d[i + 2] < 85) n++; return n; }, [x, y, rad]);
  const marker = (pg) => (pg || p).evaluate(() => { const c = document.getElementById('turtle'), d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let n = 0, sx = 0, sy = 0;
    for (let y = 0; y < c.height; y++) for (let x = 0; x < c.width; x++) { const i = 4 * (y * c.width + x); if (d[i + 3] > 120 && d[i + 2] > 110 && d[i] < 90) { n++; sx += x; sy += y; } }
    const s = window.INSPISTATE(), P = window.INSPIPATH(1)[s.drawn], q = window.INSPIPX(P[0], P[1]); return { n, x: sx / Math.max(n, 1), y: sy / Math.max(n, 1), at: q, drawn: s.drawn }; });
  const pathOf = () => p.evaluate(() => window.INSPIPATH(1));
  // the turtle's blue triangle: its point is the blue pixel farthest from the middle of the blue; "want" is the next step, on the screen
  const pointing = (pg) => (pg || p).evaluate(() => { const c = document.getElementById('turtle'), d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data, blue = []; let sx = 0, sy = 0;
    for (let y = 0; y < c.height; y++) for (let x = 0; x < c.width; x++) { const i = 4 * (y * c.width + x); if (d[i + 3] > 120 && d[i + 2] > 110 && d[i] < 90) { blue.push([x, y]); sx += x; sy += y; } }
    const n = blue.length, cx = sx / Math.max(n, 1), cy = sy / Math.max(n, 1); let far = 0, tip = [cx, cy]; for (const [x, y] of blue) { const r = Math.hypot(x - cx, y - cy); if (r > far) { far = r; tip = [x, y]; } }
    const st = window.INSPISTATE(), P = window.INSPIPATH(1), k = st.drawn; let want = null;
    if (k < st.total) { const a = window.INSPIPX(P[k][0], P[k][1]), b = window.INSPIPX(P[k + 1][0], P[k + 1][1]); want = [b[0] - a[0], b[1] - a[1]]; }
    return { n, tip: [tip[0] - cx, tip[1] - cy], want, drawn: k }; });
  const cosBetween = (u, v) => (u[0] * v[0] + u[1] * v[1]) / (Math.hypot(u[0], u[1]) * Math.hypot(v[0], v[1]) || 1);
  // how many of a closed figure's corners land on a corner when it is turned through a part of a turn about the middle of its corners
  const fits = (pts, n, part) => { let cx = 0, cy = 0; for (let k = 0; k < n; k++) { cx += pts[k][0]; cy += pts[k][1]; } cx /= n; cy /= n;
    const key = (x, y) => Math.round(x * 1e5) + ',' + Math.round(y * 1e5), set = new Set(); for (let k = 0; k < n; k++) set.add(key(pts[k][0], pts[k][1]));
    const c = Math.cos(2 * Math.PI * part), sn = Math.sin(2 * Math.PI * part); let hit = 0;
    for (let k = 0; k < n; k++) { const dx = pts[k][0] - cx, dy = pts[k][1] - cy, x = cx + dx * c - dy * sn, y = cy + dx * sn + dy * c; let ok = false;
      for (const ex of [-1, 0, 1]) for (const ey of [-1, 0, 1]) if (set.has((Math.round(x * 1e5) + ex) + ',' + (Math.round(y * 1e5) + ey))) ok = true; if (ok) hit++; }
    return hit; };
  const pyCorners = (A, I, pts) => { const c = table.corners.find(c => c.A === A && c.I === I); if (!c) return null; let worst = 0, n = 0; for (const [k, x, y] of c.at) if (pts[k]) { worst = Math.max(worst, Math.abs(pts[k][0] - x), Math.abs(pts[k][1] - y)); n++; } else worst = 9; return { worst, n }; };
  const samePath = (pts, w) => { if (pts.length !== w.xs.length) return 'lengths ' + pts.length + ' and ' + w.xs.length; let worst = 0; for (let k = 0; k < pts.length; k++) worst = Math.max(worst, Math.abs(pts[k][0] - w.xs[k]), Math.abs(pts[k][1] - w.ys[k])); return worst; };
  const widthOf = pts => { let m = 0; for (let i = 0; i < pts.length; i++) for (let j = i + 1; j < pts.length; j++) { const d = Math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1]); if (d > m) m = d; } return m; };
  const inFrame = async (pg) => { const e = await (pg || p).evaluate(() => window.INSPIPIXELS()); return { ok: e.x0 >= 4 && e.y0 >= 4 && e.x1 <= e.W - 4 && e.y1 <= e.H - 4, e }; };

  // ---- 1. as it opens
  let s = await state();
  must(errs.length === 0, 'the page opens without a script error', errs.join(' | ').slice(0, 200));
  must(s.valid && s.A === 2 * U && s.I === 20 * U && s.drawn === 0 && !s.running && !s.done && s.goes === 0 && s.report === 'The turtle is waiting at its start.', 'it opens on the book\'s turtle (first turn 2, add 20), waiting, not yet moving', s.report);
  must(await p.inputValue('#angle') === '2' && await p.inputValue('#inc') === '20', 'and the two boxes show 2 and 20');
  { const f = T.forecast(2 * U, 20 * U), py = table.whole[20][2];
    must(py === 90 && f.steps === 90 && s.forecast.steps === 90 && s.say.includes('it comes home after 90 steps') && s.say.includes('come round again every 18 steps') && s.say.includes('turned by 216°') && s.say.includes('5 laps bring it round') && s.say.includes('5 matching parts'),
      'before it moves the forecast says: home after 90 steps, laps of 18, 216 degrees a lap, 5 laps, 5 matching parts; and 90 is what Python found by walking', s.say.slice(0, 120)); }
  { const m0 = await marker(), o = await p.evaluate(() => window.INSPIPX(0, 0));
    must(m0.n > 40 && Math.hypot(m0.x - o[0], m0.y - o[1]) < 6 && (await rustNear(o[0], o[1], 10)) > 20, 'the turtle is drawn at the start, where the ring is', m0.n + ' turtle pixels, ' + Math.hypot(m0.x - o[0], m0.y - o[1]).toFixed(1) + ' px from the ring\'s middle');
    const i0 = await ink(); must(i0.line === 0, 'and no line is drawn yet', i0.line + ' dark pixels');
    const pt = await pointing(); must(pt.n > 40 && pt.tip[1] < -5 && Math.abs(pt.tip[0]) < 3, 'the waiting turtle points up the page, the way its first step will go', 'its point is ' + pt.tip.map(v => v.toFixed(1)).join(', ') + ' px from its middle');
    const rects = await p.evaluate(() => ['field', 'turtle'].map(id => { const r = document.getElementById(id).getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; }));
    must(rects[0].every((v, k) => Math.abs(v - rects[1][k]) < 0.5), 'the sheet the turtle is drawn on lies exactly over the sheet the line is drawn on', JSON.stringify(rects.map(r => r.map(v => +v.toFixed(1))))); }
  // the map as it opens
  { let away = 0; for (let inc = 1; inc < 360; inc++) for (let a = 0; a < 360; a++) if (table.whole[inc][a] === 0) away++;
    let oddAway = 0, evenNone = 0; for (let inc = 1; inc < 360; inc++) { let d = 0; for (let a = 0; a < 360; a++) if (table.whole[inc][a] === 0) d++; if (inc % 2 && d) oddAway++; if (inc % 2 === 0 && !d) evenNone++; }
    let longest = 0; for (let inc = 1; inc < 360; inc++) for (let a = 0; a < 360; a++) longest = Math.max(longest, table.whole[inc][a]);
    must(away === 14090 && s.census.away === away && s.census.home === 129240 - away && s.mapcount.includes('14,090 of the 129,240'), 'the map\'s sentence counts 14,090 of 129,240 that never come home, which is Python\'s count by walking', s.mapcount.slice(0, 60));
    must(longest === 720 && s.census.longest === 720 && s.mapcount.includes('within 720 steps'), 'and says the rest are home within 720 steps, which is the longest in Python\'s table', String(longest));
    must(oddAway === 0 && evenNone === 0 && s.census.oddAway === 0 && s.census.evenNone === 0 && s.mapcount.includes('only where the amount added is even: among these whole-degree turtles, one that adds an odd amount always comes home'), 'and says the dark dots stand only at even amounts, among these whole-degree turtles: in Python\'s table no odd amount has one and every even amount has some', oddAway + ' odd amounts with a dark dot, ' + evenNone + ' even amounts without');
    const res = await p.evaluate((whole) => { const c = document.getElementById('map'), d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data, st = window.INSPISTATE(); let wrong = 0, seen = 0, darkOK = 0, skipped = 0; const tone = {};
      const mx = st.pick ? (st.pick.inc - 1 + 0.5) * c.width / 359 : -99, my = st.pick ? (359 - st.pick.angle + 0.5) * c.height / 360 : -99;
      for (let inc = 1; inc < 360; inc++) for (let a = 0; a < 360; a++) { const x = Math.floor((inc - 1 + 0.5) * c.width / 359), y = Math.floor((359 - a + 0.5) * c.height / 360);
        if (Math.hypot(x - mx, y - my) < 16) { skipped++; continue; }
        const i = 4 * (y * c.width + x), got = [d[i], d[i + 1], d[i + 2]], steps = whole[inc][a], want = window.INSPISHADE(steps); seen++;
        if (got[0] !== want[0] || got[1] !== want[1] || got[2] !== want[2]) wrong++;
        if (steps === 0 && got[0] < 60 && got[1] < 60 && got[2] < 60) darkOK++; if (steps) tone[steps] = got[0] + got[1] + got[2]; }
      return { wrong, seen, darkOK, skipped, tone, w: c.width, h: c.height }; }, table.whole);
    const ks = Object.keys(res.tone).map(Number).sort((a, b) => a - b); let mono = true, distinct = new Set(ks.map(k => res.tone[k])).size; for (let i = 1; i < ks.length; i++) if (res.tone[ks[i]] > res.tone[ks[i - 1]]) mono = false;
    must(res.wrong === 0 && res.seen > 129000 && res.skipped < 400, 'every dot of the map has the colour that goes with Python\'s walked result for that turtle', res.seen + ' dots read back, ' + res.wrong + ' wrong, ' + res.skipped + ' under the marker left out');
    must(res.darkOK > 14000 && mono && ks.length >= 20 && distinct >= 20 && res.tone[ks[0]] - res.tone[ks[ks.length - 1]] > 100, 'the dark dots are the ones that never come home, and among the others more steps is never a paler dot', res.darkOK + ' dark; ' + ks.length + ' different numbers of steps in ' + distinct + ' tones');
    const ramp = await p.evaluate(() => { const c = document.getElementById('ramp'), d = c.getContext('2d').getImageData(0, 0, c.width, 1).data, n = c.width; return [[d[0], d[1], d[2]], [d[4 * (n - 1)], d[4 * (n - 1) + 1], d[4 * (n - 1) + 2]], window.INSPISHADE(4), window.INSPISHADE(720)]; });
    let least = 1e9; for (let inc = 1; inc < 360; inc++) for (let a = 0; a < 360; a++) if (table.whole[inc][a] && table.whole[inc][a] < least) least = table.whole[inc][a];
    must(String(ramp[0]) === String(ramp[2]) && String(ramp[1]) === String(ramp[3]) && s.key === 'home after 4 steps … 720' && least === 4 && longest === 720 && String(ramp[0]) === '246,240,226' && String(ramp[1]) === '158,186,212',
      'the key says "home after 4 steps" at its pale end and 720 at the other, the least and the most in Python\'s table, and its strip runs between those two colours', s.key + '; ' + JSON.stringify(ramp)); }
  await p.screenshot({ path: path.join(out, 'turtle-open.png'), fullPage: true });

  // ---- 2. Go, all at once: the book's figure
  s = await once();
  { const w = T.walk(2 * U, 20 * U, 90), got = await pathOf(), worst = samePath(got, w), pts = got.slice(); while (pts.length < 91) pts.push(pts[pts.length - 1]);
    must(s.done && !s.running && s.drawn === 90 && s.total === 90 && s.goes === 1, 'Go draws the 90 steps and stops', 'drawn ' + s.drawn + ' of ' + s.total);
    must(typeof worst === 'number' && worst < 1e-12 && s.home === 90 && w.home === 90, 'the path on the page is the walk core.js makes in node, corner for corner, and it is home at step 90', 'worst difference ' + worst);
    must(s.report.startsWith('Step 90: home.') && s.report.includes('its next turn would be 2° again') && s.fails.length === 0, 'the report under the picture says so: Step 90, home', s.report.slice(0, 90));
    const fr = await inFrame(), i1 = await ink(); fullLine = i1.line;
    must(fr.ok && i1.line > 2000 && Math.abs(i1.x0 - fr.e.x0) < 4 && Math.abs(i1.x1 - fr.e.x1) < 4 && Math.abs(i1.y0 - fr.e.y0) < 4 && Math.abs(i1.y1 - fr.e.y1) < 4,
      'the figure is inside the frame, and the dark line on the canvas reaches just as far as the page\'s own corners do', i1.line + ' dark pixels, x ' + i1.x0 + ' to ' + i1.x1 + ' of ' + i1.w + ', y ' + i1.y0 + ' to ' + i1.y1 + ' of ' + i1.h);
    let dots = 0, onCircle = true; const g = s.guide || { kind: 'none', cx: 0, cy: 0, r: 0 };       // a page without its circle must fail these, not stop the test
    for (let n = 1; n <= 5; n++) { const q = await p.evaluate(([x, y]) => window.INSPIPX(x, y), pts[18 * n]); if ((await rustNear(q[0], q[1], 4)) >= 12) dots++; }
    for (let n = 0; n < 5; n++) if (Math.abs(Math.hypot(pts[18 * n][0] - g.cx, pts[18 * n][1] - g.cy) - g.r) > 1e-9) onCircle = false;
    must(s.dots === 5 && dots === 5, 'a dot is drawn at the end of each of the 5 laps', dots + ' found on the canvas');
    must(g && g.kind === 'circle' && onCircle && s.report.includes('lie on the dashed circle'), 'and the ends of the laps lie on the circle the page draws dashed, as it says', 'radius ' + g.r.toFixed(4) + ' steps');
    { const c = await p.evaluate(([x, y]) => window.INSPIPX(x, y), [g.cx + g.r * Math.cos(1), g.cy + g.r * Math.sin(1)]), c2 = await p.evaluate(([x, y]) => window.INSPIPX(x, y), [g.cx + 0.6 * g.r * Math.cos(1), g.cy + 0.6 * g.r * Math.sin(1)]);
      let onArc = 0; for (const th of [0.4, 1, 1.7, 2.6, 3.3, 4.1, 5.2, 5.9]) { const q = await p.evaluate(([x, y]) => window.INSPIPX(x, y), [g.cx + g.r * Math.cos(th), g.cy + g.r * Math.sin(th)]); if ((await dashNear(q[0], q[1], 7)) > 0) onArc++; }
      must(onArc >= 6, 'the dashed circle is drawn where the page\'s own numbers put it', onArc + ' of 8 places round it have dashes'); }
    const m1 = await marker(); must(m1.n > 40 && Math.hypot(m1.x - m1.at[0], m1.y - m1.at[1]) < 6, 'the turtle is drawn at the last corner, which is the start', Math.hypot(m1.x - m1.at[0], m1.y - m1.at[1]).toFixed(1) + ' px off');
    // five matching parts: turn the corners a fifth of the way round about the circle's middle
    const key = (x, y) => Math.round(x * 1e6) + ',' + Math.round(y * 1e6), set = new Set(pts.slice(0, 90).map(q => key(q[0], q[1]))); let fit = 0, fit7 = 0;
    for (const [ang, which] of [[2 * Math.PI / 5, 5], [2 * Math.PI / 7, 7]]) for (let k = 0; k < 90; k++) { const dx = pts[k][0] - g.cx, dy = pts[k][1] - g.cy, x = g.cx + dx * Math.cos(ang) - dy * Math.sin(ang), y = g.cy + dx * Math.sin(ang) + dy * Math.cos(ang);
      let hit = false; for (const ex of [-1, 0, 1]) for (const ey of [-1, 0, 1]) if (set.has((Math.round(x * 1e6) + ex) + ',' + (Math.round(y * 1e6) + ey))) hit = true; if (hit) { if (which === 5) fit++; else fit7++; } }
    must(fit === 90 && fit7 < 10, 'the figure has the 5 matching parts the forecast promised: a fifth of a turn carries every corner onto a corner (a seventh does not)', fit + ' of 90; a seventh: ' + fit7); }
  await p.locator('.stage').screenshot({ path: path.join(out, 'turtle-book.png') });

  // ---- 3. the paces
  await p.selectOption('#pace', 'quick'); await p.click('#go'); await p.waitForTimeout(1000);
  { const a = await state(), ma = await marker(), pt = await pointing(); await p.waitForTimeout(500); const c = await state();
    must(pt.n > 40 && pt.want && cosBetween(pt.tip, pt.want) > 0.9, 'while it walks the turtle points along the step it is about to take', 'at step ' + pt.drawn + ' the cosine between its point and that step is ' + (pt.want ? cosBetween(pt.tip, pt.want).toFixed(3) : 'none'));
    must(a.running && !a.done && a.drawn >= 22 && a.drawn <= 38 && c.drawn - a.drawn >= 10 && c.drawn - a.drawn <= 20, 'quick: 90 steps at 30 a second, so about 30 are drawn after one second and 15 more half a second later', a.drawn + ' then ' + c.drawn);
    must(a.report === 'Step ' + a.drawn + ' of 90.', 'while it walks the report counts the steps', a.report);
    must(ma.n > 40 && Math.hypot(ma.x - ma.at[0], ma.y - ma.at[1]) < 6, 'and the turtle is drawn at the corner it has reached', 'step ' + ma.drawn + ', ' + Math.hypot(ma.x - ma.at[0], ma.y - ma.at[1]).toFixed(1) + ' px off');
    const ia = await ink(); must(ia.line > 0.15 * fullLine && ia.line < 0.75 * fullLine, 'only the part walked so far is drawn', ia.line + ' dark pixels of the ' + fullLine + ' in the whole figure');
    await p.waitForTimeout(2200); const e = await state(); must(e.done && e.drawn === 90 && e.report.startsWith('Step 90: home.'), 'and it finishes in about three seconds', e.report.slice(0, 20)); }
  await p.selectOption('#pace', 'slow'); await p.click('#go'); await p.waitForTimeout(2000);
  { const a = await state(); must(a.running && a.drawn >= 8 && a.drawn <= 12, 'slow: 5 steps a second, so about 10 after two seconds', String(a.drawn));
    await typed('2', '21'); const c = await state();
    must(!c.running && c.drawn === 0 && !c.done && c.I === 21 * U && c.report === 'The turtle is waiting at its start.' && c.say.includes('720 steps') && table.whole[21][2] === 720, 'changing a number while it walks stops it, puts it back at the start, and gives the new forecast', c.say.slice(0, 70));
    await p.waitForTimeout(400); const d = await state(); must(d.drawn === 0 && !d.running, 'and it stays stopped until Go is pressed'); }

  // ---- 4. the turtles on the buttons
  const want = [['2', '20', 'the book’s'], ['10', '20', 'marches away'], ['0', '7', 'two spirals'], ['1', '2', 'a chain of curls'], ['112', '135', 'the widest'], ['30', '180', 'the smallest'], ['40', '0.5', 'half a degree']];
  must(JSON.stringify(s.presets) === JSON.stringify(want), 'seven buttons, with the numbers the tests expect');
  await p.selectOption('#pace', 'once');
  for (let n = 0; n < want.length; n++) {
    const [a, i, name] = want[n]; await p.click('#preset' + n); await p.waitForTimeout(150); s = await state();
    const A = T.parse(a), I = T.parse(i), f = T.forecast(A, I), whole = A % U === 0 && I % U === 0, py = whole ? table.whole[I / U][A / U] : null, pts = await pathOf(), fr = await inFrame();
    const boxes = await p.inputValue('#angle') === a && await p.inputValue('#inc') === i;
    let ok = boxes && s.A === A && s.I === I && s.done && s.goes >= 1 && s.fails.length === 0 && fr.ok && samePath(pts, T.walk(A, I, s.total)) < 1e-12, detail = '';
    if (f.home) { ok = ok && s.total === f.steps && s.home === f.steps && (py === null || py === f.steps) && s.say.includes('it comes home after ' + T.commas(f.steps) + ' steps') && s.report.startsWith('Step ' + T.commas(f.steps) + ': home.'); detail = 'home at step ' + s.home; }
    else { const laps = s.total / f.q, d = Math.hypot(pts[s.total][0], pts[s.total][1]);
      ok = ok && Number.isInteger(laps) && laps >= 6 && s.home === 0 && py === 0 && s.say.includes('it never comes home') && s.say.includes('√' + f.q + ' = ' + Math.sqrt(f.q).toFixed(3)) && Math.abs(d - laps * Math.sqrt(f.q)) < 1e-9 && s.report.includes(laps + ' laps done, and it is ' + d.toFixed(3) + ' steps from its start, which is ' + laps + ' × √' + f.q + '.') && !/which is \d+ × \d+\.\d/.test(s.report);
      detail = laps + ' laps, ' + d.toFixed(3) + ' steps away'; }
    must(ok, 'the button "' + name + '" puts ' + a + ' and ' + i + ' in the boxes and sends the turtle off; forecast, walk and report agree with core.js' + (whole ? ' and with Python\'s walk' : ''), detail);
    { const pc = pyCorners(A, I, pts), laps = Math.floor(s.total / f.q), ik = await ink(), e = fr.e; let found = 0, want3 = 0;
      for (const m of [...new Set([1, Math.ceil(laps / 2), laps])]) { want3++; const q2 = await p.evaluate(([x, y]) => window.INSPIPX(x, y), pts[m * f.q]); if ((await rustNear(q2[0], q2[1], 4)) >= 5) found++; }
      const lineOK = ik.line > 100 && Math.abs(ik.x0 - e.x0) < 5 && Math.abs(ik.x1 - e.x1) < 5 && Math.abs(ik.y0 - e.y0) < 5 && Math.abs(ik.y1 - e.y1) < 5 && ik.x0 >= 2 && ik.y0 >= 2 && ik.x1 <= ik.w - 3 && ik.y1 <= ik.h - 3;
      must(pc && pc.n >= 5 && pc.worst < 1e-9 && s.dots === laps && found === want3 && lineOK, '   "' + name + '": its corners are where Python\'s walk stands; a dot is drawn at the end of every lap; and the dark line on the canvas is inside the frame, reaching as far as the corners do',
        (pc ? pc.n + ' places, worst ' + pc.worst.toExponential(1) : 'no places from Python') + '; ' + s.dots + ' dots for ' + laps + ' laps, ' + found + ' of ' + want3 + ' looked for found; line x ' + ik.x0 + ' to ' + ik.x1 + ', y ' + ik.y0 + ' to ' + ik.y1 + ' of ' + ik.w + ' by ' + ik.h);
      if (f.home) { const all = fits(pts, f.steps, 1 / f.laps), half = fits(pts, f.steps, 1 / (2 * f.laps));
        must(all === f.steps && half < f.steps && s.say.includes('the figure will have ' + T.commas(f.laps) + ' matching parts'), '   "' + name + '": the figure has the ' + f.laps + ' matching parts the forecast promises (and not twice as many)', all + ' of ' + f.steps + ' corners fit when turned 1/' + f.laps + ' of a turn; ' + half + ' when turned half that'); }
      if (s.guide && s.guide.kind === 'circle') { const c = e.circle; let dash = 0; for (const [x, y] of [[(c.x0 + c.x1) / 2, c.y0], [(c.x0 + c.x1) / 2, c.y1], [c.x0, (c.y0 + c.y1) / 2], [c.x1, (c.y0 + c.y1) / 2]]) if (x > 7 && y > 7 && x < e.W - 8 && y < e.H - 8 && (await dashNear(x, y, 7)) > 0) dash++;
        must(c && c.x0 >= 2 && c.y0 >= 2 && c.x1 <= e.W - 2 && c.y1 <= e.H - 2 && dash === 4 && s.report.includes('lie on the dashed circle'), '   "' + name + '": the dashed circle the report speaks of is whole inside the frame, and dashes are found at its top, bottom, left and right', dash + ' of 4; circle x ' + c.x0.toFixed(0) + ' to ' + c.x1.toFixed(0) + ', y ' + c.y0.toFixed(0) + ' to ' + c.y1.toFixed(0)); } }
    if (name === 'marches away') { await typed('10', '20'); const m0 = await marker(); await once(); const m1 = await marker(), st = await state(), e = pts[st.total], k = st.view.k;
      must(m0.n > 40 && m1.n > 40 && Math.abs((m1.x - m0.x) - k * e[0]) < 5 && Math.abs((m1.y - m0.y) + k * e[1]) < 5 && Math.abs(e[0]) > 5 && Math.abs(e[1]) > 5,
        'marches away: on the screen the turtle ends as far to the right of its start, and as far up, as the walk puts it (the picture is neither mirrored nor upside down)', 'walk: ' + e[0].toFixed(2) + ' right, ' + e[1].toFixed(2) + ' up; screen: ' + ((m1.x - m0.x) / k).toFixed(2) + ' right, ' + (-(m1.y - m0.y) / k).toFixed(2) + ' up'); }
    if (name === 'marches away') { let even = true; const B = pts[18]; for (let m = 0; m <= 13; m++) if (Math.hypot(pts[18 * m][0] - m * B[0], pts[18 * m][1] - m * B[1]) > 1e-9) even = false;
      const mid = await p.evaluate(([x, y]) => window.INSPIPX(x, y), [6.5 * B[0], 6.5 * B[1]]), lineDash = (await dashNear(mid[0], mid[1], 8)) > 0;
      must(even && Math.abs(Math.hypot(B[0], B[1]) - Math.sqrt(18)) < 1e-12 && s.guide.kind === 'line' && s.dots === 13 && s.report.includes('lie on the dashed line') && lineDash, 'marches away: the 13 lap ends are evenly spaced along one line, √18 apart, and the dashed line is drawn through them', 'one lap: ' + Math.hypot(B[0], B[1]).toFixed(12)); }
    if (name === 'the widest') { const wd = widthOf(pts); must(Math.abs(wd - WIDEST) < 1e-5, 'the widest: its corners are 83.5946 steps apart at the most, the greatest width Python found among all whole-degree turtles that come home', wd.toFixed(6)); }
    if (name === 'the smallest') { const wd = widthOf(pts); must(Math.abs(wd - NARROWEST) < 1e-5, 'the smallest: 1.9319 steps across, the least Python found', wd.toFixed(6)); }
    if (name === 'two spirals') must(s.there === 362 && s.report.includes('first at step 362, but was not then home'), 'two spirals: the report says it stood on its starting point at step 362 without being home', 'there ' + s.there);
    if (name === 'half a degree') must(s.forecast.q === 720 && s.total === 1440 && s.pick === null, 'half a degree: laps of 720, 1,440 steps, and no marker on the whole-degree map');
    await p.locator('.stage').screenshot({ path: path.join(out, 'turtle-' + name.replace(/[^a-z]+/g, '-') + '.png') });
  }

  // ---- 5. what is typed
  await typed('abc', '20'); s = await state();
  { const i5 = await ink();
    must(!s.valid && s.say === 'Type each turn as a plain number of degrees, such as 20, 2.5 or -7, with at most six figures before the point and three after.'  && await p.isDisabled('#go') && (await p.getAttribute('#angle', 'class') || '').includes('bad') && !(await p.getAttribute('#inc', 'class') || '').includes('bad') && i5.line === 0 && s.report === '',
      'a first turn that is not a number: the page asks for one, marks that box, disables Go and clears the picture', s.say); }
  await typed('2', '1.2345'); s = await state(); must(!s.valid && (await p.getAttribute('#inc', 'class') || '').includes('bad'), 'four decimals are refused too');
  await typed('2.5', '20'); s = await state();
  { const f = T.forecast(2500, 20000);
    must(s.valid && !(await p.isDisabled('#go')) && s.forecast.steps === f.steps && s.say.includes('it comes home after ' + T.commas(f.steps) + ' steps') && f.steps === 144, '2.5 and 20: the forecast is core.js\'s (144 steps)', s.say.slice(0, 80));
    await p.selectOption('#pace', 'once'); await p.press('#inc', 'Enter'); await p.waitForTimeout(150); s = await state();
    must(s.done && s.home === 144 && s.report.startsWith('Step 144: home.'), 'Enter in a box starts it, and it is home at step 144', s.report.slice(0, 30)); }
  let tried5 = 0; const bad5 = [];
  for (const r of table.decimal.filter(r => r.steps !== null && r.steps <= 20000 && 'home' in r).slice(0, 12).concat(table.decimal.filter(r => r.steps === null && r.q <= 500).slice(0, 6))) {
    await typed(T.show(r.A).replace('−', '-'), T.show(r.I).replace('−', '-')); s = await once();
    const okHome = r.steps !== null && s.home === r.steps && r.home === r.steps && s.report.startsWith('Step ' + T.commas(r.steps) + ': home.') && s.say.includes('after ' + T.commas(r.steps) + ' steps');
    const okAway = r.steps === null && s.home === 0 && s.say.includes('it never comes home') && s.report.includes('not home, and it will not be') && s.forecast.q === r.q;
    tried5++; if (!(okHome || okAway) || s.fails.length || !(await inFrame()).ok) bad5.push(T.show(r.A) + ', ' + T.show(r.I) + ': ' + s.report.slice(0, 60)); }
  must(tried5 === 18 && bad5.length === 0, 'eighteen pairs with decimals from Python\'s table (twelve that come home, six that never do): forecast, walk and report agree with Python\'s exact fractions and its walk, and each figure is in the frame', tried5 + ' tried' + (bad5.length ? '; wrong: ' + bad5.join(' | ') : ''));
  // too long to draw
  await typed('0.001', '0.1'); s = await once();
  { const f = T.forecast(1, 100); must(f.home && f.steps > 20000 && s.total === 20000 && s.say.includes('it comes home after ' + T.commas(f.steps) + ' steps') && s.say.includes('it will stop at step 20,000') && s.report.startsWith('Stopped at step 20,000 of the ' + T.commas(f.steps) + ' it needs') && s.report.includes('it has not been home yet') && s.home === 0 && s.fails.length === 0 && (await inFrame()).ok,
      'a turtle that needs more steps than the page draws: the forecast gives the number and says it will stop at 20,000; the report says it stopped and has not been home', T.commas(f.steps) + ' steps'); }
  await typed('0.001', '0.002'); s = await once();
  { const f = T.forecast(1, 2); must(!f.home && f.q === 180000 && s.total === 20000 && s.say.includes('it never comes home') && s.say.includes('A lap is more than this page draws') && s.report.startsWith('Stopped at step 20,000, before the end of its first lap of 180,000 steps') && s.fails.length === 0,
      'a turtle whose lap is longer than the page draws: the forecast says never and says the lap will not be finished; the report says it stopped inside its first lap', s.report.slice(0, 70)); }
  // the plain polygons, and turning left
  await typed('90', '0'); s = await once();
  { const pts = await pathOf(); must(s.home === 4 && s.say.includes('It makes the same turn after every step, 90°, so 4 steps bring it round') && Math.abs(pts[1][1] - 1) < 1e-12 && Math.abs(pts[2][0] - 1) < 1e-12 && s.report.startsWith('Step 4: home.') && s.say.includes('the figure will have 4 matching parts') && fits(pts, 4, 1 / 4) === 4 && fits(pts, 4, 1 / 8) < 4, '90 and 0: a square, up first and then to the right, with the 4 matching parts the forecast says', s.say.slice(28, 110)); }
  await typed('.5', '−20'); s = await state();
  must(s.valid && s.A === 500 && s.I === -20000 && s.forecast.home === T.forecast(500, -20000).home && s.forecast.steps === T.forecast(500, -20000).steps, 'a number that begins with its point, and the minus sign the page itself prints, are both accepted', '.5 and −20: ' + s.say.slice(28, 70));
  await typed('1234567', '20'); s = await state(); must(!s.valid && s.say.includes('at most six figures before the point'), 'seven figures are refused, and the page says how many it takes');
  await typed('0.1', '0'); s = await once();
  must(s.home === 3600 && s.dots === 0 && s.maxdots === 2000 && s.report.includes('The ends of the laps, too many here to mark with dots, lie on the dashed circle.') && !s.report.includes('The dots,') && s.fails.length === 0,
    '0.1 and 0 (3,600 laps): no dots are drawn, and the report says the laps are too many to mark, not that there are dots', s.report.slice(-90));
  await typed('22.5', '45'); s = await once();
  must(!T.forecast(22500, 45000).home && s.home === 0 && s.say.includes('it never comes home') && s.say.includes('√8 = 2.828') && s.report.includes('× √8.'), '22.5 and 45: an odd amount whose turtle marches away, because its first turn is not a whole number of degrees', s.report.slice(0, 80));
  await typed('25', '210'); s = await once();
  { const e = (await inFrame()).e, c = e.circle, pts = await pathOf(), pc = pyCorners(25000, 210000, pts); let dash = 0;
    for (const [x, y] of [[(c.x0 + c.x1) / 2, c.y0], [(c.x0 + c.x1) / 2, c.y1], [c.x0, (c.y0 + c.y1) / 2], [c.x1, (c.y0 + c.y1) / 2]]) if ((await dashNear(x, y, 7)) > 0) dash++;
    must(s.home === 36 && table.whole[210][25] === 36 && pc && pc.worst < 1e-9 && c.x0 >= 2 && c.y0 >= 2 && c.x1 <= e.W - 2 && c.y1 <= e.H - 2 && dash === 4, '25 and 210 (the turtle whose circle the referee found cut off): the dashed circle is whole inside the frame, with dashes at its top, bottom, left and right', dash + ' of 4; circle y ' + c.y0.toFixed(0) + ' to ' + c.y1.toFixed(0) + ' of ' + e.H); }
  await typed('180', '180'); s = await once();
  must(s.home === 4 && s.there === 2 && s.report.includes('first at step 2, but was not then home') && s.guide === null && !s.report.includes('dashed'), '180 and 180: it stands on its start at step 2 without being home, the report says so, and no circle is drawn or spoken of', s.report.slice(0, 120));
  await typed('2', '20'); s = await once(); must(!s.report.includes('stood on its starting point before'), 'and the book\'s turtle, which does not, is not said to');
  await typed('0', '0'); s = await once();
  must(s.home === 0 && s.say.includes('It never turns') && s.total === 40 && s.report.includes('40 laps done, and it is 40.000 steps from its start') && (await inFrame()).ok, '0 and 0: it never turns, and walks straight on', s.report.slice(0, 70));
  await typed('-2', '-20'); s = await once();
  { const pts = await pathOf(), w = T.walk(2 * U, 20 * U, 90); let mirror = 0; for (let k = 0; k <= 90; k++) mirror = pts[k] ? Math.max(mirror, Math.abs(pts[k][0] + w.xs[k]), Math.abs(pts[k][1] - w.ys[k])) : 9;
    must(s.home === 90 && mirror < 1e-9 && s.report.includes('its next turn would be −2° again'), '-2 and -20: the book\'s figure in a mirror, home at step 90, and the report gives the first turn as it was typed', 'worst ' + mirror.toExponential(1)); }

  // ---- 6. the map, by hand
  const mbox = async () => p.locator('#map').boundingBox();
  const cell = async (inc, a) => { const bx = await mbox(); return [bx.x + (inc - 1 + 0.5) / 359 * bx.width, bx.y + (359 - a + 0.5) / 360 * bx.height]; };
  await p.locator('#map').scrollIntoViewIfNeeded();
  let tried6 = 0, dark6 = 0; const bad6 = [];
  for (const [inc, a] of [[20, 10], [20, 2], [7, 0], [2, 155], [135, 112], [180, 90], [359, 359], [1, 0], [240, 121]]) {
    const xy = await cell(inc, a); await p.mouse.move(xy[0], xy[1]); await p.waitForTimeout(30); const txt = (await state()).mapsay, py = table.whole[inc][a], q = 360 / T.gcd(inc, 360);
    const ok = txt.startsWith('First turn ' + a + '°, add ' + inc + '°: ') && (py ? txt.endsWith('home after ' + T.commas(py) + ' steps.') : txt.includes('never comes home') && txt.includes('√' + q + ' = ' + Math.sqrt(q).toFixed(3)) && txt.includes('every lap of ' + q));
    tried6++; if (py === 0) dark6++; if (!ok) bad6.push(txt); }
  must(tried6 === 9 && dark6 === 3 && bad6.length === 0, 'pointing at a dot names its turtle and says what Python\'s walk found for it (nine dots, three of them dark)', bad6.join(' | '));
  { const xy = await cell(40, 30); await p.mouse.click(xy[0], xy[1]); await p.waitForTimeout(700); s = await state();
    const py = table.whole[40][30];
    must(await p.inputValue('#angle') === '30' && await p.inputValue('#inc') === '40' && s.A === 30 * U && s.I === 40 * U && s.pick && s.pick.inc === 40 && s.pick.angle === 30 && s.done && s.home === py && s.report.startsWith('Step ' + py + ': home.'),
      'clicking a dot puts that turtle\'s numbers in the boxes and sends it off', 'first turn 30, add 40: home at step ' + s.home);
    const ring = await p.evaluate(([inc, a]) => { const c = document.getElementById('map'), cx = (inc - 1 + 0.5) * c.width / 359, cy = (359 - a + 0.5) * c.height / 360, d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let on = 0, far = 0;
      for (let y = 0; y < c.height; y++) for (let x = 0; x < c.width; x++) { const i = 4 * (y * c.width + x); if (d[i] > 150 && d[i + 1] < 90 && d[i + 2] < 60 && d[i] - d[i + 1] > 70) { const r = Math.hypot(x - cx, y - cy); if (r > 6 && r < 12) on++; else far++; } } return { on, far }; }, [40, 30]);
    must(ring.on > 30 && ring.far === 0, 'and a ring on the map marks that dot and no other', ring.on + ' ring pixels, ' + ring.far + ' elsewhere'); }
  { const xy = await cell(2, 155); await p.mouse.click(xy[0], xy[1]); await p.waitForTimeout(700); s = await state();
    must(s.pick.inc === 2 && s.pick.angle === 155 && s.home === 0 && s.say.includes('it never comes home') && s.say.includes('√180') && table.whole[2][155] === 0, 'clicking a dark dot sends off a turtle that never comes home', s.report.slice(0, 60)); }
  await p.screenshot({ path: path.join(out, 'turtle-after.png'), fullPage: true });

  // ---- 7. the texts that do not change
  { const txt = await p.evaluate(() => document.querySelector('main').textContent.replace(/\s+/g, ' '));
    must(txt.includes('all 129,240 whole-degree turtles were walked step by step') && txt.includes('Nobody has checked any of it by hand') && txt.includes('reached the same answer by the same argument') && txt.includes("found the book's exercise answered in print under the turtle's own name; both searches were short"), 'the folded note says what was checked, by what, who else worked it, and what was not found');
    must((await p.getAttribute('a[href^="https://oolong.co.uk"]', 'href')) === 'https://oolong.co.uk/curlicue/', 'and it links to the page that asked the question of the same turtle');
    must(await p.locator('a[href="README.md"]').count() === 1 && fs.existsSync(path.join(path.dirname(path.resolve(process.argv[4])), 'README.md')), 'and it links to the write-up, which is there beside the page\'s files');
    // the first folded note: its formula as printed, worked for turtles and set beside core.js; and its other statements of fact
    const printed = txt.includes('T = q × (first turn) + 180° × p × (q − 1)'); let agree = 0, cases = 0;
    for (const [a, i] of [[2, 20], [10, 20], [0, 7], [112, 135], [30, 180], [1, 2], [89, 180], [25, 210], [5, 340]]) { const f = T.forecast(a * U, i * U), g = T.gcd(i, 360), q = 360 / g, pp = i / g; cases++; if (f.q === q && T.mod(q * a + 180 * pp * (q - 1), 360) * U === f.T) agree++; }
    must(printed && agree === cases && cases === 9, 'the first folded note prints T = q × (first turn) + 180° × p × (q − 1); worked as printed for nine turtles it is the turning core.js uses', agree + ' of ' + cases);
    must(txt.includes('(20° is 1/18)') && T.forecast(0, 20 * U).p === 1 && T.forecast(0, 20 * U).q === 18 && txt.includes('one lap ends exactly √q steps from where it began, never nought') && txt.includes('after v laps, where T is u/v of a turn in lowest terms')
      && txt.includes('every lap is the first lap again, moved along without turning') && txt.includes('or all fall on the start, when a lap happens to end there'), 'and says that 20° is 1/18 of a turn, that home comes after v laps, and that a marching lap ends exactly √q steps from where it began');
    must(txt.includes('did not in 720 steps') && txt.includes('Lehmer drew such paths in 1976 and gave, as well known, how far one or two laps carry the turtle') && txt.includes('“Home” means back where it began, facing the way it began, and about to make its first turn again'), 'the second note says the walk was of 720 steps and gives Lehmer his due; the note under the buttons says what home means'); }

  // ---- 8. narrow screens, and a change of width
  for (const wpx of [390, 320]) {
    const ph = await b.newPage({ viewport: { width: wpx, height: 800 }, deviceScaleFactor: 3 }); await ph.goto('file://' + page); await ph.waitForTimeout(400);
    await ph.selectOption('#pace', 'once'); await ph.click('#go'); await ph.waitForTimeout(200);
    const lay = await ph.evaluate(() => { const r = id => document.getElementById(id).getBoundingClientRect(), f = r('field'), t = r('turtle'), m = r('map'), st = document.querySelector('.stage').getBoundingClientRect();
      return { sw: document.documentElement.scrollWidth, iw: window.innerWidth, right: Math.max(f.right, m.right, st.right), over: Math.max(Math.abs(f.left - t.left), Math.abs(f.top - t.top), Math.abs(f.width - t.width), Math.abs(f.height - t.height)) }; });
    const st = await state(ph), fr = await inFrame(ph), ik = await ink(ph);
    must(lay.sw <= lay.iw && lay.right <= lay.iw - 13.5 && lay.over < 0.5 && st.done && st.home === 90 && fr.ok && ik.line > 1500 && ik.x0 >= 2 && ik.x1 <= ik.w - 3 && ik.y0 >= 2 && ik.y1 <= ik.h - 3,
      'on a screen ' + wpx + ' px wide nothing runs off the side, and the figure is drawn whole inside its frame', 'page ' + lay.sw + ' of ' + lay.iw + ' px, the pictures end ' + (lay.iw - lay.right).toFixed(1) + ' px from the edge; canvas ' + ik.w + ' by ' + ik.h + ', line x ' + ik.x0 + ' to ' + ik.x1);
    if (wpx === 390) await ph.screenshot({ path: path.join(out, 'turtle-phone.png'), fullPage: true });
    await ph.fill('#angle', '312'); await ph.fill('#inc', '144'); await ph.click('#go'); await ph.waitForTimeout(200);
    { const e2 = (await inFrame(ph)).e, c = e2.circle, st2 = await state(ph);
      must(st2.done && c && c.x0 >= 2 && c.y0 >= 2 && c.x1 <= e2.W - 2 && c.y1 <= e2.H - 2 && e2.x0 >= 2 && e2.x1 <= e2.W - 2, 'and there the dashed circle of 312 and 144 (the worst the referee found on a small screen) is whole inside the frame', 'circle x ' + c.x0.toFixed(0) + ' to ' + c.x1.toFixed(0) + ' of ' + e2.W + ', y ' + c.y0.toFixed(0) + ' to ' + c.y1.toFixed(0) + ' of ' + e2.H); }
    await ph.close(); }
  await p.click('#preset0'); await p.waitForTimeout(150); await p.setViewportSize({ width: 640, height: 900 }); await p.waitForTimeout(300);
  { const st = await state(), fr = await inFrame(), ik = await ink(), mk = await marker();
    must(st.done && st.drawn === 90 && fr.ok && ik.line > 1200 && Math.abs(ik.x0 - fr.e.x0) < 4 && Math.abs(ik.x1 - fr.e.x1) < 4 && mk.n > 40 && Math.hypot(mk.x - mk.at[0], mk.y - mk.at[1]) < 6, 'when the window is made narrower the finished figure is drawn again to fit, with its turtle', 'canvas ' + ik.w + ' px wide'); }

  must(errs.length === 0, 'no script error in all of this', errs.join(' | ').slice(0, 200));
  console.log('PAGE TEST: ' + asserts + ' assertions, ' + fails.length + ' failed' + (fails.length ? ': ' + fails.join('; ').slice(0, 400) : ''));
  await b.close(); process.exit(fails.length ? 1 : 0);
})().catch(async e => { asserts++; fails.unshift('the test stopped (' + String(e).split('\n')[0].slice(0, 120) + ')');
  console.log('FAIL the test stopped: ' + String(e).slice(0, 300));
  console.log('PAGE TEST: ' + asserts + ' assertions, ' + fails.length + ' failed: ' + fails.join('; ').slice(0, 400));
  try { if (browser) await browser.close(); } catch (x) {} process.exit(2); });
