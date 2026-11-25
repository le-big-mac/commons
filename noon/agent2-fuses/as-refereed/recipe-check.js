// recipe-check.js -- recipes: every meek successor on a grid has one that checks from 0 upward; numbers that Algorithm 2
// calls not fusible have none.   node --stack-size=20000 recipe-check.js K TOP
const F = require('./core.js'), fs = require('fs'), say = s => fs.writeSync(1, s + '\n'); const K = +process.argv[2], top = Math.floor(eval(process.argv[3]) * (1 << K));
const f = new F.Fusible();
function verify(node) { const ok = new Map(); function go(n) { const k = F.key(n.v); if (ok.has(k)) return ok.get(k); let r; if (!n.a) r = n.v[0] === 0n; else { const d = F.sub(n.a.v, n.b.v); r = F.cmp(d, F.UNIT) < 0 && F.cmp(d, F.D(-1, 0)) > 0 && F.cmp(F.fuse(n.a.v, n.b.v), n.v) === 0 && go(n.a) && go(n.b); } ok.set(k, r); return r; } return go(node); }
let n = 0, noRecipe = [], badRecipe = [], maxF = 0, maxAt = null, falsePos = [], nonf = 0, agree = 0;
for (let i = 0; i < top; i++) { const r = F.D(i, K), z = f.meekSucc(r), rec = f.recipe(z); n++; if (!rec) noRecipe.push(F.str(z)); else { if (!verify(rec)) badRecipe.push(F.str(z)); const sz = F.recipeSize(rec); if (sz.fuses > maxF) { maxF = sz.fuses; maxAt = z; } }
  const isf = f.isFusible(r), has = !!f.recipe(r); if (!isf) nonf++; if (has && !isf) falsePos.push(F.str(r)); if (has === isf) agree++; }
say(`grid of 1/2^${K} below ${process.argv[3]} (${n} points): the meek successor of each has a recipe that checks, except ${noRecipe.length} with none${noRecipe.length ? ' (' + noRecipe.slice(0, 4).join(' ') + ')' : ''} and ${badRecipe.length} that do not check; the most fuses in one: ${maxF}, for ${F.str(maxAt)}`);
say(`the grid points themselves: a recipe exactly when Algorithm 2 calls the point fusible at ${agree} of ${n} (${nonf} are not fusible); a recipe for a number Algorithm 2 calls not fusible: ${falsePos.length}`);
const w = f.recipe(F.parse('8449/4096')), sz = F.recipeSize(w); say(`8449/4096 = ${F.str(w.a.v)} ~ ${F.str(w.b.v)}; ${sz.fuses} fuses, height ${sz.height}`);
