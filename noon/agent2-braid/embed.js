// embed.js -- turn a saved bed (raw 64-bit floats, as fate.js writes it) into the whole numbers the page carries.
//   usage: node embed.js BEDFILE STEPS > grown.json
const { Bed } = require('./core.js'); const fs = require('fs');
const SET = JSON.parse(fs.readFileSync(__dirname + '/setting.json', 'utf8'));
const buf = fs.readFileSync(process.argv[2]); const b = new Bed(SET);
b.h.set(new Float64Array(buf.buffer.slice(buf.byteOffset, buf.byteOffset + 8 * b.NX * b.NY)));
const a = b.dump(); let lo = 0, hi = 0; for (const v of a) { if (v < lo) lo = v; if (v > hi) hi = v; }
process.stderr.write(`heights from ${(lo / 512).toFixed(2)} to ${(hi / 512).toFixed(2)} row-falls about the starting slope\n`);
process.stdout.write(JSON.stringify({ steps: +process.argv[3], b64: Buffer.from(a.buffer).toString('base64') }));
