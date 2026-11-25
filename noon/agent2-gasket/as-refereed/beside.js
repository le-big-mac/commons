// beside.js -- a broken copy of gcore.js that passed the tests, run beside the true one: where do they differ?
//   node beside.js mutants/NAME.js     (every root quadruple with outer circle -1 to -30 and the strip: place(); the whole
//   packing and 40 random views each, down to a hundred-thousandth of the packing; and how often the true program's rule
//   "the gap is the outside of its circle" is met at all)
const A = require('./gcore.js'), B = require('./' + process.argv[2]), fs = require('fs'), say = s => fs.writeSync(1, s + '\n');
let seed = 2718; const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648;
const roots = [[0, 0, 1, 1]]; for (let a = -1; a >= -30; a--) for (let b = -a; b <= 4 * a * a + 2; b++) for (let c = b; c <= 2 * (a * a) * 4 + 60; c++) { const pr = a * b + a * c + b * c; if (pr < 0) continue; const r = Math.round(Math.sqrt(pr)); if (r * r !== pr) continue; const d = a + b + c - 2 * r; if (d < c) continue; const q = [a, b, c, d]; if (A.isDescartes(q) && A.isPrimitive(q)) roots.push(q); }
// the true program with a counter where the rule is met
const src = fs.readFileSync('./gcore.js', 'utf8'), mark = "if (dc > R) return true;"; if (src.split(mark).length !== 2) throw new Error('rule not found');
fs.writeFileSync('./mutants/_counting.js', src.replace(mark, "if (dc > R) { globalThis.__outside = (globalThis.__outside || 0) + 1; return true; }")); const C = require('./mutants/_counting.js');
let nPlace = 0, dPlace = 0, nView = 0, dView = [], circles = 0;
for (const q of roots) { const pa = A.place(q), pb = B.place(q); nPlace++; if (JSON.stringify(pa) !== JSON.stringify(pb)) dPlace++;
  const R = pa.strip ? 1 : 1 / Math.abs(q[0]), cx = pa.strip ? 1 : pa.circles[0][1] / q[0], cy = pa.strip ? 0 : pa.circles[0][2] / q[0];
  for (let k = 0; k < 41; k++) { const w = k === 0 ? 2.2 * R : R * Math.pow(10, -5 * rnd()) * 2, x0 = k === 0 ? cx - 1.1 * R : cx + (rnd() * 2 - 1) * R - w / 2, y0 = k === 0 ? cy - 1.1 * R : cy + (rnd() * 2 - 1) * R - w / 2, v = [x0, y0, x0 + w, y0 + w * 0.62], minR = w / 700, ga = [], gb = [];
    A.inView(pa, v, minR, (b, X, Y) => ga.push(b + ',' + X + ',' + Y), 2000000); B.inView(pb, v, minR, (b, X, Y) => gb.push(b + ',' + X + ',' + Y), 2000000); C.inView(pa, v, minR, () => {}, 2000000); nView++; circles += ga.length;
    if (ga.length !== gb.length || ga.some((s, i) => s !== gb[i])) dView.push(JSON.stringify(q) + ' ' + v.map(x => x.toPrecision(5)).join(' ')); } }
say(process.argv[2] + ': ' + roots.length + ' root quadruples; place() differs for ' + dPlace + '; of ' + nView + ' views (' + circles + ' circles shown) the lists differ in ' + dView.length + (dView.length ? ' (first: ' + dView[0] + ')' : '') + '; in the true program the rule "the gap is the outside of its circle" was met ' + (globalThis.__outside || 0) + ' times');
