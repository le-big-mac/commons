// drive.js -- drive the page: the ninth button, then a few first turns typed in; print what the page says.
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push(String(e)));
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await page.goto('file://' + process.argv[2]);
  await page.waitForTimeout(500);
  const read = async (label) => {
    let last = '', same = 0;
    for (let i = 0; i < 80 && same < 3; i++) {
      await page.waitForTimeout(250);
      const r = await page.textContent('#report');
      if (r === last && r) same++; else { same = 0; last = r; }
    }
    console.log('== ' + label);
    console.log('  say: ' + (await page.textContent('#say')));
    console.log('  deg: ' + (await page.textContent('#deg')));
    console.log('  report: ' + last);
  };
  const btns = await page.$$('#presets button');
  console.log('preset buttons: ' + btns.length + ' ; ninth: ' + (btns[8] ? await btns[8].textContent() : 'none'));
  await page.selectOption('#pace', 'once').catch(() => {});
  if (btns[8]) { await btns[8].click(); await read('ninth button'); }
  for (const [p, q] of JSON.parse(process.argv[3])) {
    await page.fill('#num', String(p));
    await page.fill('#den', String(q));
    await page.selectOption('#pace', 'once').catch(() => {});
    await page.click('#go');
    await read(p + '/' + q);
  }
  console.log('page errors: ' + JSON.stringify(errs));
  await browser.close();
})();
