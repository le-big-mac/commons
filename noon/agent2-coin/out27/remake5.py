"""Fifth stage of the coin page's remake, after the reader's third visit (reader/visit-3.md).   python -I remake5.py
(run after remake4.py: it changes page.src.html in place)"""
H = '/home/agent2/coin/'
if __name__ == '__main__':
    s = open(H + 'page.src.html', encoding='utf8').read()
    def rep(a, b, count=1):
        global s
        assert s.count(a) == count, (a[:100], s.count(a)); s = s.replace(a, b)
    # the box for the range holds the largest amount (a visitor, twice: "Amounts from 0 to one less than" took a second reading; and its long label pushed the button, and so the rings, down at 360 wide)
    rep('<label>Amounts from 0 to one less than <input type="number" id="L" min="2" max="1000" step="1"></label>', '<label>Amounts from 0 to <input type="number" id="L" min="1" max="999" step="1"></label>')
    rep("""    if (!/^\\d+$/.test(String(text).trim())) return { error: 'The number of amounts must be a whole number from 2 to ' + MAXL + '.' };
    var v = Number(text);
    if (v < 2 || v > MAXL) return { error: 'The number of amounts must be from 2 to ' + MAXL + ': ' + v + ' is not.' };
    return { L: v };""", """    if (!/^\\d+$/.test(String(text).trim())) return { error: 'The largest amount must be a whole number from 1 to ' + (MAXL - 1) + '.' };
    var v = Number(text);
    if (v < 1 || v > MAXL - 1) return { error: 'The largest amount must be from 1 to ' + (MAXL - 1) + ': ' + v + ' is not.' };
    return { L: v + 1 };                                    /* L is the number of amounts, 0 to v */""")
    rep("    $('coins').value = coins.join(', '); $('L').value = L;", "    $('coins').value = coins.join(', '); $('L').value = L - 1;")
    rep("(S.L === 100 ? '' : ' for amounts below ' + S.L) + '.'; }", "(S.L === 100 ? '' : ' for the amounts from 0 to ' + (S.L - 1)) + '.'; }")
    # the sentence after the swap, in the reader's order
    rep("""'These are the American coins with the 10 swapped for an 18: 3.89 on average where American coins take 4.7, if the coins are well chosen every time; a cashier, who takes the largest coin that fits, needs 4.58 with these. '""",
        """'These are the American coins with the 10 swapped for an 18. They take 3.89 on average if the coins are well chosen every time (American coins take 4.7); a cashier, who takes the largest coin that fits, needs 4.58 with these. '""")
    # "paid exactly" beside "the cashier's way": the cashier pays exactly too
    rep("""    out.push(fin(p) ? 'paid exactly <b>' + p + '</b>' + (a > 0 ? ' (' + esc(wayText(P.plainWay(S.coins, a))) + ')' : '') : 'paid exactly: cannot be made');""",
        """    out.push(fin(p) ? 'paid exactly' + (fin(g) && g > p ? ', at best' : '') + ' <b>' + p + '</b>' + (a > 0 ? ' (' + esc(wayText(P.plainWay(S.coins, a))) + ')' : '') : 'paid exactly: cannot be made');""")
    rep("<th>amount</th><th>paid exactly</th><th>the cashier\\'s way</th><th>with change</th>", "<th>amount</th><th>paid exactly, at best</th><th>the cashier\\'s way</th><th>with change</th>")
    # the rings say it too when change saves nothing
    rep("""<p class="k">With change: <b>' + plural(b, 'coin') + '</b> ' + (b === 1 ? 'changes' : 'change') + ' hands' +""", """<p class="k">With change: <b>' + plural(b, 'coin') + '</b> ' + (b === 1 ? 'changes' : 'change') + ' hands' + (fin(p) && b === p ? ', no fewer than paying exactly' : '') +""")
    rep("""Press a set to try it at the top of the page. The last column is what a count shows: no set of that many coins can get under that figure, and the best sets often do not reach it.</figcaption>""",
        """Press a set to try it at the top of the page. The last column is a floor that comes from counting: with so many kinds of coin there are only so many different handfuls of one coin, of two coins, and so on, so only so many amounts can be paid with few. No set of that many coins can get under it, and the best sets often do not reach it.</figcaption>""")
    # the slider stands beside the amount, and the headings sit closer on a phone, so that the first rings are on the first screen at 360 by 640
    rep("  input[type=range] { max-width: 100%; }\n", "  input[type=range] { max-width: 100%; }\n  #fig3 .controls label:nth-child(2) { flex: 1 1 140px; } #fig3 input[type=range] { width: 100%; }\n  @media (max-width: 520px) { h2 { margin-top: 16px; } main { padding-top: 12px; } }\n")
    open(H + 'page.src.html', 'w', encoding='utf8').write(s); print('page.src.html, fifth stage:', len(s))
