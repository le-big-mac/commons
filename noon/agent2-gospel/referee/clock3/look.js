const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1000, height: 1400 } });
  await p.goto('file:///home/agent2/gospel/work7/double.html'); await p.waitForTimeout(500);
  console.log('STATE KEYS', await p.evaluate(() => Object.keys(window.GOSPELSTATE()).join(' ')));
  await p.selectOption('#pace', 'once');
  for (const [a, q] of [['1', '9'], ['1', '63'], ['1', '7'], ['1', '441'], ['1', '17325'], ['5', '36'], ['1', '12'], ['1', '1'], ['1', '4'], ['2', '9'], ['1', '27'], ['1635', '1009681'], ['1', '1194649'], ['1', '21'], ['3', '14'], ['1', '1575'], ['1', '50']]) {
    await p.fill('#num', a); await p.fill('#den', q); await p.waitForTimeout(80);
    const s0 = await p.evaluate(() => { const s = window.GOSPELSTATE(), c = window.GOSPELCLOCK(); return { say: s.say, reason: s.reason, clock: c && c.say }; });
    await p.click('#go'); await p.waitForTimeout(700);
    const rep = await p.evaluate(() => window.GOSPELSTATE().report);
    console.log('== ' + a + '/' + q + '\nSAY: ' + String(s0.say).slice(0, 600) + '\nREASON: ' + s0.reason + '\nCLOCK: ' + String(s0.clock).slice(0, 420) + '\nREPORT: ' + String(rep).slice(0, 330));
  }
  await b.close();
})();
