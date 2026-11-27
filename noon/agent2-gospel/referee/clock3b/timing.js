// Referee: how long after an example button is tapped the first step is drawn.
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1000, height: 1400 } });
  await p.goto('file:///home/agent2/gospel/work7/double.html');
  await p.waitForTimeout(600);
  const labels = await p.evaluate(() => Array.from(document.querySelectorAll('#presets button')).map(function (x) { return x.textContent.trim(); }));
  console.log('pace:', await p.evaluate(() => document.getElementById('pace').value));
  for (const i of [0, 2, 0, 1, 3, 4]) {
    const r = await p.evaluate(async (i) => {
      const btn = document.querySelectorAll('#presets button')[i];
      btn.scrollIntoView({ block: 'center' });
      await new Promise(function (res) { setTimeout(res, 300); });
      const t0 = performance.now();
      btn.click();
      let first = null, second = null, saidUntil = null;
      while (performance.now() - t0 < 4000) {
        const s = window.GOSPELSTATE();
        if (String(s.report || '') === 'About to set off.') saidUntil = performance.now() - t0;
        if (first === null && s.drawn >= 1) first = performance.now() - t0;
        if (s.drawn >= 2) { second = performance.now() - t0; break; }
        await new Promise(function (res) { setTimeout(res, 10); });
      }
      const s = window.GOSPELSTATE();
      return { P: s.P, Q: s.Q, total: s.total, first: first, second: second, saidUntil: saidUntil };
    }, i);
    console.log('button ' + i + ' "' + labels[i] + '": ' + r.P + '/' + r.Q + ', ' + r.total + ' steps drawn in all; "About to set off." last seen at ' + Math.round(r.saidUntil) + ' ms; first step drawn at ' + Math.round(r.first) + ' ms; second at ' + Math.round(r.second) + ' ms');
    await p.waitForTimeout(400);
  }
  await b.close();
})();
