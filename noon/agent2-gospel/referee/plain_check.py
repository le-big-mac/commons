"""Referee: are the FACTS in the page's reason sentence true?  The facts are rebuilt from core.js's forecast as `why` uses them;
truth is from my own orders (doubling, written here) and the blind step's rule.  Output: plain-check.out"""
import json, sys, math
sys.path.insert(0, '/home/agent2/gospel/referee')
import brute

def order(m):
    n, x = 1, 2 % m
    while x != 1:
        x = x * 2 % m; n += 1
    return n
def val(o, l):
    k = 0
    while o % l == 0: o //= l; k += 1
    return k
def factor(m):
    f = {}; l = 3
    while l * l <= m:
        while m % l == 0: m //= l; f[l] = f.get(l, 0) + 1
        l += 2
    if m > 1: f[m] = f.get(m, 0) + 1
    return f
def closes(m):            # Fuchs, to the letter: orders mod prime powers; strike what each shares with the lcm of the others
    f = factor(m); lam = {l: order(l ** e) for l, e in f.items()}
    for l in f:
        L = 1
        for r in f:
            if r != l: L = L * lam[r] // math.gcd(L, lam[r])
        if (lam[l] // math.gcd(lam[l], L)) % l == 0: return True
    return False

if __name__ == '__main__':
    out = open('/home/agent2/gospel/referee/plain-check.out', 'w')
    D = json.load(open('/home/agent2/gospel/referee/plain_dump.json'))
    bad = []; nfacts = 0; kinds = {'helps': 0, 'no square': 0, 'one undone': 0, 'several undone': 0, 'self': 0, 'test above l': 0}
    sums = 0
    for d in D:
        m = d['m']; f = factor(m); truth = closes(m)
        if m <= 3001:
            s = brute.cycle_sum(1, m)[2]; sums += 1
            if (s < 1e-9) != truth: bad.append((m, 'my rule against the sum'))
        if [[l, e] for l, e in sorted(f.items())] != d['factors']: bad.append((m, 'factors'))
        if d['bounded'] != truth: bad.append((m, 'bounded'))
        if d['round'] != order(m): bad.append((m, 'round'))
        nfacts += 3
        if d['bounded']:
            sv = d['serves']; l, e, k = sv['l'], sv['e'], sv['k']; kinds['helps'] += 1
            if f.get(l) != e: bad.append((m, 'contains l e times'))
            if k != val(order(l ** e), l) or k < 1: bad.append((m, 'test number'))
            if k > 1: kinds['test above l'] += 1
            for r in f:
                if r != l:
                    nfacts += 1
                    if order(r) % (l ** k) == 0: bad.append((m, 'said not to undo, and does', r))
        elif not d['squares']:
            kinds['no square'] += 1
            if any(e >= 2 for e in f.values()): bad.append((m, 'no prime more than once'))
        else:
            sp = d['spoilt']; kinds['one undone' if len(sp) == 1 else 'several undone'] += 1
            if sorted(b['l'] for b in sp) != sorted(l for l, e in f.items() if e >= 2): bad.append((m, 'not every repeated prime accounted for'))
            for b in sp:
                l, e = b['l'], b['e']; nfacts += 1
                if f.get(l) != e: bad.append((m, 'contains l e times'))
                if b.get('self'):
                    kinds['self'] += 1
                    if order(l ** e) != order(l ** (e - 1)): bad.append((m, 'no longer than: false'))
                else:
                    r, o, k = b['r'], b['ord'], b['k']
                    if k > 1: kinds['test above l'] += 1
                    if r not in f or r == l or order(r) != o or k != val(order(l ** e), l) or k < 1 or o % (l ** k) != 0: bad.append((m, 'undoes: false', r))
    print('%d denominators (%d of them above 3001); %d facts checked; false: %d %s' % (len(D), sum(1 for d in D if d['m'] > 3001), nfacts, len(bad), bad[:10]), file=out)
    print('kinds:', kinds, file=out)
    print('my reading of Fuchs to the letter against the round added up, odd m to 3001: %d compared' % sums, file=out)
    n, tl, s = None, None, None
    t = brute.cycle_sum(1635, 1009681)
    print('1635/1009681: factors %s; tail %d, round %d, |sum| %.4e; closes by the rule: %s' % (factor(1009681), t[0], t[1], t[2], closes(1009681)), file=out)
    out.close()
    print(open('/home/agent2/gospel/referee/plain-check.out').read())
