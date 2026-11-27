# totals of the tN_*.out files
import re, glob
tot = dict(multisets=0, withbad=0, split=0, diffa=0, free=0, triples=0, special=0, two=0, twomixed=0, one=0, attained=0)
es = {}
files = sorted(glob.glob(__file__.rsplit('/', 1)[0] + '/tN_*.out'))
ok = 0
for f in files:
    s = open(f).read()
    if '\nOK\n' not in s or 'exit 0' not in s:
        print("NOT FINISHED:", f); continue
    ok += 1
    m = re.search(r'multisets (\d+); pairs \(multiset, e\) (\d+), with a bad signing at some 2\^j e: (\d+) \(e with several primes above 2: (\d+); with different a_p: (\d+)\)', s)
    tot['multisets'] += int(m.group(1)); tot['withbad'] += int(m.group(3)); tot['split'] += int(m.group(4)); tot['diffa'] += int(m.group(5))
    m = re.search(r'Lemma N \(i\): (\d+) free levels.*?\(ii\): (\d+) \(bad signing, level, prime\).*?, (\d+) of them c', s)
    tot['free'] += int(m.group(1)); tot['triples'] += int(m.group(2)); tot['special'] += int(m.group(3))
    m = re.search(r'two values (\d+) times.*?; (\d+) of them with different a_p\), one value (\d+) times.*?attained (\d+) times', s)
    tot['two'] += int(m.group(1)); tot['twomixed'] += int(m.group(2)); tot['one'] += int(m.group(3)); tot['attained'] += int(m.group(4))
    m = re.search(r'e with bad signings: (\{.*\})', s)
    for e, c in eval(m.group(1)).items():
        es[e] = es.get(e, 0) + c
print(ok, "files finished of", len(files))
print(tot)
print("pairs (multiset, e) with a bad signing, by e:", dict(sorted(es.items())))
