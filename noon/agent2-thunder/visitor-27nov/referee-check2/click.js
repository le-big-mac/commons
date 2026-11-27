const TH = require('/home/agent2/thunder/core.js');
for (const x of [300, 500, 1500, 3000, 5000, 8000, 9000]) { const r = TH.thunder(TH.resample([[0, 5000], [0, 0]], 3), [x, 0]); let click = 0, mid = 0;
  for (let i = 0; i < r.p.length; i++) { const t = r.t0 + i / r.fs, a = Math.abs(r.p[i]); if (t >= r.last - 0.03) click = Math.max(click, a); else if (t >= r.first + 0.02) mid = Math.max(mid, a); }
  console.log('straight smooth from', x, 'm: crack', r.peak.toExponential(3), '| far-end click', click.toExponential(3), '= crack /', (r.peak / click).toFixed(1), '| largest between', mid.toExponential(3), '= crack /', (r.peak / mid).toFixed(1)); }
