// test.js -- core.js against the numbers printed in the book, and checks of the geometry that could fail.   usage: node test.js
const T = require('./core.js');
let pass = 0, fail = 0;
function check(name, ok, detail) { console.log((ok ? 'pass  ' : 'FAIL  ') + name + (detail ? '   [' + detail + ']' : '')); ok ? pass++ : fail++; }
const worst = (xs) => Math.max(...xs.map(Math.abs));

// ---- 1. section 4: the worth of 1,000 Scheffel of rye by distance (the book's table, made row by row with wagon-loads) ----
{ const book = [[0, 1500], [5, 1313], [10, 1136], [15, 968], [20, 809], [25, 656], [30, 512], [35, 374], [40, 242], [45, 116]];
  const d = book.map(([x, v]) => 1000 * T.price(x, 1.5) - v), ds = book.map(([x, v]) => 1000 * T.priceShort15(x) - v);
  check('section 4, price table: the long formula is within 1.5 Taler in 1,000 Scheffel at all ten distances (the table was worked row by row)', worst(d) <= 1.55, 'differences ' + d.map(x => x.toFixed(1)).join(', '));
  check('   and the short formula (273 - 5.5x)/(182 + x) within 4', worst(ds) <= 4 && worst(ds) > worst(d), 'differences ' + ds.map(x => x.toFixed(1)).join(', '));
  const z = T.distance(0, 1.5); check('section 4: rye is worth nothing at 49.95 miles in the table; by the formula at', Math.abs(z - 49.95) < 0.3, z.toFixed(2) + ' miles');
  check('section 4: the two worked cases, 1.313 at 5 miles and 1.136 at 10', Math.abs(T.price(5, 1.5) - 1.313) < 0.0006 && Math.abs(T.price(10, 1.5) - 1.136) < 0.0006, T.price(5, 1.5).toFixed(4) + ', ' + T.price(10, 1.5).toFixed(4)); }
// ---- 2. section 4: freight of a full load ----
{ const book = [[5, 5.33], [10, 10.4], [20, 19.8], [30, 28.2]], d = book.map(([x, v]) => T.freight(x) - v);
  check('section 4, freight of a load: 5.33, 10.4, 19.8, 28.2 Taler at 5, 10, 20, 30 miles', worst(d) < 0.06, 'differences ' + d.map(x => x.toFixed(3)).join(', ') + '; at 1 mile ' + T.freight(1).toFixed(2) + ' (the scan reads 1,00 or 1,09)'); }
// ---- 3. section 14: rents at 10 Körner ----
{ const rows = [[1.5, 1818, 1119], [1, 963, 619], [0.5, 108, 119]];
  check('section 14: land rent at 10 Körner for rye at 1 1/2, 1 and 1/2 Taler: Koppel 1818, 963, 108; three fields 1119, 619, 119', rows.every(([b, k, d]) => Math.abs(T.rentKoppel(b, 10) - k) < 0.51 && Math.abs(T.rentDrei(b, 10) - d) < 0.51));
  check('section 14: at 10 Körner the two pay alike at 0.516, Koppel pays nothing at 0.437, three fields nothing at 0.381', Math.abs(T.priceEqual(10) - 0.516) < 0.0006 && Math.abs(T.priceZeroKoppel(10) - 0.437) < 0.0006 && Math.abs(T.priceZeroDrei(10) - 0.381) < 0.0006, [T.priceEqual(10), T.priceZeroKoppel(10), T.priceZeroDrei(10)].map(x => x.toFixed(4)).join(', '));
  check('section 5 and 14: at 8 Körner Koppel pays nothing at 0.549 and three fields at 0.470', Math.abs(T.priceZeroKoppel(8) - 0.549) < 0.0006 && Math.abs(T.priceZeroDrei(8) - 0.470) < 0.0006, T.priceZeroKoppel(8).toFixed(4) + ', ' + T.priceZeroDrei(8).toFixed(4)); }
// ---- 3b. section 5: rent of the standard land by distance (the book's table, made with its short formula) ----
{ const book = [[1, 1066], [5, 892], [10, 685], [15, 488], [20, 301], [25, 124]], d = book.map(([x, v]) => T.rentKoppel(T.priceShort15(x), 8) - v), dl = book.map(([x, v]) => T.rentKoppel(T.price(x, 1.5), 8) - v);
  check('section 5, table: Koppel rent at 8 Körner by distance, with the short price formula, within 1 Taler at six distances; nothing at 28.6 miles', worst(d) < 1 && Math.abs(202202 / 7065 - 28.6) < 0.03, 'differences ' + d.map(x => x.toFixed(1)).join(', ') + '; with the long formula ' + dl.map(x => x.toFixed(1)).join(', ')); }
// ---- 4. section 14: where three-field farming begins and ends, by yield ----
{ const book = [[10, 29.9, 34.7], [9, 27.8, 33.3], [8, 24.7, 31.5], [7, 19.8, 28.6], [6, 10.5, 23.6], [5.4, 0, 18.6]];
  const out = (b) => b < 1.5 ? Math.max(0, T.distance(b, 1.5)) : 0;
  const d = book.map(([y, b0, b1]) => [out(T.priceEqual(y)) - b0, out(T.priceZeroDrei(y)) - b1]);
  check('section 14, table: three-field farming begins and ends within 0.1 mile of the book at all six yields', worst(d.flat()) <= 0.1, 'differences ' + d.map(p => p.map(x => x.toFixed(2)).join('/')).join(', '));
  check('sections 22, 23: the standard state: Koppel to 24.7 miles, three fields to 31.5', Math.abs(T.rings(1.5, 8)[3] - 24.7) < 0.05 && Math.abs(T.rings(1.5, 8)[4] - 31.5) < 0.05, T.rings(1.5, 8).map(x => x.toFixed(2)).join(', '));
  check('section 14: at 1 Taler the two pay alike on land of 6.3 Körner', Math.abs(T.priceEqual(6.3) - 1) < 0.01, 'the price of equal rent at 6.3 Körner is ' + T.priceEqual(6.3).toFixed(3)); }
// ---- 5. the text to plate III: radius of the cultivated plain by the town's price (10 Körner), and the areas ----
{ const book = [[1.5, 34.7], [1.35, 31.7], [1.2, 28.6], [1.05, 25.0], [0.9, 20.9], [0.75, 16.1], [0.6, 10.4]], d = book.map(([a, r]) => T.plain(a, 10) - r);
  check('plate III: the radius of the plain at seven town prices is within 0.25 mile of the book', worst(d) <= 0.25, 'differences ' + d.map(x => x.toFixed(2)).join(', '));
  const short = book.map(([a, r]) => 182 * (a - 0.381) / (2.3 * a + 0.381 + 2.1) - r);
  check('   (the book\'s figures lie between its long formula and its short one at every price but the first)', book.slice(1).every((_, i) => d[i + 1] >= -0.02 && short[i + 1] <= 0.02), 'short-formula differences ' + short.map(x => x.toFixed(2)).join(', '));
  const areas = [[1.35, 844], [1.2, 687], [1.05, 525], [0.9, 367], [0.75, 217]], da = areas.map(([a, v]) => 1000 * Math.pow(T.plain(a, 10) / T.plain(1.5, 10), 2) - v);
  check('plate III: areas of the plain per 1,000 at five prices (844, 687, 525, 367, 217) within 2', worst(da) <= 2, 'differences ' + da.map(x => x.toFixed(1)).join(', '));
  const fromPrinted = [[31.7, 844], [28.6, 687], [25.0, 525], [20.9, 367], [16.1, 217]].map(([r, v]) => 1000 * Math.pow(r / 34.7, 2) - v);
  check('   (the book\'s printed radii would give areas 835, 679, 519, 363, 215: the book disagrees with itself here)', worst(fromPrinted) > 5 && Math.round(1000 * Math.pow(31.7 / 34.7, 2)) === 835, 'differences ' + fromPrinted.map(x => x.toFixed(0)).join(', '));
  check('section 24: "no farm further than 23.5 miles" could deliver at 1 Taler in the town; the program gives 20.0 (NOT reproduced; the test records it)', Math.abs(T.plain(1, 8) - 20.0) < 0.05 && Math.abs(T.plain(1, 8) - 23.5) > 3, T.plain(1, 8).toFixed(2) + ' miles at 8 Körner; ' + T.plain(1, 10).toFixed(2) + ' at 10');
  check('plate III: a tax of 0.3 Taler narrows the plain from 34.7 to 28.6 miles', Math.abs(T.plain(1.2, 10) - 28.6) < 0.2 && Math.abs(T.plain(1.5, 10) - 34.7) < 0.05);
  // the third ring's width is taken from the plates, so the two figures in the text hold by construction; what can fail is the
  // run of widths the referee measured on plate III between them (referee/report.md; it says its widths may be up to half a mile short)
  const w3 = (a, y) => { const r = T.rings(a, y); return r[2] - r[1]; };
  const plate = [[1.33, 6.4], [1.22, 4.6], [1.18, 4.2], [1.07, 2.4], [1.03, 1.8], [0.99, 1.0], [0.95, 0.2], [0.93, 0]], dp = plate.map(([a, v]) => w3(a, 10) - v);
  check('plate III: the third ring at 10 Körner: 9.4 miles wide at 1 1/2 Taler and none at 0.9 (the text); eight widths between, as the referee measured them, within 0.6 mile', Math.abs(w3(1.5, 10) - 9.4) < 1e-9 && w3(0.9, 10) === 0 && worst(dp) <= 0.6, 'differences ' + dp.map(x => x.toFixed(2)).join(', '));
  check('plates I and IV: the third ring at 1 1/2 Taler: 2.9 miles wide at 8 Körner, 0.6 at 7.47, none at 7.33', Math.abs(w3(1.5, 8) - 2.9) < 1e-9 && Math.abs(w3(1.5, 7.47) - 0.6) < 0.05 && w3(1.5, 7.33) === 0, 'at 7.47 Körner ' + w3(1.5, 7.47).toFixed(2) + ' (the three points lie on one line; only two were used)');
  const kw = [[1.5, 21.4], [1.05, 13.4], [0.6, 1.6]].map(([a, v]) => { const r = T.rings(a, 10); return r[3] - r[1] - v; });
  check('plate III: Koppel and the third ring together (21.4, 13.4, 1.6 miles at 1.50, 1.05, 0.60 Taler): mine differ by under 1 mile', worst(kw) < 1, 'differences ' + kw.map(x => x.toFixed(2)).join(', ') + ' (the book\'s forest ring is wider than mine at 10 Körner)');
  const dw = [[1.5, 4.5], [1.05, 5.4], [0.6, 6.2]].map(([a, v]) => { const r = T.rings(a, 10); return r[4] - r[3] - v; });
  check('plate III: the three-field ring (4.5, 5.4, 6.2 miles wide): mine within 0.4', worst(dw) < 0.4, 'differences ' + dw.map(x => x.toFixed(2)).join(', ') + '; section 14 itself gives 4.8 for the first'); }
// ---- 6. the text to plate IV: radius of the plain by yield ----
{ const book = [[10, 34.7], [9, 33.3], [8, 31.5], [7, 28.6], [6, 23.6], [5, 13.3]], d = book.map(([y, r]) => T.plain(1.5, y) - r);
  check('plate IV: the radius of the plain at six yields is within 0.1 mile of the book', worst(d) <= 0.1, 'differences ' + d.map(x => x.toFixed(2)).join(', '));
  check('plate IV: at 4 Körner the book prints 2.2 miles; the rent formulas give no grain farming at all', T.plain(1.5, 4) === 0, 'three-field rent at 4 Körner and 1 1/2 Taler: ' + T.rentDrei(1.5, 4).toFixed(0));
  const r5 = T.rings(1.5, 5); check('plate IV: at 5 Körner Koppel is gone (the book: "schon ganz verschwunden")', r5[3] === r5[1] && T.rings(0.75, 10)[3] > T.rings(0.75, 10)[1], 'at 0.75 Taler and 10 Körner Koppel reaches ' + (100 * T.rings(0.75, 10)[3] / T.plain(0.75, 10)).toFixed(0) + '% of the radius; its own width is ' + (100 * (T.rings(0.75, 10)[3] - T.rings(0.75, 10)[1]) / T.plain(0.75, 10)).toFixed(0) + '% (the book: 38%)'); }
// ---- 7. section 28: the three problems ----
{ const rent = T.rentDrei(1.5, 5); check('section 28, first problem: land of 4.2 Körner (three-field scale) at 1 1/2 Taler pays 114 Taler', Math.abs(rent - 114) < 0.51 && Math.abs(5 * 0.84 - 4.2) < 1e-9, rent.toFixed(1));
  const b = (114 + 327) / 696, x = T.distance(b, 1.5); check('   which the standard land pays where rye is worth 441/696 Taler, "about 26 miles" out', Math.abs(x - 26) < 0.3, b.toFixed(3) + ' Taler, ' + x.toFixed(1) + ' miles; the scan prints 0,683, which would be ' + T.distance(0.683, 1.5).toFixed(1) + ' miles and is not 441/696');
  const k0 = 1119 / 201; check('section 28, second problem: three-field rent is nothing at 3.72 Körner', Math.abs((10 - k0) * 0.84 - 3.72) < 0.006 && Math.abs(T.rentDrei(1.5, 10 - k0)) < 1e-9, ((10 - k0) * 0.84).toFixed(3));
  const k1 = 699 / 152.5; check('section 28, third problem: the two pay alike at 5.42 Körner (4.55 under three fields)', Math.abs(10 - k1 - 5.42) < 0.006 && Math.abs((10 - k1) * 0.84 - 4.55) < 0.006 && Math.abs(T.rentKoppel(1.5, 10 - k1) - T.rentDrei(1.5, 10 - k1)) < 1e-9, (10 - k1).toFixed(3) + ', ' + ((10 - k1) * 0.84).toFixed(3)); }
// ---- 8. which ring: the plain state, and the book's two examples of a motley map ----
{ const want = [[2, 1], [5.5, 2], [8.5, 3], [15, 4], [28, 5], [40, 6], [60, 7]];
  check('ring: the standard state at 2, 5.5, 8.5, 15, 28, 40 and 60 miles gives rings 1 to 6 and wilderness', want.every(([d, r]) => T.ring(d, 8, 1.5) === r), want.map(([d]) => T.ring(d, 8, 1.5)).join(' '));
  let agree = 0, n = 0; for (const a of [1.5, 1.2, 0.9, 0.6]) for (const y of [10, 8, 6, 5]) { const r = T.rings(a, y); for (let d = 0.05; d < 70; d += 0.1) { let k = 0; while (k < 6 && d >= r[k]) k++; n++; if (T.ring(d, y, a) === k + 1) agree++; } }
  check('ring: the rule for one place and the radii for the plain agree at every tenth of a mile, 16 settings', agree === n, agree + ' of ' + n);
  check('section 28: sandy land 10 miles from the town falls to the sixth ring', T.ring(10, 4, 1.5, 8) === 6, 'yield 4 Körner: ring ' + T.ring(10, 4, 1.5, 8));
  check('section 28: very rich land 100 miles down a river (10 miles of land carriage) belongs to the third ring', T.ring(10, 10, 1.5, 8) === 3 && T.ring(11, 8, 1.5, 8) === 4 && T.ring(16, 10, 1.5, 8) === 3 && T.ring(17, 10, 1.5, 8) === 4, 'yield 10 Körner: ring ' + T.ring(10, 10, 1.5, 8) + '; standard land a mile further: ring ' + T.ring(11, 8, 1.5, 8)); }
// ---- 9. water ----
{ const river = [{ pts: [[0, 0], [0, 120]], ratio: 0.1 }], net = new T.Net({ x: 0, y: 0 }, river, 0.25);
  check('section 28: a farm on the river 100 miles from the market is as the farm 10 miles from the town', Math.abs(net.eq(0, 100) - 10) < 1e-9, net.eq(0, 100).toFixed(6));
  check('section 28: a farm 5 miles from the river and 100 down it is as the farm 15 miles out', Math.abs(net.eq(5, 100) - 15) < 0.03 && net.eq(5, 100) <= 15 + 1e-9, net.eq(5, 100).toFixed(4) + ': a slanting way to the river saves a fortieth of a mile on the book\'s 5 + 10');
  // the true least cost for a straight river: go over land at the angle whose sine is the ratio
  const exact = (px, py) => Math.min(Math.hypot(px, py), px * Math.sqrt(1 - 0.01) + py * 0.1); let w = 0;
  const half = new T.Net({ x: 0, y: 0 }, river, 0.5); let wn = 0;      // the page's own spacing of nodes
  for (let k = 0; k < 4000; k++) { const px = 40 * ((k * 37) % 101) / 101, py = 5 + 110 * ((k * 53) % 97) / 97; w = Math.max(w, Math.abs(half.eq(px, py) - exact(px, py)));
    let nodesOnly = Infinity; for (let i = 0; i < half.xs.length; i++) nodesOnly = Math.min(nodesOnly, half.gs[i] + Math.hypot(px - half.xs[i], py - half.ys[i])); wn = Math.max(wn, nodesOnly - exact(px, py)); }
  check('water: against the exact least cost for a straight river at 4,000 places, some of them on the bank', w < 1e-9, 'greatest difference ' + w.toExponential(1) + ' miles; joining the river only at its nodes, half a mile apart, would be out by up to ' + wn.toFixed(2));
  const plain = new T.Net({ x: 0, y: 0 }, []); let ok = true, okr = true, sym = 0;
  for (let k = 0; k < 400; k++) { const px = -60 + 120 * ((k * 37) % 101) / 101, py = -40 + 160 * ((k * 53) % 97) / 97, e = net.eq(px, py), c = Math.hypot(px, py);
    if (e > c + 1e-9 || Math.abs(plain.eq(px, py) - c) > 1e-9) ok = false; if (e < 0.1 * c - 1e-9) okr = false; sym = Math.max(sym, Math.abs(e - net.eq(-px, py))); }
  check('water: with no river the distance is the crow\'s; a river never makes any of 400 places further', ok);
  check('water: and never nearer than a tenth of the crow\'s distance; the two banks are alike', okr && sym < 1e-9, 'greatest difference between the banks ' + sym.toExponential(1));
  // a river that misses the town by 6 miles: carriage over land to it, down it, and over land again
  const miss = new T.Net({ x: 0, y: 0 }, [{ pts: [[6, -80], [6, 80]], ratio: 0.1 }], 0.25), e = miss.eq(6, 70), want = 70 * 0.1 + 6 * Math.sqrt(0.99);
  check('water: a river passing 6 miles from the town: a farm on it 70 miles up', Math.abs(e - want) < 0.002, e.toFixed(4) + ' against ' + want.toFixed(4) + ' by hand (the cart leaves the river at a node, a quarter of a mile apart here)');
  const two = new T.Net({ x: 0, y: 0 }, [{ pts: [[0, 0], [0, 60]], ratio: 0.1 }, { pts: [[0, 0], [0, 60]], ratio: 0.5 }], 0.25);
  check('water: of two ways side by side the cheaper is taken', Math.abs(two.eq(0, 60) - 6) < 1e-9, two.eq(0, 60).toFixed(4));
  // plate II in words: along the river the third ring reaches the border of the state as drawn (40 miles), and the stock ring is gone near the river
  const r40 = T.ring(net.eq(1, 40), 8, 1.5), r39 = T.ring(net.eq(4, 39), 8, 1.5), far = T.ring(net.eq(45, 0), 8, 1.5), near = []; for (let y = 5; y <= 40; y += 5) near.push(T.ring(net.eq(8, y), 8, 1.5));
  check('plate II: forty miles down the river, a mile from the bank is forest and four miles from it the third ring', r40 === 2 && r39 === 3, 'rings ' + r40 + ' and ' + r39);
  check('plate II: no stock farming within 8 miles of the river down to 40 miles, though there is at 45 miles on the open plain', far === 6 && near.every(r => r < 6), 'rings 8 miles from the river: ' + near.join(' ')); }
console.log(`${pass} pass, ${fail} fail`);
process.exit(fail ? 1 : 0);
