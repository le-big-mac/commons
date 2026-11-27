"""test-remake10.py: the page's ninth stage. The two assertions about a phone's first screen now leave room for the line
that the public build puts above the page (48 px on a phone since 27 November; none on the page as it stands at home, so
there the rings must end 48 px above the foot of the screen), and a new one puts the key to the rings under them.
python -I out27/test-remake10.py [FILE]   (after test-remake9.py)"""
import sys
if __name__ == '__main__':
    P = sys.argv[1] if len(sys.argv) > 1 else '/home/agent2/coin/tools/shot-change.js'; s = open(P, encoding='utf8').read()
    def rep(a, b):
        global s
        assert s.count(a) == 1, (a[:90], s.count(a)); s = s.replace(a, b)
    # 390 by 844
    rep("""first.greedy.includes('the same count') && first.lead >= 0 && first.both <= first.H && first.sw <= 390,
      'on a phone (390 by 844) the page opens on the United States\\' coins and 24 cents, as its first sentence says, and the first screen holds all of it without scrolling: the coins to choose, the amount, and the three ways of paying, drawn as rings: six coins, the cashier the same, a 25 handed over and a 1 handed back (a visitor: the rings "are what made me understand the page", and were more than two screens down)');""",
        """first.greedy.includes('the same count') && first.lead >= 0 && first.both <= first.H - room390 && first.key[0] >= first.both - 0.5 && first.key[1] <= first.H - room390 && first.sw <= 390,
      'on a phone (390 by 844) the page opens on the United States\\' coins and 24 cents, as its first sentence says, and the first screen holds all of it without scrolling: the coins to choose, the amount, the three ways of paying, drawn as rings (six coins, the cashier the same, a 25 handed over and a 1 handed back), and under them the key to the rings; with ' + room390 + ' px to spare, which is the room the public site\\'s line above the page takes on a phone where this copy has none (a visitor: the rings "are what made me understand the page", and were more than two screens down; and on the public site that line had pushed them off the screen again)',
      JSON.stringify([Math.round(first.both), first.key.map(Math.round), first.H, room390]));""")
    rep("""      greedy: document.querySelector('#way-greedy .k').textContent, preset:""", """      key: (function () { var k = document.getElementById('ringkey'); if (!k) return [-1, 1e9]; var q = k.getBoundingClientRect(); return [q.top, q.bottom]; })(),
      greedy: document.querySelector('#way-greedy .k').textContent, preset:""")
    rep("""    must(first.preset === '0' && first.coins === '1, 5, 10, 25' && first.amount === '24' &&""", """    const room390 = await ph.evaluate(() => document.querySelector('p.noon-by') ? 0 : 48);
    must(first.preset === '0' && first.coins === '1, 5, 10, 25' && first.amount === '24' &&""")
    # 360 by 640
    rep("""return [r('L').top, r('apply').top, r('apply').bottom, r('L').bottom, r('way-plain').top, r('way-plain').bottom, innerHeight]; });
      must(f[1] < f[3] && f[2] > f[0] && f[5] <= f[6], 'at 360 by 640 the button "Use these" stands beside the box for the range, not on a line of its own, and the first row of rings (paid exactly) is whole on the first screen (a visitor: the button "sits on its own line, so the screen now ends at the slider")', JSON.stringify(f.map(x => Math.round(x)))); await c3.close(); }""",
        """return [r('L').top, r('apply').top, r('apply').bottom, r('L').bottom, r('way-plain').top, r('way-plain').bottom, innerHeight, document.querySelector('p.noon-by') ? 0 : 48]; });
      must(f[1] < f[3] && f[2] > f[0] && f[5] <= f[6] - f[7], 'at 360 by 640 the button "Use these" stands beside the box for the range, not on a line of its own, and the first row of rings (paid exactly) is whole on the first screen with ' + f[7] + ' px to spare, the room the public site\\'s line takes where this copy has none (a visitor: the button "sits on its own line, so the screen now ends at the slider"; on the public site the line above the page had put the rings 19 px below the screen)', JSON.stringify(f.map(x => Math.round(x)))); await c3.close(); }""")
    open(P, 'w', encoding='utf8').write(s); print('test: the first screen with room for the public line; the key under the rings')
