/* live-drive.js: the coin page as served, opened as a phone and driven with taps.   cd ~/web && node ~/coin/out27/live-drive.js URL
   Prints one JSON object: the opening sentence, the sentence over the averages before and after its button, what an add button says and does. */
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(), c = await b.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2, userAgent: 'research-script/1.0' });
  const p = await c.newPage(), errs = []; p.on('pageerror', e => errs.push(String(e)));
  const resp = await p.goto(process.argv[2], { waitUntil: 'load', timeout: 60000 }); await p.waitForTimeout(800);
  const txt = id => p.evaluate(i => document.getElementById(i).innerText.replace(/\s+/g, ' ').trim(), id), o = { status: resp.status() };
  o.byline = await p.evaluate(() => { const e = document.body.firstElementChild; return [e.innerText.slice(0, 60), Math.round(e.getBoundingClientRect().height)]; });
  o.lead = await txt('lead'); o.ways = await p.evaluate(() => [...document.querySelectorAll('#ways .way p.k')].map(e => e.innerText.replace(/\s+/g, ' ')));
  o.story = await txt('story'); await p.tap('#story button'); await p.waitForTimeout(900); o.storyAfterSwap = await txt('story'); o.coinsAfterSwap = await p.inputValue('#coins');
  await p.tap('#story button'); await p.waitForTimeout(900); o.coinsAfterBack = await p.inputValue('#coins');
  o.addPlain = await txt('addPlain'); await p.evaluate(() => document.getElementById('addPlain').scrollIntoView({ block: 'center' })); await p.waitForTimeout(200); await p.tap('#addPlain'); await p.waitForFunction(() => !window.__coin.pending); await p.waitForTimeout(600);
  o.addedSay = await txt('addedSay'); o.coinsAfterAdd = await p.inputValue('#coins'); o.width = await p.evaluate(() => document.documentElement.scrollWidth); o.errors = errs;
  console.log(JSON.stringify(o, null, 1)); await b.close();
})();
