// Run the core of the public live page (extras/bed-public.html: the script between "// ---- core" and "// ---- end core ----")
// without a browser, at the page's own opening settings unless told otherwise, and report for each run:
//   the first take-over (first generation at which the commonest kind is the three-state machine at any of its three entry
//   states, with at least 60% of the bed), and which entry state it was;
//   the share of generations in which the commonest kind was all-defect, each of the three entries, tit-for-tat/grim, other;
//   the episodes: an episode starts at a take-over as above and ends when all-defect is again the commonest kind with at
//   least 60% of the bed; lengths in generations.
// usage: node bed_core_runs.js RUNS GENERATIONS BETA SEED0 [EPS] [DELTA] [N]
const fs = require('fs'), vm = require('vm');
const html = fs.readFileSync('/home/agent3/site/build/extras/bed-public.html', 'utf8');
const a = html.indexOf('// ---- core'), b = html.indexOf('// ---- end core ----');
const sandbox = { module: { exports: {} }, Math, Map, Set, Float64Array, Object, console };
vm.runInNewContext(html.slice(a, b), sandbox);
const { World, KNOWN } = sandbox.module.exports;
const [runs, gens, beta, seed0, eps = '0.03', delta = '0.98', N = '100'] = process.argv.slice(2);
const FAM = { 'D01 D02 C20': 'handshake', 'D12 D10 C21': 'shifty', 'C01 D12 D10': 'wooer' };
const all = [];
for (let r = 0; r < +runs; r++) {
  const w = new World({ N: +N, eps: +eps, delta: +delta, beta: +beta, mu: 1 / +N, seed: +seed0 + r, founder: 'D00' });
  const share = {}; let first = null, inEp = false, epStart = 0; const eps_ = []; let coopSum = 0;
  for (let g = 0; g < +gens; g++) {
    let top = null, cnt = -1;                          // the commonest kind now, as the page's measure() picks it (first of equals)
    for (const [k, c] of w.counts) if (c > cnt) { cnt = c; top = k; }
    const frac = cnt / w.N;
    w.step();                                          // step() measures this same generation (w.coop) and then breeds the next
    const kind = top === 'D00' ? 'all-defect' : FAM[top] || (KNOWN[top] ? KNOWN[top][0] : 'unnamed');
    share[kind] = (share[kind] || 0) + 1; coopSum += w.coop;
    if (!inEp && FAM[top] && frac >= 0.6) { inEp = true; epStart = g; if (first === null) first = { gen: g, entry: FAM[top] }; }
    else if (inEp && top === 'D00' && frac >= 0.6) { inEp = false; eps_.push(g - epStart); }
  }
  const open = inEp ? +gens - epStart : null;
  const pct = k => (100 * (share[k] || 0) / +gens).toFixed(1);
  console.log(`run ${r + 1} seed ${+seed0 + r}: first take-over ${first ? 'at generation ' + first.gen + ' by ' + first.entry : 'none'}; cooperative moves ${(100 * coopSum / +gens).toFixed(0)}%; commonest kind, % of generations: ${Object.keys(share).sort((x, y) => share[y] - share[x]).map(k => k + ' ' + pct(k)).join(', ')}; finished episodes (generations): [${eps_.join(', ')}]${open !== null ? '; one still running after ' + open : ''}`);
  all.push({ first, share, eps: eps_, open });
}
