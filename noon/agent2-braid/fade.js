// fade.js -- from the grown river, with the sand law made linear (M = 1): how fast do the threads fade?   usage: node fade.js BEDFILE
const { Bed } = require('./core.js'); const fs = require('fs');
const SET = JSON.parse(fs.readFileSync(__dirname + '/setting.json', 'utf8')), b = new Bed(Object.assign({}, SET, { M: 1 })), buf = fs.readFileSync(process.argv[2]);
b.h.set(new Float64Array(buf.buffer.slice(buf.byteOffset, buf.byteOffset + 8 * b.NX * b.NY)));
let half = null, one = null, sheet = null; const r0 = (b.step(true), b.braiding().relief);
for (let s = 1; s <= 40000; s++) { b.step(); if (s % 250 === 0) { const m = b.braiding();
  if (half === null && m.relief < r0 / 2) half = s; if (one === null && m.streams <= 1.0001 && m.wet > 0.999) one = s; if (sheet === null && m.relief < 0.05) sheet = s;
  if (s % 4000 === 0) console.log(`step ${s}: streams ${m.streams.toFixed(1)}, wet ${(100 * m.wet).toFixed(0)}%, relief ${m.relief.toFixed(2)} row-falls`); } }
console.log(`relief at the start ${r0.toFixed(2)} row-falls; halved by step ${half}; one thread and all the bed wet by step ${one}; relief under 0.05 row-falls by step ${sheet}  (looked at every 250 steps)`);
