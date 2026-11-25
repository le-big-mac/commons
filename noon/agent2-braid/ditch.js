// ditch.js -- a nearly smooth bed (heights scattered over a fifth of a row-fall) with one ditch dug in it: two row-falls deep,
// three cells wide, from row 40 to row 100, down the middle.  Written as a bed file for after.js.   usage: node ditch.js OUT.bed
const { Bed } = require('./core.js'); const fs = require('fs');
const SET = JSON.parse(fs.readFileSync(__dirname + '/setting.json', 'utf8')), b = new Bed(Object.assign({}, SET, { NOISE: 0.2, seed: 5 }));
for (let j = 40; j <= 100; j++) for (let i = 31; i <= 33; i++) b.h[j * b.NX + i] -= 2 * b.SLOPE;
fs.writeFileSync(process.argv[2], Buffer.from(b.h.buffer));
