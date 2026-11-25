// runs.js -- the grid lines of the sealed sheet (5 to 9).   usage: node runs.js PART
//   PART = grid12 : the grid of 1/4096 in [0, 9/4]: first point where Succ and TameSucc differ; where MeekSucc (as I read it)
//                   differs from Succ; how many of the 768 points in [33/16, 9/4) have Succ != TameSucc; the largest denominator
//   PART = grid16 : the grid of 1/65536 below 33/16: points where Succ and TameSucc differ
const F = require('./core.js'), fs = require('fs'); const part = process.argv[2], say = s => fs.writeSync(1, s + '\n');
let last = Date.now(); const f = new F.Fusible(), t0 = Date.now(), secs = () => ((Date.now() - t0) / 1000).toFixed(1);
if (part === 'grid12') {
  const E = 12, top = process.argv[3] ? +process.argv[3] : 9 * (1 << E) / 4, lo = 33 * (1 << E) / 16;  /* an optional last index, for a run that stops short of 9/4 */  let first = null, nd = 0, nd768 = 0, meekBad = [], maxE = 0, maxAt = null, diffs = [];
  for (let i = 0; i <= top; i++) {
    const r = F.D(i, E), s = f.succ(r), t = f.tameSucc(r), k = f.meekSucc(r);
    if (F.cmp(s, t) !== 0) { nd++; if (first === null) first = r; if (i >= lo && i < 9216) nd768++; if (diffs.length < 12) diffs.push(F.str(r) + ': ' + F.str(s) + ' | tame ' + F.str(t)); }
    if (F.cmp(s, k) !== 0) meekBad.push(F.str(r));
    if (F.cmp(s, t) > 0) say('!! Succ above TameSucc at ' + F.str(r));
    if (s[1] > maxE) { maxE = s[1]; maxAt = r; }
    if (Date.now() - last > 10000) { last = Date.now(); say('  .. ' + F.str(r) + ' ' + secs() + ' s, ' + f.calls.succ + ' computed, ' + f.gS.count() + ' gaps'); }
  }
  say('grid of 1/4096 in [0, ' + F.str(F.D(top, E)) + ']: ' + (top + 1) + ' points, ' + secs() + ' s');
  say('first point where Succ != TameSucc: ' + (first ? F.str(first) : 'none'));
  say('points where they differ: ' + nd + ' in all; ' + nd768 + ' of the ' + (Math.min(top + 1, 9216) - lo) + ' in [33/16, 9/4) that were run');
  say('the first twelve: ' + JSON.stringify(diffs, null, 1));
  say('points where MeekSucc (my reading) != Succ: ' + meekBad.length + (meekBad.length ? '  ' + meekBad.slice(0, 20).join(' ') : ''));
  say('largest denominator of a successor: 2^' + maxE + ' at r = ' + F.str(maxAt) + ' (Succ = ' + F.str(f.succ(maxAt)) + ')');
  say('calls: ' + JSON.stringify(f.calls));
} else if (part === 'grid16') {
  const E = 16, lo = 33 * (1 << E) / 16; let bad = [], maxE = 0, maxAt = null;
  for (let i = 0; i < lo; i++) { const r = F.D(i, E), s = f.succ(r), t = f.tameSucc(r); if (F.cmp(s, t) !== 0) bad.push(F.str(r)); if (s[1] > maxE) { maxE = s[1]; maxAt = r; }
    if (Date.now() - last > 10000) { last = Date.now(); say('  .. ' + F.str(r) + ' ' + secs() + ' s, ' + f.calls.succ + ' computed, ' + f.gS.count() + ' gaps'); } }
  say('grid of 1/65536 in [0, 33/16): ' + lo + ' points, ' + secs() + ' s');
  say('points where Succ != TameSucc: ' + bad.length + (bad.length ? '  ' + bad.slice(0, 20).join(' ') : ''));
  say('largest denominator of a successor: 2^' + maxE + ' at r = ' + F.str(maxAt));
  say('calls: ' + JSON.stringify(f.calls));
}
