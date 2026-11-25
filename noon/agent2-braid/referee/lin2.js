// referee: the ripple measurement with the smooth bed's own change taken off first (linear.js does not do this), so that what is
// projected is the response to the ripple alone.  Prints both: "raw" as linear.js has it, "net" with the smooth bed's change removed.
//   usage: node lin2.js NY J0 J1 [epsInRowFalls]
const { Bed } = require('/home/agent2/braid/core.js');
const NY = +process.argv[2], J0 = +process.argv[3], J1 = +process.argv[4], NX = 64, S = 0.05, CS = 0.05, KL = 0.4, M = 2.5, eps = (+process.argv[5] || 1e-4) * S;
const Ls = [0, 512, 256, 128, 64, 32], ns = [1, 2, 3, 4, 8, 16, 32];
const base = new Bed({ NX, NY, FEED: 1, NOISE: 0, CS, KL, M, SLOPE: S }); base.step(true);
let bmax = 0; for (let j = J0; j < J1; j++) for (let i = 0; i < NX; i++) bmax = Math.max(bmax, Math.abs(base.dh[j * NX + i]));
const F0 = Math.pow(1 * 0.3729 * (S + CS), M);
console.log(`NY ${NY}, rows ${J0}..${J1 - 1}, eps ${eps / S} row-falls; the smooth bed's own greatest change in these rows: ${(bmax / F0).toExponential(2)} of a cell's flux`);
console.log('half-waves across; then for lengths along inf 512 256 128 64 32: raw (as linear.js) / net (smooth bed taken off)');
for (const n of ns) {
  let line = String(n).padStart(4) + '  ';
  for (const L of Ls) {
    const b = new Bed({ NX, NY, FEED: 1, NOISE: 0, CS, KL, M, SLOPE: S });
    const kx = Math.PI * n / NX, ky = L ? 2 * Math.PI / L : 0, mode = (i, j) => Math.cos(kx * (i + 0.5)) * Math.cos(ky * j);
    for (let j = 1; j < NY - 1; j++) for (let i = 0; i < NX; i++) b.h[j * NX + i] += eps * mode(i, j);
    b.step(true);
    let num = 0, net = 0, den = 0; for (let j = J0; j < J1; j++) for (let i = 0; i < NX; i++) { const m = mode(i, j); num += b.dh[j * NX + i] * m; net += (b.dh[j * NX + i] - base.dh[j * NX + i]) * m; den += eps * m * m; }
    line += ((num / den) * S / F0).toFixed(4).padStart(9) + '/' + ((net / den) * S / F0).toFixed(4);
  }
  console.log(line);
}
