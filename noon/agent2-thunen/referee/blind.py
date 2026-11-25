# Blind recomputation from the formulas in Thuenen, Der isolierte Staat (1910 Jena reprint).
import math

# (a) worth of a Scheffel of rye x miles out, town price a (section 4; explanation of plate III)
def b_exact(x, a=1.5):
    return ((12000 - 150 * x) * a - 136.92 * x) / (12000 + 65.88 * x)
def b_short4(x):                      # section 4's short form, a = 1.5 only
    return (273 - 5.5 * x) / (182 + x)
def b_short(x, a):                    # plate III's short form
    return ((182 - 2.3 * x) * a - 2.1 * x) / (182 + x)
def x_exact(b, a=1.5):
    return 12000 * (a - b) / (150 * a + 136.92 + 65.88 * b)
def x_short4(b):
    return (273 - 182 * b) / (5.5 + b)
def x_short(b, a=1.5):
    return 182 * (a - b) / (2.3 * a + b + 2.1)

# (b) land rent on 100,000 square rods, k = Koerner in Koppelwirtschaft terms, p = worth of rye on the farm
def rent_kw(k, p):  return (271 * k - 1000) * p - (53 * k + 217)      # 1710-271x Schfl - (747-53x) Tlr, x = 10-k
def rent_dfw(k, p): return (152 * k - 520) * p - (27 * k + 111)       # 1000-152x Schfl - (381-27x) Tlr
def p_switch(k): return (26 * k + 106) / (119 * k - 480)              # KW rent = DFW rent
def p_zero(k):   return (27 * k + 111) / (152 * k - 520)              # DFW rent = 0
def p_zero_kw(k): return (53 * k + 217) / (271 * k - 1000)

print('2a. worth of 1000 Schfl rye (Taler)')
book = {0: 1500, 5: 1313, 10: 1136, 15: 968, 20: 809, 25: 656, 30: 512, 35: 374, 40: 242, 45: 116}
print(' miles  exact  short   book  exact-book short-book')
for x in range(0, 50, 5):
    e = 1000 * b_exact(x); s = 1000 * b_short4(x)
    print(f' {x:5d} {e:6.1f} {s:6.1f} {book[x]:6d} {e - book[x]:9.1f} {s - book[x]:9.1f}')
print(f' zero worth at: exact {18000 / 361.92:.2f}, short {273 / 5.5:.2f}, book 49.95')
print(' checks: book 1.313 at 5 mi, 1.136 at 10 mi; 0.516 Tlr at 29.9 mi -> exact x=%.2f short x=%.2f; 0.381 at 34.7 -> %.2f / %.2f'
      % (x_exact(0.516), x_short4(0.516), x_exact(0.381), x_short4(0.381)))
print(' rent check sec.5: 8 Koerner rent 1168 Schfl - 641 Tlr ->', 271 * 8 - 1000, 53 * 8 + 217,
      '; zero at x: exact %.2f short %.2f (book 28.6)' % (x_exact(641 / 1168), x_short4(641 / 1168)))

print('\n2b. three-field ring: begins / ends (miles), town price 1.5')
bookb = {10: (29.9, 34.7, 4.8), 9: (27.8, 33.3, 5.5), 8: (24.7, 31.5, 6.8), 7: (19.8, 28.6, 8.8),
         6: (10.5, 23.6, 13.1), 5.4: (0, 18.6, 18.6)}
print('  K   p_switch p_zero | exact: begin  end width | short: begin  end | book: begin end width')
for k in (10, 9, 8, 7, 6, 5.4):
    ps, pz = p_switch(k), p_zero(k)
    be, ee = max(0, x_exact(ps)), x_exact(pz)
    bs, es = max(0, x_short4(ps)), x_short4(pz)
    bb = bookb[k]
    print(f' {k:4} {ps:8.4f} {pz:6.4f} | {be:11.2f} {ee:5.2f} {ee - be:5.2f} | {bs:11.2f} {es:5.2f} | {bb[0]:5} {bb[1]:5} {bb[2]:5}'
          f'   diff exact {be - bb[0]:+.2f} {ee - bb[1]:+.2f}')
print('  raw x at 5.4 Koerner begin: exact %.3f' % x_exact(p_switch(5.4)))
print('  KW=DFW at town price 1.5 exactly when K = %.3f (book: 5.42);  DFW rent 0 at 1.5 when K = %.3f (book: 10-5.57=4.43)'
      % ((480 * 1.5 + 106) / (119 * 1.5 - 26), (520 * 1.5 + 111) / (152 * 1.5 - 27)))

print('\n2c. radius of the cultivated plain, 10 Koerner, by town price')
bookc = {1.50: '34.7', 1.35: '31.7?', 1.20: '28.6', 1.05: '25.0?', 0.90: '20.0?', 0.75: '16.1', 0.60: '10.1? (text: 10.4)'}
area = {1.35: 844, 1.20: 687, 1.05: 525, 0.90: 367, 0.75: 217}
print(' price exact(b=.381) exact(b=.38) short(b=.38) short(b=.381) | book (machine reading) | radius implied by book area')
for a in (1.50, 1.35, 1.20, 1.05, 0.90, 0.75, 0.60):
    imp = '' if a not in area else '%.2f' % (34.7 * math.sqrt(area[a] / 1000))
    print(f' {a:4.2f} {x_exact(.381, a):10.2f} {x_exact(.38, a):12.2f} {x_short(.38, a):12.2f} {x_short(.381, a):12.2f} | {bookc[a]:20s} | {imp}')
print(' KW/DFW boundary on plate III (b=0.51), and widths:')
for a in (1.50, 1.05, 0.60):
    print(f'  a={a:.2f}: exact KW end {x_exact(.51, a):.2f} DFW width {x_exact(.38, a) - x_exact(.51, a):.2f};'
          f' short KW end {x_short(.51, a):.2f} DFW width {x_short(.38, a) - x_short(.51, a):.2f}')
print('  book: DFW width 4.5 / 5.4 / 6.2; KW+FWW 21.4 / 13.4 / 1.6 -> forest outer = plain - both =',
      [round(v, 1) for v in (34.7 - 4.5 - 21.4, 25.0 - 5.4 - 13.4, 10.4 - 6.2 - 1.6)])

print('\n2d. radius of the cultivated plain at 1.5 Tlr, by yield')
bookd = {10: '34.7', 9: '33.3', 8: '31.5', 7: '28.6', 6: '23.6', 5: '13.3', 4: '0? (digit unreadable)'}
for k in (10, 9, 8, 7, 6, 5, 4):
    pz = p_zero(k) if 152 * k - 520 > 0 else float('inf')
    xe = x_exact(pz) if pz < 1.5 else 0.0
    xs = x_short4(pz) if pz < 1.5 else 0.0
    print(f' {k:3d} Koerner: p_zero {pz:6.3f}  exact {xe:5.2f}  short {xs:5.2f}  book {bookd[k]}')

print('\n3. water, ship mile = 0.1 cart mile')
k = 0.1
def best(f, lo, hi):
    n = 200000
    return min((f(lo + (hi - lo) * i / n), lo + (hi - lo) * i / n) for i in range(n + 1))
c1, s1 = best(lambda s: math.hypot(5, s) + k * (100 - s), 0, 100)
c2, s2 = best(lambda s: k * (70 - s) + math.hypot(6, s), 0, 70)
print(f' (i) farm 5 mi off the river, its foot 100 mi from the town: least {c1:.4f} (reach the river {s1:.3f} mi townward of the foot);'
      f' closed form {5 * math.sqrt(1 - k * k) + 100 * k:.4f}; straight to river then ship = 15; all by cart {math.hypot(100, 5):.2f}; book: 15')
print(f' (ii) farm on river 70 mi from the nearest point, town 6 mi off: least {c2:.4f} (land {s2:.3f} mi before the nearest point);'
      f' closed form {6 * math.sqrt(1 - k * k) + 70 * k:.4f}; ship to nearest point then cart = 13; all by cart {math.hypot(70, 6):.2f}')

print('\n2c note. which constants reproduce the printed radii? (b = 0.38)')
printed = {1.50: 34.7, 1.35: 31.7, 1.20: 28.6, 1.05: 25.0, 0.90: 20.9, 0.75: 16.1, 0.60: 10.4}
for c in (2.1, 2.08):
    row = [182 * (a - .38) / (2.3 * a + .38 + c) for a in printed]
    print(f' x = 182(a-b)/(2.3a+b+{c}):', ' '.join(f'{v:.2f}' for v in row))
print(' printed (20.9 and 10.4 are my reading of "20,0" and "10,1"):', ' '.join(str(v) for v in printed.values()))
print(' areas from printed radii (1.5 = 1000):', [round(1000 * (printed[a] / 34.7) ** 2) for a in (1.35, 1.20, 1.05, 0.90, 0.75)],
      ' book areas: [844, 687, 525, 367, 217]')
print(' areas from exact radii (b=.381):', [round(1000 * (x_exact(.381, a) / x_exact(.381, 1.5)) ** 2) for a in (1.35, 1.20, 1.05, 0.90, 0.75)])
