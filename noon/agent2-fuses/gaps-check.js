// gaps-check.js -- the gap memory against the plain one (core-mapmemo.js, a memory of single answers): the same answers?
// usage: node gaps-check.js E FROM TO      and then random dyadics with denominators up to 2^20 below TO/2^E
const A = require('./core.js'), B = require('./core-mapmemo.js'), fs = require('fs'), say = s => fs.writeSync(1, s + '\n');
const E = +process.argv[2], a = +process.argv[3], b = +process.argv[4]; const fa = new A.Fusible(), fb = new B.Fusible();
let n = 0, bad = 0, badW = 0, t0 = Date.now(), ta = 0, tb = 0, t;
for (let i = a; i <= b; i++) { const r = A.D(i, E); t = Date.now(); const x = fa.succ(r); ta += Date.now() - t; t = Date.now(); const y = fb.succ(r); tb += Date.now() - t; n++; if (A.cmp(x, y) !== 0) bad++;
  if (A.cmp(fa.weakSucc(r), fb.weakSucc(r)) !== 0) badW++; }
say(`grid 1/2^${E}, ${a}..${b}: Succ the same at ${n - bad} of ${n}, WeakSucc at ${n - badW} of ${n};  gap memory ${ta} ms (${fa.calls.succ} computed, ${fa.gS.count()} gaps), plain memory ${tb} ms (${fb.calls.succ} computed)`);
let seed = 12345; const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648; n = 0; bad = 0; badW = 0;
for (let j = 0; j < 3000; j++) { const e = 1 + Math.floor(rnd() * 20), top = Math.floor(b / Math.pow(2, E) * Math.pow(2, e)), r = A.D(Math.floor(rnd() * top), e); n++; if (A.cmp(fa.succ(r), fb.succ(r)) !== 0) bad++; if (A.cmp(fa.weakSucc(r), fb.weakSucc(r)) !== 0) badW++; }
say(`3000 random dyadics below ${b}/2^${E} with denominators up to 2^20: Succ the same at ${n - bad}, WeakSucc at ${n - badW}`);
