const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1000, height: 1500 } });
  await p.goto('file:///home/agent2/gospel/double.html'); await p.waitForTimeout(400);
  const fixed = await p.evaluate(() => { const h = document.getElementById('why'); let t = '', e = h; while (e && !(e.tagName === 'H2' && e !== h)) { if (e.tagName !== 'CANVAS') t += ' ' + e.textContent; e = e.nextElementSibling; } return t.replace(/\s+/g, ' '); });
  console.log('FIXED:', fixed.slice(0, 1500));
  for (const [a, q] of [['1', '9'], ['1', '45'], ['1', '63'], ['1', '21'], ['1', '7'], ['5', '36'], ['1', '225'], ['1', '441'], ['1', '1194649'], ['1635', '1009681'], ['1', '4'], ['1', '121'], ['2', '9'], ['1', '189'], ['1', '18'], ['1', '2525'], ['1', '99']]) {
    await p.fill('#num', a); await p.fill('#den', q); await p.waitForTimeout(120);
    const k = await p.evaluate(() => window.GOSPELCLOCK());
    console.log(a + '/' + q + ' :: ' + (k && k.say) + ' || polys ' + (k && k.polys) + ' bold ' + (k && k.bold) + ' cross ' + (k && JSON.stringify(k.cross)));
  }
  await b.close();
})();
