"""The eclipse possibilities of the Saros dial as Iversen and Jones (2019), Table 5, resolve them: 49 cells.
Typed from the table (Arch. Hist. Exact Sci. 73, 469-511, pp. 505-506). ATTESTED are the entries the table gives
without brackets, the ones read on the fragments; the rest are deduced. Cell 196's solar entry is their "[Yes?]"."""
TABLE5 = """
2 [Y] [N]
8 Y Y
13 N Y
14 [Y] [N]
20 Y N
25 N Y
26 Y N
31 [N] [Y]
32 [Y] [N]
37 [Y] [Y]
43 [Y] [Y]
49 [Y] [N]
55 [Y] [Y]
60 [N] [Y]
61 Y [N]
67 Y N
72 N Y
73 [Y] [N]
78 N Y
79 Y N
84 [Y] [Y]
90 [Y] [Y]
96 [Y] [N]
102 [Y] [Y]
107 [N] [Y]
108 [Y] [N]
114 Y [N]
119 N Y
120 Y N
125 Y Y
131 Y Y
137 Y Y
143 [Y] [N]
149 [Y] [Y]
154 [N] [Y]
155 [Y] [N]
161 [Y] [N]
166 [N] [Y]
167 [Y] [N]
172 Y Y
178 Y Y
184 Y Y
190 Y N
196 [Y] [Y]
201 [N] [Y]
202 [Y] [N]
208 [Y] [N]
213 [Y] [Y]
219 [Y] [Y]
"""
ROWS = [l.split() for l in TABLE5.strip().split('\n')]
CELLS = [int(r[0]) for r in ROWS]
LUNAR = [int(r[0]) for r in ROWS if 'Y' in r[1]]
SOLAR = [int(r[0]) for r in ROWS if 'Y' in r[2]]
LUNAR_ATTESTED = [int(r[0]) for r in ROWS if r[1] == 'Y']
SOLAR_ATTESTED = [int(r[0]) for r in ROWS if r[2] == 'Y']
assert len(CELLS) == 49 and len(LUNAR) == 38 and len(SOLAR) == 28, (len(CELLS), len(LUNAR), len(SOLAR))

if __name__ == '__main__':
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import dial
    fl, fs = dial.glyph_months(); fl, fs = sorted(fl), sorted(fs)
    print(f'Iversen and Jones 2019, Table 5: {len(CELLS)} cells, {len(LUNAR)} lunar, {len(SOLAR)} solar; read on the fragments: {len(LUNAR_ATTESTED)} lunar, {len(SOLAR_ATTESTED)} solar, in {len(set(LUNAR_ATTESTED) | set(SOLAR_ATTESTED))} cells')
    print(f'Freeth 2014 as coded: {len(set(fl) | set(fs))} cells, {len(fl)} lunar, {len(fs)} solar')
    print('lunar in Freeth only:', sorted(set(fl) - set(LUNAR)), '; in Iversen and Jones only:', sorted(set(LUNAR) - set(fl)))
    print('solar in Freeth only:', sorted(set(fs) - set(SOLAR)), '; in Iversen and Jones only:', sorted(set(SOLAR) - set(fs)))
    print('lunar read on the fragments:', LUNAR_ATTESTED)
    print('solar read on the fragments:', SOLAR_ATTESTED)
    print('read on the fragments but not in Freeth 2014 as coded: lunar', sorted(set(LUNAR_ATTESTED) - set(fl)), 'solar', sorted(set(SOLAR_ATTESTED) - set(fs)))
    no_l = [int(r[0]) for r in ROWS if r[1] == 'N']; no_s = [int(r[0]) for r in ROWS if r[2] == 'N']
    print('read as having no lunar glyph but lunar in Freeth 2014 as coded:', sorted(set(no_l) & set(fl)), '; no solar glyph but solar in Freeth:', sorted(set(no_s) & set(fs)))
