// Open the public copy of the bed as a visitor would (no settings touched) and time the first take-over by the handshake:
// the first moment the commonest kind is named "the handshake" (or one of its two other entries) with at least 60 of 100.
// usage: node bedtime.js RUNS MAXSECONDS [SHOT.png]
const { chromium } = require('/home/agent3/web/node_modules/playwright');
(async () => {
  const [runs, maxs, shot] = process.argv.slice(2);
  const b = await chromium.launch();
  for (let r = 0; r < parseInt(runs); r++) {
    const p = await b.newPage({ viewport: { width: 1200, height: 1300 } });
    await p.goto('file:///home/agent3/site/build/extras/bed-public.html');
    const t0 = Date.now(); let hit = null, last = '';
    while ((Date.now() - t0) / 1000 < parseFloat(maxs)) {
      await p.waitForTimeout(250);
      const s = await p.evaluate(() => [document.getElementById('topname').textContent, document.getElementById('s_gen').textContent, document.getElementById('s_coop').textContent]);
      last = s.join(' | ');
      const m = s[0].match(/(\d+)% of the bed/) || s[0].match(/(\d+) of \d+/);
      if (/handshake|stiffened wooer/.test(s[0]) && m && parseInt(m[1]) >= 60) { hit = { secs: (Date.now() - t0) / 1000, gen: s[1], name: s[0] }; break; }
    }
    console.log('run', r + 1, hit ? `take-over after ${hit.secs.toFixed(1)} s at generation ${hit.gen}: ${hit.name}` : `no take-over in ${maxs} s; last: ${last}`);
    if (hit && shot && r === 0) {
      await p.waitForTimeout(1500); await p.click('#pause');
      const box = await p.evaluate(() => { const a = document.getElementById('bed').getBoundingClientRect(), c = document.getElementById('chart').getBoundingClientRect(); return { x: a.left - 6, y: a.top - 6, width: Math.max(a.right, c.right) - a.left + 12, height: c.bottom - a.top + 46 }; });
      await p.screenshot({ path: shot, clip: box });
      console.log('  shot taken:', JSON.stringify(box), await p.evaluate(() => [document.getElementById('topname').textContent, document.getElementById('s_gen').textContent].join(' | ')));
    }
    await p.close();
  }
  await b.close();
})();
