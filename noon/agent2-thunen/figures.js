// figures.js -- how many of the book's printed figures does the program give exactly, rounded as the book prints them?
// Each entry: what the book prints, what the program gives, and to how many decimals the book prints it.   usage: node figures.js
const T = require('./core.js'); let same = 0, n = 0; const lines = [];
function tally(name, rows) { let s = 0; rows.forEach(([book, mine, dec]) => { n++; if (Math.abs(+mine.toFixed(dec) - book) < 1e-9) { same++; s++; } }); lines.push(`${name}: ${s} of ${rows.length}` + (s < rows.length ? '   (misses: ' + rows.filter(([b, m, d]) => Math.abs(+m.toFixed(d) - b) >= 1e-9).map(([b, m, d]) => b + ' against ' + m.toFixed(d)).join(', ') + ')' : '')); }
const out = (b, a) => b < a ? Math.max(0, T.distance(b, a)) : 0;
tally('section 4: worth of 1,000 Scheffel at 0 to 45 miles', [[1500, 0], [1313, 5], [1136, 10], [968, 15], [809, 20], [656, 25], [512, 30], [374, 35], [242, 40], [116, 45]].map(([v, d]) => [v, 1000 * T.price(d, 1.5), 0]));
tally('section 4: where rye is worth nothing', [[49.95, T.distance(0, 1.5), 2]]);
tally('section 4: freight of a load', [[5.33, 5, 2], [10.4, 10, 1], [19.8, 20, 1], [28.2, 30, 1]].map(([v, d, dec]) => [v, T.freight(d), dec]));
tally('section 5: rent of the standard land by distance (long price formula, as on the page)', [[1066, 1], [892, 5], [685, 10], [488, 15], [301, 20], [124, 25]].map(([v, d]) => [v, T.rentKoppel(T.price(d, 1.5), 8), 0]).concat([[28.6, out(T.priceZeroKoppel(8), 1.5), 1]]));
tally('section 14: rents at 10 Körner', [[1818, T.rentKoppel(1.5, 10), 0], [963, T.rentKoppel(1, 10), 0], [108, T.rentKoppel(0.5, 10), 0], [1119, T.rentDrei(1.5, 10), 0], [619, T.rentDrei(1, 10), 0], [119, T.rentDrei(0.5, 10), 0]]);
tally('section 14: prices of equal and of no rent', [[0.516, T.priceEqual(10), 3], [0.437, T.priceZeroKoppel(10), 3], [0.381, T.priceZeroDrei(10), 3], [0.549, T.priceZeroKoppel(8), 3], [0.470, T.priceZeroDrei(8), 3]]);
tally('section 14: where three fields begin and end', [[10, 29.9, 34.7], [9, 27.8, 33.3], [8, 24.7, 31.5], [7, 19.8, 28.6], [6, 10.5, 23.6], [5.4, 0, 18.6]].flatMap(([y, b0, b1]) => [[b0, out(T.priceEqual(y), 1.5), 1], [b1, out(T.priceZeroDrei(y), 1.5), 1]]));
tally('plate III: radius of the plain by town price', [[1.5, 34.7], [1.35, 31.7], [1.2, 28.6], [1.05, 25.0], [0.9, 20.9], [0.75, 16.1], [0.6, 10.4]].map(([a, r]) => [r, T.plain(a, 10), 1]));
tally('plate III: areas of the plain', [[1.35, 844], [1.2, 687], [1.05, 525], [0.9, 367], [0.75, 217]].map(([a, v]) => [v, 1000 * Math.pow(T.plain(a, 10) / T.plain(1.5, 10), 2), 0]));
tally('plate III: widths of Koppel with the third ring, and of three fields', [[1.5, 21.4, 4.5], [1.05, 13.4, 5.4], [0.6, 1.6, 6.2]].flatMap(([a, kw, dw]) => { const r = T.rings(a, 10); return [[kw, r[3] - r[1], 1], [dw, r[4] - r[3], 1]]; }));
tally('plate IV: radius of the plain by yield', [[10, 34.7], [9, 33.3], [8, 31.5], [7, 28.6], [6, 23.6], [5, 13.3], [4, 2.2]].map(([y, r]) => [r, T.plain(1.5, y), 1]));
tally('section 24: the plain at 1 Taler in the town', [[23.5, T.plain(1, 8), 1]]);
tally('section 28: the three problems', [[114, T.rentDrei(1.5, 5), 0], [26, T.distance(441 / 696, 1.5), 0], [3.72, (10 - 1119 / 201) * 0.84, 2], [5.42, 10 - 699 / 152.5, 2], [4.55, (10 - 699 / 152.5) * 0.84, 2]]);
lines.forEach(l => console.log(l)); console.log(`in all: ${same} of ${n} printed figures are given exactly, rounded as printed`);
