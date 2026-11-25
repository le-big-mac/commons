// linear.js -- which small ripples on a smooth sheet of water grow?  A ripple eps*cos(kx x)*cos(ky y) is laid on a smooth bed with
// water in every head cell; one step's change of the bed is reckoned with the ripple and without it, and the difference is
// projected back on the ripple.  Printed: the rate of growth in units of (the sand one cell of the sheet sends straight on) per
// row-fall, so that -1 means "fills at about the rate the sheet moves sand".
//
// Taking off the change of the smooth bed itself matters, and my first version did not do it.  A smooth sheet between walls
// is not at rest (it changes beside the walls and below the head), and that change, projected on an even ripple and divided
// by a tiny ripple height, looked like growth.  The referee found this by making the ripple a hundred times higher: a rate
// cannot depend on the ripple's height.  Each table is therefore made at two heights, and the greatest difference is printed.
//   usage: node linear.js CS KL [long|page]
//     long: a bed of 2,600 rows, measured over rows 2,000 to 2,511 (the water has settled to the ripple there)
//     page: the page's own bed of 256 rows, measured over rows 64 to 191
const { Bed } = require('./core.js');
const CS = +process.argv[2], KL = +process.argv[3], which = process.argv[4] || 'long', NX = 64, S = 0.05;
const NY = which === 'long' ? 2600 : 256, J0 = which === 'long' ? 2000 : 64, JN = which === 'long' ? 512 : 128;
const Ls = which === 'long' ? [0, 512, 256, 128, 64, 32, 16, 8, 4] : [0, 128, 64, 32, 16, 8, 4], ns = [1, 2, 4, 8, 16, 24, 32];
function change(mode, eps) {            // one step's raw change of the bed, with a ripple of height eps (or none)
  const b = new Bed({ NX, NY, FEED: 1, NOISE: 0, CS, KL, SLOPE: S });
  if (mode) for (let j = 1; j < NY - 1; j++) for (let i = 0; i < NX; i++) b.h[j * NX + i] += eps * mode(i, j);
  b.step(true); return b.dh;
}
const base = change(null, 0), F0 = Math.pow(0.3729 * (S + CS), 2.5);
function rates(n, L, eps) {
  const kx = Math.PI * n / NX, ky = L ? 2 * Math.PI / L : 0, mode = (i, j) => Math.cos(kx * (i + 0.5)) * Math.cos(ky * j), dh = change(mode, eps);
  let num = 0, raw = 0, den = 0; for (let j = J0; j < J0 + JN; j++) for (let i = 0; i < NX; i++) { const m = mode(i, j), c = j * NX + i; num += (dh[c] - base[c]) * m; raw += dh[c] * m; den += eps * m * m; }
  return [num / den * S / F0, raw / den * S / F0];
}
console.log(`CS ${CS} (${(CS / S).toFixed(0)} x slope), KL ${KL}; ${which === 'long' ? 'a bed of 2,600 rows, measured over rows 2,000 to 2,511' : "the page's bed of 256 rows, measured over rows 64 to 191"}.`);
console.log('rows: half-waves across the 64 cells; columns: length of the ripple along the flow, in rows.  Ripple 1e-4 of a row-fall high, the smooth bed\'s own change taken off.');
console.log('across \\ along  ' + Ls.map(L => (L ? String(L) : 'none').padStart(9)).join(''));
let best = [-1e9, 0, 0], worst = 0, grow = 0, count = 0; const rawLines = [];
for (const n of ns) {
  let line = String(n).padStart(6) + '          ';
  for (const L of Ls) {
    const [a, araw] = rates(n, L, 1e-4 * S), [b, braw] = rates(n, L, 1e-2 * S);
    count++; if (a > 0) grow++; if (a > best[0]) best = [a, n, L]; worst = Math.max(worst, Math.abs(a - b));
    if (L === 0 && (n === 2 || n === 4)) rawLines.push(`   ${n} half-waves across, no length along: with the smooth bed's change left in, ${araw.toFixed(3)} at a height of 1e-4 and ${braw.toFixed(3)} at 1e-2; taken off, ${a.toFixed(4)} and ${b.toFixed(4)}`);
    line += a.toFixed(3).padStart(9);
  }
  console.log(line);
}
console.log(`${count} shapes; ${grow} grow; greatest rate ${best[0].toFixed(4)} at ${best[1]} half-waves across, length ${best[2] || 'none'} along; a ripple a hundred times higher gives the same rates to within ${worst.toExponential(1)}`);
rawLines.forEach(l => console.log(l));
