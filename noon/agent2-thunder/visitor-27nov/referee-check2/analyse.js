const TH = require('/home/agent2/thunder/core.js'), D = require('./states.json'), rows = D.rows.filter(r => !/^NOT DRAWN/.test(r.tag));
const bow0 = TH.thunder(TH.arc(0, 0, 3000, 150, 95), [0, 0]).peak;
console.log('my bow crack', bow0, 'THUNDERREF', D.REF, 'equal:', bow0 === D.REF, '| not drawn:', D.rows.length - rows.length);
const fmt = x => x < 9.95 ? x.toFixed(1) : Number(x.toPrecision(2)).toLocaleString('en-US'), num = s => parseFloat(s.replace(/,/g, ''));
const CR = 'the crack that “A bow about you” makes', forms = {}, bad = []; let snd = 0, sndWorst = 0, rootDiff = 0, rootEx = [], lvlDiff = 0, f3b = 0; const f1 = [], f3a = [];
for (const r of rows) {
  const rel = bow0 / r.peak, q = Math.pow(Math.max(rel, 1), 0.25); let f, m;
  if (!r.say.includes(r.loud)) bad.push(['sentence is not THUNDERLOUD(peak)', r.tag, r.L]);
  if (Math.abs(r.level / (0.9 / q) - 1) > 1e-9) bad.push(['level is not 0.9 over the fourth root', r.tag, r.L, r.level, 0.9 / q]);
  if (r.say.includes(', as loud as this page plays anything.')) { f = 'as loud as anything'; f1.push(r.level / 0.9); if (!(rel < 1.06 && rel > 1 / 1.06)) bad.push(['F1 outside 6%', r.tag, rel]); }
  else if ((m = new RegExp('with about ([\\d.,]+) times the pressure of ' + CR + '; the page plays it no louder than that crack\\.').exec(r.say))) { f = 'more pressure'; if (m[1] !== fmt(1 / rel) || rel > 1 / 1.06 || r.level !== 0.9) bad.push(['F2', r.tag, m[1], 1 / rel, r.level]); }
  else if ((m = new RegExp('with about ([\\d.,]+) times less pressure than ' + CR + '; the page plays it very nearly as loud\\.').exec(r.say))) { f = 'very nearly as loud'; f3a.push([rel, r.level / 0.9]); if (m[1] !== fmt(rel) || q >= 1.05) bad.push(['F3a', r.tag, m[1], rel, q]); }
  else if ((m = new RegExp('with about ([\\d.,]+) times less pressure than ' + CR + '; it is played about ([\\d.,]+) times quieter \\(loudness is squeezed: see the foot of the page\\)\\.').exec(r.say))) { f = 'quieter'; f3b++;
    if (m[1] !== fmt(rel)) bad.push(['F3b first figure', r.tag, m[1], rel]); if (m[2] !== fmt(q)) bad.push(['F3b second figure', r.tag, m[2], q]);
    const X = num(m[1]), Y = num(m[2]); r.X = X; r.Y = Y; r.q = q; r.rel = rel;
    if (fmt(Math.pow(X, 0.25)) !== m[2]) { rootDiff++; if (rootEx.length < 8) rootEx.push(m[1] + ' -> printed ' + m[2] + ', fourth root of the printed figure ' + Math.pow(X, 0.25).toFixed(3) + ' (true ' + rel.toFixed(1) + ', ' + q.toFixed(3) + ')'); }
    const half = Y < 9.95 ? 0.0501 : 0.05 * Y; if (Math.abs(0.9 / r.level - Y) > half) lvlDiff++; }
  else { f = 'NO FORM'; bad.push(['no form', r.tag, r.L, r.say.slice(-200)]); }
  r.form = f; const t = r.tag.replace(/:.*/, ''); forms[f] = forms[f] || {}; forms[f][t] = (forms[f][t] || 0) + 1;
  if (r.sound !== null) { snd++; sndWorst = Math.max(sndWorst, Math.abs(r.sound / r.level - 1)); }
}
console.log('states', rows.length, JSON.stringify(forms)); console.log('faults by my rules:', bad.length); bad.slice(0, 12).forEach(b => console.log('  ', JSON.stringify(b)));
console.log('samples against level: checked', snd, 'worst', sndWorst.toExponential(2), '| "quieter" sentences', f3b, '; 0.9/level differs from the printed second figure by more than its rounding:', lvlDiff);
console.log('fourth root of the PRINTED first figure, formatted, differs from the printed second figure in', rootDiff, 'of', f3b, ':'); rootEx.forEach(e => console.log('    ', e));
console.log('"as loud as anything":', f1.length, 'level/top from', Math.min(...f1).toFixed(4), 'to', Math.max(...f1).toFixed(4), '| "very nearly as loud":', f3a.length, f3a.map(a => a[0].toFixed(3) + ':' + a[1].toFixed(3)).join(' '));
console.log('BORDERS (rel, side, clause, level/0.9):'); D.borders.forEach(b => console.log('  ', b[0].toPrecision(6), b[1] < 1 ? 'just more pressure' : 'just less', '|', b[3].replace(CR, 'CRACK').slice(0, 110), '|', (b[4] / 0.9).toFixed(4))); console.log('odd peaks:', JSON.stringify(D.odd).replace(new RegExp(CR, 'g'), 'CRACK').slice(0, 500));
const rng = a => Math.min(...a).toPrecision(3) + ' to ' + Math.max(...a).toPrecision(3), mean = a => a.reduce((s, v) => s + v, 0) / a.length, med = a => { const s = a.slice().sort((x, y) => x - y); return (s[Math.floor((s.length - 1) / 2)] + s[Math.ceil((s.length - 1) / 2)]) / 2; };
const cb = rows.filter(r => r.tag === 'bow-crooked'), dur = cb.map(r => r.last - r.fh), first100 = cb.filter(r => r.L !== 3000).concat(cb.filter(r => r.L === 3000).slice(0, 20));
for (const [name, set] of [['100 bows (20 at each of five places)', first100], ['all ' + cb.length + ' bows', cb]]) { const d = set.map(r => r.last - r.fh), ys = {}; set.forEach(r => ys[r.Y] = (ys[r.Y] || 0) + 1);
  console.log('BOW', name, ': times lower', rng(set.map(r => r.rel)), '(below 80:', set.filter(r => r.rel < 80).length, ', above 170:', set.filter(r => r.rel > 170).length, ', below 75 or above 180:', set.filter(r => r.rel < 75 || r.rel > 180).length + ')', '| played times quieter', rng(set.map(r => r.q)), 'printed', JSON.stringify(ys), '| above 3.5 (true):', set.filter(r => r.q > 3.5).length, 'below 3.0:', set.filter(r => r.q < 3).length, '| lasts', rng(d), 's; under a third:', d.filter(v => v < 1 / 3).length, '; under 0.35:', d.filter(v => v < 0.35).length, '; median rel', med(set.map(r => r.rel)).toFixed(0)); }
const shortest = cb.slice().sort((a, b) => (a.last - a.fh) - (b.last - b.fh)).slice(0, 3); shortest.forEach(r => console.log('   shortest:', (r.last - r.fh).toFixed(3), '|', /lasts ([^.]*\.[^ ]* s|[^.]*second)/.exec(r.say)[0]));
const up3 = rows.filter(r => r.tag === 'stroke' && r.L === 3000).map(r => r.energy), u3 = mean(up3), aw = rows.filter(r => r.tag === 'away');
console.log('AWAY: upright from 3 km: n', up3.length, 'mean energy', u3.toExponential(3), 'median', med(up3).toExponential(3), 'range', rng(up3), '| all', aw.length, 'pointing away / that mean:', rng(aw.map(r => r.energy / u3)), 'mean', mean(aw.map(r => r.energy / u3)).toFixed(3), 'median', med(aw.map(r => r.energy / u3)).toFixed(3), '; between 0.05 and 0.2:', aw.filter(r => r.energy / u3 >= 0.05 && r.energy / u3 <= 0.2).length);
for (const x of [500, 1500, 3000, 5000, 8000]) { const a = aw.filter(r => r.L === x).map(r => r.energy / u3); console.log('   listener', x, ':', rng(a), 'mean', mean(a).toFixed(3), 'lasts', rng(aw.filter(r => r.L === x).map(r => r.last - r.fh))); }
rows.filter(r => r.tag === 'straight').forEach(r => console.log('STRAIGHT @', r.L, ': first 0.02 s', (100 * r.early).toFixed(2) + '%, between', (100 * (1 - r.ends)).toFixed(2) + '%, far end', (100 * (r.ends - r.early)).toFixed(3) + '%; energy', r.energy.toExponential(2), '=> between', (r.energy * (1 - r.ends)).toExponential(2), 'far end', (r.energy * (r.ends - r.early)).toExponential(2), '| level', r.level.toFixed(3)));
for (const x of [300, 500, 1500, 3000, 5000, 8000, 9000]) { const s = rows.filter(r => r.tag === 'stroke' && r.L === x); console.log('QUIETER @', x, 'n', s.length, 'mean peak', mean(s.map(r => r.peak)).toExponential(2), 'mean level', mean(s.map(r => r.level)).toFixed(3), 'printed second figure', rng(s.map(r => r.Y))); }
