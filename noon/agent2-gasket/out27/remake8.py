"""remake8.py -- the eighth stage of the gasket page's remake: what the referee's check of the mending and the plain reader's fifth
visit found (referee27/mending-report.md, reader27/visit-5.md).  It changes page.src.html in place, from
out27/page.src.stage7.html.txt to out27/page.src.stage8.html.txt.        python -I out27/remake8.py
  1. The circle round the rest was still counted when the picture lay wholly outside it (dragged past a corner): "1 circle drawn" over
     an empty picture.  It is counted only when its edge crosses the picture.
  2. "1 circle drawn, 1 of them a square" is "1 circle drawn, and it is a square".
  3. Where no square can pass the test of remainders (the bug-eye), "does not rule out the squares" sent a visitor looking for squares
     that cannot be there: the page now says that none can be, and names only the forms that can pass.
  4. The third panel's passage on fourth powers gives the outcome first and the reason after; a circle numbered 0 is said to be a
     straight line; the old list's button goes while a look is going on.
  5. The foot: "the paper's guess" for "the paper conjectures it"; the fourth-power families are named as the exception to "worked out
     from the four numbers"; "the arXiv archive"; "the lists the authors keep with their programs, in a place their paper names".
  6. Under the paper's figure the sentence that the third panel looks for fourth powers is dropped: the next sentence gives the answer."""
import os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); P = os.path.join(HERE, 'page.src.html')
def rep(s, a, b, n=1):
    assert s.count(a) == n, (s.count(a), a[:90]); return s.replace(a, b)
def main():
    s = open(P, encoding='utf-8').read()
    assert s == open(os.path.join(HERE, 'out27', 'page.src.stage7.html.txt'), encoding='utf-8').read(), 'page.src.html is not stage 7'
    # 1. the circle round the rest: its edge must cross the picture
    s = rep(s, "For the circle round the rest: its edge does.\n", "For the circle round the rest: its edge does, which is to say that the picture's nearest point is within it and its farthest corner is not.\n")
    s = rep(s, "qx, qy; if (b < 0) return (dx + W / 2) * (dx + W / 2) + (dy + H / 2) * (dy + H / 2) >= r * r; qx = Math.max(dx - W / 2, 0); qy = Math.max(dy - H / 2, 0); return qx * qx + qy * qy <= r * r; }",
               "qx = Math.max(dx - W / 2, 0), qy = Math.max(dy - H / 2, 0); if (qx * qx + qy * qy > r * r) return false; return b > 0 || (dx + W / 2) * (dx + W / 2) + (dy + H / 2) * (dy + H / 2) >= r * r; }")
    # 2. one circle
    s = rep(s, "($('hi').value === 'none' ? '' : ', <b>' + group(lit) + '</b> of them ' + words)", "($('hi').value === 'none' ? '' : ncirc === 1 ? ', and it is ' + (lit ? '' : 'not ') + words : ', <b>' + group(lit) + '</b> of them ' + words)")
    # 3. the forms the theorem does not rule out, among those that can pass the test at all
    s = rep(s, "  function famRow(u) {", "  // Of the four forms, those with a member that leaves one of the gasket's remainders; and the sentence for a gasket in which the theorem rules none of them out.\n"
               "  function notRuled(res, who) { var can = [1, 2, 3, 6].filter(function (u) { for (var n = 1; n <= 24; n++) if (res.indexOf(u * n * n % 24) >= 0) return true; return false; }),\n"
               "      tail = can.filter(function (u) { return u !== 1; }).map(function (u) { return u === 2 ? 'twice' : u === 3 ? 'three times' : 'six times'; }).join(', ').replace(/, ([^,]+)$/, ' or $1') + ' a square';\n"
               "    return can.indexOf(1) >= 0 ? who + ' does not rule out the squares in it, nor ' + tail + '.' : 'No square leaves any of these remainders, so no square can be here. ' + who + ' does not rule out ' + tail + '.'; }\n"
               "  function famRow(u) {")
    s = rep(s, ": 'The theorem of 2023 does not rule out the squares in it, nor twice, three times or six times a square.') + (t.quartic ? ' In some gaskets with these remainders", ": notRuled(t.res, 'The theorem of 2023')) + (t.quartic && pack.root.join(',') !== '-23,48,49,52' ? ' In some gaskets with these remainders")
    s = rep(s, ": 'The paper’s theorem does not rule out the squares in it, nor twice, three times or six times a square. ';", ": notRuled(t.res, 'The paper’s theorem') + ' ';")
    # 4. the third panel: a circle numbered 0; the fourth powers, outcome first; the old list's button
    s = rep(s, "'These circles belong to the gasket whose four largest circles are <b>' + qname(rootq) + '</b>. ');\n", "'These circles belong to the gasket whose four largest circles are <b>' + qname(rootq) + '</b>. ') + (rootq.indexOf(0) >= 0 ? 'A circle numbered 0 is a straight line. ' : '');\n")
    a = s[s.index("      h += t.k === 1 ? 'In a gasket with these remainders the fourth powers, and 4, 9 and 36 times a fourth power, are either all ruled out or none of them is."):s.index("    var q4 = t.quartic && t.k !== 1 ?")]
    assert a.count('\n') == 3, a.count('\n')
    b = ("      var wit = may.concat(no)[0], ALL = 'in a gasket with these remainders the fourth powers, and 4, 9 and 36 times a fourth power, are either all ruled out or none of them is', TWO = 'in a gasket with these remainders either the fourth powers and 4 times a fourth power are ruled out, or 9 and 36 times a fourth power are',\n"
         "        shown = function (w) { var u = [1, 4, 9, 36].filter(function (u) { var r4 = Math.round(Math.sqrt(Math.sqrt(w / u))); return w % u === 0 && r4 * r4 * r4 * r4 === w / u; })[0], r = group(Math.round(Math.sqrt(Math.sqrt(w / u)))); return group(w) + ' is on a circle, and ' + group(w) + ' = ' + (u === 1 ? '' : u + ' × (') + r + ' × ' + r + ' × ' + r + ' × ' + r + (u === 1 ? '' : ')'); };      /* the outcome first, the reason after */\n"
         "      if (t.k === 1) h += wit ? 'In this gasket no fourth powers are ruled out. The page finds that by looking: ' + shown(wit) + '; and ' + ALL + '. ' : 'In a gasket' + ALL.slice(11) + '. The page finds which by looking for one of them on a circle. Up to ' + group(N) + ' it finds none, which is what would be seen if they are all ruled out, and does not prove it. ';\n"
         "      else h += may.length ? 'In this gasket 9 times and 36 times a fourth power are ruled out as well. The page finds that by looking: ' + shown(may[0]) + '; and ' + TWO + '. ' : no.length ? 'In this gasket the fourth powers, and 4 times a fourth power, are ruled out as well. The page finds that by looking: ' + shown(no[0]) + '; and ' + TWO + '. ' : 'In a gasket' + TWO.slice(11) + '. The page finds which by looking for one of them on a circle, and up to ' + group(N) + ' it finds none. '; }\n")
    s = s.replace(a, b)
    s = rep(s, "$('tsay').textContent = 'Looking through the circles\\u2026'; $('show').disabled = true; setTimeout(look, 30); }", "$('tsay').textContent = 'Looking through the circles\\u2026'; $('show').disabled = true; $('tlist').hidden = true; $('tnums').innerHTML = ''; setTimeout(look, 30); }")
    s = rep(s, ", h, en, miss, fam, spor, list, i, v, wit, u, n, may = [], no = [];", ", h, en, miss, fam, spor, list, i, v, u, n, may = [], no = [];")
    # 5. the foot
    s = rep(s, "as the lists in the authors' own files, which their paper names.", "as the lists the authors keep with their programs, in a place their paper names.")
    s = rep(s, "That the blue numbers come to an end is not known; the paper conjectures it, and the lists only show", "That the blue numbers come to an end is not known: it is the paper's guess, and the lists only show")
    s = rep(s, "by their paper as it stands on arXiv)", "by their paper as it stands in the arXiv archive)")
    s = rep(s, "are worked out from the four numbers by the paper's rules, and the list of missing numbers by going through the circles.</p>", "are worked out from the four numbers by the paper's rules, except the families of fourth powers, which the page finds by looking among the circles; the list of missing numbers comes from going through the circles.</p>")
    open(P, 'w', encoding='utf-8').write(s); open(os.path.join(HERE, 'out27', 'page.src.stage8.html.txt'), 'w', encoding='utf-8').write(s)
    print('page.src.html: stage 8,', len(s), 'characters')
if __name__ == '__main__':
    main()
