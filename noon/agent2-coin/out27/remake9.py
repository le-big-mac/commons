"""Ninth stage of the coin page's remake, after the page's own test was run on the page as built for the public site
(27 November 2026, 17:48 UTC): the line that the build puts above the page pushed the rings below a small phone's first
screen. The build's line is now 48 px on a phone (it was 88 to 107), and here the key to the rings (solid: handed over;
dashed: handed back) goes under the rings, where it had stood above the box for the amount: 47 px the higher for the rings.
python -I remake9.py   (run after remake8.py)"""
H = '/home/agent2/coin/'
if __name__ == '__main__':
    s = open(H + 'page.src.html', encoding='utf8').read()
    def rep(a, b, count=1):
        global s
        assert s.count(a) == count, (a[:100], s.count(a)); s = s.replace(a, b)
    rep("""  <figure class="viz-root" id="fig3">
    <figcaption>A coin with a <b>solid ring</b> is handed over; a coin with a <b>dashed ring</b> is handed back.</figcaption>
    <div class="controls">""", """  <figure class="viz-root" id="fig3">
    <div class="controls">""")
    rep("""    <div class="ways" id="ways"></div>
  </figure>""", """    <div class="ways" id="ways"></div>
    <figcaption id="ringkey">A coin with a <b>solid ring</b> is handed over; a coin with a <b>dashed ring</b> is handed back.</figcaption>
  </figure>""")
    rep("""  figcaption { color: var(--text-secondary); margin: 0 0 8px; max-width: 900px; } figcaption b { color: var(--text-primary); font-weight: 600; }""",
        """  figcaption { color: var(--text-secondary); margin: 0 0 8px; max-width: 900px; } figcaption b { color: var(--text-primary); font-weight: 600; }
  #ringkey { margin: 8px 0 0; }                 /* the key to the rings, under them */""")
    open(H + 'page.src.html', 'w', encoding='utf8').write(s); print('page: the key to the rings goes under them')
