"""The gasket page's test, second stage: the page as a phone meets it.   python -I out27/test-remake2.py [FILE]   (run after test-remake.py: it changes tools/shot-gasket.js in place)"""
import sys
H = '/home/agent2/gasket/'
if __name__ == '__main__':
    P = sys.argv[1] if len(sys.argv) > 1 else H + 'tools/shot-gasket.js'; s = open(P, encoding='utf8').read()
    a = """  must(ferrs.length === 0, 'no error on the page in all of this', ferrs.join(' ; ')); await fresh.close();
"""
    b = a + """  // ================= as a phone: 390 by 844 and 360 by 640, touch, twice as sharp as its measure =================
  for (const [w, h] of [[390, 844], [360, 640]]) {
    const ctx = await b.newContext({ viewport: { width: w, height: h }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 }), ph = await ctx.newPage(), perrs = []; ph.on('pageerror', e => perrs.push(String(e)));
    await ph.goto('file://' + page); await ph.waitForTimeout(700);
    const pst = () => ph.evaluate(() => { const cv = document.getElementById('g'), r = cv.getBoundingClientRect(), GP = window.GasketPage; return { box: [r.left, r.top, r.width, r.height], canvas: [cv.width, cv.height], size: GP.size(), view: GP.view(), root: GP.pack().root, chosen: GP.chosen(), drawn: GP.drawn().map(c => c.join(',')), pick: document.getElementById('gpick').textContent, say: document.getElementById('gsay').textContent, scrollY: scrollY, H: innerHeight, room: document.querySelector('p.noon-by') ? 0 : 48, wide: Math.max(document.documentElement.scrollWidth, innerWidth), swap: document.getElementById('swap').getBoundingClientRect().bottom }; });
    const s0 = await pst(), v = s0.view, got = [];
    must(s0.size.narrow && s0.size.W === Math.round(s0.box[2]) && s0.size.H === s0.size.W && Math.round(s0.box[3]) === s0.size.H && s0.canvas[0] === 2 * s0.size.W && s0.canvas[1] === 2 * s0.size.H && s0.box[0] >= 0 && s0.box[0] + s0.box[2] <= w && s0.wide === w,
      'on a phone ' + w + ' wide the picture is drawn at the width it is shown, square, twice as sharp as its measure as the screen is, and inside the screen (a visitor: 336 by 208 px, with lettering of 3 to 6 px that did not grow)', JSON.stringify([s0.box.map(Math.round), s0.canvas, s0.size, s0.wide]));
    must(s0.scrollY === 0 && s0.box[1] > 0 && s0.box[1] + s0.box[3] <= s0.H - s0.room, 'on a phone of ' + w + ' by ' + h + ' the picture is whole on the first screen, with ' + s0.room + ' px to spare, the room the public site\\'s line takes where this copy has none (a visitor: "No picture" on the first screen)', JSON.stringify([Math.round(s0.box[1] + s0.box[3]), s0.H, s0.room]));
    G.inView(G.place(s0.root), { cx: v.cx, cy: v.cy, hw: s0.size.W / 2 / v.s, hh: s0.size.H / 2 / v.s }, 0.7 / v.s, (bb, X, Y, wx, wy, k) => got.push([bb, X, Y, k || 0].join(',')), 600000);
    must(got.length === s0.drawn.length && got.every((x, i) => x === s0.drawn[i]) && Math.abs(v.s - (Math.min(s0.size.W, s0.size.H) / 2 - 15) * 4) < 1e-9 && s0.drawn.filter(x => x.startsWith('36,')).length === 2,
      'on a phone ' + w + ' wide the circles drawn are those the program finds in a picture of that size, the outer circle 15 px inside its edge, the two 36s among them', got.length + ' against ' + s0.drawn.length);
    if (w === 390) {
      must(s0.swap <= s0.H - s0.room, 'at 390 by 844 the sentence under the picture and its button are on the first screen as well, with ' + s0.room + ' px to spare', Math.round(s0.swap) + ' of ' + s0.H);
      const c36 = s0.drawn.map(x => x.split(',').map(Number)).filter(c => c[0] === 36)[0], at = c => [s0.box[0] + s0.size.W / 2 + (c[1] / c[0] - v.cx) * v.s, s0.box[1] + s0.size.H / 2 - (c[2] / c[0] - v.cy) * v.s], q = at(c36);
      await ph.touchscreen.tap(q[0], q[1]); await ph.waitForTimeout(250); const s1 = await pst();
      must(s1.chosen && s1.chosen[0] === 36 && s1.pick === 'The circle marked 36. 36 = 6 × 6, a square. Divided by 24 it leaves 12. “Magnify” now closes in on this circle.' && s1.scrollY === 0, 'a tap on a circle marked 36 chooses it, and the line under the picture says what 36 is (a visitor: "Tap on a circle: nothing")', s1.pick);
      const cdp = await ctx.newCDPSession(ph), touch = (type, pts) => cdp.send('Input.dispatchTouchEvent', { type, touchPoints: pts.map((t, i) => ({ x: t[0], y: t[1], id: i })) }), bx = s0.box;
      await touch('touchStart', [[bx[0] + 150, bx[1] + 160], [bx[0] + 190, bx[1] + 160]]); for (let k = 1; k <= 8; k++) { await touch('touchMove', [[bx[0] + 150 - 8 * k, bx[1] + 160], [bx[0] + 190 + 8 * k, bx[1] + 160]]); await ph.waitForTimeout(16); } await touch('touchEnd', []); await ph.waitForTimeout(300);
      const s2 = await pst(); must(s2.view.s / s1.view.s > 3 && s2.view.s / s1.view.s < 5 && /Magnified 4(\\.\\d+)? times/.test(s2.say) && s2.scrollY === 0, 'two fingers drawn apart, from 40 px to 168, magnify the picture about four times, and the page does not move (a visitor: "Two-finger pinch: does not magnify")', (s2.view.s / s1.view.s).toFixed(2) + ' | ' + s2.say.slice(0, 80));
      await ph.tap('#home'); await ph.waitForTimeout(250); const s3 = await pst();
      await touch('touchStart', [[bx[0] + 150, bx[1] + 250]]); for (let k = 1; k <= 8; k++) { await touch('touchMove', [[bx[0] + 150, bx[1] + 250 - 25 * k]]); await ph.waitForTimeout(16); } await touch('touchEnd', []); await ph.waitForTimeout(500);
      const s4 = await pst(); must(s4.scrollY - s3.scrollY > 100 && s4.view.cx === s3.view.cx && s4.view.cy === s3.view.cy && s4.view.s === s3.view.s && s4.drawn.length === s3.drawn.length, 'a thumb that lands on the picture and flicks upwards scrolls the page, and the gasket stays in its frame (a visitor: the page stayed still and the gasket was thrown out: "0 circles drawn")', JSON.stringify([s4.scrollY - s3.scrollY, s4.view, s4.drawn.length]));
      await ph.evaluate(() => scrollTo(0, 0)); await ph.waitForTimeout(200); const s5 = await pst();
      await touch('touchStart', [[bx[0] + 220, bx[1] + 150]]); for (let k = 1; k <= 8; k++) { await touch('touchMove', [[bx[0] + 220 - 12 * k, bx[1] + 150 + 2 * k]]); await ph.waitForTimeout(16); } await touch('touchEnd', []); await ph.waitForTimeout(300);
      const s6 = await pst(); must(s6.scrollY === s5.scrollY && Math.abs((s6.view.cx - s5.view.cx) * s5.view.s - 96) < 1.5 && Math.abs((s6.view.cy - s5.view.cy) * s5.view.s - 16) < 1.5, 'one finger that sets off sideways moves the picture with it (96 px left and 16 down) and the page stays', JSON.stringify([s6.scrollY - s5.scrollY, (s6.view.cx - s5.view.cx) * s5.view.s, (s6.view.cy - s5.view.cy) * s5.view.s]));
    }
    must(perrs.length === 0, 'no error on the page as a phone ' + w + ' wide', perrs.join(' ; ')); await ctx.close(); }
"""
    assert s.count(a) == 1, s.count(a); s = s.replace(a, b); open(P, 'w', encoding='utf8').write(s); print('test: the page as a phone')
