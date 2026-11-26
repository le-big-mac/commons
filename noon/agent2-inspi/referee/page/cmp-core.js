// Fork's check of core.js (read-only use of /home/agent2/inspi/core.js) against the referee's own programs.
'use strict';
const fs = require('fs'); const T = require('/home/agent2/inspi/core.js');
const F = 360000n;
const bmod = (a, m) => ((a % m) + m) % m; const bgcd = (a, b) => { while (b) { [a, b] = [b, a % b]; } return a < 0n ? -a : a; };
function theory(A, I) { const a = bmod(BigInt(A), F), i = bmod(BigInt(I), F); let q = 1n, p = 0n; if (i !== 0n) { const g = bgcd(i, F); q = F / g; p = i / g; }
  const TT = (q * a + 180000n * p * (q - 1n)) % F; if (TT === 0n) return { home: false, q: Number(q) }; return { home: true, q: Number(q), steps: Number(q * (F / bgcd(TT, F))) }; }
function lit(A, I, cap) { const FF = 360000, K = 2 * Math.PI / FF; const a0 = ((A % FF) + FF) % FF, inc = ((I % FF) + FF) % FF; let ang = a0, h = 0, x = 0, y = 0, home = 0, there = 0;
  for (let k = 1; k <= cap; k++) { x += Math.sin(h * K); y += Math.cos(h * K); h = (h + ang) % FF; ang = (ang + inc) % FF; if (Math.hypot(x, y) < 1e-9) { if (!there) there = k; if (h === 0 && ang === a0) { home = k; break; } } }
  return { home, there, x, y }; }
// 1. all whole-degree pairs against inspi_ref_out.json
const rows = JSON.parse(fs.readFileSync('/home/agent2/inspi/referee/inspi_ref_out.json', 'utf8')).rows; let bad = 0, maxg = 0;
for (const r of rows) { const f = T.forecast(r.ang * 1000, r.inc * 1000); if (f.home !== r.home) bad++; else if (f.home) { if (f.steps !== r.n0) bad++; } else { if (f.q !== r.n0) bad++; maxg = Math.max(maxg, Math.abs(f.gain - r.absD)); } }
console.log('1. whole degrees:', rows.length, 'pairs; core.js forecast disagrees with inspi_ref_out.json on', bad, '; max |gain - |D|| =', maxg);
// 2. random thousandths against exact theory, and against a literal walk where short
let seed = 12345; const rnd = () => { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; };
let bad2 = 0, n2 = 0, bad3 = 0, n3 = 0;
for (let t = 0; t < 40000; t++) { const span = t % 2 ? 999999999 : 720000; const A = Math.floor((rnd() * 2 - 1) * span), I = t % 5 === 0 ? Math.floor(rnd() * 720) * 500 : Math.floor((rnd() * 2 - 1) * span);
  const f = T.forecast(A, I), th = theory(A, I); n2++; if (f.home !== th.home || f.q !== th.q || (f.home && f.steps !== th.steps)) bad2++;
  if (th.home && th.steps <= 20000) { n3++; if (lit(A, I, th.steps).home !== th.steps) bad3++; } else if (!th.home && th.q <= 300) { n3++; const w = lit(A, I, 12 * th.q); if (w.home || Math.abs(Math.hypot(w.x, w.y) - 12 * Math.sqrt(th.q)) > 1e-7) bad3++; } }
console.log('2. random thousandths:', n2, 'pairs; core.js against exact BigInt theory, disagreements', bad2, ';', n3, 'of them walked literally, disagreements', bad3);
// 3. parse
for (const s of ['.5', '5.', '+5', '−5', '-5', '1234567', '999999.999', ' 5 ', '1e3', '', '0.3333', '1,5', '22.5', '-0', '00012', '５']) console.log('3. parse', JSON.stringify(s), '->', T.parse(s));
// 4. chosen turtles
for (const [a, i] of [['22.5', '45'], ['0.5', '1'], ['2', '22.5'], ['0', '0.1'], ['0', '0.333'], ['-10', '-20'], ['10', '-20'], ['999999', '999999.999'], ['0', '0'], ['90', '0'], ['360', '0'], ['0', '360'], ['90', '360'], ['0.001', '0'], ['0.1', '0'], ['0.05', '180'], ['0', '0.001'], ['0.0005', '0.001'], ['0', '0.007'], ['179.999', '0.002'], ['3.5', '7'], ['0', '8'], ['4', '8'], ['180', '180'], ['0', '180']]) {
  const A = T.parse(a), I = T.parse(i); if (A === null || I === null) { console.log('4.', a, i, 'not accepted'); continue; }
  const f = T.forecast(A, I), th = theory(A, I); let w = '';
  if (th.home && th.steps <= 20000) { const l = lit(A, I, th.steps); w = 'walk: home ' + l.home + ', first on start ' + l.there; } else if (!th.home) { const n = Math.min(20000, 3 * th.q), l = lit(A, I, n); w = 'walk ' + n + ' steps: home ' + l.home + ', dist ' + Math.hypot(l.x, l.y).toFixed(6) + (n === 3 * th.q ? ' (3 sqrt q = ' + (3 * Math.sqrt(th.q)).toFixed(6) + ')' : ''); } else { const l = lit(A, I, 20000); w = 'walk 20000: home ' + l.home; }
  console.log('4.', a, i, '| core:', JSON.stringify(f), '| theory:', JSON.stringify(th), '|', w, (f.home === th.home && f.q === th.q && (!f.home || f.steps === th.steps)) ? '' : '  <<< DISAGREE'); }
// 5. report arithmetic as printed: "d steps from its start, which is laps x gain"
let mis = 0, tot = 0, ex = [];
for (const r of rows) if (!r.home) { const q = r.n0, laps = Math.max(6, Math.min(40, Math.round(240 / q))), g = Math.sqrt(q), d = laps * g; tot++; const printed = d.toFixed(3), prod = (laps * Number(g.toFixed(3))).toFixed(3); if (printed !== prod) { mis++; if (ex.length < 4 || (r.inc === 20 && r.ang === 10)) ex.push([r.ang, r.inc, laps, g.toFixed(3), printed, prod]); } }
console.log('5. never-home whole-degree pairs:', tot, '; report prints "d, which is laps x gain" where laps x the printed gain does not give the printed d:', mis, 'e.g. [angle, inc, laps, gain, d printed, laps*gain]', JSON.stringify(ex));
// 6. dashed circle outside the canvas?  (the page's own plan/setView arithmetic, two canvas sizes)
function circleOut(A, I, W, H) { const f = T.forecast(A, I); if (!f.home || f.steps > 20000 || f.laps < 3) return null; const w = T.walk(A, I, f.steps), q = f.q; let cx = 0, cy = 0; for (let n = 0; n < f.laps; n++) { cx += w.xs[n * q]; cy += w.ys[n * q]; } cx /= f.laps; cy /= f.laps; const r = Math.hypot(cx, cy); if (r <= 1e-6) return null;
  const b = T.box(w), pad = 22, bw = Math.max(b[1] - b[0], 1e-9), bh = Math.max(b[3] - b[2], 1e-9); let k = Math.min((W - 2 * pad) / bw, (H - 2 * pad) / bh); k = Math.min(k, 90); const ox = W / 2 - k * (b[0] + b[1]) / 2, oy = H / 2 + k * (b[2] + b[3]) / 2;
  const over = Math.max(0 - (ox + k * (cx - r)), (ox + k * (cx + r)) - W, 0 - (oy - k * (cy + r)), (oy - k * (cy - r)) - H); return { over, r, k, laps: f.laps, steps: f.steps }; }
for (const [W, H, name] of [[830, 515, 'desktop 830x515'], [290, 260, 'phone 290x260']]) { let out = 0, seen = 0, worst = null; for (let inc = 1; inc < 360; inc++) for (let a = 0; a < 360; a++) { const c = circleOut(a * 1000, inc * 1000, W, H); if (!c) continue; seen++; if (c.over > 1) { out++; if (!worst || c.over > worst.over) worst = Object.assign({ a, inc }, c); } }
  console.log('6.', name, ': whole-degree turtles with a dashed circle', seen, '; circle reaching more than 1 px outside the canvas', out, '; worst', JSON.stringify(worst)); }
