// strike density through the piece: node dens.js SEED   (strikes in each 10 s, by kind)
const D = require('./core.js'); if (process.env.DRYADS_P) Object.assign(D.P, JSON.parse(process.env.DRYADS_P));
const g = D.grove(+process.argv[2]); const n = Math.ceil(g.duration / 10); const rows = [];
for (let k = 0; k < n; k++) { const w = g.strikes.filter(s => s.t >= 10 * k && s.t < 10 * k + 10); rows.push(`${String(10 * k).padStart(3)}s  ${String(w.length).padStart(3)}  ` + ['name', 'fork', 'leaf', 'round'].map(q => q[0] + w.filter(s => s.kind === q).length).join(' ') + '  ' + '#'.repeat(w.length)); }
console.log(rows.join('\n')); console.log('grown', g.grown, 'fall', g.fallAt, 'rounds', g.roundsAt, 'duration', g.duration);
