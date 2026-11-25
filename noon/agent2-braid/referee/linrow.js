// referee: the ripple measurement row by row (L = inf ripple, n half-waves across), to see where along the bed a ripple grows.
const { Bed } = require('/home/agent2/braid/core.js');
const NY = +process.argv[2], n = +process.argv[3], NX = 64, S = 0.05, eps = (+process.argv[4] || 1e-4) * S;
const b = new Bed({ NX, NY, FEED: 1, NOISE: 0, CS: 0.05, KL: 0.4, M: 2.5, SLOPE: S });
const kx = Math.PI * n / NX, mode = i => Math.cos(kx * (i + 0.5));
for (let j = 1; j < NY - 1; j++) for (let i = 0; i < NX; i++) b.h[j * NX + i] += eps * mode(i);
b.step(true);
const F0 = Math.pow(0.3729 * (S + 0.05), 2.5); let out = [];
for (const j of [1, 2, 3, 5, 10, 20, 40, 64, 65, 66, 67, 100, 128, 129, 191, 254].filter(j => j < NY - 1)) {
  let num = 0, den = 0, qn = 0; for (let i = 0; i < NX; i++) { const m = mode(i); num += b.dh[j * NX + i] * m; den += eps * m * m; qn += (b.Q[j * NX + i] - 1) * m; }
  out.push(`row ${j}: rate ${((num / den) * S / F0).toFixed(4)}, water ripple ${(qn / den * S).toFixed(3)}`);
}
console.log(`n=${n} NY=${NY} eps=${eps / S} row-falls\n  ` + out.join('\n  '));
