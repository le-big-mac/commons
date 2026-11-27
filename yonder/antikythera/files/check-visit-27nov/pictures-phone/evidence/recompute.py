"""Independent recomputation of what the three phone pictures letter, from the data files. No plotting."""
import json, math, sys
today = json.load(open(sys.argv[1]))
print('dial of 23 November: pointer, sky, signed difference (pointer minus sky, folded to -180..180), absolute, lettering as I would write it')
for b in ['moon', 'mercury', 'venus', 'sun', 'mars', 'jupiter', 'saturn']:
    p, s = today[b]
    d = p - s
    while d > 180: d -= 360
    while d <= -180: d += 360
    a = abs(d)
    # rounding to a whole degree by hand, half up (not Python's formatting)
    whole = int(math.floor(a + 0.5))
    word = 'less than 1° apart' if a < 1 else f'{whole}° apart'
    print(f'  {b:8s} ptr {p:9.4f} sky {s:9.4f} diff {d:+9.4f} abs {a:8.4f} -> {word}   (mid-angle of the pair {s + d/2:8.3f}, ring radius {["moon","mercury","venus","sun","mars","jupiter","saturn"].index(b)+1.4})')
two = json.load(open(sys.argv[2]))
print('two_lists.json keys:', list(two.keys()))
rows = two['F']
print('rows in F:', len(rows), 'keys of a row:', sorted(rows[0].keys()))
print('first rows:', [(r['cycle'], r['A'], r['S']) for r in rows[:6]])
print('cycles consecutive from', rows[0]['cycle'], 'to', rows[-1]['cycle'], all(rows[i+1]['cycle'] - rows[i]['cycle'] == 1 for i in range(len(rows)-1)))
fa = [r['cycle'] for r in rows if r['A'] == 0]; fs = [r['cycle'] for r in rows if r['S'] == 0]
print('first cycle with A == 0:', fa[0], '-> years after 205 BC', fa[0]*18.03, '-> AD', fa[0]*18.03-204, '; any A > 0 after it?', any(r['A'] > 0 for r in rows if r['cycle'] > fa[0]))
print('first cycle with S == 0:', fs[0], '-> years after 205 BC', fs[0]*18.03, '-> AD', fs[0]*18.03-204, '; any S > 0 after it?', any(r['S'] > 0 for r in rows if r['cycle'] > fs[0]))
print('last cycle with A > 0:', max(r['cycle'] for r in rows if r['A'] > 0), ' last with S > 0:', max(r['cycle'] for r in rows if r['S'] > 0))
print('max A', max(r['A'] for r in rows), 'max S', max(r['S'] for r in rows))
print('last cycle', rows[-1]['cycle'], '-> years', rows[-1]['cycle']*18.03, '-> AD', rows[-1]['cycle']*18.03-204)
print('A by cycle:', [r['A'] for r in rows])
print('S by cycle:', [r['S'] for r in rows])
# is A or S ever increasing?
print('A ever rises:', any(rows[i+1]['A'] > rows[i]['A'] for i in range(len(rows)-1)), ' S ever rises:', any(rows[i+1]['S'] > rows[i]['S'] for i in range(len(rows)-1)))
print('scale: AD Y at Y+204:')
for y, lab in [(None, '205 BC'), (250, 'AD 250'), (500, '500'), (750, '750'), (1000, '1000'), (1250, '1250')]:
    if y is None:
        # 205 BC is astronomical year -204; AD Y is year Y; so Y - (-204) = Y + 204 years after 205 BC
        print('  205 BC = astronomical year -204, placed at 0')
    else:
        print(f'  AD {y}: {y} - (-204) = {y + 204} years after 205 BC')
