// pagetest.js: the page opened in a headless browser and read back: its numbers against lantern.py's (the cases file), its words, the
// pixels of its two pictures, and its controls worked as a visitor would work them.
// NODE_PATH=~/web/node_modules node pagetest.js PAGE.html CASES.json [PREFIX-for-pictures]
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const [html, casesFile, prefix] = process.argv.slice(2); const cases = JSON.parse(fs.readFileSync(casesFile, 'utf8'));
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1000, height: 1500 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + html);
  let pass = 0, fail = 0; const ok = (name, cond, detail) => { if (cond) { pass++; console.log('pass  ' + name); } else { fail++; console.log('FAIL  ' + name + (detail === undefined ? '' : '   ' + JSON.stringify(detail))); } };
  const near = (a, c, tol) => a !== null && a !== undefined && Math.abs(a - c) <= tol * Math.max(1, Math.abs(c));
  const read = () => p.evaluate(() => {
    const lum = (d, i) => 0.2126 * d[i] + 0.7152 * d[i + 1] + 0.0722 * d[i + 2];
    const cv = document.getElementById('seen'), c = cv.getContext('2d'), W = cv.width, H = cv.height, d = c.getImageData(0, 0, W, H).data;
    let mx = 0; for (let i = 0; i < d.length; i += 4) mx = Math.max(mx, lum(d, i));
    let top = -1, bottom = -1, n = 0, sum = 0, border = 0, grad = 0;
    for (let y = 0; y < H; y++) { let any = false; for (let x = 0; x < W; x++) { const l = lum(d, 4 * (y * W + x)); if (l > 16 && l >= 0.25 * mx) { any = true; n++; sum += l; } if (x < 2 || y < 2 || x >= W - 2 || y >= H - 2) border = Math.max(border, l); if (x > 0) grad = Math.max(grad, Math.abs(l - lum(d, 4 * (y * W + x - 1)))); } if (any) { if (top < 0) top = y; bottom = y; } }
    const cb = document.getElementById('behind'), b2 = cb.getContext('2d'); const px = (x, y) => { const q = b2.getImageData(Math.round(x), Math.round(y), 1, 1).data; return [q[0], q[1], q[2]]; };
    const S = window.SHOWN, marks = S.marks, pm = {}; for (const k in marks) pm[k] = px(marks[k][0], marks[k][1]);
    const mid = (a, c) => { let best = [0, 0, 0]; for (let dx = -1; dx <= 1; dx++) for (let dy = -1; dy <= 1; dy++) { const q = px((a[0] + c[0]) / 2 + dx, (a[1] + c[1]) / 2 + dy); if (q[0] > best[0]) best = q; } return best; };      // the reddest of the nine pixels about the middle of the rod (its edge is half-tinted)
    const rb = document.querySelector('input[name=mech]:checked');
    return { shown: S, state: window.STATE(), faults: window.FAULTS || [], controls: { mech: rb ? rb.value : null, shade: document.getElementById('shade').checked, slider: Number(document.getElementById('slider').value) }, texts: ['r-m', 'r-lens', 'r-patch', 'r-light'].map(id => document.getElementById(id).textContent),
      seen: { max: mx, top, bottom, n, mean: n ? sum / n : 0, border, grad, W, H }, behind: { W: cb.width, H: cb.height, pm, rodIK: marks.I && marks.K ? mid(marks.I, marks.K) : null, rodKN: marks.N && marks.K ? mid(marks.N, marks.K) : null, rodKL: marks.L && marks.K ? mid(marks.L, marks.K) : null } };
  });
  const kept = {};
  for (const c of cases) {
    await p.evaluate(c => window.SET({ m: c.m, mech: c.mech, shade: c.shade }), c); const g = await read(), o = g.shown.o, lab = c.mech + ' at ' + c.m + ' times' + (c.shade ? ', shaded' : '');
    kept[c.mech + '/' + c.m + '/' + c.shade] = g; const capDom = await p.locator('#cap-behind').textContent();
    ok(lab + ': the words under the side view give these rods\' own lengths' + (c.rods ? ' (' + c.rods.map(v => v.toFixed(2)).join(', ') + ')' : ' (none)'), c.rods ? c.rods.every(v => capDom.includes(v.toFixed(2))) && capDom.includes(c.rods[2].toFixed(2) + ', moves') : /No rods/.test(capDom), capDom);
    ok(lab + ': the buttons, the box and the slider stand as the state does', g.controls.mech === c.mech && g.controls.shade === c.shade && Math.abs(g.controls.slider - 1000 * Math.log(c.m) / Math.log(20)) <= 0.5, g.controls);
    if (c.jam) {
      ok(lab + ': the rods jam, the page says so, and no ghost is drawn', o.jam === true && /jam/.test(g.texts[1]) && g.seen.n === 0 && g.texts[2] === '', [o.jam, g.texts[1], g.seen.n]);
      continue;
    }
    ok(lab + ': lens, the place a sharp image wants, patch, size and brightness are lantern.py\'s to 1 part in 10^9', o.jam === false && near(o.s, c.s, 1e-9) && near(o.want, c.want, 1e-9) && near(o.patch, c.patch, 1e-9) && near(o.size, c.size, 1e-9) && near(o.light10, c.light10, 1e-9), [o, c]);
    ok(lab + ': the words carry those numbers', g.texts[0].includes(c.m.toFixed(2) + ' times') && g.texts[1].includes(c.s.toFixed(4)) && g.texts[1].includes(c.want.toFixed(4)) && g.texts[2].includes(c.patch.toFixed(4)) && (c.patch < 5e-5) === /sharp\.$/.test(g.texts[2]) && g.texts[3].includes(c.light10 >= 10 ? c.light10.toFixed(0) : c.light10.toFixed(2)) && g.texts[3].includes(c.shade ? 'under the same shade' : 'with no shade'), g.texts);
    const Hpx = Math.min(c.size * 0.3 * 62, 376), blurPx = Math.min(c.patch * 0.25 * 62 / 2, 60), span = g.seen.bottom - g.seen.top + 1, shut = Math.pow(c.light10, 1 / 2.2) * 0.62 < 0.06;
    if (shut) ok(lab + ': the shade is all but shut here, and the picture is all but dark', g.seen.max < 30 && g.seen.border < 30, [g.seen.max]);
    else ok(lab + ': a ghost is drawn, about ' + Hpx.toFixed(0) + ' pixels tall, and inside its frame', g.seen.n > 0 && Math.abs(span - Hpx) <= 0.12 * Hpx + 2.5 * blurPx + 6 && (blurPx > 12 || g.seen.border < 30), [span, Hpx, blurPx, g.seen.border]);
    const inside = Object.values(g.shown.marks).every(q => q[0] >= 0 && q[0] <= g.behind.W && q[1] >= 0 && q[1] <= g.behind.H), white = q => q && q[0] > 200 && q[1] > 200 && q[2] > 200, orange = q => q && q[0] > 170 && q[1] > 60 && q[1] < 190 && q[2] < 150;
    if (c.mech === 'none') ok(lab + ': no rods are drawn, and the lens is', !g.shown.marks.K && !!g.shown.marks.lens && inside, g.shown.marks);
    else {
      const k = 30, xs = 900 - 46, yp = 470 - 78, M = g.shown.marks, K = o.K, far = Math.hypot(M.K[0] - M.I[0], M.K[1] - M.I[1]) > 14 && Math.hypot(M.K[0] - M.L[0], M.K[1] - M.L[1]) > 14;
      ok(lab + ': the four pivots are drawn where the sums put them (I two focal lengths before the slider, L one past the lens, N at the screen, K at the joint), white dots, inside the picture', inside && Math.abs(M.L[0] - (xs - (c.D - (c.s + 1)) * k)) < 0.01 && Math.abs(M.K[0] - (xs - (c.D - K[0]) * k)) < 0.01 && Math.abs(M.K[1] - (yp - K[1] * k)) < 0.01 && Math.abs(M.lens[0] - (xs - (c.D - c.s) * k)) < 0.01 && Math.abs(M.slider[0] - (xs - c.D * k)) < 0.01 && ['I', 'L', 'N', 'K'].every(q => white(g.behind.pm[q])), [M, g.behind.pm]);
      ok(lab + ': the three rods are drawn between them (orange half way along each)', !far || (orange(g.behind.rodIK) && orange(g.behind.rodKN) && orange(g.behind.rodKL)), [g.behind.rodIK, g.behind.rodKN, g.behind.rodKL]);
    }
  }
  const G = k => kept[k];
  ok('at ten times the ghost is far softer with no rods than with them (the sharpest edge in the picture)', G('right/10/false').seen.grad > 3 * G('none/10/false').seen.grad, [G('right/10/false').seen.grad, G('none/10/false').seen.grad]);
  ok('with no shade a ghost of 1.5 times is drawn brighter than one of 20 times, and the shade brings them nearer', G('right/1.5/false').seen.mean > 1.5 * G('right/20/false').seen.mean && Math.abs(Math.log(G('right/1.5/true').shown.o.light10 / G('right/10/true').shown.o.light10)) < Math.abs(Math.log(G('right/1.5/false').shown.o.light10 / G('right/10/false').shown.o.light10)), [G('right/1.5/false').seen.mean, G('right/20/false').seen.mean]);
  // ---- the controls, worked as a visitor would
  await p.evaluate(() => window.SET({ m: 5, mech: 'right', shade: false }));
  const box = await p.locator('#slider').boundingBox(); await p.mouse.move(box.x + box.width * 0.2, box.y + box.height / 2); await p.mouse.down(); await p.mouse.move(box.x + box.width * 0.5, box.y + box.height / 2, { steps: 5 }); const mid = (await read()).state.m; await p.mouse.move(box.x + box.width * 0.85, box.y + box.height / 2, { steps: 5 }); await p.mouse.up(); const end = (await read()).state.m;
  ok('dragging the slider from a fifth of its length to the middle and on to 85 parts in 100 rolls the lantern out (about 4.5 times, then about 12.8)', mid > 3.5 && mid < 5.6 && end > 10.5 && end < 15, [mid, end]);
  await p.locator('#slider').focus(); const before = (await read()).state.m; await p.keyboard.press('ArrowLeft'); const after = (await read()).state.m; ok('the left arrow key on the slider rolls it a step nearer', after < before && after > before * 0.98, [before, after]);
  for (const v of ['plate', 'words', 'nhigh', 'lhigh', 'none', 'right']) { await p.locator('input[name=mech][value=' + v + ']').check(); const g = await read(); ok('choosing "' + v + '" by its button sets the rods so, and the words change with it', g.state.mech === v && (v === 'right' ? /sharp\.$/.test(g.texts[2]) : true), [g.state, g.texts[2]]); }
  const l0 = (await read()).shown.o.light10; await p.locator('#shade').check(); const g1 = await read(); ok('ticking the shade puts it on (the words say "under the same shade")', g1.state.shade === true && /under the same shade/.test(g1.texts[3]) && g1.shown.o.light10 !== l0, [g1.state, g1.texts[3]]); await p.locator('#shade').uncheck();
  await p.locator('#go').click(); await p.waitForTimeout(450); const a1 = (await read()).state.m; await p.waitForTimeout(450); const a2 = (await read()).state.m; const label = await p.locator('#go').textContent(); await p.locator('#go').click(); await p.waitForTimeout(150); const a3 = (await read()).state.m; await p.waitForTimeout(350); const a4 = (await read()).state.m;
  ok('the button lets the ghost advance by itself (it is at two different sizes 450 ms apart, the button then says Stop) and stops it', a1 !== a2 && label === 'Stop' && a3 === a4, [a1, a2, label, a3, a4]);
  const g = await read(); ok('no script errors, and none of the page\'s own assertions failed', errs.length === 0 && g.faults.length === 0, [errs, g.faults]);
  if (prefix) { await p.evaluate(() => window.SET({ m: 8, mech: 'right', shade: false })); await p.screenshot({ path: prefix + '-right.png', fullPage: true }); await p.evaluate(() => window.SET({ m: 2, mech: 'words', shade: false })); await p.screenshot({ path: prefix + '-words.png', fullPage: true }); await p.evaluate(() => window.SET({ m: 12, mech: 'none', shade: false })); await p.screenshot({ path: prefix + '-none.png', fullPage: true }); }
  console.log(pass + ' passed, ' + fail + ' failed'); await b.close(); process.exit(fail ? 1 : 0);
})();
