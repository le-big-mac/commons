/* make-best.js: the table of best sets for the page, from the searches. node make-best.js -> best.json
   One way, one to six coins, and both ways, one to three: searched again here (seconds).
   One way, seven coins, and both ways, four: read from study.out. Both ways, five: read from both5.out. */
'use strict';
var fs = require('fs'), path = require('path'), cp = require('child_process'), P = require('./pcore.js');
function search(mode, D, L, M) {
  var out = cp.execFileSync(path.join(__dirname, 'search'), [mode, String(D), String(L), String(M)], { encoding: 'utf8' }), best = [];
  out.split('\n').forEach(function (l) { var q = /^\s+best (.*)$/.exec(l); if (q) best.push(q[1].trim().split(/\s+/).map(Number)); });
  return { total: Number(/least total (-?\d+)/.exec(out)[1]), sets: best };
}
function parseSets(s) { return s.split(' and ').map(function (x) { return x.replace(/[()]/g, '').split(',').map(Number); }); }
var study = fs.readFileSync(path.join(__dirname, 'study.out'), 'utf8'), b5 = fs.readFileSync(path.join(__dirname, 'both5.out'), 'utf8');
var plain = [], both = [], D, m;
for (D = 1; D <= 6; D++) plain.push(search('plain', D, 100, 99));
m = /seven coins, least total: (\d+) by (.*?) \(\d+ sets tried\)/.exec(study);
plain.push({ total: Number(m[1]), sets: parseSets(m[2]) });
for (D = 1; D <= 3; D++) both.push(search('both', D, 100, 150));
m = /best four: (\d+) by (.*?) \(\d+ sets\)/.exec(study);
both.push({ total: Number(m[1]), sets: parseSets(m[2]) });
var s5 = []; b5.split('\n').forEach(function (l) { var q = /^\s+best (.*)$/.exec(l); if (q) s5.push(q[1].trim().split(/\s+/).map(Number)); });
both.push({ total: Number(/least total (\d+)/.exec(b5)[1]), sets: s5 });
/* every set named here is scored again by the core, so a slip in the reading would show */
plain.forEach(function (r, i) { r.sets.forEach(function (s) { if (s.length !== i + 1 || P.total(P.plain(s, 100)) !== r.total) throw new Error('one way ' + s); }); r.bound = P.bound(i + 1, 100, 'plain'); });
both.forEach(function (r, i) { r.sets.forEach(function (s) { if (s.length !== i + 1 || P.total(P.both(s, 100)) !== r.total) throw new Error('both ways ' + s); }); r.bound = P.bound(i + 1, 100, 'both'); });
fs.writeFileSync(path.join(__dirname, 'best.json'), JSON.stringify({ L: 100, plainMax: 99, bothMax: 150, plain: plain, both: both }));
console.log(JSON.stringify({ plain: plain, both: both }, null, 0));
