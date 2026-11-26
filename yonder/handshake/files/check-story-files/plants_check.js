// What plant does the live page draw for each of the three entry states? (its opening(): first 7 moves against its own twin, no slips; first round at the bottom)
const fs = require('fs'), vm = require('vm');
const html = fs.readFileSync('/home/agent3/site/build/extras/bed-public.html', 'utf8');
const sandbox = { module: { exports: {} }, Math, Map, Set, Float64Array, Object };
vm.runInNewContext(html.slice(html.indexOf('// ---- core'), html.indexOf('// ---- end core ----')), sandbox);
const { fromKey, KNOWN, payoff } = sandbox.module.exports;
for (const key of ['D01 D02 C20', 'D12 D10 C21', 'C01 D12 D10', 'D00', 'C01 D01', 'D10 C00']) {
  const m = fromKey(key); let a = 0, b = 0; const o = [];
  for (let t = 0; t < 7; t++) { const x = m.play[a], y = m.play[b]; o.push(x ? 'thorn' : 'leaf'); a = m.nxt[a][y]; b = m.nxt[b][x]; }
  console.log(KNOWN[key][0].padEnd(22), key.padEnd(12), 'from the bottom:', o.join(' '));
}
const h = fromKey('D01 D02 C20'), d = fromKey('D00');
const hd = payoff(h, d, 0.03, 0.98), dd = payoff(d, d, 0.03, 0.98), hh = payoff(h, h, 0.03, 0.98);
console.log('at the page\'s opening settings: the machine earns', hd[0].toFixed(3), 'from a defector; a defector earns', dd[0].toFixed(3), 'from a defector and', hd[1].toFixed(3), 'from the machine; two machines earn', hh[0].toFixed(3));
