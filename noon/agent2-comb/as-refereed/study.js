// study.js -- the trial of the sealed sheet, and its verdicts.   node study.js > study.out
// Curves: seeds 1..1000 (one curve each, turning number drawn from -3..3); pairs: seeds 1001..2000 (two curves from one
// generator, turning numbers drawn independently), and seeds 2001..3000 (two curves of turning number 1).
'use strict';
const C = require('./ccore.js'), crypto = require('crypto'), fs = require('fs'), N = 400, J = 6, AMP = 1.5;
const draw = (rand, n) => C.shape(C.resample(C.randomCurve(rand, n, J, AMP, N), N));
const moments = []; for (let i = 1; i <= 49; i++) moments.push(i / 50);
console.log('sha256 of expectations.md: ' + crypto.createHash('sha256').update(fs.readFileSync(__dirname + '/expectations.md')).digest('hex') + '\n');
let keep = 0, wrongClass = 0, slow = 0, parity = 0, thm2 = 0, within = 0; const leastAll = [], meanMax = [], crossAt = [], worst = [];
const t0 = Date.now();
for (let seed = 1; seed <= 1000; seed++) { const rand = C.rng(seed), n = Math.floor(rand() * 7) - 3, A = draw(rand, n); if (A.n !== n) wrongClass++;
  const S = C.shape(C.standard(A.n, N)); let same = true, least = Infinity, mmax = 0, cmax = 0; const c0 = C.crossings(A.pts).length, c1 = C.crossings(S.pts).length;
  for (const u of moments) { const w = C.whitney(A, S, u); if (C.turning(w.pts) !== A.n) same = false; if (w.least < least) least = w.least; if (w.mean > mmax) mmax = w.mean; const c = C.crossings(w.pts).length; if (c > cmax) cmax = c; }
  keep += same; leastAll.push(least); if (least > 0.05) slow++; meanMax.push(mmax); if (cmax <= Math.max(c0, c1) + 2) within++; crossAt.push([c0, c1, cmax]); worst.push([least, seed, A.n]);
  if ((c0 + A.n) % 2 !== 0) parity++; if (C.theorem2(A.pts).n === A.n) thm2++; }
let signed = 0; const kinkCounts = {};
for (let seed = 1001; seed <= 2000; seed++) { const rand = C.rng(seed), n0 = Math.floor(rand() * 7) - 3, n1 = Math.floor(rand() * 7) - 3, A = draw(rand, n0), B = draw(rand, n1), k = C.kinks(A, B);
  if (k.reduce((s, x) => s + x.sense, 0) === B.n - A.n) signed++; const d = Math.abs(B.n - A.n); (kinkCounts[d] = kinkCounts[d] || []).push(k.length); }
let free = 0; const sameKinks = [];
for (let seed = 2001; seed <= 3000; seed++) { const rand = C.rng(seed), A = draw(rand, 1), B = draw(rand, 1), k = C.kinks(A, B).length; if (k === 0) free++; sameKinks.push(k); }
const med = a => { const s = a.slice().sort((x, y) => x - y); return (s[Math.floor((s.length - 1) / 2)] + s[Math.ceil((s.length - 1) / 2)]) / 2; }, q = (a, f) => a.slice().sort((x, y) => x - y)[Math.floor(f * (a.length - 1))];
const V = []; const line = (n, kind, odds, held, what) => { V.push([kind, odds, held]); console.log((n < 10 ? ' ' : '') + n + '. ' + (held ? 'HELD ' : 'FELL ') + ' (' + kind + ', odds ' + odds.toFixed(2) + ')  ' + what); };
line(1, 'worked', 0.95, keep === 1000, 'the turning number is the same at all 49 moments in ' + keep + ' of 1,000 (' + wrongClass + ' random curves did not have the turning number asked for)');
line(2, 'guessed', 0.60, slow >= 950, 'least speed above 0.05 in ' + slow + ' of 1,000 (sealed: at least 950); the least of all ' + Math.min(...leastAll).toFixed(4) + ', the 5th centile ' + q(leastAll, 0.05).toFixed(3) + ', the median ' + med(leastAll).toFixed(3));
line(3, 'worked', 0.90, signed === 1000, 'the signed count of opposed tangents is n1 - n0 in ' + signed + ' of 1,000 pairs; counts without sign, by |n1 - n0|: ' + Object.keys(kinkCounts).sort().map(d => d + ': least ' + Math.min(...kinkCounts[d]) + ', median ' + med(kinkCounts[d])).join('; '));
line(4, 'guessed', 0.70, free < 300, free + ' of 1,000 pairs of turning number 1 have no opposed tangents (sealed: fewer than 300); median number of opposed places ' + med(sameKinks) + ', most ' + Math.max(...sameKinks));
line(5, 'worked', 0.90, parity === 1000, 'crossings plus turning number is odd in ' + parity + ' of 1,000');
line(6, 'worked', 0.80, thm2 === 1000, 'mu + N+ - N- is the turning number in ' + thm2 + ' of 1,000');
line(7, 'guessed', 0.50, med(meanMax) >= 0.10 && med(meanMax) <= 0.40, 'the largest length of the average direction: median ' + med(meanMax).toFixed(3) + ' (sealed: between 0.10 and 0.40); 5th and 95th centiles ' + q(meanMax, 0.05).toFixed(3) + ' and ' + q(meanMax, 0.95).toFixed(3) + ', greatest ' + Math.max(...meanMax).toFixed(3));
line(8, 'guessed', 0.50, within >= 800, 'crossings never more than the larger of start and end by more than 2 in ' + within + ' of 1,000 (sealed: at least 800); the greatest excess ' + Math.max(...crossAt.map(c => c[2] - Math.max(c[0], c[1]))));
const h = V.filter(v => v[2]).length; console.log('\n' + h + ' of ' + V.length + ' held.');
for (const k of ['worked', 'guessed']) console.log('  ' + k + ': ' + V.filter(v => v[0] === k && v[2]).length + ' of ' + V.filter(v => v[0] === k).length);
console.log('  mean squared error of the odds (Brier): ' + (V.reduce((s, v) => s + (v[1] - (v[2] ? 1 : 0)) ** 2, 0) / V.length).toFixed(3) + '; had every line been given 0.5: 0.250');
worst.sort((a, b) => a[0] - b[0]); console.log('\nthe five nearest to a kink (least speed, seed, turning number): ' + worst.slice(0, 5).map(w => w[0].toFixed(4) + ' seed ' + w[1] + ' n ' + w[2]).join('; '));
const byn = {}; worst.forEach(w => { (byn[w[2]] = byn[w[2]] || []).push(w[0]); }); console.log('least speed by turning number (median; least): ' + Object.keys(byn).sort((a, b) => a - b).map(n => n + ': ' + med(byn[n]).toFixed(3) + '; ' + Math.min(...byn[n]).toFixed(4) + ' (' + byn[n].length + ')').join(' | '));
console.log('crossings of the 1,000 random curves: median ' + med(crossAt.map(c => c[0])) + ', most ' + Math.max(...crossAt.map(c => c[0])) + '; run time ' + ((Date.now() - t0) / 1000).toFixed(0) + ' s');
