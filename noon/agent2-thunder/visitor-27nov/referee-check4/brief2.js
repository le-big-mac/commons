// the longest short forms (hand-drawn smooth bows close in) at phone widths: does the pinned block keep its height?
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 800 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 }); const p = await ctx.newPage();
  for (const w of [320, 360, 390]) { await p.setViewportSize({ width: w, height: 800 }); await p.goto('file:///home/agent2/thunder/thunder.html'); await p.waitForTimeout(350);
    const out = await p.evaluate(() => { const scene = document.getElementById('scene'), res = [];
      function xy(x, z) { const v = window.THUNDERSTATE().view, r = scene.getBoundingClientRect(); return [r.left + (x - v[0]) / (v[1] - v[0]) * r.width, r.top + (1 - (z - v[2]) / (v[3] - v[2])) * r.height]; }
      function ev(type, x, y) { scene.dispatchEvent(new PointerEvent(type, { clientX: x, clientY: y, pointerId: 1, bubbles: true, cancelable: true })); }
      const click = id => document.getElementById(id).click();
      function rec(tag) { const pin = document.getElementById('pin').getBoundingClientRect(), br = document.getElementById('brief'), cs = getComputedStyle(br); const rg = document.createRange(); rg.selectNodeContents(br); const tr = rg.getBoundingClientRect();
        res.push({ tag, pin: pin.height, box: br.getBoundingClientRect().height, text: tr.height, lines: Math.round(tr.height / parseFloat(cs.lineHeight)), room: parseFloat(cs.minHeight), chars: br.textContent.length, s: br.textContent }); }
      rec('opening'); click('b-bow'); rec('bow smooth');
      for (const [R, a1] of [[1000, 30], [1000, 110], [1000, 100], [800, 115], [600, 120], [600, 100], [1500, 115], [2000, 95]]) { if (!window.THUNDERSTATE().draw) click('b-draw'); const q = [], k = Math.floor(R * (150 - a1) * Math.PI / 180 / 31); for (let i = 0; i <= k; i++) { const a = (150 + (a1 - 150) * i / k) * Math.PI / 180; q.push([3000 + R * Math.cos(a), R * Math.sin(a)]); }
        let c = xy(q[0][0], q[0][1]); ev('pointerdown', c[0], c[1]); for (let i = 1; i < q.length; i++) { c = xy(q[i][0], q[i][1]); ev('pointermove', c[0], c[1]); } ev('pointerup', c[0], c[1]); if (window.THUNDERSTATE().crooked) click('jag'); rec('own smooth bow ' + R + ' m'); click('jag'); rec('own crooked'); }
      return res; });
    const pins = [...new Set(out.map(o => o.pin.toFixed(1)))], worst = out.slice().sort((a, b) => b.text - a.text)[0];
    console.log('WIDTH', w, ': states', out.length, '| pinned block heights', pins.join(', '), '| room kept for the short form', out[0].room.toFixed(1), 'px | its words need', Math.min(...out.map(o => o.text)).toFixed(1), 'to', Math.max(...out.map(o => o.text)).toFixed(1), 'px (', Math.min(...out.map(o => o.lines)), 'to', Math.max(...out.map(o => o.lines)), 'lines ) | states where they need more than the room:', out.filter(o => o.text > o.room + 0.5).length, '| longest:', worst.chars, 'characters:', worst.s); }
  await b.close();
})();
