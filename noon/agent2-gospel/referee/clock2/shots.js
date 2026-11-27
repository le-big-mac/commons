const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  await p.goto('file:///home/agent2/gospel/double.html'); await p.waitForTimeout(500);
  const set = async (a, q) => { await p.fill('#num', a); await p.fill('#den', q); await p.waitForTimeout(250); };
  for (const [a, q] of [['1', '9'], ['1', '45'], ['1', '63'], ['1', '21'], ['1', '441'], ['1', '25'], ['1', '1000000']]) {
    await set(a, q);
    const r = await p.evaluate(() => { const c = document.getElementById('clock').getBoundingClientRect(), w = document.getElementById('clockwhy').getBoundingClientRect(), s = document.getElementById('clocksay').getBoundingClientRect();
      return { top: c.top + scrollY, bottom: Math.max(w.bottom, s.bottom) + scrollY, cw: c.width, ch: c.height, cl: c.left, docw: document.documentElement.scrollWidth }; });
    await p.screenshot({ path: 'shots/clock-' + q + '.png', fullPage: true, clip: { x: 0, y: r.top - 8, width: 390, height: Math.min(r.bottom - r.top + 16, 1500) } });
    const k = await p.evaluate(() => window.GOSPELCLOCK());
    console.log('== ' + a + '/' + q + ' canvas ' + Math.round(r.cw) + 'x' + Math.round(r.ch) + ' at left ' + Math.round(r.cl) + ', page width ' + r.docw + ', picture+words ' + Math.round(r.bottom - r.top) + ' px tall');
    console.log('SAY: ' + (await p.evaluate(() => document.getElementById('say').textContent)).slice(0, 700));
    console.log('CLOCK: ' + k.say);
  }
  for (const [a, q] of [['1', '17325'], ['5', '36'], ['1', '12'], ['1', '28'], ['1', '1575'], ['1', '121'], ['1', '1194649'], ['1', '99225'], ['1', '27'], ['1', '7'], ['1', '50'], ['3', '14']]) {
    await set(a, q); const k = await p.evaluate(() => window.GOSPELCLOCK());
    console.log('== ' + a + '/' + q); console.log('SAY: ' + (await p.evaluate(() => document.getElementById('say').textContent)).replace(/Its turns.*?(That round closes[^.]*\.|A round does not close[^.]*\.)/, '[turns] ').slice(0, 520)); console.log('CLOCK: ' + k.say.replace(/^.*?(Why)/, '$1').slice(0, 900));
  }
  await b.close();
})();
