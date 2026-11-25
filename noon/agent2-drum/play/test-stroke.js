// usage: node test-stroke.js loads.json "rings, 1.43 skins" stroke.f32  → writes one stroke (half way out, 146.83 Hz, 3.2 s) as raw 32-bit floats and prints the modes and strengths used
const C = require('./core.js'), fs = require('fs'); const load = JSON.parse(fs.readFileSync(process.argv[2]))[process.argv[3]];
const modes = C.allModes(load, 6.6), amps = C.strengths(modes, 0.5); let t0 = Date.now(); let y; for (let i = 0; i < 5; i++) y = C.stroke(modes, amps, 146.83, 3.2, 44100); const ms = (Date.now() - t0) / 5;
fs.writeFileSync(process.argv[4], Buffer.from(y.buffer)); console.log(JSON.stringify({ ms, modes: modes.map((m, i) => [m.m, m.n, m.ratio, amps[i]]) }));
