// chain-check.js -- gapOrSmall against the full procedures: where it gives a gap it must be THE gap; where it says "at most
// 2^-k" the full gap must be at most that; and it must never say small when asked with p at or above the true exponent - 1.
const F = require('./core.js'), fs = require('fs'), say = s => fs.writeSync(1, s + '\n');
let seed = 777; const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648;
for (const meek of [false, true]) { const full = new F.Fusible(); let n = 0, exact = 0, small = 0, bad = [], nulls = 0;
  for (let i = 0; i < 6000; i++) { const e = Math.floor(rnd() * 22), r = F.D(Math.floor((rnd() * 3.4 - 1) * Math.pow(2, e)), e), p = Math.floor(rnd() * 40);
    const truth = meek ? full.meekM(r) : full.M(r), g = new F.Fusible().gapOrSmall(r, p, 0, meek); n++;
    if (g === null) { nulls++; continue; }
    if (g.gap) { exact++; if (F.cmp(g.gap, truth) !== 0) bad.push(F.str(r) + ' p=' + p); }
    else { small++; if (!(g.small > p && F.cmp(truth, F.D(1, g.small)) <= 0)) bad.push(F.str(r) + ' p=' + p + ' small ' + g.small); } }
  say((meek ? 'meek' : 'tame') + ' rule, 6000 random dyadics in [-1, 2.4) with denominators up to 2^21 and p up to 39: exact gap given at ' + exact + ', "at most 2^-k" at ' + small + ', budget spent at ' + nulls + '; wrong: ' + bad.length + (bad.length ? ' ' + bad.slice(0, 5).join('; ') : '')); }
// with a shared memory and a budget, as the page uses it
{ const f = new F.Fusible(), full = new F.Fusible(); let bad = 0, nulls = 0, n = 0;
  for (let i = 0; i < 4000; i++) { const e = Math.floor(rnd() * 30), r = F.D(Math.floor(rnd() * 2.3 * Math.pow(2, e)), e), p = Math.floor(rnd() * 50), meek = rnd() < 0.5, g = f.gapOrSmall(r, p, 3000, meek), truth = meek ? full.meekM(r) : full.M(r); n++;
    if (g === null) nulls++; else if (g.gap ? F.cmp(g.gap, truth) !== 0 : !(F.cmp(truth, F.D(1, g.small)) <= 0)) bad++; }
  say('one shared memory, budget 3000 steps, 4000 random dyadics in [0, 2.3) with denominators up to 2^29: wrong ' + bad + ', budget spent at ' + nulls); }
