// shares.js -- of the circles of a gasket with curvature up to N, what share falls in each class of remainders modulo 24;
// beside it, how many sporadic numbers the class has (from data.json).  The referee's test of my remark: the classes with
// the fewest circles have the most numbers missing.   node shares.js [N]
const G = require('./gcore.js'), fs = require('fs'), DATA = JSON.parse(fs.readFileSync(__dirname + '/data.json', 'utf8')), N = +(process.argv[2] || 3000000);
for (const d of DATA) { const q = d.root, cnt = new Float64Array(24), strip = q[0] === 0 && q[1] === 0; let total = 0;
  const stack = [q[0], q[1], q[2], q[3], -1, 0]; let sp = 6; for (const c of q) if (c > 0) { cnt[c % 24]++; total++; }
  while (sp) { const top = sp - 6, i = stack[top + 5]; if (i > 3) { sp -= 6; continue; } stack[top + 5] = i + 1; const last = stack[top + 4]; if (i === last) continue;
    const s = stack[top] + stack[top + 1] + stack[top + 2] + stack[top + 3], nw = 2 * (s - stack[top + i]) - stack[top + i]; if (nw > N) continue; if (last < 0 && strip && nw <= stack[top + i] && stack[top + i] === 1) continue;
    cnt[nw % 24]++; total++; stack[sp] = stack[top]; stack[sp + 1] = stack[top + 1]; stack[sp + 2] = stack[top + 2]; stack[sp + 3] = stack[top + 3]; stack[sp + i] = nw; stack[sp + 4] = i; stack[sp + 5] = 0; sp += 6; }
  const res = G.type(q).res, top100 = d.sporadic.slice(-100), line = res.map(r => r + ': share ' + (cnt[r] / total).toFixed(3) + ', sporadic ' + d.sporadic.filter(v => v % 24 === r).length + ', of the last hundred ' + top100.filter(v => v % 24 === r).length).join('; ');
  fs.writeSync(1, JSON.stringify(q) + ' (' + total + ' circles up to ' + N + '): ' + line + '\n'); }
