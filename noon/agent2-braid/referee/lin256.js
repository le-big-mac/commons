// referee: Noon's ripple measurement (linear.js) redone on the page's own bed (256 rows) and near the head of a long bed.
// One step on a smooth bed + ripple eps*cos(kx(i+.5))*cos(ky j); change of the bed projected on the ripple over rows J0..J1-1.
// Rate in units of (sheet's flux per cell)/(row-fall), as in linear.js.   usage: node lin256.js NY J0 J1
const { Bed } = require('/home/agent2/braid/core.js');
const NY = +process.argv[2], J0 = +process.argv[3], J1 = +process.argv[4], NX = 64, S = 0.05, CS = 0.05, KL = 0.4, M = 2.5, eps = 1e-4 * S;
const Ls = [0, 512, 256, 128, 64, 32], ns = [1, 2, 4, 8, 16, 32];
console.log(`NY ${NY}, measured over rows ${J0}..${J1 - 1}; rows: half-waves across; columns: ripple length along (inf 512 256 128 64 32)`);
for (const n of ns) {
  let line = String(n).padStart(4) + '  ';
  for (const L of Ls) {
    const b = new Bed({ NX, NY, FEED: 1, NOISE: 0, CS, KL, M, SLOPE: S });
    const kx = Math.PI * n / NX, ky = L ? 2 * Math.PI / L : 0, mode = (i, j) => Math.cos(kx * (i + 0.5)) * Math.cos(ky * j);
    for (let j = 1; j < NY - 1; j++) for (let i = 0; i < NX; i++) b.h[j * NX + i] += eps * mode(i, j);
    b.step();
    let num = 0, den = 0; for (let j = J0; j < J1; j++) for (let i = 0; i < NX; i++) { const m = mode(i, j); num += b.dh[j * NX + i] * m; den += eps * m * m; }
    const F0 = Math.pow(1 * 0.3729 * (S + CS), M);
    line += ((num / den) * S / F0).toFixed(4).padStart(9);
  }
  console.log(line);
}
