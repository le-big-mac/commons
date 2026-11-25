// succ-one.js -- Algorithm 1 at one number, with progress.   node --stack-size=60000 succ-one.js R
const F = require('./core.js'), fs = require('fs'), say = s => fs.writeSync(1, s + '\n');
const r = F.parse(process.argv[2]), f = new F.Fusible(), t0 = Date.now(); let last = t0;
const orig = f.gS.set.bind(f.gS); f.gS.set = function (t, z) { if (Date.now() - last > 60000) { last = Date.now(); say('  .. ' + ((last - t0) / 1000).toFixed(0) + ' s, ' + f.calls.succ + ' computed, ' + f.gS.count() + ' gaps'); } return orig(t, z); };
const z = f.succ(r), g = F.sub(z, r);
say('Algorithm 1: the smallest fusible number above ' + F.str(r) + ' is ' + (F.str(z).length < 60 ? F.str(z) : 'a fraction with denominator 2^' + z[1]) + '; the gap is ' + (g[0] === 1n ? '2^-' + g[1] : F.str(g)) + ';  ' + ((Date.now() - t0) / 1000).toFixed(1) + ' s, ' + f.calls.succ + ' computed, ' + f.gS.count() + ' gaps');
say('the meek rule gives the gap 2^-' + f.meekM(r)[1] + ', the tame rule 2^-' + f.M(r)[1]);
