// Where is the picture when Go is pressed on a phone?  usage: node phone.js PAGE.html
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch();
  for (const [w, h] of [[320, 568], [360, 640], [390, 844], [412, 915]]) {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 3 }); await p.goto('file://' + path.resolve(process.argv[2])); await p.waitForTimeout(250);
    for (const preset of ['#go', '#preset2']) {
      if (preset !== '#go') await p.locator(preset).scrollIntoViewIfNeeded();
      await p.click(preset); await p.waitForTimeout(500);
      const r = await p.evaluate(() => { const s = document.querySelector('.stage').getBoundingClientRect(), g = document.getElementById('go').getBoundingClientRect(), rep = document.getElementById('report').getBoundingClientRect(); return { stageTop: Math.round(s.top), stageBottom: Math.round(s.bottom), goBottom: Math.round(g.bottom), reportTop: Math.round(rep.top), vh: window.innerHeight, scrollY: Math.round(window.scrollY) }; });
      const seen = Math.max(0, Math.min(r.vh, r.stageBottom) - Math.max(0, r.stageTop)), tall = r.stageBottom - r.stageTop;
      console.log(w + 'x' + h + ' after ' + (preset === '#go' ? 'Go (page as it opens, not scrolled)' : 'the button "HAKMEM’s rule says yes"') + ': picture from ' + r.stageTop + ' to ' + r.stageBottom + ' px in a window ' + r.vh + ' px tall; ' + seen + ' of its ' + tall + ' px are on the screen; report at ' + r.reportTop);
    }
    await p.close();
  }
  await b.close();
})().catch(e => { console.log('STOPPED ' + String(e).slice(0, 300)); process.exit(2); });
