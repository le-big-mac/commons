// Does a headless browser started as the soak starts it run its sound?   usage: node audio-state.js PAGE.html
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required', '--enable-precise-memory-info'] }); const p = await b.newPage();
  await p.goto('file://' + path.resolve(process.argv[2]) + '#seed=11');
  // watch every AudioContext the page makes, and count the oscillators it starts
  await p.evaluate(() => { const A = window.AudioContext; window.__made = []; window.__osc = 0; const co = A.prototype.createOscillator;
    A.prototype.createOscillator = function () { window.__osc++; if (!window.__made.includes(this)) window.__made.push(this); return co.call(this); }; });
  await p.selectOption('#speed', '4'); await p.click('#sound'); await p.waitForTimeout(20000);
  const r = await p.evaluate(() => ({ contexts: window.__made.length, states: window.__made.map(c => c.state), clocks: window.__made.map(c => +c.currentTime.toFixed(1)), oscillators: window.__osc, cuts: window.__river.state().ncut, label: document.getElementById('sound').textContent }));
  console.log('after 20 s with the bells on, at the fastest speed:', JSON.stringify(r)); await b.close();
})();
