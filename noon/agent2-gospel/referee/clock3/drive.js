const { chromium } = require('playwright'); const fs = require('fs');
const gcd = (a, b) => { while (b) { [a, b] = [b, a % b]; } return a; };
const L = []; const seen = new Set(); const add = (p, q) => { const k = p + '/' + q; if (q >= 1 && gcd(Math.abs(p), q) === 1 && !seen.has(k)) { seen.add(k); L.push([p, q]); } };
for (let q = 3; q <= 2001; q += 2) add(1, q);                                   // 1,000 odd bottoms, first turn 1
let x = 20261127; const rnd = n => { x = (x * 1103515245 + 12345) % 2147483648; return Math.floor(x / 65536) % n; };
const rep = [9, 25, 27, 45, 49, 63, 75, 81, 99, 117, 121, 125, 147, 169, 171, 189, 225, 243, 275, 315, 343, 441, 513, 675, 1125, 1323, 1575, 2025, 3087, 17325, 99225, 11025, 5775, 3465, 1089, 1225];
const mul = [1, 2, 4, 8, 16, 32, 3, 5, 7, 11, 13, 6, 10, 12, 14, 20, 28, 44, 64];
while (L.length < 1500) { const q = rep[rnd(rep.length)] * mul[rnd(mul.length)]; add(2 + rnd(q - 2), q); }        // repeated primes, tails, first turns other than 1
while (L.length < 2100) { const q = 1000 + rnd(60000); add(1 + rnd(q - 1), q); }                                    // bottoms above 999, odd and even
while (L.length < 2300) { const q = 2 + rnd(998); add(1 + rnd(q - 1), q); }
for (const pq of [[1, 1], [1, 2], [1, 4], [3, 8], [1, 1024], [1, 1194649], [1635, 1009681], [1, 1000000], [1999999, 2000000], [7, 1953125], [1, 12327121], [-1, 9], [10, 9], [1, 1594323]]) add(pq[0], pq[1]);
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1000, height: 1400 } });
  await p.goto('file:///home/agent2/gospel/work7/double.html'); await p.waitForTimeout(500); await p.selectOption('#pace', 'once');
  const t0 = Date.now();
  const out = await p.evaluate(async (L) => { const num = document.getElementById('num'), den = document.getElementById('den'), go = document.getElementById('go'), res = [];
    const wait = ms => new Promise(r => setTimeout(r, ms));
    for (let i = 0; i < L.length; i++) { num.value = String(L[i][0]); den.value = String(L[i][1]); den.dispatchEvent(new Event('input', { bubbles: true }));
      const s = window.GOSPELSTATE(), c = window.GOSPELCLOCK(); const row = { p: L[i][0], q: L[i][1], valid: s.valid, say: s.say, reason: s.reason, clock: c ? c.say : null, report: null, total: s.total };
      if (s.valid && (i % 4 === 0 || L[i][1] > 100000 || i >= L.length - 14) && s.total <= 20000) { go.click(); let n = 0; while (!window.GOSPELSTATE().done && n++ < 400) await wait(10); const d = window.GOSPELSTATE(); row.report = d.done ? d.report : 'NOT DONE'; row.fails = d.fails; }
      res.push(row); }
    return res; }, L);
  fs.writeFileSync('/home/agent2/gospel/referee/clock3/page.json', JSON.stringify(out));
  console.log(out.length, 'turtles read in', Date.now() - t0, 'ms;', out.filter(r => r.report).length, 'walked;', out.filter(r => r.report === 'NOT DONE').length, 'not done;', out.filter(r => !r.valid).length, 'refused');
  await b.close();
})();
