"""remake6.py -- the sixth stage of the gasket page's remake for a phone: the wordings the plain reader's fourth visit stopped at
(reader27/visit-4.md).  It changes page.src.html in place, from out27/page.src.stage5.html.txt to out27/page.src.stage6.html.txt.
        python -I out27/remake6.py
  1. A product is written so that its square shows: "216 = 6 × (6 × 6)", not "216 = 6 × 6 × 6", which reads as a cube; under the
     gasket too ("12 = 3 × (2 × 2), three times a square").
  2. The strip's answer says "It is one of 18 marks under your finger" (from three marks up), not "the nearest of the 18 marks crowded there".
  3. What is true of the gasket is said in two short sentences, the second ending "that was proved in 2023".
  4. The notes about fourth powers, under the menus and in the third panel, in plain words: no "second sign", no "witness"."""
import os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); P = os.path.join(HERE, 'page.src.html')
def rep(s, a, b, n=1):
    assert s.count(a) == n, (s.count(a), a[:90]); return s.replace(a, b)
def main():
    s = open(P, encoding='utf-8').read()
    assert s == open(os.path.join(HERE, 'out27', 'page.src.stage5.html.txt'), encoding='utf-8').read(), 'page.src.html is not stage 5'
    # 1. the square shows
    s = rep(s, "facts.push(group(b) + ' = ' + (u === 1 ? '' : u + ' \\u00d7 ') + group(n) + ' \\u00d7 ' + group(n) + (u === 1 ? ', a square'",
               "facts.push(group(b) + ' = ' + (u === 1 ? '' : u + ' \\u00d7 (') + group(n) + ' \\u00d7 ' + group(n) + (u === 1 ? '' : ')') + (u === 1 ? ', a square'")
    s = rep(s, "return (u === 1 ? '' : u + ' × ') + group(n) + ' × ' + group(n); }", "return (u === 1 ? '' : u + ' × (') + group(n) + ' × ' + group(n) + (u === 1 ? '' : ')'); }      /* 6 × (6 × 6), so that the square shows: 6 × 6 × 6 reads as a cube */")
    # 2. the crowd under a finger
    s = rep(s, "(crowd > 1 ? ' It is the nearest of the ' + group(crowd) + ' marks crowded there.' : '')", "(crowd > 2 ? ' It is one of ' + group(crowd) + ' marks ' + (CNARROW ? 'under your finger' : 'within 12 px of the pointer') + '.' : '')")
    # 3. two short sentences about the gasket
    s = rep(s, "var kind = 'The numbers of this gasket all leave ' + t.res.join(', ').replace(/, (\\d+)$/, ' or $1') + ' on division by 24 (the test told of below)' + (t.quad === null ? '; the page could not work out its sign, and so not its families' : fams.length ? '; it is proved (Haag, Kertzer, Rickards and Stange, 2023) that none of them is ' + fams.map(famWords).join(' or ') : '; the theorem of 2023 rules out no family of squares in it') + (t.quartic ? ' (for this kind there may be a family of fourth powers as well: see the third panel)' : '') + '.' +",
               "var kind = 'Every number in this gasket leaves ' + t.res.join(', ').replace(/, (\\d+)$/, ' or $1') + ' on division by 24 (the test told of below). ' + (t.quad === null ? 'The page could not work out which families are ruled out in it.' : fams.length ? 'None of them is ' + fams.map(famWords).join(' or ') + ': that was proved in 2023.' : 'The theorem of 2023 rules out no family of squares in it.') + (t.quartic ? ' In some gaskets with these remainders a family of fourth powers is ruled out: the third panel looks for them in this one.' : '') +")
    s = rep(s, "' This is the gasket of the paper\\u2019s first figure, whose caption says that the old guess fails in it for every remainder; by the paper\\u2019s table that means no number in it is n⁴, 4n⁴, 9n⁴ or 36n⁴.'",
               "' This is the gasket drawn in the paper\\u2019s first figure. From what its caption says, and the paper\\u2019s table, no number in it is a fourth power, or 4, 9 or 36 times one.'")
    # 4. the third panel's note on fourth powers
    a = s[s.index("      h += 'For a gasket of this kind the paper has a second sign,"):s.index("    h += '<br>Going through its '")]
    assert a.count('\n') == 3, a.count('\n')
    b = ("      h += t.k === 1 ? 'In a gasket with these remainders the fourth powers, and 4, 9 and 36 times a fourth power, are either all ruled out or none of them is. Which, the page does not work out from the four numbers; it looks among the circles: ' : 'In a gasket with these remainders either the fourth powers and 4 times a fourth power are ruled out, or 9 and 36 times a fourth power are. Which, the page does not work out from the four numbers; it looks among the circles: ';\n"
         "      if (t.k === 1) h += may.length + no.length ? group((may.concat(no))[0]) + ' is one of those numbers and is the number of a circle, so none of them is ruled out here. ' : 'none of those numbers up to ' + group(N) + ' is the number of a circle, which is what would be seen if they are all ruled out, and does not prove it. ';\n"
         "      else h += may.length ? group(may[0]) + ' is a fourth power or 4 times one, and is the number of a circle, so it is 9 and 36 times a fourth power that are ruled out. ' : no.length ? group(no[0]) + ' is 9 or 36 times a fourth power, and is the number of a circle, so it is the fourth powers and 4 times a fourth power that are ruled out. ' : 'it finds none of them up to ' + group(N) + '. '; }\n")
    s = s.replace(a, b)
    open(P, 'w', encoding='utf-8').write(s); open(os.path.join(HERE, 'out27', 'page.src.stage6.html.txt'), 'w', encoding='utf-8').write(s)
    print('page.src.html: stage 6,', len(s), 'characters')
if __name__ == '__main__':
    main()
