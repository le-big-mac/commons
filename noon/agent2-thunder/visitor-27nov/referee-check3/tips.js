// my own numbers for the five tips, from core.js in node (no browser)
const TH = require('/home/agent2/thunder/core.js'); const C = 343;
const rng = a => Math.min(...a).toPrecision(3) + ' to ' + Math.max(...a).toPrecision(3), mean = a => a.reduce((s, v) => s + v, 0) / a.length;
const shown = x => x < 9.95 ? Number(x.toFixed(1)) : Number(x.toPrecision(2)), fmt = x => x < 9.95 ? x.toFixed(1) : Number(x.toPrecision(2)).toLocaleString('en-US');
const REF = TH.thunder(TH.arc(0, 0, 3000, 150, 95), [0, 0]).peak; console.log('crack', REF, 'keys', Object.keys(TH.thunder(TH.arc(0, 0, 3000, 150, 95), [0, 0])).join(','));
const start = r => (r.firstHeard === null || r.firstHeard === undefined) ? r.first : r.firstHeard;
// tip 1
console.log('TIP 1: 40 made-up strokes (seeds 101-140) from each place');
for (const x of [-1700, -500, 300, 500, 1000, 2000, 3000, 4000, 5000, 6000, 8000, 9000, 9700]) { let a = 0, mid = 0, late = 0; const pk = [], du = [], fs = [];
  for (let s = 101; s <= 140; s++) { const r = TH.thunder(TH.stroke(s), [x, 0]), t0 = start(r), f = (r.tpeak - t0) / (r.last - t0); if (f < 0.1) a++; else if (f > 0.9) late++; else mid++; pk.push(r.peak); du.push(r.last - t0); fs.push(t0); }
  console.log('  from', x, 'm: loudest in first tenth', a, ', middle', mid, ', last tenth', late, 'of 40 | mean peak', mean(pk).toExponential(2), '| mean length', mean(du).toFixed(1), 's | mean first sound', mean(fs).toFixed(2), 's =', (mean(fs) / Math.abs(x) * 1000).toFixed(2), 's a km'); }
// tip 2: crooked bows
const raw = TH.arc(3000, 0, 3000, 150, 95), bs = TH.thunder(raw, [3000, 0]); const rel = [], dur = [], M = [];
for (let s = 1; s <= 300; s++) { const r = TH.thunder(TH.jag(raw, s * 31 + 5), [3000, 0]); rel.push(REF / r.peak); dur.push(r.last - start(r)); M.push(Math.pow(shown(REF / r.peak), 0.25)); }
const mp = M.map(v => fmt(v)), tally = {}; mp.forEach(v => tally[v] = (tally[v] || 0) + 1);
console.log('TIP 2: smooth bow peak', bs.peak.toFixed(5), 'lasts', (bs.last - start(bs)).toFixed(4), 's | 300 crooked bows (seeds 1-300): times lower', rng(rel), 'median', rel.slice().sort((a, b) => a - b)[150].toFixed(0), '; below 50 or above 200:', rel.filter(v => v < 50 || v > 200).length, '| printed "times quieter"', JSON.stringify(tally), '; printed below 3.0:', mp.filter(v => parseFloat(v) < 3).length, ', above 4.0:', mp.filter(v => parseFloat(v) > 4).length, '| lasts', rng(dur), 's; under 0.30:', dur.filter(v => v < 0.3).length, ', under a third:', dur.filter(v => v < 1 / 3).length, ', over 1.0:', dur.filter(v => v > 1).length, ', over 1.1:', dur.filter(v => v > 1.1).length, '; the page would print "0.3 s" for', dur.filter(v => v.toFixed(1) === '0.3').length, ', "0.2 s" for', dur.filter(v => v.toFixed(1) === '0.2').length);
// tip 3: pointing away
function away(Lx) { const ce = Math.cos(38 * Math.PI / 180), se = Math.sin(38 * Math.PI / 180), X0 = -2000, X1 = 10000, right = (X1 - 150 - Lx) / ce, left = (Lx - X0 - 150) / ce, side = right >= left ? 1 : -1, far = Math.min(8000, Math.max(right, left), 4900 / se); return [[Lx + side * 2500 * ce, 2500 * se], [Lx + side * far * ce, far * se]]; }
const up = []; for (let s = 101; s <= 140; s++) up.push(TH.thunder(TH.stroke(s), [3000, 0]).energy); const u3 = mean(up);
console.log('TIP 3: 40 upright strokes from 3 km: mean energy', u3.toExponential(3), 'range', rng(up));
let all = [], outside = 0;
for (const x of [-1700, 0, 500, 1500, 3000, 4000, 5000, 6500, 8000, 9000, 9700]) { const ra = away(x), e = [], d = [], tr = []; for (let s = 1; s <= 20; s++) { const pts = TH.jag(ra, s * 31 + 5), r = TH.thunder(pts, [x, 0]); e.push(r.energy / u3); d.push(r.last - start(r)); const dd = TH.distances(pts, [x, 0]).r; let c = 0; for (let i = 2; i < dd.length; i++) if ((dd[i] - dd[i - 1]) * (dd[i - 1] - dd[i - 2]) < 0) c++; tr.push(c / (pts.length - 1)); }
  const sm = TH.thunder(TH.resample(ra, 3), [x, 0]); let ends = 0, tot = 0; for (let i = 0; i < sm.p.length; i++) { const t = sm.t0 + i / sm.fs, v = sm.p[i] * sm.p[i]; tot += v; if (t < sm.first + 0.02 || t >= sm.last - 0.03) ends += v; }
  all = all.concat(e); console.log('  listener', x, ': stroke from', ra[0].map(Math.round).join(','), 'to', ra[1].map(Math.round).join(','), '| energy / upright-from-3-km', rng(e), 'mean', mean(e).toFixed(3), '| lasts', rng(d), 's | share of joints where the distance turns round', (100 * mean(tr)).toFixed(1) + '%', '| smooth: two ends hold', (100 * ends / tot).toFixed(2) + '% ; peak', sm.peak.toExponential(2)); }
console.log('  all', all.length, ': ratio', rng(all), 'mean', mean(all).toFixed(3), '; outside 0.05..0.2:', all.filter(v => v < 0.05 || v > 0.2).length, '; outside 0.033..0.3:', all.filter(v => v < 1 / 30 || v > 0.3).length);
// tip 4: straight smooth
console.log('TIP 4: the smooth straight stroke');
const st = TH.resample([[0, 5000], [0, 0]], 3);
for (const x of [-1700, 0, 30, 100, 300, 500, 1000, 1500, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 9700]) { const r = TH.thunder(st, [x, 0]); let click = 0, mid = 0, eC = 0, eM = 0, eK = 0;
  for (let i = 0; i < r.p.length; i++) { const t = r.t0 + i / r.fs, a = Math.abs(r.p[i]); if (t >= r.last - 0.03) { click = Math.max(click, a); eK += a * a; } else if (t >= r.first + 0.02) { mid = Math.max(mid, a); eM += a * a; } else eC += a * a; }
  console.log('  from', x, 'm: crack', r.peak.toExponential(3), '(loudest', (r.tpeak - r.first).toFixed(4), 's after first) | click', click.toExponential(3), '= crack /', (r.peak / click).toFixed(2), '| largest between = crack /', (r.peak / mid).toFixed(1), '| energy: crack', (100 * eC / (eC + eM + eK)).toFixed(2) + '%, between', (100 * eM / (eC + eM + eK)).toFixed(2) + '%, click', (100 * eK / (eC + eM + eK)).toFixed(3) + '%; click energy / crack energy', (eK / eC).toFixed(4)); }
