/* beside.js: the broken copies of ocore.js that the tests let through, run beside the true one on clouds full of
   ties, lines and grids. If they never differ, the rule each one drops is not needed.   node beside.js > beside.out */
var T = require('./ocore.js'), path = require('path');
var names = ['js-right-upright-side-forgotten', 'js-points-in-a-line-not-one-layer'];
names.forEach(function (name) {
  var M = require(path.join(__dirname, 'mutants', name, 'ocore.js')), r = T.rng(99), differ = 0, n = 0, t, i;
  function cmp(x, y) { var a = T.peel(x, y), b = M.peel(x, y); n++; for (var j = 0; j < x.length; j++) if (a.depth[j] !== b.depth[j]) { differ++; return; } }
  for (t = 0; t < 3000; t++) {                                   /* coarse clouds: coordinates on a grid of 5 to 60 steps across */
    var m = 3 + Math.floor(r() * 300), c = T.sample(T.SHAPES[t % 4], m, r), g = T.RAD / (2 + Math.floor(r() * 30));
    for (i = 0; i < m; i++) { c.x[i] = Math.round(c.x[i] / g); c.y[i] = Math.round(c.y[i] / g); }
    cmp(c.x, c.y);
  }
  for (t = 0; t < 300; t++) {                                    /* points all in one line: level, upright, slanted */
    var k = 1 + Math.floor(r() * 12), x = [], y = [], dx = [1, 0, 2, -3][t % 4], dy = [0, 1, 1, 2][t % 4];
    for (i = 0; i < k; i++) { var s = Math.floor(r() * 9); x.push(s * dx); y.push(s * dy); }
    cmp(Int32Array.from(x), Int32Array.from(y));
  }
  for (var a = 1; a <= 9; a++) for (var b = 1; b <= 9; b++) { var gx = [], gy = []; for (i = 0; i < a; i++) for (var j = 0; j < b; j++) { gx.push(i); gy.push(j); } cmp(Int32Array.from(gx), Int32Array.from(gy)); }   /* blocks of grid points */
  console.log(name + ': run beside the true program on ' + n + ' clouds full of ties (coarse clouds, lines, blocks of grid points): different depths in ' + differ);
});
