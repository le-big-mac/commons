const D = require('./touch-' + process.argv[2] + '.json'); const r = D.rect;
console.log('picture at 390 wide:', JSON.stringify({ left: r.l, top: r.t, width: r.w, height: r.h, ground: r.groundY.toFixed(1), strikeTop: r.strikeTop, strikeLeft: r.strikeLeft, strikeRight: r.strikeRight }));
let other = [], dead = [], moved = 0, groundTaps = 0, skyChanged = [], n = 0;
for (const t of D.picture) { n++; const ppx = r.w / (r.v[1] - r.v[0]), lpx = r.l + (t.before.L - r.v[0]) * ppx, near = Math.abs(t.x - lpx) < 24 && t.y > r.groundY - 44, should = t.ground || near;
  if (t.under !== '#scene') { other.push('under the finger was ' + t.under + ' at ' + t.x.toFixed(0) + ',' + t.y.toFixed(0)); continue; }
  if (t.clicks.some(c => c !== '#scene') || t.after.strikes !== t.before.strikes || t.after.kind !== t.before.kind || t.after.draw !== t.before.draw) other.push('tap at ' + t.x.toFixed(0) + ',' + t.y.toFixed(0) + ' (' + (t.ground ? 'ground' : 'sky') + ') answered by ' + t.clicks.join(',') + ' strikes ' + t.before.strikes + '->' + t.after.strikes);
  if (should) { groundTaps++; const wantX = Math.max(-1700, Math.min(9700, Math.round(t.worldX))); if (Math.abs(t.after.L - wantX) <= 40) moved++; else dead.push('tap at ' + t.x.toFixed(0) + ',' + t.y.toFixed(0) + ' wanted listener ' + wantX + ' got ' + t.after.L + ' (was ' + t.before.L + ') clicks ' + t.clicks.join(',')); }
  else if (t.after.L !== t.before.L || t.after.computed !== t.before.computed) skyChanged.push('sky tap at ' + t.x.toFixed(0) + ',' + t.y.toFixed(0) + ' moved the listener ' + t.before.L + '->' + t.after.L); }
console.log('picture taps', n, '| ground or listener taps', groundTaps, 'moved the listener to the finger:', moved, '| answered by something else:', other.length, '| ground taps that did not put the listener under the finger:', dead.length, '| sky taps that changed something:', skyChanged.length);
other.slice(0, 12).forEach(s => console.log('   OTHER', s)); dead.slice(0, 12).forEach(s => console.log('   DEAD', s)); skyChanged.slice(0, 6).forEach(s => console.log('   SKY', s));
const ch = t => ['kind', 'crooked', 'draw', 'playing', 'L', 'strikes', 'computed', 'skip'].filter(k => t.before[k] !== t.after[k]).map(k => k + ' ' + t.before[k] + '->' + t.after[k]).join(', ');
let ins = 0, insDead = [], outs = 0, outHit = [], outOther = [];
for (const t of D.controls) { const c = ch(t);
  if (t.where === 'inside') { ins++; if (!c && !t.clicks.length) insDead.push(t.control + ' (under the finger: ' + t.under + ')'); else if (t.under !== t.control && !(t.under || '').startsWith('label')) insDead.push(t.control + ': under the finger was ' + t.under + '; clicks ' + t.clicks.join(',') + '; ' + c); }
  else { outs++; if (t.clicks.length && t.clicks[0] !== t.under) outHit.push(t.where + ' of ' + t.control + ': under the finger ' + t.under + ', answered by ' + t.clicks.join(',') + (c ? ' (' + c + ')' : '')); else if (c && t.under !== t.control) outOther.push(t.where + ' of ' + t.control + ': under the finger ' + t.under + ', clicks ' + t.clicks.join(',') + ' (' + c + ')'); } }
console.log('control taps: inside', ins, ', dead or misdirected:', insDead.length, '| outside', outs, ', answered by something other than the thing under the finger:', outHit.length, ', other changes:', outOther.length);
insDead.forEach(s => console.log('   INSIDE', s.slice(0, 200))); outHit.forEach(s => console.log('   OUT', s.slice(0, 230))); outOther.slice(0, 20).forEach(s => console.log('   OUT-CHANGE', s.slice(0, 230)));
console.log('script errors', D.errs.length);
