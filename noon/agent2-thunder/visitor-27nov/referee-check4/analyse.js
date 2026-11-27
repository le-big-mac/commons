const TH = require('/home/agent2/thunder/core.js'), D = require('./states.json');
const REF = TH.thunder(TH.arc(0, 0, 3000, 150, 95), [0, 0]).peak, fmt = x => x < 9.95 ? x.toFixed(1) : Number(x.toPrecision(2)).toLocaleString('en-US');
const NAME = { stroke: 'An upright stroke', straight: 'A straight one', bow: 'A bow about you', away: 'Pointing away', own: 'Your own stroke' };
const rows = D.rows.filter(r => r.say !== undefined), bad = [], kinds = {}; let n = 0, shadow = 0, drag = 0;
console.log('not drawn:', D.rows.filter(r => r.say === undefined).map(r => r.tag).join('; ') || 'none', '|', D.head.join(' '));
for (const r of rows) { n++; kinds[r.tag.replace(/:.*/, '')] = (kinds[r.tag.replace(/:.*/, '')] || 0) + 1;
  if (r.tag === 'DRAGGING') { drag++; if (r.brief !== r.say || !/^Nearest point/.test(r.say)) bad.push(['dragging', r.L, r.say, r.brief]); continue; }
  if (r.tag === 'TOO SHORT') { if (!/^Too short/.test(r.say)) bad.push(['too short: the sentence is', r.say]); if (r.brief !== r.briefBefore) bad.push(['too short: the short form changed', r.briefBefore, r.brief]); console.log('TOO SHORT: sentence "' + r.say + '" | short form "' + r.brief + '"'); continue; }
  const head = NAME[r.kind] + (r.crooked ? ', crooked' : ', smooth') + '. '; let want;
  if (/you would hear next to nothing/.test(r.say)) { shadow++; want = head + 'Next to nothing to hear from here.'; }
  else { const rel = REF / r.peak, m = /so the thunder lasts (.+?)\. It is loudest/.exec(r.say), mine = (() => { const d = r.last - r.fh; return d < 0.1 ? Math.round(d * 1000) + ' thousandths of a second' : d.toFixed(1) + ' s'; })();
    if (!m || m[1] !== mine) bad.push(['lasts in the sentence is not my reckoning', r.tag, m && m[1], mine]);
    const loud = rel < 1.06 && rel > 1 / 1.06 ? 'as loud as the page plays anything.' : rel <= 1 / 1.06 ? fmt(1 / rel) + ' times the pressure of the bow’s crack.' : fmt(rel) + ' times less pressure than the bow’s crack.';
    want = head + 'Lasts ' + mine + '; ' + loud;
    const inSay = rel < 1.06 && rel > 1 / 1.06 ? /as loud as this page plays anything/.test(r.say) : rel <= 1 / 1.06 ? r.say.includes('about ' + fmt(1 / rel) + ' times the pressure of') : r.say.includes('about ' + fmt(rel) + ' times less pressure than'); if (!inSay) bad.push(['the sentence does not carry the same figure', r.tag, r.say.slice(-170)]);
    if (!/as loud as this page/.test(r.say) && !/about <b>[\d.,]+ times<\/b>/.test(r.html)) bad.push(['pressure figure not in bold', r.tag]); }
  if (r.brief !== want) bad.push(['short form', r.tag + '@' + r.L, 'page: ' + r.brief, 'mine: ' + want]); }
console.log('PART 3 (desktop): states', n, JSON.stringify(kinds), '| in the shadow:', shadow, '| dragging:', drag, '| FAILURES', bad.length); bad.slice(0, 12).forEach(b => console.log('   ', JSON.stringify(b).slice(0, 420)));
const lens = rows.filter(r => r.brief).map(r => r.brief.length); console.log('short form length in characters:', Math.min(...lens), 'to', Math.max(...lens), '| longest:', rows.filter(r => r.brief && r.brief.length === Math.max(...lens))[0].brief); rows.filter(r => /LOW AND FAR/.test(r.tag)).forEach(r => console.log('   ', r.tag, '@', r.L, '|', r.brief, '|', r.say.slice(0, 120)));
// part 1
console.log('TIP BUTTONS:', D.tipWords.map((w, i) => i + ' "' + w + '"').join('  '));
const want = [a => a.kind === 'bow' && !a.crooked && !a.draw && /as loud as this page plays anything/.test(a.loud), a => a.kind === 'bow' && a.crooked && a.lasts > 0.25 && a.lasts < 1.3, a => a.kind === 'away' && a.crooked && !a.draw, a => a.kind === 'away' && !a.crooked && a.ends > 0.99, a => a.kind === 'straight' && !a.crooked && !a.draw, a => a.kind === 'straight' && a.crooked, a => a.draw === true];
let tot1 = 0, tot2 = 0;
for (let t = 0; t < 7; t++) { const cs = D.cases.filter(c => c.t === t), m1 = cs.filter(c => !want[t](c.a1)), m2 = cs.filter(c => !want[t](c.a2)); tot1 += m1.length; tot2 += m2.length;
  const play1 = cs.filter(c => c.a1.playing), play2 = cs.filter(c => c.a2.playing), drawOn = cs.filter(c => t !== 6 && c.a1.draw), same2 = cs.filter(c => c.a2.computed === c.a1.computed && c.a2.kind === c.a1.kind && c.a2.crooked === c.a1.crooked).length;
  console.log('  button', t, ': cases', cs.length, '| first press not what the words promise:', m1.length, m1.slice(0, 3).map(c => c.kind + (c.crooked ? ' crooked' : ' smooth') + ' -> ' + c.a1.kind + (c.a1.crooked ? ' crooked' : ' smooth')).join('; '), '| second press not:', m2.length, '| still playing after the first press:', play1.length, play1.slice(0, 2).map(c => c.kind + (c.crooked ? ' crooked' : ' smooth') + ', button reads "' + c.a1.label + '"').join('; '), '| after the second:', play2.length, '| drawing left on after the first press:', drawOn.length, '| second press worked nothing out again:', same2); }
console.log('TOTAL of 280: first press', tot1, ', second press', tot2);
