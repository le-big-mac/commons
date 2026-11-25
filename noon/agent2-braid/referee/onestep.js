// referee: Noon's core.js stepped from a saved bed, bed written out, for comparison with my C program
const { Bed } = require('/home/agent2/braid/core.js'); const fs = require('fs');
const [file, nsteps, out, extra] = process.argv.slice(2);
const SET = Object.assign({ NX: 64, NY: 256, FEED: 1, NOISE: 3, CS: 0.05, KL: 0.4 }, extra ? JSON.parse(extra) : {});
const b = new Bed(SET), buf = fs.readFileSync(file);
b.h.set(new Float64Array(buf.buffer.slice(buf.byteOffset, buf.byteOffset + 8 * b.NX * b.NY)));
for (let s = 0; s < +nsteps; s++) b.step();
fs.writeFileSync(out, Buffer.from(b.h.buffer));
const br = b.braiding(); console.log(nsteps, br.streams.toFixed(3), br.wet.toFixed(4), br.relief.toFixed(4), br.top.toFixed(4), 'time', b.time.toFixed(2));
