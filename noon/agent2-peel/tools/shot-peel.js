// Headless checks of the page "Peeling a cloud": what it shows against ocore.js run here in node.
// usage: node shot-peel.js PAGE.html OUTDIR OCORE.js      (run from ~/web, where playwright is)
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [page, out] = [path.resolve(process.argv[2]), path.resolve(process.argv[3])]; const O = require(path.resolve(process.argv[4]));
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1100, height: 1600 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + page); await p.waitForTimeout(500);
  const text = sel => p.evaluate(s => document.querySelector(s).textContent, sel), count = sel => p.evaluate(s => document.querySelectorAll(s).length, sel);
  const fails = []; let asserts = 0; const must = (cond, what) => { asserts++; if (!cond) fails.push(what); };
  const fmt = v => String(Math.round(v)).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  const tiles = () => p.evaluate(() => [...document.querySelectorAll('.tile')].map(t => ({ v: t.querySelector('.v').textContent, d: t.querySelector('.d').textContent })));
  const attrs = () => p.evaluate(() => { const f = document.querySelector('#fig1'); return { shape: f.getAttribute('data-shape'), n: Number(f.getAttribute('data-n')), seed: Number(f.getAttribute('data-seed')), stretched: f.getAttribute('data-stretched') === '1', poly: f.getAttribute('data-poly'), view: f.getAttribute('data-view').split(',').map(Number) }; });
  const setK = async k => { await p.evaluate(k => { const e = document.querySelector('#k'); e.value = String(k); e.dispatchEvent(new Event('input', { bubbles: true })); }, k); await p.waitForTimeout(30); };
  // the cloud the page says it is showing, made again here
  const again = a => { const base = O.sample(a.shape, a.n, O.rng(a.seed), a.poly ? JSON.parse(a.poly) : undefined); const c = a.stretched ? O.stretch(base.x, base.y) : base; return { c, base, peel: O.peel(c.x, c.y) }; };
  const polys = () => p.evaluate(() => [...document.querySelectorAll('#over polygon, #over polyline')].map(e => ({ cls: e.getAttribute('class'), layer: Number(e.getAttribute('data-layer')), pts: e.getAttribute('points').trim().split(/\s+/).map(q => q.split(',').map(Number)) })));
  const inked = () => p.evaluate(() => { const c = document.querySelector('#cv'), g = c.getContext('2d'), d = g.getImageData(0, 0, c.width, c.height).data; let n = 0, x0 = 1e9, x1 = -1, y0 = 1e9, y1 = -1;
    for (let y = 0; y < c.height; y++) for (let x = 0; x < c.width; x++) { const i = 4 * (y * c.width + x); if (d[i] !== 19 || d[i + 1] !== 19 || d[i + 2] !== 18) { n++; if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; } } return { n, x0, x1, y0, y1 }; });
  const checkCloud = async (label, k) => {      // tiles, sentence, rings and canvas against the cloud made again here
    const a = await attrs(), w = again(a), N = w.peel.layers, t = await tiles(), D = O.discLayers(a.n), diff = 100 * (N / D - 1);
    must(t[0].v === fmt(N) && t[0].d.includes(fmt(a.n) + ' points') && t[0].d.includes('the first layer has ' + w.peel.sizes[1] + ', the last ' + w.peel.sizes[N] + '.'), label + ': the count of layers and the first and last layers');
    const spread = 1.32 * Math.pow(a.n / 10000, 0.176), round = a.shape === 'disc' || a.shape === 'ellipse';
    must(t[1].v === 'about ' + fmt(D) && t[2].v === (diff >= 0 ? '+' : '−') + Math.abs(diff).toFixed(1) + '%' && t[2].d.includes('by about ' + spread.toFixed(1) + ' layers') && round === t[2].d.includes('(' + (100 * spread / D).toFixed(1) + '%)') && round !== t[2].d.includes('a square has 4.8% more'), label + ': the disc of as many points, the difference, and the spread from chance');
    await setK(k); const say = await text('#say1'); let left = 0; for (let i = k + 1; i <= N; i++) left += w.peel.sizes[i];
    must(k < N ? say.includes(fmt(k) + ' of ' + fmt(N) + ' layers taken away; ' + fmt(left) + ' of ' + fmt(a.n) + ' points are left. The next layer has ' + w.peel.sizes[k + 1] + ' points.') : say.includes('All ' + fmt(N) + ' layers are taken away'), label + ': the sentence at ' + k + ' layers taken away');
    const ps = await polys(), [s, ox, oy] = a.view; let good = 0, n = 0, inFrame = true;
    for (const q of ps) { n++; const ring = O.ring(w.c.x, w.c.y, w.peel.depth, q.layer); let ok = q.pts.length === ring.length && q.pts.length === w.peel.sizes[q.layer];
      for (let i = 0; ok && i < ring.length; i++) { if (Math.abs(q.pts[i][0] - (ox + s * w.c.x[ring[i]])) > 0.06 || Math.abs(q.pts[i][1] - (oy - s * w.c.y[ring[i]])) > 0.06) ok = false; }
      for (const pt of q.pts) if (pt[0] < 0 || pt[0] > 1000 || pt[1] < 0 || pt[1] > 640) inFrame = false; if (ok) good++; }
    const cur = ps.filter(q => q.cls === 'current'), tenth = ps.filter(q => q.cls === 'tenth'), wantTenth = []; for (let bb = 1; bb < 10; bb++) { const kk = 1 + Math.floor(bb * N / 10); if (kk > k + 1 && kk <= N && w.peel.sizes[kk] >= 3) wantTenth.push(kk); }
    must(good === n && inFrame && (k < N ? cur.length === 1 && cur[0].layer === k + 1 : cur.length === 0) && tenth.map(q => q.layer).join() === wantTenth.join(), label + ': the rings drawn are the layers (' + good + ' of ' + n + '), in the frame, the orange one the next to go');
    const ink = await inked(); must((left > 0 ? ink.n > 0 && ink.x0 >= 8 && ink.x1 <= 991 && ink.y0 >= 8 && ink.y1 <= 631 : ink.n === 0), label + ': the points drawn are inside the picture' + (left > 0 ? '' : ' (none, when all are taken away)'));
    return { a, w, N, ink };
  };
  // every shape offered, at three stages of the peeling
  for (const sh of ['disc', 'ellipse', 'square', 'triangle']) {
    await p.selectOption('#shape', sh); await p.waitForTimeout(300); const a = await attrs(); must(a.shape === sh && a.n === 10000, 'the shape ' + sh + ' is shown with 10,000 points');
    const r0 = await checkCloud(sh, 0), r1 = await checkCloud(sh + ', half way', Math.round(r0.N / 2)), r2 = await checkCloud(sh + ', all gone', r0.N);
    must(r1.ink.n < r0.ink.n && r2.ink.n === 0, sh + ': fewer points drawn as layers go, none at the end'); console.log(`${sh}: seed ${a.seed}, ${r0.N} layers, ${r0.ink.n} pixels inked at the start, ${r1.ink.n} half way`);
  }
  // the shade runs from dark at the rim to light in the middle, as the legend says
  { await p.selectOption('#shape', 'disc'); await p.waitForTimeout(300); await setK(0); const a = await attrs(), [s, ox, oy] = a.view;
    const light = await p.evaluate(([s, ox, oy, R]) => { const c = document.querySelector('#cv'), g = c.getContext('2d'), d = g.getImageData(0, 0, c.width, c.height).data; let inn = [0, 0], outr = [0, 0];
      for (let y = 0; y < c.height; y++) for (let x = 0; x < c.width; x++) { const i = 4 * (y * c.width + x); if (d[i] === 19 && d[i + 1] === 19 && d[i + 2] === 18) continue; const r = Math.hypot(x - ox, y - oy) / (s * R), L = d[i] + d[i + 1] + d[i + 2]; if (r < 0.25) { inn[0] += L; inn[1]++; } else if (r > 0.9) { outr[0] += L; outr[1]++; } }
      return [inn[0] / inn[1], outr[0] / outr[1]]; }, [s, ox, oy, O.RAD]);
    must(light[0] > light[1] + 60, 'points near the middle are drawn lighter than points near the rim (' + light.map(v => v.toFixed(0)).join(' against ') + ')'); }
  // number of points, a new cloud
  { await p.selectOption('#shape', 'disc'); await p.selectOption('#n', '2000'); await p.waitForTimeout(200); const a = await attrs(); must(a.n === 2000, 'two thousand points when asked'); await checkCloud('2,000 points', 3);
    await setK(20); await p.click('#new'); await p.waitForTimeout(200); const a2 = await attrs(); must(a2.seed === a.seed + 1 && (await p.inputValue('#k')) === '0' && (await text('#say1')).startsWith('0 of '), 'a new cloud is another cloud, with nothing taken away'); await checkCloud('a new cloud', 0); }
  // stretching
  { await p.selectOption('#n', '10000'); await p.selectOption('#shape', 'square'); await p.waitForTimeout(300); const before = await checkCloud('square before stretching', 5);
    await p.click('#stretch'); await p.waitForTimeout(300); const a = await attrs(), say = await text('#say1'); const after = await checkCloud('square stretched', 5);
    let same = 0; for (let i = 0; i < a.n; i++) if (before.w.peel.depth[i] === after.w.peel.depth[i]) same++;
    must(a.stretched && same === a.n && say.includes('every one of the 10,000 points is on the same layer as before') && (await p.evaluate(() => document.querySelector('#stretch').getAttribute('aria-pressed'))) === 'true' && after.N === before.N, 'stretched and sheared: the page says every point kept its layer, and so it is here');
    must(Math.abs(after.a.view[0] - before.a.view[0]) > 1e-9 && after.ink.x1 - after.ink.x0 > 1.5 * (before.ink.x1 - before.ink.x0), 'the stretched cloud is drawn wider and still fits');
    await p.click('#stretch'); await p.waitForTimeout(300); const a3 = await attrs(); must(!a3.stretched && !(await text('#say1')).includes('Stretched'), 'unstretched again');
    await p.click('#stretch'); await p.waitForTimeout(200); await p.selectOption('#shape', 'triangle'); await p.waitForTimeout(300); { const a4 = await attrs(); must(a4.shape === 'triangle' && !a4.stretched && (await p.evaluate(() => document.querySelector('#stretch').getAttribute('aria-pressed'))) === 'false', 'a change of shape begins unstretched'); await checkCloud('triangle after a stretched square', 2); } await p.selectOption('#shape', 'square'); await p.waitForTimeout(300); console.log('stretch: ' + same + ' of ' + a.n + ' points kept their layer'); }
  // every tenth
  { await setK(0); const n1 = await count('#over .tenth'); await p.click('#tenths'); await p.waitForTimeout(60); const n2 = await count('#over .tenth'); await p.click('#tenths'); await p.waitForTimeout(60); must(n1 === 9 && n2 === 0 && (await count('#over .tenth')) === 9, 'the nine rings can be hidden and shown'); }
  // the chart: both lines read back from the drawing through the axis labels
  { await p.selectOption('#shape', 'disc'); await p.waitForTimeout(300); const a = await attrs(), w = again(a), N = w.peel.layers;
    const g = await p.evaluate(() => { const svg = document.querySelector('#chart'), T = [...svg.querySelectorAll('text')]; const box = id => { const q = document.getElementById(id).getBBox(); return [q.x, q.y, q.x + q.width, q.y + q.height]; };
      return { yt: T.filter(t => t.getAttribute('text-anchor') === 'end').map(t => [Number(t.textContent), Number(t.getAttribute('y')) - 4]), xt: T.filter(t => t.getAttribute('text-anchor') === 'middle' && /^\d+$/.test(t.textContent)).map(t => [Number(t.textContent), Number(t.getAttribute('x'))]),
        cloud: document.getElementById('line-cloud').getAttribute('d'), disc: document.getElementById('line-disc').getAttribute('d'), b1: box('line-cloud'), b2: box('line-disc'), labels: T.map(t => { const q = t.getBBox(); return [q.x, q.x + q.width, q.y, q.y + q.height]; }), names: T.filter(t => t.getAttribute('class') === 'dlabel').map(t => t.textContent) }; });
    const lin = pts => { const a0 = pts[0], c = pts[pts.length - 1], k = (c[0] - a0[0]) / (c[1] - a0[1]); return v => a0[0] + (v - a0[1]) * k; }, yv = lin(g.yt), xv = lin(g.xt);
    const read = d => [...d.matchAll(/[ML]([-\d.]+),([-\d.]+)/g)].map(m => [xv(Number(m[1])), yv(Number(m[2]))]);
    const c = read(g.cloud), d = read(g.disc); let good = 0; for (let k = 1; k <= N; k++) if (c[k - 1] && Math.abs(c[k - 1][0] - k) < 0.2 && Math.abs(c[k - 1][1] - w.peel.sizes[k]) < 0.25) good++;
    let goodD = 0; for (let k = 1; k <= d.length; k++) if (Math.abs(d[k - 1][1] - O.discSize(a.n, k)) < 0.25) goodD++;
    must(c.length === N && good === N && d.length >= N - 3 && goodD === d.length, 'the chart: the line of this cloud, read back from the drawing, is the size of every layer (' + good + ' of ' + N + '), and the dashed line the formula');
    const inb = q => q[0] >= 47 && q[2] <= 981 && q[1] >= 25 && q[3] <= 267; must(inb(g.b1) && inb(g.b2) && g.labels.every(l => l[0] >= -0.5 && l[1] <= 1000.5 && l[2] >= -0.5 && l[3] <= 300.5) && g.names.join('|') === 'this cloud|a disc, by the formula', 'the chart stays in its frame, labels and all, and names both lines');
    const rows = await p.evaluate(() => [...document.querySelectorAll('#tab2 tr')].slice(1).map(tr => [...tr.children].map(td => td.textContent)));
    must(rows.length === N && rows.every((r, i) => r[0] === String(i + 1) && r[1] === String(w.peel.sizes[i + 1]) && r[2] === O.discSize(a.n, i + 1).toFixed(1)), 'the table of layers');
    const shown = () => p.evaluate(() => getComputedStyle(document.querySelector('#tab2')).display); const s0 = await shown(); await p.click('#t2'); const s1 = await shown(); await p.click('#t2'); must(s0 === 'none' && s1 === 'block' && (await shown()) === 'none', 'the Table button opens and closes the table');
    await p.locator('#chart').scrollIntoViewIfNeeded(); const bx = await p.locator('#chart').boundingBox(), sxk = k => bx.x + (48 + (k - 1) / (N - 1) * (1000 - 48 - 20)) / 1000 * bx.width;
    await p.mouse.move(sxk(40), bx.y + bx.height / 2); await p.waitForTimeout(60); const tip = await text('#tip2'), say2 = await text('#say2');
    must(tip === 'Layer 40 of ' + N + ' has ' + w.peel.sizes[40] + ' points; a disc, by the formula, ' + O.discSize(a.n, 40).toFixed(1) + '.' && say2 === tip && (await p.evaluate(() => getComputedStyle(document.querySelector('#tip2')).display)) === 'block', 'hovering over layer 40 names its size and the formula\'s');
    await p.mouse.move(sxk(N), bx.y + bx.height / 2); await p.waitForTimeout(60); { const tb = await p.locator('#tip2').boundingBox(), fb = await p.locator('#fig2').boundingBox(); must(tb.x >= fb.x && tb.x + tb.width <= fb.x + fb.width + 1 && tb.width >= 200 && (await text('#tip2')).startsWith('Layer ' + N + ' of'), 'at the right edge the tooltip stays inside its figure and is not squeezed'); }
    await p.mouse.click(sxk(60), bx.y + bx.height / 2); await p.waitForTimeout(80); must((await p.inputValue('#k')) === '59' && (await text('#say1')).startsWith('59 of ' + fmt(N)) && Math.abs((await p.evaluate(() => Number(document.querySelector('#pick').getAttribute('x1')))) - (48 + 59 / (N - 1) * 932)) < 0.5, 'a click on layer 60 takes away the 59 before it, and the mark stands there');
    await p.mouse.move(5, 5); await p.locator('#chart').focus(); await p.keyboard.press('ArrowRight'); await p.keyboard.press('ArrowRight'); await p.waitForTimeout(40); const kt = await text('#say2'); await p.keyboard.press('Enter'); await p.waitForTimeout(60);
    must(kt.startsWith('Layer 62 of') && (await p.inputValue('#k')) === '61', 'two presses of the right arrow and Enter go two layers on');
    await p.mouse.move(5, 5); await p.locator('#k').focus(); await p.waitForTimeout(40); { let aa = a, ww = w, tries = 0; while (ww.peel.sizes[1] === ww.peel.sizes[2] && tries++ < 20) { await p.click('#new'); await p.waitForTimeout(250); aa = await attrs(); ww = again(aa); }
      const first = await text('#say2'); must(ww.peel.sizes[1] !== ww.peel.sizes[2] && first.includes('The first layer has ' + ww.peel.sizes[1] + ' points, about ' + (ww.peel.sizes[1] / Math.pow(aa.n, 1 / 3)).toFixed(2) + ' times the cube root of 10,000'), 'at rest the chart\'s sentence gives the first layer (on a cloud whose first two layers differ)'); }
    console.log('chart: read back ' + good + ' of ' + N + ' layers'); }
  // Play runs to the end: asked, not slept
  { await setK(0); await p.click('#play'); const lab = await text('#play'); let k = 0, done = false; for (let i = 0; i < 2400 && !done; i++) { await p.waitForTimeout(50); done = (await text('#play')) === 'Play'; } k = Number(await p.inputValue('#k'));      /* the slider is read after the end, not beside it */
    const N = Number(await p.evaluate(() => document.querySelector('#k').max)); must(lab === 'Pause' && done && k === N && (await text('#say1')).startsWith('All '), 'Play takes every layer away and stops');
    await p.click('#play'); await p.waitForTimeout(30); const k2 = Number(await p.inputValue('#k')); await p.click('#play'); must(k2 < N && (await text('#play')) === 'Play', 'Play at the end begins again; a second press pauses'); console.log('play: reached ' + k + ' of ' + N); }
  // a shape of one's own
  { await p.selectOption('#shape', 'own'); await p.waitForTimeout(100); const note = await text('#notice'); must(note.includes('Draw a closed loop') && (await p.evaluate(() => getComputedStyle(document.querySelector('#notice')).display)) === 'block', 'choosing "your own" asks for a loop');
    { await p.click('#stretch'); await p.waitForTimeout(100); must((await p.evaluate(() => document.querySelector('#stretch').getAttribute('aria-pressed'))) === 'false' && !(await text('#say1')).includes('Stretched'), 'with no shape drawn yet, Stretch does nothing'); }
    { const before = await tiles(); await p.selectOption('#n', '2000'); await p.waitForTimeout(150); const cb = await p.locator('#chart').boundingBox(); await p.locator('#chart').scrollIntoViewIfNeeded(); const cb2 = await p.locator('#chart').boundingBox(); await p.mouse.move(cb2.x + cb2.width * 0.3, cb2.y + cb2.height / 2); await p.waitForTimeout(60); const tip = await text('#tip2'); await p.mouse.move(5, 5); await p.waitForTimeout(60);
      const N0 = Number(await p.evaluate(() => document.querySelector('#k').max)), kk = Number(/Layer (\d+) of/.exec(tip)[1]);
      must(JSON.stringify(await tiles()) === JSON.stringify(before) && before[0].d.includes('10,000 points') && tip.includes('a disc, by the formula, ' + O.discSize(10000, kk).toFixed(1)) && (await text('#say2')).includes('times the cube root of 10,000') && (await attrs()).n === 10000, 'with no shape drawn yet, changing the number of points leaves the cloud shown, and its sentences, as they were (the referee\'s first fault)'); }
    await p.locator('#stage').scrollIntoViewIfNeeded(); const bx = await p.locator('#stage').boundingBox(); const loop = async f => { const n = 80; await p.mouse.move(bx.x + bx.width * f(0)[0], bx.y + bx.height * f(0)[1]); await p.mouse.down(); for (let i = 1; i <= n; i++) await p.mouse.move(bx.x + bx.width * f(i / n)[0], bx.y + bx.height * f(i / n)[1]); await p.mouse.up(); await p.waitForTimeout(300); };
    const T = 2 * Math.PI, bean = t => [0.42 + 0.26 * Math.cos(T * t) * (1 + 0.35 * Math.cos(2 * T * t)), 0.36 + 0.24 * Math.sin(T * t)]; await loop(bean);          // a bean, not convex, up and to the left of the middle
    const a = await attrs(), poly = JSON.parse(a.poly); let insideAll = true; const w = again(a); for (let i = 0; i < a.n; i++) if (!O.inside(poly.x, poly.y, w.c.x[i], w.c.y[i])) insideAll = false;
    must(a.n === 2000, 'the number of points chosen while there was no shape is used for the first cloud of the new shape'); await p.selectOption('#n', '10000'); await p.waitForTimeout(300); { const a9 = await attrs(); Object.assign(a, a9); const w9 = again(a9); w.c = w9.c; w.peel = w9.peel; }
    const mx = poly.x.reduce((u, v) => u + v, 0) / poly.x.length, my = poly.y.reduce((u, v) => u + v, 0) / poly.y.length;
    const sc = 1.6 * O.RAD / (640 / 2 - 20), want = []; for (let i = 0; i <= 80; i++) { const q = bean(i / 80); want.push([(q[0] * 1000 - 500) * sc, (320 - q[1] * 640) * sc]); }
    const ext = (arr, f) => f(...arr), near = (u, v) => Math.abs(u - v) < 0.03 * O.RAD;
    must(a.shape === 'own' && poly.x.length >= 20 && insideAll && (await text('#notice')) === '' && mx < -0.1 * O.RAD && my > 0.2 * O.RAD && near(ext(poly.x, Math.min), ext(want.map(q => q[0]), Math.min)) && near(ext(poly.x, Math.max), ext(want.map(q => q[0]), Math.max)) && near(ext(poly.y, Math.min), ext(want.map(q => q[1]), Math.min)) && near(ext(poly.y, Math.max), ext(want.map(q => q[1]), Math.max)),
      'a loop drawn on the picture becomes the shape, the right way up and the right size, and the points are inside it');
    { let x0 = Infinity, x1 = -Infinity; for (let i = 0; i < a.n; i++) { if (w.c.x[i] < x0) x0 = w.c.x[i]; if (w.c.x[i] > x1) x1 = w.c.x[i]; } must(near(x0, Math.min(...poly.x)) && near(x1, Math.max(...poly.x)) && Math.min(...poly.x) < -1.7 * O.RAD, 'the cloud fills the shape drawn from end to end, though the loop reaches farther left than the built-in shapes do'); } await checkCloud('your own shape', 4);
    await p.click('#stretch'); await p.waitForTimeout(300); must((await text('#say1')).includes('is on the same layer as before'), 'your own shape, stretched: every point keeps its layer'); await checkCloud('your own shape, stretched', 4); await p.click('#stretch'); await p.waitForTimeout(200);
    const before = JSON.stringify(await attrs()); await loop(t => [0.5 + 0.02 * Math.cos(T * t), 0.5 + 0.02 * Math.sin(T * t)]); must((await text('#notice')).includes('too small') && JSON.stringify(await attrs()) === before, 'a loop too small is refused, and the cloud stays');
    await p.click('#new'); await p.waitForTimeout(300); must((await text('#notice')) === '' && (await attrs()).seed === JSON.parse(before).seed + 1, 'a new cloud in the same shape clears the notice'); await checkCloud('your own shape, a new cloud', 0);
    await loop(t => [0.5 + 0.4 * Math.sin(T * t), 0.5 + 0.35 * Math.sin(2 * T * t)]); { const a8 = await attrs(), w8 = again(a8), poly8 = JSON.parse(a8.poly); let lft = 0, rgt = 0, ins = true; for (let i = 0; i < a8.n; i++) { if (w8.c.x[i] < 0) lft++; else rgt++; if (!O.inside(poly8.x, poly8.y, w8.c.x[i], w8.c.y[i])) ins = false; }
      must((await text('#notice')) === '' && ins && lft > 0.4 * a8.n && rgt > 0.4 * a8.n && a8.poly !== JSON.parse(before).poly, 'a large figure of eight is taken, and both its lobes are filled (the referee\'s second fault)'); await checkCloud('a figure of eight', 3); }
    { const polyBefore = (await attrs()).poly; await loop(t => [0.5 + 0.39 * Math.cos(T * t), 0.5 + 0.61 * Math.sin(T * t)]);          // begun inside the picture, carried above its top and below its bottom
      const a7 = await attrs(), poly7 = JSON.parse(a7.poly), edge = 1.6 * O.RAD / 300 * 320, top7 = Math.max(...poly7.y.map(Math.abs));
      must((await text('#notice')) === '' && a7.poly !== polyBefore && top7 <= edge + 2 && top7 >= edge - 0.02 * O.RAD, 'a loop dragged beyond the top and bottom of the picture is held at its edges (it reaches ' + (top7 / O.RAD).toFixed(2) + ' radii, the edge is at ' + (edge / O.RAD).toFixed(2) + ')'); await checkCloud('a loop larger than the picture', 2); }
    { const t0 = Date.now(); await p.selectOption('#n', '60000'); await p.waitForTimeout(100); await p.click('#stretch'); await p.waitForTimeout(100); const ms = Date.now() - t0, a6 = await attrs(); must(ms < 60000 && a6.n === 60000 && a6.stretched && (await text('#say1')).includes('every one of the 60,000 points'), 'the slowest view (your own shape, 60,000 points, stretched) takes ' + ms + ' ms');
      await p.click('#stretch'); await p.selectOption('#n', '10000'); await p.waitForTimeout(300); console.log('slowest view: ' + ms + ' ms'); }
    await p.locator('#fig1').screenshot({ path: path.join(out, 'own.png') }); console.log('own shape: ' + poly.x.length + ' corners, ' + w.peel.layers + ' layers'); }
  // the largest cloud offered
  { await p.selectOption('#shape', 'disc'); const t0 = Date.now(); await p.selectOption('#n', '60000'); await p.waitForTimeout(100); const ms = Date.now() - t0; const r = await checkCloud('60,000 points', 100); must(ms < 30000 && r.a.n === 60000, 'sixty thousand points are peeled in ' + ms + ' ms'); console.log('largest cloud: ' + ms + ' ms, ' + r.N + ' layers'); }
  await p.selectOption('#n', '10000'); await p.selectOption('#shape', 'triangle'); await p.waitForTimeout(300); await setK(30); await p.locator('#fig1').screenshot({ path: path.join(out, 'triangle.png') }); await p.screenshot({ path: path.join(out, 'page.png'), fullPage: true });
  for (const wv of [320, 360, 400]) { await p.setViewportSize({ width: wv, height: 900 }); await p.waitForTimeout(150); const sw = await p.evaluate(() => document.documentElement.scrollWidth); must(sw <= wv, 'no sideways scroll of the page at ' + wv + ' px (' + sw + ')'); if (wv === 360) await p.screenshot({ path: path.join(out, 'narrow.png'), fullPage: true }); }
  must(errs.length === 0, 'no error on the page');
  console.log('errors: ' + JSON.stringify(errs)); fails.forEach(f => console.log('FAILED: ' + f));
  console.log(`PAGE TEST: ${asserts} assertions, ${fails.length} failed`); await b.close(); process.exit(fails.length ? 1 : 0);
})();
