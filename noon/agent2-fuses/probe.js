const F = require('./core.js'), P = F.parse, S = F.str;
for (const r of ['1/2', '1', '9/8', '5/4', '3/2', '7/4', '15/8', '31/16', '2', '65/32', '33/16']) {
  const f = new F.Fusible(), t0 = Date.now(); let out;
  // run with a budget: stop if too many calls
  const orig = f.succ.bind(f); let n = 0; f.succ = function (a) { if (++n > 3e6) throw new Error('budget'); return orig(a); };
  try { out = S(f.succ(P(r))); } catch (e) { out = 'stopped after ' + n + ' calls (' + e.message + ')'; }
  console.log('succ(' + r + ') = ' + out + '   distinct arguments ' + f.calls.succ + ', ' + (Date.now() - t0) + ' ms');
}
