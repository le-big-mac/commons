// usage: node gen.js SEED > grove-SEED.json        or: node gen.js stats FIRST LAST
const D = require('./core.js');
if (process.env.DRYADS_P) Object.assign(D.P, JSON.parse(process.env.DRYADS_P));     // for trying settings
if (process.argv[2] === 'stats') {
  const a = +process.argv[3], b = +process.argv[4], rows = [];
  for (let s = a; s <= b; s++) {
    const g = D.grove(s), ts = g.strikes.map(x => x.t); let peak = 0;
    for (let i = 0; i < ts.length; i++) { let j = i; while (j < ts.length && ts[j] < ts[i] + 2) j++; peak = Math.max(peak, (j - i) / 2); }
    rows.push({ seed: s, dur: g.duration, grown: g.grown, nodes: g.trees.map(t => t.X.length), steps: g.trees.map(t => t.steps), forks: g.trees.map(t => t.forks), rung: g.trees.map(t => t.rung), hushed: g.trees.map(t => t.hushed),
      tips: g.trees.map(t => t.tips.length), unspent: g.trees.map(t => t.unspent + '/' + t.points), strikes: g.strikes.length, fork: g.strikes.filter(x => x.kind === 'fork').length, leaf: g.strikes.filter(x => x.kind === 'leaf').length, leaves: g.leaves.length, peak });
  }
  const brief = process.env.BRIEF;
  for (const r of rows) console.log(brief ? `seed ${r.seed} dur ${r.dur.toFixed(0)} grown ${r.grown.toFixed(0)} nodes ${r.nodes.join(',')} steps ${r.steps.join(',')} forks ${r.forks.join(',')} rung ${r.rung.join(',')} hushed ${r.hushed.join(',')} tips ${r.tips.join(',')} strikes ${r.strikes} (fork ${r.fork}, leaf ${r.leaf} of ${r.leaves}) peak ${r.peak}/s` : JSON.stringify(r));
} else process.stdout.write(JSON.stringify(D.grove(+process.argv[2])));
