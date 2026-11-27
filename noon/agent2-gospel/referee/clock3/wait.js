// Referee: what the page says under the picture while an example waits before walking.
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1000, height: 1400 } });
  await p.goto('file:///home/agent2/gospel/work7/double.html');
  await p.waitForTimeout(500);
  const read = () => p.evaluate(() => {
    const s = window.GOSPELSTATE();
    return { drawn: s.drawn, running: s.running, report: String(s.report || ''), shown: document.getElementById('report').textContent };
  });
  const pres = await p.$$('#presets button');
  for (const i of [0, 2, 5]) {
    await pres[i].scrollIntoViewIfNeeded();
    await pres[i].click();
    await p.waitForTimeout(300);
    console.log('button ' + i + ', 0.3 s:', JSON.stringify(await read()).slice(0, 260));
    await p.waitForTimeout(900);
    console.log('button ' + i + ', 1.2 s:', JSON.stringify(await read()).slice(0, 200));
    await p.waitForTimeout(700);
    console.log('button ' + i + ', 1.9 s:', JSON.stringify(await read()).slice(0, 200));
  }
  await b.close();
})();
