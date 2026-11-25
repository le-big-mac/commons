// Headless checks of the braids page: its bed against core.js run in node (bit for bit), stills, the controls, the record.
//   usage: node shot-braid.js PAGE.html OUTDIR CORE.js GROWN.json SETTING.json
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const [page, out] = [path.resolve(process.argv[2]), path.resolve(process.argv[3])];
  const { Bed } = require(path.resolve(process.argv[4])); const grown = JSON.parse(fs.readFileSync(process.argv[5], 'utf8')), SET = JSON.parse(fs.readFileSync(process.argv[6], 'utf8'));
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1100, height: 1000 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + page + '#still=1');
  // 1. the grown river, stepped in the page and here
  const buf = Buffer.from(grown.b64, 'base64'); const mine = new Bed(SET); mine.load(new Int16Array(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.length)), grown.steps);
  let same = 0, n = 0;
  for (const steps of [0, 1, 50, 500, 3000]) {
    const got = await p.evaluate(k => { window.__braid.advance(k); return { hash: window.__braid.bed.hash(), steps: window.__braid.bed.steps }; }, steps);
    for (let k = 0; k < steps; k++) mine.step();
    n++; if (got.hash === mine.hash() && got.steps === mine.steps) same++;
    console.log(`after ${got.steps - grown.steps} steps from the grown river: page ${got.hash}, node ${mine.hash()}  ${got.hash === mine.hash() ? 'the same' : 'DIFFERENT'}`);
  }
  console.log(`bed in the page against core.js in node: ${same} of ${n} the same, bit for bit`);
  await p.locator('#river').screenshot({ path: path.join(out, 'grown.png') });
  const said = await p.evaluate(() => document.getElementById('say').textContent); console.log('the line under the picture:', said);
  const br = mine.braiding(0.0035); console.log(`node's measures at the same moment: ${br.streams.toFixed(1)} threads, ${Math.round(100 * br.wet)}% wet, fullest ${Math.round(100 * br.top)}%, relief ${br.relief.toFixed(1)}`);
  // 2. rough and smooth starts
  for (const how of ['rough', 'smooth']) {
    await p.selectOption('#from', how); await p.click('#again'); await p.evaluate(() => window.__braid.advance(2000));
    const s = await p.evaluate(() => { const b = window.__braid.bed, m = b.braiding(0.0035); return { steps: b.steps, noise: b.NOISE, seed: b.seedUsed, streams: m.streams, wet: m.wet, relief: m.relief }; });
    console.log(`begun from ${how} sand, 2000 steps: ${JSON.stringify(s)}`); await p.locator('#river').screenshot({ path: path.join(out, how + '.png') });
  }
  // 3. the two switches change the rule the bed is using
  await p.click('#banks'); await p.click('#law');
  const sw = await p.evaluate(() => ({ KL: window.__braid.bed.KL, M: window.__braid.bed.M, banks: document.getElementById('banks').textContent, law: document.getElementById('law').textContent }));
  console.log('both switches pressed:', JSON.stringify(sw));
  await p.click('#banks'); await p.click('#law');
  const sw2 = await p.evaluate(() => ({ KL: window.__braid.bed.KL, M: window.__braid.bed.M })); console.log('pressed again:', JSON.stringify(sw2));
  // 4. the page left to itself: it runs, the record grows, nothing is thrown
  await p.close(); const p2 = await b.newPage({ viewport: { width: 1100, height: 1000 } }); p2.on('pageerror', e => errs.push(String(e)));
  await p2.goto('file://' + page); await p2.waitForTimeout(4000);
  const a = await p2.evaluate(() => ({ steps: window.__braid.bed.steps, cols: window.__braid.cols })); await p2.waitForTimeout(4000);
  const a2 = await p2.evaluate(() => ({ steps: window.__braid.bed.steps, cols: window.__braid.cols, say: document.getElementById('say').textContent }));
  console.log(`left alone: ${a.steps} steps and ${a.cols} strips of record after 4 s, ${a2.steps} and ${a2.cols} after 8 s`); console.log('the line then:', a2.say);
  await p2.screenshot({ path: path.join(out, 'page.png'), fullPage: true });
  await p2.click('#run'); await p2.waitForTimeout(300); const s1 = await p2.evaluate(() => window.__braid.bed.steps); await p2.waitForTimeout(700); const s2 = await p2.evaluate(() => window.__braid.bed.steps);
  console.log(`stopped: ${s1} steps, and ${s2} a moment later  ${s1 === s2 ? 'it holds still' : 'IT MOVED'}`);
  console.log('script errors:', JSON.stringify(errs));
  await b.close();
})();
