"""remake9.py -- the ninth stage of the gasket page's remake: the last points of the plain reader's sixth visit and of the referee's
last check (reader27/visit-6.md, referee27/last-report.md).  It changes page.src.html in place, from
out27/page.src.stage8.html.txt to out27/page.src.stage9.html.txt.        python -I out27/remake9.py
  1. When the whole gasket has left the picture, the line directly under the picture says so and how to bring it back; before, only
     the count said it, below a phone's screen.
  2. "0 circles drawn, 0 of them a square" is "0 circles drawn".
  3. Third panel, the kind with two pairs of fourth-power forms, when the circles looked at show neither pair: one pair is ruled out
     and the page does not know which, so the numbers "not" in the families ruled out are "not, or not known to be".
  4. "In this gasket no fourth powers are ruled out" said less than its reason gives: it now names all four forms."""
import os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); P = os.path.join(HERE, 'page.src.html')
def rep(s, a, b, n=1):
    assert s.count(a) == n, (s.count(a), a[:90]); return s.replace(a, b)
def main():
    s = open(P, encoding='utf-8').read()
    assert s == open(os.path.join(HERE, 'out27', 'page.src.stage8.html.txt'), encoding='utf-8').read(), 'page.src.html is not stage 8'
    s = rep(s, "return c[0] !== 0 && seen(c); }).length;", "return c[0] !== 0 && seen(c); }).length; if (ncirc === 0 && !sel) $('gpick').innerHTML = 'Nothing of the gasket is in view: \\u201cThe whole gasket\\u201d brings it back.';")
    s = rep(s, "($('hi').value === 'none' ? '' : ncirc === 1 ? ', and it is '", "($('hi').value === 'none' || ncirc === 0 ? '' : ncirc === 1 ? ', and it is '")
    s = rep(s, "' ruled out (marked with an orange square) and ' + group(spor.length) + ' not' : '') + '.';", "' ruled out (marked with an orange square) and ' + group(spor.length) + ' not' + (t.quartic && t.k !== 1 && !q4.length ? ', or not known to be' : '') : '') + '.';      /* one pair of fourth-power forms is ruled out there, and the page has not found which */")
    s = rep(s, "'In this gasket no fourth powers are ruled out. The page finds that by looking: '", "'In this gasket the fourth powers are not ruled out, nor 4, 9 or 36 times a fourth power. The page finds that by looking: '")
    open(P, 'w', encoding='utf-8').write(s); open(os.path.join(HERE, 'out27', 'page.src.stage9.html.txt'), 'w', encoding='utf-8').write(s)
    print('page.src.html: stage 9,', len(s), 'characters')
if __name__ == '__main__':
    main()
