// Leave the Sloughs page running on its own clock and note its state every minute.   usage: node soak-river.js PAGE.html MINUTES SPEED SEED
// SPEED is the value of the page's speed control (0.2 is "steady", 4 is "hurried").
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const page = path.resolve(process.argv[2]), minutes = +process.argv[3], speed = process.argv[4], seed = process.argv[5] || '1';
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required', '--enable-precise-memory-info'] }); const p = await b.newPage({ viewport: { width: 1280, height: 1000 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + page + '#seed=' + seed); await p.selectOption('#speed', speed); await p.click('#sound');
  console.log('started', new Date().toISOString(), 'speed', speed, 'seed', seed);
  const end = Date.now() + minutes * 60000; let k = 0, last = null, stalled = 0;
  while (Date.now() < end) {
    await p.waitForTimeout(60000); k++;
    const s = await p.evaluate(() => Object.assign(window.__river.state(), { heap: performance.memory ? Math.round(performance.memory.usedJSHeapSize / 1e6) : null, label: document.getElementById('now').textContent }));
    if (last !== null && s.now <= last) stalled++;
    console.log(`minute ${k}: time ${s.now.toFixed(1)}, nodes ${s.N}, length/valley ${s.S.toFixed(2)} (shown ${s.label}), mean ${s.mean === null ? '-' : s.mean.toFixed(3)}, loops cut ${s.ncut}, lakes showing ${s.lakes}, bells kept ${s.strikes}, chart points ${s.series}, river from y ${s.ymin.toFixed(0)} to ${s.ymax.toFixed(0)}, heap ${s.heap} MB, errors ${errs.length}`);
    last = s.now;
  }
  const s = await p.evaluate(() => window.__river.state());
  await p.screenshot({ path: path.join(path.dirname(page), 'page', 'shots', 'soak-end-speed' + speed + '.png') }).catch(() => {});
  console.log('ended', new Date().toISOString(), 'minutes', k, 'time reached', s.now.toFixed(1), 'loops cut', s.ncut, 'minutes with no advance', stalled, 'script errors', JSON.stringify(errs.slice(0, 5)));
  await b.close();
})();
