/* pagefacts.js: figures the page states about clouds of its own sizes, counted with the page's own core.   node pagefacts.js > pagefacts.out */
var O = require('./ocore.js');
function sd(v) { var m = v.reduce(function (a, b) { return a + b; }, 0) / v.length; return [m, Math.sqrt(v.reduce(function (a, b) { return a + (b - m) * (b - m); }, 0) / (v.length - 1))]; }
[['disc', 2000, 300], ['disc', 10000, 200], ['disc', 30000, 60], ['disc', 60000, 30], ['ellipse', 10000, 200], ['square', 10000, 200], ['triangle', 10000, 200]].forEach(function (q) {
  var v = [], i, r = O.rng(1000 + q[1]);
  for (i = 0; i < q[2]; i++) { var c = O.sample(q[0], q[1], r); v.push(O.peel(c.x, c.y).layers); }
  var s = sd(v), D = O.discLayers(q[1]);
  console.log(q[0] + ' ' + q[1] + ' points, ' + q[2] + ' clouds: mean ' + s[0].toFixed(2) + ' layers, standard deviation ' + s[1].toFixed(2) + ' (' + (100 * s[1] / s[0]).toFixed(2) + '%); the disc formula gives ' + D.toFixed(2) + '; mean against the formula ' + (100 * (s[0] / D - 1)).toFixed(2) + '%; the law 1.32 (n/10^4)^0.176 gives ' + (1.32 * Math.pow(q[1] / 1e4, 0.176)).toFixed(2));
});
