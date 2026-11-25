// rtest.js -- rcore.js on data.json against figures counted in Python straight from the pair table (expect.json), and against the
// Python tables (out/score.json, out/families.json).    node rtest.js
'use strict';
const fs = require('fs'), path = require('path'), R = require('./rcore.js');
const D = JSON.parse(fs.readFileSync(path.join(__dirname, 'data.json'), 'utf8')), E = JSON.parse(fs.readFileSync(path.join(__dirname, 'expect.json'), 'utf8'));
const S = JSON.parse(fs.readFileSync(path.join(__dirname, 'out', 'score.json'), 'utf8')), F = JSON.parse(fs.readFileSync(path.join(__dirname, 'out', 'families.json'), 'utf8'));
const X = R.index(D); let pass = 0, fail = 0;
const ok = (name, cond, extra) => { if (cond) pass++; else fail++; console.log((cond ? 'ok    ' : 'FAIL  ') + name + (extra ? ': ' + extra : '')); };
// 1. partners of sixteen words: the same partners, counts and verdicts as the pair table gives
{ let good = 0, n = 0, total = 0; const bad = [];
  for (const w of Object.keys(E.partners)) { n++; const got = R.partners(D, X, w), want = E.partners[w];
    if (want.length === 0) { if (got === null) good++; else bad.push(w); continue; }
    const g = got.map(p => [p.word, p.n, p.ok, p.poets.map(i => D.poets[i].id).sort()]); total += g.length;
    if (JSON.stringify(g) === JSON.stringify(want)) good++; else bad.push(w + ' ' + JSON.stringify(g.slice(0, 3)) + ' / ' + JSON.stringify(want.slice(0, 3))); }
  ok('partners(): for ' + n + ' words (one of them not in the corpus) the partners, their counts, their poets and whether they still rhyme are those counted from the pair table (' + total + ' partners)', good === n, good + ' of ' + n + (bad.length ? ' ' + bad.join('; ') : ''));
  let tgood = 0; for (const w of Object.keys(E.partners)) { const want = E.partners[w]; if (!want.length) { tgood++; continue; } const t = R.tally(R.partners(D, X, w)), sum = k => want.filter(x => x[2] === k).reduce((s, x) => s + x[1], 0);
    if (t.n === want.reduce((s, x) => s + x[1], 0) && t.still === sum(1) && t.not === sum(0) && t.unjudged === sum(2)) tgood++; }
  ok('tally(): how many of a word\'s rhymes still rhyme, no longer do, or cannot be judged', tgood === n, tgood + ' of ' + n);
  ok('clean(): case, spaces and marks are dropped; partners() takes a word in any dress', R.clean(' Pray\'er! ') === 'prayer' && JSON.stringify(R.partners(D, X, ' LOVE ')) === JSON.stringify(R.partners(D, X, 'love'))); }
// 2. every cell of the families table
{ let good = 0, n = 0; const idx = {}; D.poets.forEach((p, i) => { idx[p.id] = i; });
  D.families.forEach((f, fi) => D.poets.forEach((p, pi) => { n++; const want = E.fam_poet[f.name + '|' + p.id] || 0; if (f.byPoet[pi] === want && R.failsOf(D, X, fi, pi).length === want) good++; }));
  ok('families: every cell (family by poet) holds the count from the pair table, and failsOf() lists that many', good === n, good + ' of ' + n); }
// 3. totals
ok('totals: failing pairs, all pairs, distinct pairs', D.fails.length === E.n_fails && D.counts.pairs === E.n_pairs && D.pairs.length === E.distinct && D.pairs.reduce((s, p) => s + p[2], 0) === E.n_pairs, D.fails.length + ', ' + D.counts.pairs + ', ' + D.pairs.length);
ok('failsOf(-1, -1) is every failing pair once, in order', (() => { const a = R.failsOf(D, X, -1, -1); return a.length === D.fails.length && a.every((v, i) => v === i); })());
// 4. single pairs
{ let good = 0, n = 0; for (const k of Object.keys(E.pair_fails)) { n++; const [a, b] = k.split('/'); if (R.failsOfPair(X, a, b).length === E.pair_fails[k] && R.failsOfPair(X, b.toUpperCase(), ' ' + a + '!').length === E.pair_fails[k]) good++; }
  ok('failsOfPair(): seven pairs, either way round and in any case, as counted from the pair table', good === n, Object.entries(E.pair_fails).map(([k, v]) => k + ' ' + v).join(', ')); }
// 5. the poets' figures are score.json's, and the rates are counts over evaluable pairs
{ let good = 0; D.poets.forEach(p => { const m = S.poets[p.id]; if (p.M === m.M && p.M_A === m.M_A && p.M_B === m.M_B && p.evaluable === m.evaluable && p.pairs === m.pairs && p.lo <= p.M && p.M <= p.hi) good++; });
  ok('poets: M, M_A, M_B, pairs and evaluable are the scoring table\'s, and M lies inside its own interval', good === 32, good + ' of 32'); }
{ let good = 0, n = 0; D.families.forEach((f, fi) => D.poets.forEach((p, pi) => { n++; if (Math.abs(R.rate(D, fi, pi) - 1000 * (E.fam_poet[f.name + '|' + p.id] || 0) / S.poets[p.id].evaluable) < 1e-9 && Math.abs(R.rate(D, fi, pi) - F.by_poet[f.name][p.id][1]) < 0.006) good++; }));
  ok('rate(): a family\'s failing pairs per thousand of a poet\'s evaluable pairs, from the pair table and the scoring table', good === n, good + ' of ' + n); }
{ let good = 0, n = 0; D.families.forEach((f, fi) => { D.groups.forEach((g, gi) => { n++; if (Math.abs(R.groupRate(D, fi, gi) - F.by_group[f.name][g.id][1]) < 0.006) good++; }); });
  ok('groupRate(): per thousand evaluable, as the families table prints it', good === n, good + ' of ' + n); }
// 6. the verse lines of a failing pair end in its two words
{ let good = 0, n = 0, none = 0; const end = s => { const t = s.replace(/[^A-Za-z'\- ]/g, ' ').trim().split(/\s+/).filter(x => /[A-Za-z]/.test(x)); return t[t.length - 1].toLowerCase().replace(/[^a-z]/g, ''); };
  D.fails.forEach(f => { if (f[4] < 0) { none++; return; } n++; if (end(D.lines[f[4]]) === f[2].replace(/[^a-z]/g, '') && end(D.lines[f[5]]) === f[3].replace(/[^a-z]/g, '')) good++; });
  ok('verses: the two lines shown for a failing pair end in its two words (' + none + ' failing pairs have no verses matched)', good === n && none === D.counts.failing_without_verse, good + ' of ' + n); }
// 7. the families' members add up, and the order of poets is by year of birth
ok('families: the cells of each family add up to its total, and the totals to the failing pairs', D.families.every(f => f.byPoet.reduce((a, b) => a + b, 0) === f.total && f.byGroup.reduce((a, b) => a + b, 0) === f.total) && D.families.reduce((s, f) => s + f.total, 0) === D.fails.length);
ok('poets are in order of birth (the two of unknown birth placed at 1566)', D.poets.every((p, i) => i === 0 || (D.poets[i - 1].born || 1566) <= (p.born || 1566)));
// 8. no British-dictionary symbol in the page's data: endings are respelt from the American dictionary only
{ const allowed = /^(ee|i|ay|e|a|ah|aw|oh|uu|oo|u|er|eye|ow|oy)(-[a-z]+)?$/; let bad = 0, shown = 0; D.fails.forEach(f => { for (const e of [f[7], f[8]]) { if (e === '') continue; shown++; if (!allowed.test(e)) bad++; } });
  ok('endings: every ending shown is one of fifteen respelt vowels with or without consonants after it (' + shown + ' shown)', bad === 0, bad + ' not'); }
ok('obey / tea is in Pope, in the family sea : way, with its two lines', (() => { const i = R.failsOfPair(X, 'tea', 'obey'); return i.length === 1 && D.poets[D.fails[i[0]][0]].id === 'pope' && D.families[D.fails[i[0]][1]].name === 'sea : way' && /realms obey/.test(D.lines[D.fails[i[0]][4]]) && /sometimes Tea/.test(D.lines[D.fails[i[0]][5]]); })());
ok('words that are also names of things every object has (constructor, valueOf, toString) are simply not in the corpus', R.partners(D, X, 'constructor') === null && R.partners(D, X, 'valueOf') === null && R.partners(D, X, 'toString') === null && R.failsOfPair(X, 'constructor', 'love').length === 0);
ok('pct() rounds to one place and group3() groups in threes', R.pct(86.96) === '87.0' && R.pct(87.4466) === '87.4' && R.pct(99.95) === '100.0' && R.pct(0) === '0.0' && R.group3(58501) === '58,501' && R.group3(1234567) === '1,234,567' && R.group3(999) === '999');
ok('the shares in the data carry four places, so the page does not round a rounded figure', D.poets.some(p => Math.abs(p.M * 100 - Math.round(p.M * 100)) > 1e-6) && Math.abs(D.all.M - 100 * (D.all.evaluable - D.fails.length) / D.all.evaluable) < 1e-4);
console.log('\n' + pass + ' pass, ' + fail + ' fail'); process.exit(fail ? 1 : 0);
