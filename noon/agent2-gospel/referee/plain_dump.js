// dump the page's forecast facts (core.js only; no browser) for a list of odd denominators
const T = require('/home/agent2/gospel/core.js');
const ms = [];
for (let m = 3; m <= 3001; m += 2) ms.push(m);
// larger ones: three or more primes, or high powers, up to 2,000,000
const extra = [99225, 1194649, 189, 3 ** 9, 3 ** 12, 5 ** 8, 7 ** 7, 9 * 49 * 25, 27 * 49 * 5, 81 * 7 * 13 * 19, 9 * 7 * 73, 27 * 7 * 73, 81 * 73 * 7, 243 * 73, 729 * 487, 9 * 1093, 3 * 1093, 5 * 1093, 1093 * 7 * 9, 1093 * 25, 1093 * 49 * 3, 9 * 127 * 73, 25 * 11 * 31 * 41, 125 * 11 * 101, 625 * 101 * 11, 3125 * 101, 49 * 29 * 43 * 3, 343 * 29, 2401 * 29 * 3, 121 * 23 * 89 * 3, 169 * 53 * 79, 289 * 103 * 3, 9 * 25 * 49 * 121, 27 * 125 * 49, 81 * 25 * 7 * 13, 3 ** 6 * 7 * 19 * 13, 3 ** 5 * 19 * 37 * 7, 1009681];
let x = 12345;
while (extra.length < 420) { x = (x * 1103515245 + 12345) % 2147483648; let m = 3 + 2 * (x % 999998); const f = T.factor(m); if (f.length >= 3 && f.some(a => a[1] >= 2) || f.some(a => a[1] >= 4)) extra.push(m); }
const out = [];
for (const m of ms.concat(extra)) { const f = T.forecast(1, m); out.push({ m: m, round: f.round, factors: f.factors, bounded: f.bounded, serves: f.serves, spoilt: f.spoilt, squares: f.squares }); }
require('fs').writeFileSync('/home/agent2/gospel/referee/plain_dump.json', JSON.stringify(out));
console.log(out.length, 'denominators dumped;', extra.length, 'larger');
