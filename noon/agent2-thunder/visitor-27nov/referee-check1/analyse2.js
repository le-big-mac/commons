const TH = require('/home/agent2/thunder/core.js'), rows = require('./states2.json');
const bow0 = TH.thunder(TH.arc(0, 0, 3000, 150, 95), [0, 0]).peak;
console.log('my bow crack (core.js in node):', bow0.toFixed(5), ' page smooth bows:', rows.filter(r => r.tag === 'bow').map(r => r.L + ':' + r.peak.toFixed(5)).join(' '));
const fmt = x => x < 9.95 ? x.toFixed(1) : Number(x.toPrecision(2)).toLocaleString('en-US');
const num = s => parseFloat(s.replace(/,/g, ''));
const forms = {}, bad = []; let soundChecked = 0, soundWorst = 0, tpk = 0;
for (const r of rows) {
  const rel = bow0 / r.peak, q = 0.9 / r.level; let f, m;
  if (/you would hear next to nothing/.test(r.say)) f = 'F0 shadow';
  else if (/, as loud as this page plays anything\./.test(r.say)) { f = 'F1 as loud as anything'; if (r.level < 0.9 - 1e-12) bad.push(['F1 but not at top level', r.tag, r.L, r.peak, r.level]); if (Math.abs(rel - 1) > 0.06) bad.push(['F1 but pressure differs >6%', r.tag, r.L, rel]); }
  else if ((m = /with about ([\d.,]+) times the pressure of the smooth bow's crack; the page plays it no louder than that crack\./.exec(r.say))) { f = 'F2 more pressure'; if (m[1] !== fmt(1 / rel)) bad.push(['F2 figure', r.tag, r.L, m[1], 1 / rel]); if (r.level < 0.9 - 1e-12 || r.peak <= bow0) bad.push(['F2 wrong', r.tag, r.L, r.peak, r.level]); }
  else if ((m = /with about ([\d.,]+) times less pressure than the crack of the smooth bow; the page plays it just as loud\./.exec(r.say))) { f = 'F3a less pressure, just as loud'; if (m[1] !== fmt(rel)) bad.push(['F3a figure', r.tag, r.L, m[1], rel]); r.justas = r.level / 0.9; }
  else if ((m = /with about ([\d.,]+) times less pressure than the crack of the smooth bow; it is played about ([\d.]+) times quieter \(loudness is squeezed: see the foot of the page\)\./.exec(r.say))) { f = 'F3b less pressure, quieter';
    if (m[1] !== fmt(rel) || Math.abs(num(m[1]) / rel - 1) > 0.051) bad.push(['F3b pressure figure', r.tag, r.L, m[1], rel]);
    const Y = parseFloat(m[2]); if (q >= 2.5 ? Math.abs(Y - q) > 0.5 : Math.abs(Y - q) > 0.0501) bad.push(['F3b played figure', r.tag, r.L, m[2], q]);
    r.X = num(m[1]); r.Y = Y; r.rel = rel; r.q = q; }
  else { f = 'NO FORM'; bad.push(['no form', r.tag, r.L, r.say.slice(-160)]); }
  r.form = f; const k = f; forms[k] = forms[k] || {}; const t = r.tag.replace(/:.*/, ''); forms[k][t] = (forms[k][t] || 0) + 1;
  if (r.sound !== null) { soundChecked++; soundWorst = Math.max(soundWorst, Math.abs(r.sound / r.level - 1)); }
  const mt = /It is loudest ([\d.]+) s after the flash/.exec(r.say); if (mt && Math.abs(parseFloat(mt[1]) - r.tpeak) > 0.0501) tpk++;
  // what SHOULD be: anything at the top level that does not say so in some form
  if (r.level >= 0.9 - 1e-12 && !/F1|F2|F3a/.test(f)) bad.push(['top level but called quieter', r.tag, r.L]);
  if (r.level < 0.9 / 1.06 && !/F3b|F0/.test(f)) bad.push(['below top level by >6% but not called quieter', r.tag, r.L, r.level, f]);
}
console.log('states', rows.length); console.log('forms by kind:', JSON.stringify(forms));
console.log('faults found by my rules:', bad.length); bad.slice(0, 25).forEach(b => console.log('   ', JSON.stringify(b)));
console.log('loudspeaker samples against level: checked', soundChecked, 'worst relative difference', soundWorst.toExponential(2), '; "loudest T s" off by more than rounding:', tpk);
const ja = rows.filter(r => r.justas !== undefined); console.log('"just as loud" said', ja.length, 'times; level/top from', Math.min(...ja.map(r => r.justas)).toFixed(3), 'to', Math.max(...ja.map(r => r.justas)).toFixed(3), ja.map(r => r.tag + '@' + r.L + ' rel ' + (bow0 / r.peak).toFixed(2)).join('; '));
rows.filter(r => /F2|F1/.test(r.form)).forEach(r => console.log('  ', r.form, '|', r.tag, '@', r.L, 'peak', r.peak.toFixed(4), 'x crack', (r.peak / bow0).toFixed(3), 'level', r.level.toFixed(3), '|', r.say.slice(r.say.indexOf('It is loudest'), r.say.indexOf('It is loudest') + 150)));
rows.filter(r => /^own/.test(r.tag)).forEach(r => console.log('  own:', r.tag, 'nearest', r.nearest.toFixed(0), 'peak', r.peak.toExponential(3), 'x crack', (r.peak / bow0).toFixed(3), 'level', r.level.toFixed(3), r.form));
// C: four to one against the printed figures
const fb = rows.filter(r => r.form === 'F3b less pressure, quieter'); let dis = 0, ex = [];
for (const r of fb) { const four = Math.pow(r.X, 0.25), want = four >= 2.5 ? Math.round(four) : Math.round(four * 10) / 10; if (want !== r.Y) { dis++; if (ex.length < 6) ex.push(r.X + ' times less -> printed ' + r.Y + ', fourth root ' + four.toFixed(2)); } }
console.log('C: of', fb.length, 'sentences with both figures, the fourth root of the printed pressure figure rounds to a different "times quieter" in', dis, ':', ex.join('; '));
const near100 = fb.filter(r => r.X >= 90 && r.X <= 110); console.log('   printed pressure 90 to 110:', near100.length, 'sentences; "times quieter" printed:', [...new Set(near100.map(r => r.Y))].join(','), '; q from', Math.min(...near100.map(r => r.q)).toFixed(2), 'to', Math.max(...near100.map(r => r.q)).toFixed(2));
const three = fb.filter(r => r.Y === 3); console.log('   "about 3 times quieter" printed for pressure figures from', Math.min(...three.map(r => r.X)), 'to', Math.max(...three.map(r => r.X)), '(', three.length, 'sentences )');
