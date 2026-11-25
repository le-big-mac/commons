// beside.js -- the two broken copies that pass the tests, run beside the true program on the study's curves: do they ever differ?
'use strict';
const fs = require('fs'), path = require('path'), C = require('./ccore.js'), N = 400, src = fs.readFileSync(path.join(__dirname, 'ccore.js'), 'utf8');
const make = (a, b, name) => { if (src.split(a).length !== 2) throw new Error('pattern ' + name); const f = path.join(__dirname, 'mutants', name + '.js'); fs.writeFileSync(f, src.replace(a, b)); return require(f); };
const M1 = make('if (a > Math.PI) a -= TAU; if (a <= -Math.PI) a += TAU; return a;', 'if (a > Math.PI) a -= TAU; if (a < -Math.PI) a += TAU; return a;', 'beside-wrap');
const M2 = C;
let d1 = 0, d2 = 0, n = 0;
for (let seed = 1; seed <= 400; seed++) { const rand = C.rng(seed), k = Math.floor(rand() * 7) - 3, p = C.resample(C.randomCurve(rand, k, 6, 1.5, N), N), S = C.standard(k, N); n++;
  const A = C.shape(p), A1 = M1.shape(M1.resample(M1.randomCurve(M1.rng(seed + 0), k, 6, 1.5, N), N));
  const w = C.whitney(A, C.shape(S), 0.37), q = M1.shape(p), w1 = M1.whitney(q, M1.shape(S), 0.37);
  if (JSON.stringify([A.F, A.n, w.pts, C.kinks(A, C.shape(S))]) !== JSON.stringify([q.F, q.n, w1.pts, M1.kinks(q, M1.shape(S))])) d1++;
 }
const hair = [[0, 0], [1, 0], [0, 0], [0, 1], [-1, 1], [-1, 0]]; console.log('wrap taken half-open the other way: differs from the true program on ' + d1 + ' of ' + n + ' curves (angles, turning number, a deformed curve, the kinks); on a polygon with an edge that doubles straight back the two give turning numbers ' + C.turning(hair) + ' and ' + M1.turning(hair));

