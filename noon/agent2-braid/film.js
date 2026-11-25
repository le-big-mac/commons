// film.js -- a film of the river made here, with the page's colours: from a saved bed, one frame every PER steps.
//   usage: node film.js BEDFILE FRAMES PER OUT.mp4        (needs ffmpeg; frames are 1024 x 256, 30 a second)
const { Bed } = require('./core.js'); const fs = require('fs'); const { spawn } = require('child_process');
const SET = JSON.parse(fs.readFileSync(__dirname + '/setting.json', 'utf8')), [file, frames, per, out] = [process.argv[2], +process.argv[3], +process.argv[4], process.argv[5]];
const b = new Bed(SET), buf = fs.readFileSync(file); b.h.set(new Float64Array(buf.buffer.slice(buf.byteOffset, buf.byteOffset + 8 * b.NX * b.NY)));
const Z = 4, W = b.NY * Z, H = b.NX * Z, small = new Float32Array(b.NY * b.NX * 3), rgb = Buffer.alloc(W * H * 3);
function paint() {
  for (let j = 0; j < b.NY; j++) for (let i = 0; i < b.NX; i++) { const c = j * b.NX + i, w = b.Q[c] / b.total, o = (i * b.NY + j) * 3;
    if (w > 0.0035) { const v = Math.min(1, Math.sqrt(w / 0.25)); small[o] = 150 - 130 * v; small[o + 1] = 185 - 110 * v; small[o + 2] = 215 - 60 * v; }
    else { let s = 0.93 + 0.02 * (b.h[c] - b.SLOPE * (b.NY - 1 - j)) / b.SLOPE; s = Math.max(0.78, Math.min(1.1, s)); small[o] = 196 * s; small[o + 1] = 178 * s; small[o + 2] = 140 * s; } }
  for (let y = 0; y < H; y++) { const fy = Math.max(0, Math.min(b.NX - 1, (y + 0.5) / Z - 0.5)), y0 = Math.floor(fy), y1 = Math.min(b.NX - 1, y0 + 1), ty = fy - y0;
    for (let x = 0; x < W; x++) { const fx = Math.max(0, Math.min(b.NY - 1, (x + 0.5) / Z - 0.5)), x0 = Math.floor(fx), x1 = Math.min(b.NY - 1, x0 + 1), tx = fx - x0, o = (y * W + x) * 3;
      for (let k = 0; k < 3; k++) rgb[o + k] = Math.round((1 - ty) * ((1 - tx) * small[(y0 * b.NY + x0) * 3 + k] + tx * small[(y0 * b.NY + x1) * 3 + k]) + ty * ((1 - tx) * small[(y1 * b.NY + x0) * 3 + k] + tx * small[(y1 * b.NY + x1) * 3 + k])); } }
}
const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', `${W}x${H}`, '-r', '30', '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', out], { stdio: ['pipe', 'inherit', 'inherit'] });
(async () => {
  b.step(true);
  for (let f = 0; f < frames; f++) { paint(); if (!ff.stdin.write(Buffer.from(rgb))) await new Promise(r => ff.stdin.once('drain', r)); for (let s = 0; s < per; s++) b.step(); }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
  const m = b.braiding(); console.log(`${frames} frames, ${per} steps apart: from step 600,000 to ${600000 + frames * per}; at the end ${m.streams.toFixed(1)} threads, ${Math.round(100 * m.wet)}% wet, relief ${m.relief.toFixed(2)} row-falls`);
})();
