"""algebra2.py with a sixth move, the balanced lift (the method balanced_entries below); everything else is as there.
usage: algebra3.py  (prints the comparison with the five-move bound of status.json and writes U6-M.json)

The text of algebra2.py:
The calculus of algebra.py with two more moves, and with the SET of sizes kept for every pattern of every proper quotient group.

On Z_N (N a divisor of M) a state is (pattern P on the divisors > 1 of N, size s).  Moves:
  atom       a coset of cZ_N' (c | N' | N), lifted in general position: ({d | N' : d does not divide c}, N'/c)
  lift       a multiset on Z_N' (N' | N) lifted in general position: same pattern, same size
  (x)        convolution: (P1 ∪ P2, s1 s2)
  (+)        sum of translates: (P1 ∩ P2, s1 + s2)
  (L)        reduce modulo N' | N and lift: (P ∩ div N', s)
  dilation   for c | N, K = N/c, a multiset B on Z_K: the multiset cB on Z_N has pattern {d | N : d/gcd(d, c) in pattern(B)}, same size
  stacking   for c | N, c > 1, K = N/c: multisets B_r on Z_K, one for each r mod c, ALL OF THE SAME SIZE w, put in the classes r + cZ_N:
             pattern {d | c, d > 1} ∪ {d | N, d not dividing c : d/gcd(d, c) in every pattern(B_r)}, size c w
             (the B_r may have different patterns; only their intersection counts; at most c different ones can be used)
For N < M all sizes up to 2N are kept; for N = M only the least cost.  U2(D) = the least cost on Z_M.  Every derivation is recorded,
so that realise2.py can build the multiset.   usage: algebra2.py  (prints the comparison with the tables)"""
import sys, json, itertools, math
from functools import lru_cache

def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]

class Calc:
    def __init__(self, p, q):
        self.p, self.q = p, q; self.M = p * p * q * q
        self.S = {}      # N -> {pattern (frozenset of divisors) -> {size: derivation}}
        for N in divisors(self.M):
            if N < self.M: self.S[N] = self.full(N)
        self.U, self.how = self.top()

    def atoms(self, N):
        out = []
        for N1 in divisors(N):
            for c in divisors(N1):
                if c != N1 or N1 == 1:
                    out.append((frozenset(d for d in divisors(N1) if d > 1 and c % d != 0), N1 // c, ('atom', N1, c)))
        return out

    def stack_entries(self, N):
        """all (pattern, size, derivation) from dilation and stacking into Z_N, from the size sets of the quotient groups"""
        out = []
        for c in divisors(N):
            if c == 1: continue
            K = N // c; SK = self.S[K]
            def up(T): return frozenset(d for d in divisors(N) if d > 1 and (d // math.gcd(d, c)) in T)
            for T, sizes in SK.items():
                for w in sizes: out.append((up(T), w, ('dil', c, K, T, w)))
            cap = 2 * N // c
            bysize = {}
            for P, sizes in SK.items():
                for w in sizes:
                    if w <= cap: bysize.setdefault(w, []).append(P)
            base = frozenset(d for d in divisors(c) if d > 1)
            for w, fam in bysize.items():
                # intersections reachable with j <= c members; remember one family for each
                reach = {P: (P,) for P in fam}
                frontier = dict(reach)
                for j in range(2, c + 1):
                    new = {}
                    for I, membs in frontier.items():
                        for P in fam:
                            J = I & P
                            if J not in reach and J not in new: new[J] = membs + (P,)
                    if not new: break
                    reach.update(new); frontier = new
                for T, membs in reach.items():
                    out.append((base | up(T), c * w, ('stack', c, K, membs, w)))
        return out

    def balanced_entries(self, N):
        """balanced lift: for a prime r with r^j exactly dividing N, j >= 2, and K = N/r: a multiset B on Z_K whose pattern holds r, r^2, ..., r^(j-1)
        and whose size is divisible by r^j is lifted to Z_N so that each class modulo r^(j-1) is spread evenly over its r lifts modulo r^j:
        the pattern keeps what it had on the divisors of K and gains r^j; same size.  The program supposes that nothing else comes in, which is
        false for some inputs (the note, section 2): a cost found with this move counts only if realise3.py has built the multiset."""
        out = []
        for r in (self.p, self.q):
            j = 0
            while N % r ** (j + 1) == 0: j += 1
            if j < 2: continue
            K = N // r; need = frozenset(r ** i for i in range(1, j))
            for P, sizes in self.S[K].items():
                if need <= P:
                    for s in sizes:
                        if s % r ** j == 0: out.append((P | {r ** j}, s, ('bal', r, j, K, P, s)))
        return out

    def full(self, N):
        cap = 2 * N; D = [d for d in divisors(N) if d > 1]
        S = {}
        def add(P, s, how):
            if s > cap: return False
            t = S.setdefault(P, {})
            if s in t: return False
            t[s] = how; return True
        for P, s, h in self.atoms(N): add(P, s, h)
        for N1 in divisors(N):
            if N1 < N:
                for P, sizes in self.S[N1].items():
                    for s in sizes: add(P, s, ('lift', N1, P, s))
        for P, s, h in self.stack_entries(N): add(P, s, h)
        for P, s, h in self.balanced_entries(N): add(P, s, h)
        low = [frozenset(d for d in divisors(N1) if d > 1) for N1 in divisors(N)]
        changed = True
        while changed:
            changed = False
            items = [(P, s) for P, t in S.items() for s in t]
            for P, s in items:
                for N1, lm in zip(divisors(N), low):
                    if add(P & lm, s, ('L', N1, P, s)): changed = True
            pats = list(S)
            for P1, P2 in itertools.combinations_with_replacement(pats, 2):
                s1s = sorted(S[P1]); s2s = sorted(S[P2])
                for s1 in s1s:
                    for s2 in s2s:
                        if s1 + s2 > cap: break
                        if add(P1 & P2, s1 + s2, ('+', P1, s1, P2, s2)): changed = True
                    for s2 in s2s:
                        if s1 * s2 > cap: break
                        if add(P1 | P2, s1 * s2, ('x', P1, s1, P2, s2)): changed = True
        return S

    def top(self):
        N = self.M; U = {}; how = {}
        def add(P, s, h):
            if s < U.get(P, float('inf')): U[P] = s; how[P] = h; return True
            return False
        for P, s, h in self.atoms(N): add(P, s, h)
        for N1 in divisors(N):
            if N1 < N:
                for P, sizes in self.S[N1].items(): add(P, min(sizes), ('lift', N1, P, min(sizes)))
        for P, s, h in self.stack_entries(N): add(P, s, h)
        for P, s, h in self.balanced_entries(N): add(P, s, h)
        low = [frozenset(d for d in divisors(N1) if d > 1) for N1 in divisors(N)]
        changed = True
        while changed:
            changed = False
            for P in list(U):
                for N1, lm in zip(divisors(N), low):
                    if add(P & lm, U[P], ('L', N1, P, U[P])): changed = True
            for P1, P2 in itertools.combinations_with_replacement(list(U), 2):
                if add(P1 | P2, U[P1] * U[P2], ('x', P1, U[P1], P2, U[P2])): changed = True
                if add(P1 & P2, U[P1] + U[P2], ('+', P1, U[P1], P2, U[P2])): changed = True
        return U, how

if __name__ == '__main__':
    sys.path.insert(0, '/home/agent3/pq2/rule')
    st = json.load(open('status.json'))
    for M, p, q in ((36, 2, 3), (100, 2, 5), (225, 3, 5)):
        C = Calc(p, q)
        rows = st[str(M)]['rows']; eq = lt = gt = 0; improved = []; bad = []; newly = []; kinds = {}
        for r in rows:
            D = frozenset(r['D']); u2 = C.U.get(D)
            assert u2 is not None and u2 <= r['U5'], (M, r['D'], u2, r['U5'])
            if u2 < r['U5']: improved.append((r['S'], r['LB'], r['least'], r['U5'], u2, C.how[D][0]))
            if r['least'] is not None:
                if u2 == r['least']: eq += 1
                elif u2 > r['least']: gt += 1
                else: lt += 1; bad.append((r['S'], r['least'], u2))
            elif u2 == r['LB']: newly.append((r['S'], u2))
        print(f'Z_{M}: the six-move cost = least for {eq} of the known; > least for {gt}; < least (a move is dishonest) for {lt}: {bad}')
        print(f'   six moves < five moves for {len(improved)} patterns (pattern, LB, least, five moves, six moves, last move): {improved}')
        print(f'   open patterns with U2 = LB (newly settled if the multiset is real): {newly}')
        json.dump({','.join(map(str, sorted(D))): C.U[D] for D in C.U}, open(f'U6-{M}.json', 'w'))
