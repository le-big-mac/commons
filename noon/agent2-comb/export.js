// export.js -- forty curves for the referee's blind step, as lists of points; my own answers go to referee-compare.out.
'use strict';
const C = require('./ccore.js'), fs = require('fs'), N = 400; const curves = [], mine = [];
for (let i = 0; i < 40; i++) { const rand = C.rng(7000 + i), n = Math.floor(rand() * 7) - 3, p = C.resample(C.randomCurve(rand, n, 6, 1.5, N), N); curves.push(p.map(q => [+q[0].toFixed(9), +q[1].toFixed(9)])); }
fs.writeFileSync(__dirname + '/referee-curves.json', JSON.stringify(curves));
const S = curves.map(p => C.shape(p));
console.log('A. turning numbers: ' + S.map(s => s.n).join(' '));
console.log('B. crossings: ' + S.map(s => C.crossings(s.pts).length).join(' '));
console.log('C. for the pairs (0,1), (2,3), ..., (38,39): places where the directions are opposite, and their sum with signs: ' + Array.from({ length: 20 }, (_, i) => { const k = C.kinks(S[2 * i], S[2 * i + 1]); return k.length + '/' + k.reduce((t, x) => t + x.sense, 0); }).join(' '));
console.log('D. Whitney\'s deformation of each curve into a circle-like standard is mine to define; instead, of curve 0 into curve k for the k with the same turning number (' + S.map((s, k) => k > 0 && s.n === S[0].n ? k : null).filter(x => x !== null).join(', ') + '): least speed at u = 0.5: ' + S.map((s, k) => k > 0 && s.n === S[0].n ? C.whitney(S[0], s, 0.5).least.toFixed(4) : null).filter(x => x !== null).join(' '));
console.log('E. the plain way from curve 0 to curve 1 at u = L0/(L0+L1) = ' + (S[0].L / (S[0].L + S[1].L)).toFixed(4) + ': shortest edge over mean edge ' + C.straight(S[0], S[1], S[0].L / (S[0].L + S[1].L)).least.toFixed(4) + '; at u = 0.2: ' + C.straight(S[0], S[1], 0.2).least.toFixed(4));
