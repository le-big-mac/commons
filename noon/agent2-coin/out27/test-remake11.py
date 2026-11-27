"""test-remake11.py: after the referee's sixth message (referee27/built.md): a copy of the page that hid the key to the rings on a screen
up to 340 px wide passed, because no assertion looked for the key at 320 wide. The loop over narrow widths now looks for the key, shown
under the rings, at each, and takes in 412 px (a phone wider than any the test had tried).   python -I out27/test-remake11.py [FILE]"""
import sys
if __name__ == '__main__':
    P = sys.argv[1] if len(sys.argv) > 1 else '/home/agent2/coin/tools/shot-change.js'; s = open(P, encoding='utf8').read()
    def rep(a, b):
        global s
        assert s.count(a) == 1, (a[:90], s.count(a)); s = s.replace(a, b)
    rep("""    for (const wv of [320, 360, 390]) { await ph.setViewportSize({ width: wv, height: 800 }); await ph.waitForTimeout(250); const q = await ph.evaluate(() => [document.documentElement.scrollWidth, document.getElementById('chartA').viewBox.baseVal.width, document.getElementById('chartA').getBoundingClientRect().width, [...document.querySelectorAll('table.best')].every(t => t.getBoundingClientRect().right <= innerWidth)]);
      must(q[0] <= wv && Math.abs(q[1] - q[2]) < 1.5 && q[3], 'at ' + wv + ' px wide nothing runs off the side, the tables of best sets fit, and the pictures are drawn again at their new width', JSON.stringify(q)); }""",
        """    for (const wv of [320, 360, 390, 412]) { await ph.setViewportSize({ width: wv, height: 800 }); await ph.waitForTimeout(250); const q = await ph.evaluate(() => [document.documentElement.scrollWidth, document.getElementById('chartA').viewBox.baseVal.width, document.getElementById('chartA').getBoundingClientRect().width, [...document.querySelectorAll('table.best')].every(t => t.getBoundingClientRect().right <= innerWidth),
        (function () { var k = document.getElementById('ringkey'), w = document.getElementById('ways'); if (!k || !w) return false; var a = k.getBoundingClientRect(), b = w.getBoundingClientRect(), st = getComputedStyle(k);
          return a.height > 10 && a.width > 100 && st.visibility !== 'hidden' && Number(st.opacity) > 0.5 && a.top >= b.bottom - 0.5 && a.right <= innerWidth && /solid ring is handed over; a coin with a dashed ring is handed back\\./.test(k.textContent); })()]);
      must(q[0] <= wv && Math.abs(q[1] - q[2]) < 1.5 && q[3] && q[4], 'at ' + wv + ' px wide nothing runs off the side, the tables of best sets fit, the pictures are drawn again at their new width, and the key to the rings is shown under them (the referee: a copy that hid the key on a screen up to 340 px wide passed)', JSON.stringify(q)); }""")
    open(P, 'w', encoding='utf8').write(s); print('test: the key at 320, 360, 390 and 412 px wide')
