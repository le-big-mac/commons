// Film the page frame by frame: the canvas at each 1/24 s of the piece, as JPEG files.   usage: node film-dryads.js PAGE.html FRAMEDIR SEED [FPS]
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const page = path.resolve(process.argv[2]), out = path.resolve(process.argv[3]), seed = process.argv[4], fps = +(process.argv[5] || 24);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 778 } });
  await p.goto('file://' + page + '#seed=' + seed);
  const dur = await p.evaluate(() => window.__dryads.grove().duration), n = Math.ceil(dur * fps);
  for (let k = 0; k < n; k++) {
    await p.evaluate(t => window.__dryads.drawAt(t), k / fps);
    await p.screenshot({ path: path.join(out, 'f-' + String(k).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 93, clip: { x: 0, y: 0, width: 1280, height: 720 } });
    if (k % 500 === 0) console.log('frame', k, 'of', n);
  }
  console.log('frames', n, 'seconds', dur); await b.close();
})();
