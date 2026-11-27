// Does the picture's ground carry, where the record says, the words the record holds?  The recorded word is drawn afresh on a canvas of the ground's colour and set against the picture's pixels.   node pixels.js PAGE...
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const page of process.argv.slice(2)) for (const [W, H, dpr] of [[1100, 900, 1], [390, 844, 2]]) {
    const ctx = await b.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: dpr }), p = await ctx.newPage(); await p.goto('file://' + page); await p.waitForTimeout(400);
    const res = await p.evaluate(() => { const s = window.THUNDERSTATE(), c = document.getElementById('scene'), g = c.getContext('2d'), out = [];
      for (const m of s.marks) { const x0 = Math.floor(m.x) - 1, y0 = Math.floor(m.y) - 1, w = Math.ceil(m.w) + 3, h = Math.ceil(m.h * 1.3) + 2, a = g.getImageData(x0, y0, w, h).data;
        const o = document.createElement('canvas'); o.width = w; o.height = h; const q = o.getContext('2d'); q.fillStyle = '#1b2118'; q.fillRect(0, 0, w, h); q.fillStyle = m.fill; q.font = m.font; q.textBaseline = 'top'; q.fillText(m.word, m.x - x0, m.y - y0);
        const d = q.getImageData(0, 0, w, h).data; let ink = 0, diff = 0; for (let i = 0; i < a.length; i += 4) { const la = a[i] + a[i + 1] + a[i + 2], lb = d[i] + d[i + 1] + d[i + 2]; if (lb > 200) ink++; if (Math.abs(la - lb) > 120) diff++; }
        out.push(m.word + ': ink ' + ink + ', differing ' + diff); } return out.join('; '); });
    console.log(page.split('/').pop() + ' at ' + W + ': ' + res); await ctx.close(); }
  await b.close();
})();
