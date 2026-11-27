"""Evidence reading: the date in "In short" (about AD 1058) by each of the lists in two_lists.json.
usage: python ev5_lists.py RECORDS_DIR ; prints, writes nothing."""
import json, os, sys
R = sys.argv[1]
two = json.load(open(os.path.join(R, 'dial', 'two_lists.json')))
sys.path.insert(0, os.path.join(R, 'dial'))
for name in ('F', 'IJ', 'read'):
    rows = two[name]
    last_any = max(r['cycle'] for r in rows if r['A'] > 0 or r['S'] > 0)
    lastA = max(r['cycle'] for r in rows if r['A'] > 0); lastS = max(r['cycle'] for r in rows if r['S'] > 0)
    print(f'{name:5s}: last cycle with a marked lunar month holding an eclipse: {lastA} (none from {lastA + 1}: {round((lastA + 1) * 18.03)} years on, AD {round((lastA + 1) * 18.03) - 204}); '
          f'solar: {lastS} (none from {lastS + 1}: {round((lastS + 1) * 18.03)} years on, AD {round((lastS + 1) * 18.03) - 204}); S in cycles 69 to 73: {[r["S"] for r in rows[69:74]]}')
