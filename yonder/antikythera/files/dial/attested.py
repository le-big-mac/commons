"""The glyphs that survive on the fragments (Carman & Evans 2014: 14 lunar and 11 solar month cells), against
the model's months and against the sky of the first four cycles. After the sealed sheet. usage: attested.py DATADIR"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import dial, mech
LUNAR = [20, 26, 61, 67, 79, 114, 120, 125, 131, 137, 172, 178, 184, 190]
SOLAR = [13, 25, 72, 78, 119, 125, 131, 137, 172, 178, 184]
lunar, solar = dial.glyph_months()
print('surviving lunar months all among the model\'s 38:', all(n in lunar for n in LUNAR), '; surviving solar months all among its 28:', all(n in solar for n in SOLAR))
DATA = sys.argv[1]
sz = dial.syzygies(mech.read(os.path.join(DATA, 'moon_then.txt')), mech.read(os.path.join(DATA, 'sun_then.txt')))
FM, NM = dial.number(sz)
for j in range(4):
    lat_l = [FM[223 * j + n] for n in LUNAR]; lat_s = [NM[223 * j + n] for n in SOLAR]
    print(f'cycle {j}: surviving lunar months with the full moon within 1.43 deg: {sum(abs(b) <= dial.LIM_N for b in lat_l)} of 14 (within 1.0: {sum(abs(b) < 1.0 for b in lat_l)}; largest {max(abs(b) for b in lat_l):.2f}); '
          f'surviving solar months with the new moon between -0.51 and +1.43: {sum(-dial.LIM_S <= b <= dial.LIM_N for b in lat_s)} of 11 (lowest {min(lat_s):+.2f}, highest {max(lat_s):+.2f})')
