const TH = require('/home/agent2/thunder/core.js'), D = require('./states.json');
const REF = TH.thunder(TH.arc(0, 0, 3000, 150, 95), [0, 0]).peak, fmt = x => x < 9.95 ? x.toFixed(1) : Number(x.toPrecision(2)).toLocaleString('en-US');
const NAME = { stroke: 'An upright stroke', straight: 'A straight one', bow: 'A bow about you', away: 'Pointing away', own: 'Your own stroke' };
const rows = D.rows.filter(r => r.say !== undefined), bad = [], kinds = {}, parts = { name: 0, first: 0, dist: 0, lasts: 0, into: 0, loud: 0, whole: 0 }; let n = 0, shadow = 0, drag = 0, intoOverLasts = [], intoNeg = 0, started = 0, whenSmooth = 0;
console.log('not drawn:', D.rows.filter(r => r.say === undefined).map(r => r.tag).join('; ') || 'none', '|', D.head.join(' '));
for (const r of rows) { n++; kinds[r.tag.replace(/:.*/, '')] = (kinds[r.tag.replace(/:.*/, '')] || 0) + 1;
  if (r.tag === 'DRAGGING') { drag++; if (r.brief !== r.say || !/^Nearest point/.test(r.say)) bad.push(['dragging', r.L, r.say, r.brief]); continue; }
  if (r.tag === 'TOO SHORT') { if (!/^Too short/.test(r.say)) bad.push(['too short: the sentence is', r.say]); if (r.brief !== r.briefBefore) bad.push(['too short: the short form changed', r.briefBefore, r.brief]); console.log('TOO SHORT: short form "' + r.brief + '"'); continue; }
  const head = NAME[r.kind] + (r.crooked ? ', crooked' : ', smooth') + '. ';
  if (/you would hear next to nothing/.test(r.say)) { shadow++; if (r.brief !== head + 'Next to nothing to hear from here.') bad.push(['shadow', r.brief]); continue; }
  const rel = REF / r.peak, d = r.last - r.fh, lasts = d < 0.1 ? Math.round(d * 1000) + ' thousandths of a second' : d.toFixed(1) + ' s';
  const m = /The first sound comes ([\d.]+) s after the flash, from ([\d.]+ km) away; .*so the thunder lasts (.+?)\. It is loudest ([\d.]+) s after the flash/.exec(r.say);
  if (!m) { bad.push(['cannot read the sentence', r.tag, r.say.slice(0, 200)]); continue; }
  const reader = (Math.round(parseFloat(m[4]) * 10) - Math.round(parseFloat(m[1]) * 10)) / 10;          // what a reader subtracting the two printed times gets
  const into = d < 0.1 ? '' : reader === 0 ? ', loudest at its start' : ', loudest ' + reader.toFixed(1) + ' s in';
  const loud = rel < 1.06 && rel > 1 / 1.06 ? 'as loud as this page plays anything.' : rel <= 1 / 1.06 ? 'about ' + fmt(1 / rel) + ' times the pressure of the bow’s crack.' : 'about ' + fmt(rel) + ' times less pressure than ' + (r.kind === 'bow' ? 'when smooth.' : 'the bow’s crack.');
  const want = head + 'First sound ' + r.fh.toFixed(1) + ' s, from ' + (r.fh * 343 / 1000).toFixed(1) + ' km; lasts ' + lasts + into + '; ' + loud;
  if (!r.brief.startsWith(head)) parts.name++; if (!r.brief.includes('First sound ' + m[1] + ' s,') || m[1] !== r.fh.toFixed(1)) parts.first++; if (!r.brief.includes(', from ' + m[2] + ';') || m[2] !== (r.fh * 343 / 1000).toFixed(1) + ' km') parts.dist++;
  if (!r.brief.includes('; lasts ' + m[3]) || m[3] !== lasts) parts.lasts++; if (!r.brief.includes('lasts ' + lasts + into + '; ')) parts.into++; if (!r.brief.endsWith('; ' + loud) || r.short !== loud) parts.loud++;
  if (r.brief !== want) { parts.whole++; bad.push(['short form', r.tag + '@' + r.L, 'page: ' + r.brief, 'mine: ' + want]); }
  if (reader < 0) intoNeg++; if (reader === 0 && d >= 0.1) started++; if (/when smooth/.test(r.brief)) whenSmooth++;
  if (d >= 0.1 && reader > parseFloat(lasts) + 1e-9) intoOverLasts.push(r.tag + '@' + r.L + ': "' + r.brief.slice(r.brief.indexOf('lasts'), r.brief.indexOf('; about')) + '"');
  const inSay = rel < 1.06 && rel > 1 / 1.06 ? /as loud as this page plays anything/.test(r.say) : rel <= 1 / 1.06 ? r.say.includes('about ' + fmt(1 / rel) + ' times the pressure of') : r.say.includes('about ' + fmt(rel) + ' times less pressure than'); if (!inSay) bad.push(['the sentence does not carry the same pressure figure', r.tag]); }
console.log('PART 2 (desktop): states', n, JSON.stringify(kinds), '| in the shadow:', shadow, '| dragging:', drag, '| parts that differ from my reckoning:', JSON.stringify(parts), '| FAILURES', bad.length); bad.slice(0, 10).forEach(b => console.log('   ', JSON.stringify(b).slice(0, 520)));
console.log('"loudest at its start":', started, '| negative "in":', intoNeg, '| "when smooth":', whenSmooth, '(crooked bows:', rows.filter(r => r.kind === 'bow' && r.crooked && r.tag !== 'DRAGGING').length + ')', '| "loudest N s in" with N more than the length printed:', intoOverLasts.length); intoOverLasts.slice(0, 6).forEach(s => console.log('    ', s));
const lens = rows.filter(r => r.brief).map(r => r.brief.length); console.log('short form length in characters:', Math.min(...lens), 'to', Math.max(...lens), '| longest:', rows.filter(r => r.brief && r.brief.length === Math.max(...lens))[0].brief);
// part 1
console.log('TIP BUTTONS:', D.tipWords.map((w, i) => i + ' "' + w + '"').join('  '));
const want = [a => a.kind === 'bow' && !a.crooked && !a.draw && /as loud as this page plays anything/.test(a.loud), a => a.kind === 'bow' && a.crooked && a.lasts > 0.25 && a.lasts < 1.3, a => a.kind === 'away' && a.crooked && !a.draw, a => a.kind === 'away' && !a.crooked && a.ends > 0.99, a => a.kind === 'straight' && !a.crooked && !a.draw, a => a.kind === 'straight' && a.crooked, a => a.draw === true];
let tot1 = 0, tot2 = 0;
for (let t = 0; t < 7; t++) { const cs = D.cases.filter(c => c.t === t), m1 = cs.filter(c => !want[t](c.a1)), m2 = cs.filter(c => !want[t](c.a2)); tot1 += m1.length; tot2 += m2.length;
  const play1 = cs.filter(c => c.a1.playing), play2 = cs.filter(c => c.a2.playing), drawOn = cs.filter(c => t !== 6 && c.a1.draw), same2 = cs.filter(c => c.a2.computed === c.a1.computed && c.a2.kind === c.a1.kind && c.a2.crooked === c.a1.crooked).length;
  console.log('  button', t, ': cases', cs.length, '| first press not what the words promise:', m1.length, m1.slice(0, 3).map(c => c.kind + (c.crooked ? ' crooked' : ' smooth') + ' -> ' + c.a1.kind + (c.a1.crooked ? ' crooked' : ' smooth')).join('; '), '| second press not:', m2.length, '| still playing after the first press:', play1.length, play1.slice(0, 2).map(c => c.kind + (c.crooked ? ' crooked' : ' smooth') + ', button reads "' + c.a1.label + '"').join('; '), '| after the second:', play2.length, '| drawing left on after the first press:', drawOn.length, '| second press worked nothing out again:', same2); }
console.log('TOTAL of 280: first press', tot1, ', second press', tot2);
