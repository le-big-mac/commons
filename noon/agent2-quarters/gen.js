// usage: node gen.js at HOUR MINUTE > chime.json        one chime, as the clock rings it at that time (minute 0, 15, 30 or 45)
//        node gen.js hour HOUR > hour.json              the four chimes of the hour that ends at HOUR o'clock, one after another, 3.5 s apart
const Q = require('./core.js'); const [mode, a, b] = process.argv.slice(2);
if (mode === 'at') { const c = Q.at(+a, +b); process.stdout.write(JSON.stringify({ what: `${a}:${String(b).padStart(2, '0')}`, P: Q.P, rows: c.rows, strikes: c.strikes, notes: c.notes, duration: c.lasts })); }
else {
  const H = +a, notes = []; let t = 0.5; const parts = [];
  for (const [h, m] of [[(H + 23) % 24, 15], [(H + 23) % 24, 30], [(H + 23) % 24, 45], [H, 0]]) {
    const c = Q.at(h, m); parts.push({ at: `${h}:${String(m).padStart(2, '0')}`, starts: +t.toFixed(3), rows: c.rows, strikes: c.strikes });
    for (const n of c.notes) notes.push(Object.assign({}, n, { t: +(n.t + t).toFixed(4) }));
    t += c.notes[c.notes.length - 1].t + 3.5 + (m === 0 ? 0 : 0.0);
  }
  process.stdout.write(JSON.stringify({ what: `the four chimes of the hour ending at ${H} o'clock`, P: Q.P, parts, notes, duration: +(notes[notes.length - 1].t + 9).toFixed(3) }));
}
