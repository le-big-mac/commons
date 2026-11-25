/* The numerical core of the page: no browser needed, so it can be tested in node against the Python of the study.
   A round skin of radius 1 under even tension, fixed at the rim, with mass per area 1 + load in each of 40 equal rings.
   Finite differences on the radial equation, 40 cells to a ring; eigenvalues by bisection on a Sturm count,
   mode shapes by inverse iteration. */
const RINGS = 40, PER = 40, N = RINGS * PER, H = 1 / N;
const NINE = [[0, 1], [1, 1], [2, 1], [0, 2], [3, 1], [1, 2], [4, 1], [2, 2], [0, 3]], TARGET = [1, 2, 3, 3, 4, 4, 5, 5, 5];
const SIXTEEN = NINE.concat([[5, 1], [3, 2], [1, 3], [6, 1], [4, 2], [2, 3], [0, 4]]), TARGET16 = TARGET.concat([6, 6, 6, 7, 7, 7, 7]);   // mode (m, n) is aimed at the multiple m + 2n - 1
function operator(m, load) {
  const a = new Float64Array(N), b = new Float64Array(N - 1), sc = new Float64Array(N);
  for (let i = 0; i < N; i++) {
    const r = (i + 0.5) * H, rho = 1 + load[Math.floor(i / PER)]; sc[i] = Math.sqrt(r * rho);
    let d = (2 * i + 1) / H + m * m / r; if (i === N - 1) d += N / H;
    a[i] = d / (sc[i] * sc[i]);
  }
  for (let i = 0; i < N - 1; i++) b[i] = -((i + 1) / H) / (sc[i] * sc[i + 1]);
  return { a, b, sc };
}
function countBelow(a, b, x) {            // how many eigenvalues of the tridiagonal matrix lie below x
  let c = 0, q = a[0] - x; if (q < 0) c++;
  for (let i = 1; i < a.length; i++) { if (q === 0) q = 1e-300; q = a[i] - x - b[i - 1] * b[i - 1] / q; if (q < 0) c++; }
  return c;
}
function lowest(a, b, k) {                // the k lowest eigenvalues
  let hi = 4; while (countBelow(a, b, hi) < k) hi *= 2;
  const out = [];
  for (let j = 0; j < k; j++) {
    let lo = j ? out[j - 1] : 0, up = hi;
    for (let it = 0; it < 56; it++) { const mid = 0.5 * (lo + up); if (countBelow(a, b, mid) > j) up = mid; else lo = mid; }
    out.push(0.5 * (lo + up));
  }
  return out;
}
function vector(a, b, lam) {              // the eigenvector for eigenvalue lam: inverse iteration, tridiagonal elimination with row swaps
  const n = a.length, dl = new Float64Array(n - 1), d = new Float64Array(n), du = new Float64Array(n - 1), du2 = new Float64Array(n - 2), piv = new Uint8Array(n - 1);
  const s = lam * (1 + 1e-10);
  for (let i = 0; i < n; i++) d[i] = a[i] - s;
  for (let i = 0; i < n - 1; i++) { dl[i] = b[i]; du[i] = b[i]; }
  for (let i = 0; i < n - 1; i++) {
    if (Math.abs(d[i]) >= Math.abs(dl[i])) {
      if (d[i] === 0) d[i] = 1e-300;
      const f = dl[i] / d[i]; dl[i] = f; d[i + 1] -= f * du[i];
    } else {
      const f = d[i] / dl[i]; d[i] = dl[i]; dl[i] = f; const t = du[i]; du[i] = d[i + 1]; d[i + 1] = t - f * d[i + 1];
      if (i < n - 2) { du2[i] = du[i + 1]; du[i + 1] = -f * du[i + 1]; }
      piv[i] = 1;
    }
  }
  if (d[n - 1] === 0) d[n - 1] = 1e-300;
  let x = new Float64Array(n); for (let i = 0; i < n; i++) x[i] = 1 + 0.3 * Math.sin(1.7 * i + 0.4);
  for (let it = 0; it < 3; it++) {
    for (let i = 0; i < n - 1; i++) {
      if (piv[i]) { const t = x[i]; x[i] = x[i + 1]; x[i + 1] = t - dl[i] * x[i]; } else x[i + 1] -= dl[i] * x[i];
    }
    x[n - 1] /= d[n - 1]; x[n - 2] = (x[n - 2] - du[n - 2] * x[n - 1]) / d[n - 2];
    for (let i = n - 3; i >= 0; i--) x[i] = (x[i] - du[i] * x[i + 1] - du2[i] * x[i + 2]) / d[i];
    let nrm = 0; for (let i = 0; i < n; i++) nrm += x[i] * x[i]; nrm = Math.sqrt(nrm); for (let i = 0; i < n; i++) x[i] /= nrm;
  }
  return x;
}
function nineRatios(load) {               // the nine modes as multiples of the lowest, and the lowest's own frequency
  const need = [3, 2, 2, 1, 1], w = {};
  for (let m = 0; m < 5; m++) { const op = operator(m, load), ev = lowest(op.a, op.b, need[m]); for (let n = 0; n < need[m]; n++) w[m + ',' + (n + 1)] = Math.sqrt(ev[n]); }
  const w0 = w['0,1']; return { ratios: NINE.map(([m, n]) => w[m + ',' + n] / w0), w0 };
}
function sixteenRatios(load) {            // the sixteen modes of the first seven families
  const need = [4, 3, 3, 2, 2, 1, 1], w = {};
  for (let m = 0; m < 7; m++) { const op = operator(m, load), ev = lowest(op.a, op.b, need[m]); for (let n = 0; n < need[m]; n++) w[m + ',' + (n + 1)] = Math.sqrt(ev[n]); }
  const w0 = w['0,1']; return { ratios: SIXTEEN.map(([m, n]) => w[m + ',' + n] / w0), w0 };
}
function largestMiss(ratios, count) { const k = count || 9; let t = 0; for (let i = 1; i < k; i++) t = Math.max(t, Math.abs(ratios[i] / TARGET16[i] - 1)); return t; }   // over the first nine modes unless told sixteen
const cents = x => 1200 * Math.log2(x);
function addedMass(load) { let s = 0; for (let j = 0; j < RINGS; j++) s += load[j] * (((j + 1) / RINGS) ** 2 - (j / RINGS) ** 2); return s; }
function shapeOf(m, n, load) {            // the radial shape of mode (m, n) at the cell centres, positive at its first swing
  const op = operator(m, load), ev = lowest(op.a, op.b, n), v = vector(op.a, op.b, ev[n - 1]), R = new Float64Array(N);
  let big = 0; for (let i = 0; i < N; i++) { R[i] = v[i] / op.sc[i]; if (Math.abs(R[i]) > big) big = Math.abs(R[i]); }
  let first = 0; while (first < N - 1 && Math.abs(R[first]) < 0.2 * big) first++;
  if (R[first] < 0) for (let i = 0; i < N; i++) R[i] = -R[i];
  return { R, w: Math.sqrt(ev[n - 1]) };
}
function allModes(load, top) {            // every mode up to `top` times the lowest: {m, n, ratio, R}
  const w0 = Math.sqrt(lowest(operator(0, load).a, operator(0, load).b, 1)[0]), out = [];
  for (let m = 0; m < 10; m++) {
    const op = operator(m, load), ev = lowest(op.a, op.b, 8);
    for (let n = 0; n < 8; n++) {
      const ratio = Math.sqrt(ev[n]) / w0; if (ratio > top) break;
      const v = vector(op.a, op.b, ev[n]), R = new Float64Array(N); for (let i = 0; i < N; i++) R[i] = v[i] / op.sc[i];
      out.push({ m, n: n + 1, ratio, R });
    }
  }
  out.sort((p, q) => p.ratio - q.ratio); return out;
}
function strengths(modes, strikeAt) {     // how strongly a stroke at radius strikeAt sets each mode going (the rule of the study's sound files)
  const x = strikeAt * N - 0.5, i0 = Math.max(0, Math.min(N - 2, Math.floor(x))), f = Math.max(0, Math.min(1, x - i0));
  return modes.map(md => { const a = (md.R[i0] * (1 - f) + md.R[i0 + 1] * f) / (md.m === 0 ? 2 : 1); return a / Math.sqrt(md.ratio) * Math.exp(-((md.ratio / 7) ** 2)); });
}
function stroke(modes, amps, f0, seconds, rate) {   // one stroke: each mode rings at its frequency and dies away, higher ones sooner (decay times invented)
  const n = Math.floor(seconds * rate), y = new Float32Array(n); let top = 0; for (const v of amps) top = Math.max(top, Math.abs(v));
  for (let k = 0; k < modes.length; k++) {
    const f = f0 * modes[k].ratio; if (f > 9000 || Math.abs(amps[k]) < 1e-7 * top) continue;
    const tau = 1.3 * Math.pow(modes[k].ratio, -0.8), g = Math.exp(-1 / (tau * rate)), w = 2 * Math.PI * f / rate, c = g * Math.cos(w), s = g * Math.sin(w);
    let re = 0, im = amps[k];             // im * sin(wt) e^(-t/tau), by turning a decaying phasor
    for (let i = 0; i < n; i++) { y[i] += re; const t = re * c + im * s; im = im * c - re * s; re = t; }
  }
  const ramp = Math.floor(0.004 * rate); for (let i = 0; i < ramp && i < n; i++) y[i] *= i / ramp;
  return y;
}
if (typeof module !== 'undefined') module.exports = { RINGS, PER, N, NINE, TARGET, SIXTEEN, TARGET16, sixteenRatios, operator, lowest, vector, nineRatios, largestMiss, cents, addedMass, shapeOf, allModes, strengths, stroke };
