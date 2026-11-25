// usage: node test-core.js cases.json → the page's numbers for each case, and a sampling check of market()
const C = require('./core.js'), fs = require('fs'); const cases = JSON.parse(fs.readFileSync(process.argv[2])); const out = [];
for (const [q, g, N, a] of cases) { const t0 = Date.now(), p = C.dist(q, g, N, a); let s = 0; for (const v of p) s += v; out.push({ q, g, N, a, ahead: C.ahead(p), sum: s, third: C.below(p, 1 / 3), ms: Date.now() - t0 }); }
let seed = 12345; const rand = () => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; };
let wins = 0; const M = 40000; for (let i = 0; i < M; i++) { const t = C.market(1.1, 1, 1000, 1, Math.random); if (t[1000] > 500) wins++; else if (t[1000] === 500) wins += 0.5; }
console.log(JSON.stringify({ out, sampled: wins / M, M }));
