const F = require('./core.js'), P = F.parse, S = F.str, fs = require('fs');
const f = new F.Fusible(); let line = '';
for (const r of ['0', '1/4', '1/2', '3/4', '1', '9/8', '5/4', '3/2', '7/4', '2', '33/16']) line += `meekSucc(${r}) = ${S(f.meekSucc(P(r)))}, succ = ${S(f.succ(P(r)))}; `;
fs.writeSync(1, line + '\n');
for (const r of ['0', '1/4', '1/2']) { try { fs.writeSync(1, `as printed: MeekSucc(${r}) = ${S(new F.Fusible().meekSucc(P(r), true))}\n`); } catch (e) { fs.writeSync(1, e.message + '\n'); } }
