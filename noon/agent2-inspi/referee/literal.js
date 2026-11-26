// Second witness: the rule taken literally, one step at a time, no state-return logic, no hull.
//   repeat: FORWARD 1; RIGHT ANGLE; ANGLE += INC      (whole degrees kept as integers mod 360)
// home = |position| < TOL and heading == 0 and ANGLE == first ANGLE (mod 360).
// "never" here means only: not home within CAP steps (the proof that it is never is in the report).
'use strict';
const TOL = 1e-9, CAP = 5000;
const C = new Float64Array(360), S = new Float64Array(360);
for (let h = 0; h < 360; h++) { C[h] = Math.cos(-Math.PI * h / 180); S[h] = Math.sin(-Math.PI * h / 180); }
let never = 0, homeCount = 0, maxSteps = 0, q6 = [], neverVisit = 0;
let closest = { d: 1e9, list: [] };
const neverInc = new Set();
let widest = { d: -1, list: [] }, narrowest = { d: 1e9, list: [] };
const X = new Float64Array(CAP + 1), Y = new Float64Array(CAP + 1);
let homeEarlyVisits = 0;
const t0 = Date.now();
for (let inc = 1; inc < 360; inc++) {
  for (let ang = 0; ang < 360; ang++) {
    let a = ang, h = 0, x = 0, y = 0, homeAt = 0, minD = 1e9, minAt = 0, minH = 0, early = 0;
    for (let n = 1; n <= CAP; n++) {
      x += C[h]; y += S[h];
      h = (h + a) % 360;
      a = (a + inc) % 360;
      X[n] = x; Y[n] = y;
      const d = Math.hypot(x, y);
      if (d < TOL && h === 0 && a === ang) { homeAt = n; break; }
      if (d < TOL) { early++; if (h === 0) q6.push([inc, ang, n]); }
      if (d < minD) { minD = d; minAt = n; minH = h; }
    }
    if (homeAt) {
      homeCount++; if (homeAt > maxSteps) maxSteps = homeAt;
      if (early) homeEarlyVisits++;
      // brute-force greatest distance between two corners (all positions 1..homeAt)
      let best = 0;
      for (let i = 1; i <= homeAt; i++) {
        const xi = X[i], yi = Y[i];
        for (let j = i + 1; j <= homeAt; j++) {
          const dx = xi - X[j], dy = yi - Y[j], s = dx * dx + dy * dy;
          if (s > best) best = s;
        }
      }
      const dm = Math.sqrt(best);
      if (dm > widest.d + 1e-7) widest = { d: dm, list: [[inc, ang]] };
      else if (Math.abs(dm - widest.d) <= 1e-7) widest.list.push([inc, ang]);
      if (dm < narrowest.d - 1e-7) narrowest = { d: dm, list: [[inc, ang]] };
      else if (Math.abs(dm - narrowest.d) <= 1e-7) narrowest.list.push([inc, ang]);
    } else {
      never++; neverInc.add(inc);
      if (early) neverVisit++;
      if (minD < closest.d - 1e-9) closest = { d: minD, list: [[inc, ang, minAt, minH]] };
      else if (Math.abs(minD - closest.d) <= 1e-9) closest.list.push([inc, ang, minAt, minH]);
    }
  }
}
const incs = Array.from(neverInc).sort((p, q) => p - q);
console.log(JSON.stringify({
  cap: CAP, tol: TOL, pairs: 359 * 360, notHomeWithinCap: never, home: homeCount, maxSteps,
  neverIncCount: incs.length, neverIncAllEven: incs.every(i => i % 2 === 0),
  neverPairsStandingOnStartWithinCap: neverVisit, closest, q6hits: q6.length,
  homePairsOnStartEarly: homeEarlyVisits, widest, narrowest, seconds: (Date.now() - t0) / 1000
}, null, 1));
