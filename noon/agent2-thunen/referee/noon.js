// Referee: Noon's core.js run on the settings of plates III and IV, beside what I measured on the plates.
const T = require('/home/agent2/thunen/core.js');
const f = (x) => x.toFixed(2);
console.log('plate III settings (10 Koerner): town price, rings r1..r6, third-ring width');
for (const a of [1.5, 1.35, 1.2, 1.05, 0.9, 0.75, 0.6]) { const r = T.rings(a, 10); console.log(a.toFixed(2), r.map(f).join(' '), ' width3', f(r[2] - r[1])); }
let gone = null; for (let a = 1.5; a > 0.6; a -= 0.001) { const r = T.rings(a, 10); if (r[2] - r[1] <= 0) { gone = a; break; } }
console.log('third ring gone at town price', gone.toFixed(3), '(10 Koerner)');
console.log('plate IV settings (1.5 Taler): yield, rings, third-ring width');
for (const y of [10, 9, 8, 7.5, 7, 6.5, 6, 5, 4]) { const r = T.rings(1.5, y); console.log(y, r.map(f).join(' '), ' width3', f(r[2] - r[1])); }
let goney = null; for (let y = 10; y > 4; y -= 0.001) { const r = T.rings(1.5, y); if (r[2] - r[1] <= 0) { goney = y; break; } }
console.log('third ring gone at yield', goney.toFixed(2), '(1.5 Taler)');
// rye worth at the plate's third-ring edges (my measurements, miles) on plate III
for (const [a, d] of [[1.5, 18.2], [1.5, 17.6], [1.35, 14.4], [1.2, 11.2], [1.05, 8.5]]) console.log('worth of rye at', d, 'miles, town price', a, ':', T.price(d, a).toFixed(3));
console.log('worth at 10.4 mi (1.5):', T.price(10.4, 1.5).toFixed(4), ' at 10.67:', T.price(10.67, 1.5).toFixed(4));
// how many printed figures are reproduced when the program's value is rounded as printed
let hit = 0, n = 0; const cnt = (v, book, dec) => { n++; if (Math.abs(Number(v.toFixed(dec)) - book) < 1e-9) hit++; };
[[0,1500],[5,1313],[10,1136],[15,968],[20,809],[25,656],[30,512],[35,374],[40,242],[45,116]].forEach(([x,v]) => cnt(1000*T.price(x,1.5), v, 0));
cnt(T.distance(0,1.5), 49.95, 2);
[[5,5.33,2],[10,10.4,1],[20,19.8,1],[30,28.2,1]].forEach(([x,v,d]) => cnt(T.freight(x), v, d));
[[1,1066],[5,892],[10,685],[15,488],[20,301],[25,124]].forEach(([x,v]) => cnt(T.rentKoppel(T.price(x,1.5),8), v, 0));
[[1.5,1818,1119],[1,963,619],[0.5,108,119]].forEach(([b,k,d]) => { cnt(T.rentKoppel(b,10),k,0); cnt(T.rentDrei(b,10),d,0); });
cnt(T.priceEqual(10),0.516,3); cnt(T.priceZeroKoppel(10),0.437,3); cnt(T.priceZeroDrei(10),0.381,3);
const out = (b) => b < 1.5 ? Math.max(0, T.distance(b, 1.5)) : 0;
[[10,29.9,34.7],[9,27.8,33.3],[8,24.7,31.5],[7,19.8,28.6],[6,10.5,23.6],[5.4,0,18.6]].forEach(([y,b0,b1]) => { cnt(out(T.priceEqual(y)),b0,1); cnt(out(T.priceZeroDrei(y)),b1,1); });
[[1.5,34.7],[1.35,31.7],[1.2,28.6],[1.05,25.0],[0.9,20.9],[0.75,16.1],[0.6,10.4]].forEach(([a,r]) => cnt(T.plain(a,10), r, 1));
[[1.35,844],[1.2,687],[1.05,525],[0.9,367],[0.75,217]].forEach(([a,v]) => cnt(1000*Math.pow(T.plain(a,10)/T.plain(1.5,10),2), v, 0));
[[1.5,21.4],[1.05,13.4],[0.6,1.6]].forEach(([a,v]) => { const r = T.rings(a,10); cnt(r[3]-r[1], v, 1); });
[[1.5,4.5],[1.05,5.4],[0.6,6.2]].forEach(([a,v]) => { const r = T.rings(a,10); cnt(r[4]-r[3], v, 1); });
[[10,34.7],[9,33.3],[8,31.5],[7,28.6],[6,23.6],[5,13.3]].forEach(([y,r]) => cnt(T.plain(1.5,y), r, 1));
console.log('printed figures in the README table reproduced exactly when rounded as printed:', hit, 'of', n);
