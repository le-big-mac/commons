const { chromium } = require('/home/agent3/web/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1180, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  const t0 = Date.now();
  await p.goto('file://' + process.argv[2]);
  await p.waitForFunction(() => window.HEMI && document.getElementById('nLand').textContent !== '–');
  console.log('loaded in', Date.now() - t0, 'ms; errors:', JSON.stringify(errs));
  const pts = [['Catalan summit', 40.82, 1.72], ['Breton summit', 47.42, -2.36], ['Nantes', 47.2167, -1.5333], ['Brandenburg', 52.37, 12.68], ['Valais', 46.0, 7.18], ['Gascony', 43.0, -0.9], ['0,0', 0, 0], ['South Pole', -89.9, 0]];
  for (const [name, la, lo] of pts) {
    const r = await p.evaluate(([la, lo]) => { const o = {}; o.land = HEMI.land(la, lo); o.birds = HEMI.birds(la, lo); o.pop = {}; for (const [i, y] of [[0, 1975], [3, 2010], [5, 2020]]) { HEMI.setYear(i); o.pop[y] = HEMI.people(la, lo); } HEMI.setYear(5); return o; }, [la, lo]);
    console.log(name.padEnd(16), 'land', (100 * r.land).toFixed(3), ' people 1975/2010/2020', (100 * r.pop[1975]).toFixed(3), (100 * r.pop[2010]).toFixed(3), (100 * r.pop[2020]).toFixed(3), ' birds', (100 * r.birds).toFixed(2));
  }
  const t1 = Date.now();
  await p.evaluate(() => { for (let i = 0; i < 20; i++) { HEMI.go(10 + i, 20 + i); } });
  const per = await p.evaluate(() => { const t = performance.now(); for (let i = 0; i < 20; i++) { HEMI.land(10 + i, 5); HEMI.people(10 + i, 5); HEMI.birds(10 + i, 5); } return (performance.now() - t) / 20; });
  console.log('one set of three shares takes', per.toFixed(1), 'ms');
  await p.evaluate(() => HEMI.go(40.82, 1.72)); await p.waitForTimeout(200);
  await p.screenshot({ path: process.argv[3] + '/explore-1.png' });
  // nantes then climb land
  await p.click('button[data-go="47.2167,-1.5333"]'); await p.waitForTimeout(100); await p.click('#climbLand'); await p.waitForTimeout(300);
  console.log('after Nantes + climb land:', await p.evaluate(() => HEMI.state().map(v => v.toFixed(2)).join(', ')), '|', await p.textContent('#msg'));
  await p.click('button[data-go="40.82,1.72"]'); await p.click('#climbLand'); await p.waitForTimeout(300);
  console.log('after Tarragona + climb land:', await p.evaluate(() => HEMI.state().map(v => v.toFixed(2)).join(', ')), '|', await p.textContent('#msg'));
  // people layer, 1975, from Berlin
  await p.check('input[value=people]'); await p.evaluate(() => { const s = document.getElementById('yr'); s.value = 0; s.dispatchEvent(new Event('input')); });
  await p.click('button[data-go="52.26,12.77"]'); await p.click('#climbPop'); await p.waitForTimeout(300);
  console.log('1975, from Berlin, climb people:', await p.evaluate(() => HEMI.state().map(v => v.toFixed(2)).join(', ')), '|', await p.textContent('#msg'));
  await p.evaluate(() => { const s = document.getElementById('yr'); s.value = 5; s.dispatchEvent(new Event('input')); });
  await p.click('button[data-go="46.0,7.17"]'); await p.click('#climbPop'); await p.waitForTimeout(300);
  console.log('2020, from the Valais, climb people:', await p.evaluate(() => HEMI.state().map(v => v.toFixed(2)).join(', ')), '|', await p.textContent('#msg'));
  await p.screenshot({ path: process.argv[3] + '/explore-2.png' });
  // drag test
  const box = await p.locator('#c').boundingBox();
  await p.mouse.move(box.x + box.width / 2, box.y + box.height / 2); await p.mouse.down(); await p.mouse.move(box.x + box.width / 2 + 120, box.y + box.height / 2 + 40, { steps: 6 }); await p.mouse.up();
  console.log('after a drag of 120 px right, 40 px down:', await p.evaluate(() => HEMI.state().map(v => v.toFixed(2)).join(', ')));
  await p.locator('#c').focus(); await p.keyboard.press('ArrowUp'); await p.keyboard.press('Shift+ArrowLeft');
  console.log('after ArrowUp and Shift+ArrowLeft:', await p.evaluate(() => HEMI.state().map(v => v.toFixed(2)).join(', ')));
  console.log('errors at end:', JSON.stringify(errs));
  await b.close();
})();
