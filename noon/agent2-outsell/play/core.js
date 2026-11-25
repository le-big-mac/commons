/* The numerical core of the page (no browser needed, so it can be tested in node against the study's Python).
   Two products, A the better. With nA and nB sold, the next buyer takes A with probability
   q (a + nA)^g / (q (a + nA)^g + (a + nB)^g). */
function weights(g, N, a) { const w = new Float64Array(N + 1); for (let k = 0; k <= N; k++) w[k] = Math.pow(a + k, g); return w; }
function dist(q, g, N, a) {               // the exact probability of each nA = 0..N after N sales
  const w = weights(g, N, a), p = new Float64Array(N + 2); p[0] = 1;
  for (let n = 0; n < N; n++) {            // go down so that p[k] is still the old value when it is used
    for (let k = n; k >= 0; k--) { const wa = q * w[k], move = p[k] * wa / (wa + w[n - k]); p[k + 1] += move; p[k] -= move; }
  }
  return p.subarray(0, N + 1);
}
function ahead(p) {                       // the chance that A has sold more than B, plus half the chance of a tie
  const N = p.length - 1; let s = 0; for (let k = Math.floor(N / 2) + 1; k <= N; k++) s += p[k];
  return s + (N % 2 === 0 ? 0.5 * p[N / 2] : 0);
}
function below(p, share) { const N = p.length - 1; let s = 0; for (let k = 0; k <= N && k < share * N; k++) s += p[k]; return s; }   // the chance that A's share is under `share`
function market(q, g, N, a, rand) {       // one market, sale by sale: A's sales after each sale
  const w = weights(g, N, a), out = new Int32Array(N + 1); let nA = 0;
  for (let n = 0; n < N; n++) { const wa = q * w[nA]; if (rand() < wa / (wa + w[n - nA])) nA++; out[n + 1] = nA; }
  return out;
}
function settles(q, g) { if (g >= 1) return null; const o = Math.pow(q, 1 / (1 - g)); return o / (1 + o); }   // where A's share settles when copying is less than in proportion
if (typeof module !== 'undefined') module.exports = { dist, ahead, below, market, settles };
