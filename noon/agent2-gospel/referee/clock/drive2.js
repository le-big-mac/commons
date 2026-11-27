const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1000, height: 1500 } });
  await p.goto('file:///home/agent2/gospel/double.html'); await p.waitForTimeout(400);
  for (const [a, q] of [['1', '28'], ['1', '12'], ['3', '20'], ['1', '17325'], ['1', '1575'], ['-1', '9'], ['1', '3'], ['1', '1'], ['1', '6'], ['1', '50']]) {
    await p.fill('#num', a); await p.fill('#den', q); await p.waitForTimeout(120);
    const k = await p.evaluate(() => window.GOSPELCLOCK());
    console.log(a + '/' + q + ' :: ' + (k && k.say));
  }
  await b.close();
})();
