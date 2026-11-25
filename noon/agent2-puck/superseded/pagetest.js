// node pagetest.js [PAGE] : puck.html in a headless browser, with a made-up hand moving the real pointer
const { chromium } = require('playwright'); const path = require('path'); const P = require(path.join(__dirname, 'core.js'));
(async () => {
  const file = path.resolve(process.argv[2] || path.join(__dirname, 'puck.html')); let bad = 0, n = 0; const must = (ok, what) => { n++; if (!ok) { bad++; console.log('FAILED: ' + what); } };
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1000, height: 1000 } }); const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto('file://' + file);
  const state = () => p.evaluate(() => window.PUCKSTATE()); let box = await p.locator('#board').boundingBox(); let s = await state(); const k = box.width / s.N;
  const toScreen = h => [box.x + (s.C + h[0]) * k, box.y + (s.C + h[1]) * k];      // the board may have moved on the screen since (a click scrolls the page): put() asks again each time
  let hand = [60, -40];
  const put = async h => { hand = h; const q = toScreen(h); await p.mouse.move(q[0], q[1]); };
  const click = async sel => { await p.click(sel); box = await p.locator('#board').boundingBox(); };
  const home = async () => { await put([0, 0]); await p.waitForTimeout(200); await put([0.5, 0.5]); await p.waitForTimeout(60); s = await state(); };
  // a hand that only chases: it looks at the ring and the dot as the page shows them and moves the way the dot lies from the ring
  const chase = async (g, maxSteps) => { let steps = 0; s = await state(); const trial = s.trial, rounds = s.rounds;
    while (steps < maxSteps) { s = await state(); if (s.phase !== 'go' || s.trial !== trial || s.rounds !== rounds) break; await put([hand[0] + g * (s.target[0] - s.ring[0]), hand[1] + g * (s.target[1] - s.ring[1])]); steps++; if (Math.hypot(s.target[0] - s.ring[0], s.target[1] - s.ring[1]) < s.catchR) await p.waitForTimeout(160); }
    return steps; };
  // a hand that knows the turn: it goes straight to where the dot's place lies for the hand
  const knowing = async deg => { s = await state(); const t = s.target, steps = 24; for (let i = 1; i <= steps; i++) { const q = P.turn(t[0] * i / steps, t[1] * i / steps, -deg); await put(q); } await p.waitForTimeout(200); await put([hand[0] + 0.3, hand[1]]); await p.waitForTimeout(40); };
  const rows = () => p.$$eval('#rounds tbody tr', rs => rs.map(r => [...r.children].map(c => c.textContent)));
  const seen = [];
  const round = async (g) => { for (let i = 0; i < 8; i++) { await home(); must(s.phase === 'go', 'brought to the middle, the ring is given a dot (dot ' + (i + 1) + ')'); seen.push(s.target.slice()); await chase(g, 400); s = await state(); must(s.lastD <= s.catchR, 'the dot was caught with the ring upon it: ' + (s.lastD / s.catchR).toFixed(2) + ' of the catching distance'); } };

  must((await p.$$eval('#turns button', bs => bs.map(x => x.textContent))).join('|') === 'straight|an eighth turn|a quarter turn|three eighths|half a turn|a surprise', 'six turns to choose from');
  await p.waitForTimeout(400); s = await state();
  must(s.phase === 'home' && !s.seen && s.angle === 0 && (await p.textContent('#say')).includes('on the board: a ring will follow it'), 'it begins straight, and nothing starts until the pointer has been on the board');
  must(!(await p.locator('#none').isHidden()), 'before any round the table says there is none');
  // straight
  await round(0.25); let r = await rows();
  must(r.length === 1 && r[0][0] === 'straight' && r[0][1] === '8 of 8' && r[0][3] === '1.00' && r[0][4] === '1.00', 'a chasing hand with no turn catches eight dots by straight paths: ' + JSON.stringify(r[0]));
  must(await p.locator('#none').isHidden(), 'and the table no longer says there is no round');
  const dirs = seen.slice(0, 8).map(t => Math.round(Math.atan2(t[0], -t[1]) * 180 / Math.PI + 360) % 360).sort((a, b) => a - b);
  must(JSON.stringify(dirs) === JSON.stringify([0, 45, 90, 135, 180, 225, 270, 315]) && seen.slice(0, 8).every(t => Math.abs(Math.hypot(t[0], t[1]) / s.R - 1) < 1e-9), 'the eight dots of a round stand an eighth of a turn apart, all as far from the middle: ' + dirs.join(' '));
  // hovering beside a dot does not catch it
  await home(); const t0 = s.target; await put([t0[0] * (1 - 1.6 * s.catchR / s.R), t0[1] * (1 - 1.6 * s.catchR / s.R)]); await p.waitForTimeout(350); await put([hand[0] + 0.2, hand[1]]); await p.waitForTimeout(60); s = await state();
  must(s.phase === 'go' && s.trial === 0, 'a ring held beside the dot, at 1.6 times the catching distance, does not catch it');
  await put([t0[0], t0[1]]); await p.waitForTimeout(200); await put([t0[0] + 0.2, t0[1]]); await p.waitForTimeout(60); s = await state(); must(s.trial === 1 && s.results.length === 1, 'and brought onto it, does');
  // a round left half way: choosing a turn starts afresh
  await click('#turns button:nth-child(1)'); s = await state(); must(s.trial === 0 && s.results.length === 0 && s.phase === 'home', 'choosing a turn in the middle of a round throws the round away');
  must((await rows()).length === 1, 'and the round thrown away is not in the table');
  // an eighth turn
  await click('#turns button:nth-child(2)'); s = await state(); must(s.angle === 45 && s.phase === 'home' && s.trial === 0, 'choosing a turn starts a fresh round at that turn');
  must((await p.$eval('#puck g', e => e.getAttribute('transform'))) === 'rotate(45)', 'the mouse in the picture is turned by the turn chosen');
  await round(0.05); r = await rows(); let vals = r[1][2].split(', ').map(Number);
  must(r.length === 2 && r[1][1] === '8 of 8' && vals.every(v => Math.abs(v / Math.SQRT2 - 1) < 0.05) && r[1][4] === '1.41', 'at an eighth of a turn the chasing hand\'s paths are 1.41 times the straight line, each within a twentieth: ' + r[1][2]);
  // a sixth of a turn, the other way, set from outside
  await p.evaluate(() => window.PUCKSET(-60)); await round(0.04); r = await rows(); vals = r[2][2].split(', ').map(Number);
  must(vals.every(v => Math.abs(v / 2 - 1) < 0.06) && r[2][4] === '2.00' && r[2][0] === 'a surprise (it was -60 degrees)', 'at a sixth of a turn the other way they are twice the straight line, and the surprise is told afterwards: ' + r[2][2]);
  // a quarter turn: the chaser circles
  await click('#turns button:nth-child(3)'); await home(); const steps = await chase(0.02, 300); s = await state(); const d = s.target ? Math.hypot(s.target[0] - s.ring[0], s.target[1] - s.ring[1]) : NaN;
  must(steps === 300 && s.phase === 'go' && d > 0.9 * s.R && d < 1.3 * s.R, 'at a quarter turn the chasing hand goes round the dot and does not arrive: after 300 steps it is ' + (d / s.R).toFixed(2) + ' of the way off that it began');
  // three eighths: it runs away; and a hand that knows the turn goes straight
  await click('#turns button:nth-child(4)'); await home(); await chase(0.05, 12); s = await state(); const d2 = Math.hypot(s.target[0] - s.ring[0], s.target[1] - s.ring[1]);
  must(d2 > 1.25 * s.R, 'at three eighths of a turn the chasing hand runs away: after 12 steps it is ' + (d2 / s.R).toFixed(2) + ' times as far off');
  await click('#again'); for (let i = 0; i < 8; i++) { await home(); await knowing(135); } r = await rows();
  must(r[r.length - 1][0] === 'three eighths' && r[r.length - 1][1] === '8 of 8' && r[r.length - 1][3] === '1.00' && r[r.length - 1][4] === 'runs away', 'a hand that knows the turn catches all eight by straight paths, where the chaser runs away: ' + JSON.stringify(r[r.length - 1]));
  // half a turn, knowing
  await click('#turns button:nth-child(5)'); for (let i = 0; i < 8; i++) { await home(); await knowing(180); } r = await rows();
  must(r[r.length - 1][0] === 'half a turn' && r[r.length - 1][3] === '1.00', 'and so at half a turn: ' + r[r.length - 1][2]);
  // the robot
  await click('#turns button:nth-child(2)'); await click('#robot'); let say = await p.textContent('#say'); s = await state();
  must(s.robot && /it arrives, by a path 1\.4\d times/.test(say), 'the page\'s own chaser at an eighth of a turn: ' + say);
  await p.waitForTimeout(3500); s = await state(); must(!s.robot && s.phase === 'home', 'when it has done, the board is yours again');
  await click('#turns button:nth-child(3)'); await click('#robot'); say = await p.textContent('#say'); must(say.includes('round and round'), 'at a quarter turn: ' + say);
  await click('#turns button:nth-child(5)'); await click('#robot'); say = await p.textContent('#say'); must(say.includes('runs away'), 'at half a turn: ' + say);
  // a surprise hides its angle
  await click('#turns button:nth-child(6)'); s = await state(); const puck = await p.$eval('#puck', e => e.textContent);
  must((await p.$eval('#puck g', e => e.getAttribute('transform') || '')) === '', 'for a surprise the mouse in the picture is not turned');
  must(s.hidden && puck.includes('?') && !(await p.textContent('#say')).match(/\d+ degrees/) && [30, 60, 75, 105, 120, 150, -30, -60, -90, -120].includes(s.angle), 'a surprise shows a question mark and does not say its angle');
  await click('#robot'); say = await p.textContent('#say'); must(!/\d+ degrees/.test(say), 'nor does the chaser give it away: ' + say);
  must(errs.length === 0, 'no script error: ' + errs.slice(0, 2));
  for (const w of [1000, 600, 390, 320]) { await p.setViewportSize({ width: w, height: 900 }); const o = await p.evaluate(() => [document.documentElement.scrollWidth - window.innerWidth, document.getElementById('board').getBoundingClientRect().right - window.innerWidth]); must(o[0] <= 0 && o[1] <= 0, `at ${w} wide nothing runs off the side`); }
  console.log(`${n - bad} of ${n} checks passed`); await b.close(); process.exit(bad ? 1 : 0);
})();
