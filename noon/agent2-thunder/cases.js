// Three cases for a reader to work out blind, by this page's core, without the air or the bending of sound: the model as
// it was put to the reader.   node cases.js > cases.out
const TH = require('./core.js');
function peak(res) { let pk = 0, ipk = 0, neg = 0, ineg = 0; for (let i = 0; i < res.dry.length; i++) { if (res.dry[i] > pk) { pk = res.dry[i]; ipk = i; } if (res.dry[i] < neg) { neg = res.dry[i]; ineg = i; } }
  return 'largest ' + pk.toFixed(5) + ' at ' + (res.t0 + ipk / TH.FS).toFixed(4) + ' s after the flash; most negative ' + neg.toFixed(5) + ' at ' + (res.t0 + ineg / TH.FS).toFixed(4) + ' s; first sound ' + res.first.toFixed(4) + ' s, last ' + res.last.toFixed(4) + ' s'; }
const A = TH.resample([[0, -3000], [0, 3000]], 3);
console.log('A. straight, from (0, -3000) to (0, 3000), listener at (1000, 0): ' + peak(TH.thunder(A, [1000, 0], { air: 0, bend: 0 })));
const B = TH.arc(0, 0, 2000, 20, 50);
console.log('B. an arc of radius 2000 about the listener at (0, 0), from 20 to 50 degrees: ' + peak(TH.thunder(B, [0, 0], { air: 0, bend: 0 })));
const Z = [[0, 5000], [400, 3800], [-300, 2500], [200, 1200], [0, 0]];
const C1 = TH.resample(Z, 3);
console.log('C. the zigzag (0,5000) (400,3800) (-300,2500) (200,1200) (0,0), listener at (2000, 0): ' + peak(TH.thunder(C1, [2000, 0], { air: 0, bend: 0 })));
const r = TH.thunder(C1, [2000, 0], { air: 0, bend: 0 }); let e = 0; for (let i = 0; i < r.dry.length; i++) e += r.dry[i] * r.dry[i];
console.log('   C: the sum of squares of the pressure times the sample time: ' + (e / TH.FS).toExponential(4));
