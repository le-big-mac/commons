const T = require('/home/agent2/gospel/core.js'); const out = [];
const add = (p, q) => { const f = T.forecast(p, q), c = T.clock(p, q), t = T.takeOut(p, q); out.push({ p: f.p, q: f.q, m: f.m, tail: f.tail, n: f.round, bounded: f.bounded, kinds: c.kinds, first: c.hours[0], take: t }); };
for (let q = 3; q <= 3001; q += 2) add(1, q);
let x = 4242; let made = 0;
while (made < 500) { x = (x * 1103515245 + 12345) % 2147483648; const a = Math.floor(x / 65536); x = (x * 1103515245 + 12345) % 2147483648; const b = Math.floor(x / 65536);
  let q = made % 3 === 0 ? [9, 25, 27, 45, 49, 63, 81, 99, 117, 121, 147, 171, 189, 225, 441, 513, 1323, 3, 7, 15, 21, 105][a % 22] * [2, 4, 8, 16, 6, 10, 12, 20, 28, 1, 3, 5, 7][b % 13] : 3 + a % 30000; const p = 2 + b % (q - 2);
  if (T.gcd(p, q) === 1) { add(p, q); made++; } }
require('fs').writeFileSync('/home/agent2/gospel/referee/clock2/dump.json', JSON.stringify(out)); console.log(out.length, 'turtles;', out.filter(d => d.q % 2 === 0).length, 'with even q;', out.filter(d => d.p !== 1).length, 'with p not 1');
