const F = require('./core.js'), P = F.parse, S = F.str, fs = require('fs');
const [name, r] = process.argv.slice(2), f = new F.Fusible(), t0 = Date.now(); let n = 0; const orig = f[name].bind(f); f[name] = function (a) { if (++n > 3e6) throw new Error('budget'); return orig(a); };
let out; try { out = S(f[name](P(r))); } catch (e) { out = 'stopped (' + e.message.slice(0, 40) + ')'; }
fs.writeSync(1, name + '(' + r + ') = ' + (out.length > 60 ? out.slice(0, 30) + '... (' + out.length + ' characters)' : out) + '   ' + (Date.now() - t0) + ' ms, calls ' + JSON.stringify(f.calls) + '\n');
