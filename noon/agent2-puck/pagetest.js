// node pagetest.js [PAGE] : puck.html in a headless browser, with a made-up hand moving the real pointer, and a made-up finger
const { chromium } = require('playwright'); const path = require('path'); const P = require(path.join(__dirname, 'core.js'));
(async () => {
  const file = path.resolve(process.argv[2] || path.join(__dirname, 'puck.html')); let bad = 0, n = 0; const must = (ok, what) => { n++; if (!ok) { bad++; console.log('FAILED: ' + what); } };
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1000, height: 1000 } }); const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto('file://' + file);
  const state = () => p.evaluate(() => window.PUCKSTATE()); let box = await p.locator('#board').boundingBox(); let s = await state(); const k = box.width / s.N;
  const toScreen = h => [box.x + (s.C + h[0]) * k, box.y + (s.C + h[1]) * k];      // the board may move on the screen (a click scrolls the page): click() asks again
  let hand = [60, -40];
  const put = async h => { hand = h; const q = toScreen(h); await p.mouse.move(q[0], q[1]); };
  const click = async sel => { await p.click(sel); box = await p.locator('#board').boundingBox(); };
  const home = async () => { await put([0, 0]); await p.waitForTimeout(200); await put([0.5, 0.5]); await p.waitForTimeout(60); s = await state(); };
  const dist = (a, c) => Math.hypot(a[0] - c[0], a[1] - c[1]);
  // a hand that only chases, in steps: it looks at the ring and the dot as the page shows them and moves a share g of the way the dot lies from the ring
  const chase = async (g, maxSteps, each) => { let steps = 0; s = await state(); const trial = s.trial, rounds = s.rounds;
    while (steps < maxSteps) { s = await state(); if (s.phase !== 'go' || s.trial !== trial || s.rounds !== rounds) break; if (each) each(s); await put([hand[0] + g * (s.target[0] - s.ring[0]), hand[1] + g * (s.target[1] - s.ring[1])]); steps++; if (dist(s.target, s.ring) < s.catchR) await p.waitForTimeout(160); }
    return steps; };
  // a hand that knows the turn: it goes straight to where the dot's place lies for the hand
  const knowing = async deg => { s = await state(); const t = s.target, steps = 24; for (let i = 1; i <= steps; i++) await put(P.turn(t[0] * i / steps, t[1] * i / steps, -deg)); await p.waitForTimeout(200); await put([hand[0] + 0.3, hand[1]]); await p.waitForTimeout(40); };
  const rows = () => p.$$eval('#rounds tbody tr', rs => rs.map(r => [...r.children].map(c => c.textContent)));
  const pixel = at => p.evaluate(([x, y]) => [...document.getElementById('board').getContext('2d').getImageData(Math.round(x), Math.round(y), 1, 1).data], at);
  const isInk = d => d[3] > 150 && d[0] < 90 && d[1] < 90 && d[2] < 90, isOrange = d => d[3] > 150 && d[0] > 170 && d[1] > 70 && d[1] < 130 && d[2] < 80;
  const seen = [];
  const round = async (g, deg) => { const want = P.stepRatio(deg, g); for (let i = 0; i < 8; i++) { await home(); must(s.phase === 'go', 'brought to the middle, the ring is given a dot (dot ' + (i + 1) + ')'); seen.push(s.target.slice()); await chase(g, 500); s = await state(); must(s.lastD <= s.catchR, 'the dot was caught with the ring upon it: ' + (s.lastD / s.catchR).toFixed(2) + ' of the catching distance'); } return want; };
  const near = (vals, want, tol) => vals.length === 8 && vals.every(v => Math.abs(v / want - 1) < tol);

  must((await p.$$eval('#turns button', bs => bs.map(x => x.textContent))).join('|') === 'straight|an eighth turn|a quarter turn|three eighths|half a turn|a surprise', 'six turns to choose from');
  await p.waitForTimeout(400); s = await state();
  must(s.phase === 'home' && !s.seen && s.angle === 0 && (await p.textContent('#say')).includes('on the board: a ring will follow it'), 'it begins straight, and nothing starts until the pointer has been on the board');
  await p.mouse.move(box.x + 30, box.y - 90); await p.mouse.move(box.x + 200, box.y - 60); s = await state(); const blank = await pixel([s.C + 11, s.C]);
  must(!s.seen && s.hand[0] === 0 && s.hand[1] === 0 && !s.fresh && !isInk(blank), 'a pointer moving about the page above the board is not followed, and no ring is drawn');
  must(Math.abs(2 * s.R + 11 - s.C) < 0.06 * s.N && 2 * s.R + 11 < s.C, 'the board is wide enough for a whole circle about any dot: twice the dots\' distance, and the ring, is ' + ((2 * s.R + 11) / s.C).toFixed(2) + ' of its half-width');
  must(!(await p.locator('#none').isHidden()), 'before any round the table says there is none');
  // straight
  let want = await round(0.25, 0); let r = await rows();
  must(r.length === 1 && r[0][0] === 'straight' && r[0][1] === '8 of 8' && r[0][3] === '1.00' && r[0][4] === '1.00' && want === 1, 'a chasing hand with no turn catches eight dots by straight paths: ' + JSON.stringify(r[0]));
  must(await p.locator('#none').isHidden(), 'and the table no longer says there is no round');
  const dirs = seen.slice(0, 8).map(t => Math.round(Math.atan2(t[0], -t[1]) * 180 / Math.PI + 360) % 360).sort((a, c) => a - c);
  must(JSON.stringify(dirs) === JSON.stringify([0, 45, 90, 135, 180, 225, 270, 315]) && seen.slice(0, 8).every(t => Math.abs(Math.hypot(t[0], t[1]) / s.R - 1) < 1e-9), 'the eight dots of a round stand an eighth of a turn apart, all as far from the middle: ' + dirs.join(' '));
  // what is drawn: the ring where the page says it is, and the dot where the page says it is
  await home(); await put([-70, 40]); s = await state(); let px = await pixel([s.C + s.ring[0] + 11, s.C + s.ring[1]]); const dot = await pixel([s.C + s.target[0], s.C + s.target[1]]);
  must(isInk(px) && isOrange(dot) && s.ring[0] === -70 && s.ring[1] === 40, 'with no turn the ring is drawn where the hand is, and the dot where the page says: ' + px + ' / ' + dot);
  // hovering beside a dot does not catch it
  const t0 = s.target; await put([t0[0] * (1 - 1.6 * s.catchR / s.R), t0[1] * (1 - 1.6 * s.catchR / s.R)]); await p.waitForTimeout(350); await put([hand[0] + 0.2, hand[1]]); await p.waitForTimeout(60); s = await state();
  must(s.phase === 'go' && s.trial === 0, 'a ring held beside the dot, at 1.6 times the catching distance, does not catch it');
  await put([t0[0], t0[1]]); await p.waitForTimeout(200); await put([t0[0] + 0.2, t0[1]]); await p.waitForTimeout(60); s = await state(); must(s.trial === 1 && s.results.length === 1, 'and brought onto it, does');
  await click('#turns button:nth-child(1)'); s = await state(); must(s.trial === 0 && s.results.length === 0 && s.phase === 'home', 'choosing a turn in the middle of a round throws the round away');
  must((await rows()).length === 1, 'and the round thrown away is not in the table');
  // an eighth turn
  await click('#turns button:nth-child(2)'); s = await state(); must(s.angle === 45 && s.phase === 'home' && s.trial === 0, 'choosing a turn starts a fresh round at that turn');
  must((await p.$eval('#puck g', e => e.getAttribute('transform'))) === 'rotate(-45)', 'the mouse in the picture is turned the other way from the pointer, as a real one would be');
  await put([-70, 40]); s = await state(); const tr = P.turn(-70, 40, 45); px = await pixel([s.C + tr[0] + 11, s.C + tr[1]]); const not = await pixel([s.C - 70 + 11, s.C + 40]);
  must(isInk(px) && !isInk(not) && dist(s.ring, tr) < 1e-9, 'at an eighth of a turn the ring is drawn at the hand\'s place turned by 45 degrees about the middle, and not at the hand');
  want = await round(0.05, 45); r = await rows(); let vals = r[1][2].split(', ').map(Number);
  must(r.length === 2 && r[1][1] === '8 of 8' && near(vals, want, 0.015) && r[1][4] === '1.41', 'at an eighth of a turn a hand chasing in steps of a twentieth traces ' + want.toFixed(3) + ' times the distance, as the stepped equation says, each within 1.5 per cent: ' + r[1][2]);
  // a sixth of a turn, the other way, set from outside
  await p.evaluate(() => window.PUCKSET(-60)); want = await round(0.04, -60); r = await rows(); vals = r[2][2].split(', ').map(Number);
  must(near(vals, want, 0.015) && r[2][4] === '2.00' && r[2][0] === 'a surprise (it was -60 degrees)', 'at a sixth of a turn the other way, in steps of a twenty-fifth, ' + want.toFixed(3) + ' times; the equation\'s column says 2.00; and the surprise is told afterwards: ' + r[2][2]);
  // a quarter turn: the chaser goes round the dot
  await click('#turns button:nth-child(3)'); await home(); let swept = 0, last = null, moved = 0, lo = 9, hi = 0;
  const steps = await chase(0.02, 320, st => { const a = Math.atan2(st.ring[1] - st.target[1], st.ring[0] - st.target[0]); if (last !== null) { let da = a - last.a; while (da > Math.PI) da -= 2 * Math.PI; while (da < -Math.PI) da += 2 * Math.PI; swept += da; if (dist(st.ring, last.ring) > 1e-6) moved++; } last = { a, ring: st.ring.slice() }; const d = dist(st.ring, st.target) / st.R; lo = Math.min(lo, d); hi = Math.max(hi, d); });
  s = await state();
  must(steps === 320 && s.phase === 'go' && Math.abs(swept) * 180 / Math.PI > 330 && moved >= 318 && lo > 0.98 && hi < 1.1, 'at a quarter turn the chasing hand goes round the dot: in 320 steps the ring moved ' + moved + ' times, swept ' + (Math.abs(swept) * 180 / Math.PI).toFixed(0) + ' degrees about the dot, and kept between ' + lo.toFixed(2) + ' and ' + hi.toFixed(2) + ' of its first distance');
  // the pointer is followed beyond the board, and the ring's absence is marked
  await p.mouse.move(box.x - 60, box.y + box.height / 2); s = await state();
  must(s.hand[0] < -s.C && s.off, 'a pointer taken off the side of the board is still followed: the hand is ' + s.hand[0].toFixed(0) + ' from the middle, and the ring is off the board');
  const m = Math.max(Math.abs(s.ring[0]), Math.abs(s.ring[1])), edge = [s.C + s.ring[0] / m * (s.C - 14), s.C + s.ring[1] / m * (s.C - 14)]; px = await pixel(edge);
  must(isInk(px), 'and a mark stands at the edge of the board on the line to it: ' + px);
  for (const [cx, cy] of [[-1, -1], [1, -1], [1, 1], [-1, 1]]) { await put([cx * (s.C - 4), cy * (s.C - 4)]); s = await state(); const mm = Math.max(Math.abs(s.ring[0]), Math.abs(s.ring[1])); px = await pixel([s.C + s.ring[0] / mm * (s.C - 14), s.C + s.ring[1] / mm * (s.C - 14)]); must(s.off && isInk(px), 'with the hand in a corner of the board at a quarter turn the ring is off the board, and the mark shows where'); }
  // three eighths: it runs away; and a hand that knows the turn goes straight
  await click('#turns button:nth-child(4)'); await home(); await chase(0.05, 12); s = await state(); const d2 = dist(s.target, s.ring);
  must(d2 > 1.25 * s.R, 'at three eighths of a turn the chasing hand runs away: after 12 steps it is ' + (d2 / s.R).toFixed(2) + ' times as far off');
  await click('#again'); for (let i = 0; i < 8; i++) { await home(); await knowing(135); } r = await rows();
  must(r[r.length - 1][0] === 'three eighths' && r[r.length - 1][1] === '8 of 8' && r[r.length - 1][3] === '1.00' && r[r.length - 1][4] === 'runs away', 'a hand that knows the turn catches all eight by straight paths, where the chaser runs away: ' + JSON.stringify(r[r.length - 1]));
  await click('#turns button:nth-child(5)'); must((await p.$eval('#puck g', e => e.getAttribute('transform'))) === 'rotate(-180)', 'half a turn: the mouse in the picture is upside down');
  for (let i = 0; i < 8; i++) { await home(); await knowing(180); } r = await rows(); must(r[r.length - 1][0] === 'half a turn' && r[r.length - 1][3] === '1.00', 'and a hand that knows it goes straight at half a turn: ' + r[r.length - 1][2]);
  // the page's own chaser, which follows the equation
  const robot = async () => { await click('#robot'); const st = await state(); return [await p.textContent('#say'), st]; };
  await click('#turns button:nth-child(2)'); let [say, rs] = await robot(); let end = rs.robotPath[2];
  must(rs.robot && say.includes('it arrives, by a path 1.41 times the distance') && Math.abs(rs.robotLen / (rs.R - dist(end, rs.robotTarget)) / Math.SQRT2 - 1) < 0.002 && rs.robotFar < rs.C, 'the page\'s chaser at an eighth of a turn says 1.41 and draws a path 1.414 times the distance it closes, inside the board: ' + (rs.robotLen / (rs.R - dist(end, rs.robotTarget))).toFixed(4));
  await p.waitForTimeout(700); s = await state(); px = await pixel([s.C + rs.robotTarget[0], s.C + rs.robotTarget[1]]); must(isOrange(px), 'while it plays, its dot is drawn');
  await p.waitForTimeout(5300); s = await state(); must(!s.robot && s.phase === 'home' && (await p.textContent('#say')).includes('middle'), 'within six seconds it has done, and the board is yours again');
  await click('#turns button:nth-child(3)'); [say, rs] = await robot();
  must(say.includes('round and round the dot for ever') && rs.robotPath.every(q => Math.abs(dist(q, rs.robotTarget) / rs.R - 1) < 0.005) && rs.robotFar < rs.C - 10 && rs.robotLen > 2 * 2 * Math.PI * rs.R * 0.99, 'at a quarter turn it says round and round, and draws a true circle about the dot, twice round, inside the board: farthest ' + (rs.robotFar / rs.C).toFixed(2) + ' of the half-width');
  await p.waitForTimeout(6000); s = await state(); must(!s.robot, 'and it too gives the board back within six seconds');
  await click('#turns button:nth-child(5)'); [say, rs] = await robot(); end = rs.robotPath[2];
  must(say.includes('runs away from the dot, and off the board') && rs.robotFar <= rs.C - 12 + 1e-9 && dist(end, rs.robotTarget) > 1.5 * rs.R, 'at half a turn it says it runs away, and its path stops at the edge of the board: ' + (dist(end, rs.robotTarget) / rs.R).toFixed(2) + ' times as far from the dot');
  await click('#turns button:nth-child(4)'); s = await state(); must(!s.robot && s.angle === 135, 'choosing a turn while it plays stops it at once');
  // a surprise hides its angle
  await click('#turns button:nth-child(6)'); s = await state(); const puck = await p.$eval('#puck', e => e.textContent);
  must((await p.$eval('#puck g', e => e.getAttribute('transform') || '')) === '', 'for a surprise the mouse in the picture is not turned');
  must(s.hidden && puck.includes('?') && !(await p.textContent('#say')).match(/\d+ degrees/) && [30, 60, 75, 105, 120, 150, -30, -60, -90, -120].includes(s.angle), 'a surprise shows a question mark and does not say its angle');
  [say, rs] = await robot(); must(!/\d+ degrees/.test(say) && say.includes('this turn'), 'nor does the chaser give it away: ' + say);
  const hiddenAngle = s.angle; await click('#again'); s = await state(); must(s.hidden && s.angle === hiddenAngle && s.trial === 0, 'starting a surprise again keeps the same hidden turn');
  // a finger: a drag is counted, a lift and a tap elsewhere is not
  await click('#turns button:nth-child(2)'); box = await p.locator('#board').boundingBox();
  const touch = (type, h) => p.evaluate(([type, x, y]) => { document.getElementById('board').dispatchEvent(new PointerEvent(type, { pointerType: 'touch', pointerId: 7, clientX: x, clientY: y, bubbles: true })); }, [type, ...toScreen(h)]);
  const fingerHome = async () => { await touch('pointerdown', [0, 0]); await p.waitForTimeout(220); await touch('pointermove', [0.4, 0.4]); await p.waitForTimeout(60); s = await state(); };
  await p.mouse.move(5, 5);
  for (let i = 0; i < 8; i++) {
    await fingerHome(); must(s.phase === 'go', 'a finger held in the middle is given a dot (dot ' + (i + 1) + ')'); const t = s.target, h = P.turn(t[0], t[1], -45);
    if (i % 2 === 0) { for (let j = 1; j <= 20; j++) await touch('pointermove', [h[0] * j / 20, h[1] * j / 20]); await p.waitForTimeout(220); await touch('pointermove', [h[0] + 0.3, h[1]]); await p.waitForTimeout(60); await touch('pointerup', h); s = await state(); must(s.results.length === (i + 1) % 8 || s.rounds > 0, 'a finger dragged to the dot catches it'); }
    else { await touch('pointerup', [0, 0]); await touch('pointerdown', h); const st = await state(); const said = await p.textContent('#say'); must((i === 7 || (st.results.length === i + 1 && !isFinite(st.results[i]))) && (i === 7 || said.includes('went away and came back somewhere else')), 'a finger lifted and put down on the dot is not counted: ' + said.slice(0, 60)); await touch('pointerup', h); }
  }
  r = await rows(); const lastRow = r[r.length - 1]; const got = lastRow[2].split(', ');
  must(lastRow[0] === 'an eighth turn' && lastRow[1] === '4 of 8' && got.filter(x => x === 'not caught').length === 4 && got.filter(x => Number(x) >= 1 && Number(x) < 1.02).length === 4 && got.every((x, i) => (x === 'not caught') === (i % 2 === 1)) && lastRow[3] === 'not caught', 'a round with four dots dragged and four tapped: four straight paths, four not caught, and the middle of the eight is "not caught": ' + JSON.stringify(lastRow));
  // other ways of not travelling: a finger put down beside the board, a pen lifted and tapped, a mouse out of the window and back
  const ev = (type, kind, h, onBody) => p.evaluate(([type, kind, x, y, onBody]) => { (onBody ? document.body : document.getElementById('board')).dispatchEvent(new PointerEvent(type, { pointerType: kind, pointerId: kind === 'pen' ? 9 : 7, clientX: x, clientY: y, bubbles: true })); }, [type, kind, ...toScreen(h), onBody]);
  const before = (await rows()).length;
  await fingerHome(); let tt = s.target, hh = P.turn(tt[0], tt[1], -45); await touch('pointerup', [0, 0]); await ev('pointerdown', 'touch', [s.C + 40, 0], true); let after = await state();
  must(!isFinite(after.results[after.results.length - 1]) && after.results.length === 1, 'a finger lifted and put down beside the board loses the dot: nothing travelled there');
  await ev('pointerup', 'touch', [s.C + 40, 0], true);
  await ev('pointerdown', 'pen', [0, 0]); await p.waitForTimeout(220); await ev('pointermove', 'pen', [0.4, 0.4]); await p.waitForTimeout(60); s = await state(); must(s.phase === 'go', 'a pen held in the middle is given a dot');
  tt = s.target; hh = P.turn(tt[0], tt[1], -45); await ev('pointerup', 'pen', [0, 0]); await ev('pointerdown', 'pen', hh); after = await state();
  must(after.results.length === 2 && !isFinite(after.results[1]), 'a pen lifted and tapped on the dot is not counted either'); await ev('pointerup', 'pen', hh);
  await home(); must(s.phase === 'go', 'the mouse again: a dot'); tt = s.target; hh = P.turn(tt[0], tt[1], -45);
  await p.evaluate(() => document.documentElement.dispatchEvent(new PointerEvent('pointerleave', { pointerType: 'mouse' }))); await put(hh); after = await state();
  must(after.results.length === 3 && !isFinite(after.results[2]), 'a mouse that leaves the window and comes back on the dot is not counted');
  await put([hh[0] + 30, hh[1]]); await home(); must(s.phase === 'go', 'and after that the next dot is given as usual'); await knowing(45); after = await state();
  must(after.results.length === 4 && Math.abs(after.results[3] - 1) < 0.02, 'and a path travelled is counted: ' + after.results[3].toFixed(2));
  // a page left alone records nothing
  await home(); must(s.phase === 'go', 'a dot is up, and then nobody moves'); await p.waitForTimeout(8700); after = await state(); const said2 = await p.textContent('#say');
  must(after.phase === 'home' && after.results.length === 4 && said2.includes('Nobody moved'), 'after eight seconds without a movement the dot is put away and nothing is recorded: ' + said2.slice(0, 40));
  await p.waitForTimeout(1500); after = await state(); must(after.phase === 'home' && after.results.length === 4 && (await rows()).length === before, 'and with the ring still in the middle no new dot comes until something moves');
  await put([1, 1]); await p.waitForTimeout(200); await put([0.5, 0.5]); await p.waitForTimeout(60); after = await state(); must(after.phase === 'go', 'a movement brings the next dot');
  must(errs.length === 0, 'no script error: ' + errs.slice(0, 2));
  for (const w of [1000, 600, 390, 320]) { await p.setViewportSize({ width: w, height: 900 }); const o = await p.evaluate(() => [document.documentElement.scrollWidth - window.innerWidth, document.getElementById('board').getBoundingClientRect().right - window.innerWidth]); must(o[0] <= 0 && o[1] <= 0, `at ${w} wide nothing runs off the side`); }
  console.log(`${n - bad} of ${n} checks passed`); await b.close(); process.exit(bad ? 1 : 0);
})();
