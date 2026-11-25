"""The eclipse year model (EYM) of Freeth 2014 (PLoS ONE 9(7): e103275), as its main text gives it:
38 units to a lunar month, 446 to an eclipse year; the n-th full moon at 38(n-1)+17 and the n-th new moon at
38(n-1)+36 (mod 446) from the start of the eclipse year; node points at 66 (descending) and 289 (ascending);
a lunar glyph if the full moon is within 20 units of a node point; a solar glyph if the new moon is within 20
units when the Moon is north of the node, within 7 when south."""
DNP, ANP, YEAR = 66, 289, 446

def offset(p):
    """Signed distance from the nearer node point, and which one ('D' or 'A')."""
    best = None
    for node, name in ((DNP, 'D'), (ANP, 'A')):
        d = (p - node + YEAR // 2) % YEAR - YEAR // 2
        if best is None or abs(d) < abs(best[0]): best = (d, name)
    return best

def north(d, name):
    """Before the descending node the Moon is north of the ecliptic, after it south; the other way at the ascending."""
    return (d < 0) if name == 'D' else (d > 0)

def glyphs(months=223, lunar_limit=20, north_limit=20, south_limit=7):
    lunar, solar = {}, {}
    for n in range(1, months + 1):
        d, name = offset((38 * (n - 1) + 17) % YEAR)
        if abs(d) <= lunar_limit: lunar[n] = (d, name)
        d, name = offset((38 * (n - 1) + 36) % YEAR)
        lim = north_limit if (north(d, name) or d == 0) else south_limit
        if abs(d) <= lim: solar[n] = (d, name)
    return lunar, solar

if __name__ == '__main__':
    lunar, solar = glyphs()
    print('before any rule about consecutive months: lunar', len(lunar), 'solar', len(solar), 'months with a glyph', len(set(lunar) | set(solar)))
    cons = [n for n in lunar if n + 1 in lunar]
    print('lunar predictions in consecutive months:', [(n, lunar[n][0], n + 1, lunar[n + 1][0]) for n in cons])
    cons_s = [n for n in solar if n + 1 in solar]
    print('solar predictions in consecutive months:', [(n, solar[n][0], n + 1, solar[n + 1][0]) for n in cons_s])
    print('lunar months:', sorted(lunar))
    print('solar months:', sorted(solar))
    for n in (13, 137, 149):
        print('glyph', n, 'lunar' if n in lunar else '', lunar.get(n), 'solar' if n in solar else '', solar.get(n))
