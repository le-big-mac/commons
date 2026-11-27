const T = require('/home/agent2/gospel/core.js'); const out = [];
const add = (p, q) => { const c = T.clock(p, q), f = T.forecast(p, q); out.push({ p: f.p, q: c.q, n: c.n, tail: c.tail, kinds: c.kinds, off: c.off, bounded: f.bounded, first: c.hours[0] }); };
for (let q = 3; q <= 3001; q += 2) add(1, q);
let x = 777; for (let i = 0; i < 400; i++) { x = (x * 1103515245 + 12345) % 2147483648; const q = 3 + x % 20000; x = (x * 1103515245 + 12345) % 2147483648; const p = 2 + x % (q - 2); if (T.gcd(p, q) === 1) add(p, q); }
for (const [p, q] of [[5, 36], [1, 18], [7, 72], [1, 126], [3, 8], [1, 4], [1, 2], [1, 1194649], [1635, 1009681], [1, 99225], [1, 225], [11, 1125]]) add(p, q);
require('fs').writeFileSync('/home/agent2/gospel/referee/clock/dump.json', JSON.stringify(out)); console.log(out.length);
