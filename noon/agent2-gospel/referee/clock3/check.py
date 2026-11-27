"""Referee, third clock check: every made sentence of 1(a)-(d) against my own arithmetic and my own walk.  Output: check.out"""
import json, math, re
from decimal import Decimal, ROUND_HALF_UP
import numpy as np

def commas(n): return format(n, ',')
def order(m):
    if m == 1: return 1
    n, x = 1, 2 % m
    while x != 1: x = x * 2 % m; n += 1
    return n
def factor(n):
    f = {}; d = 2
    while d * d <= n:
        while n % d == 0: n //= d; f[d] = f.get(d, 0) + 1
        d += 1 if d == 2 else 2
    if n > 1: f[n] = f.get(n, 0) + 1
    return f
def walk_gain(p, q, s, n):
    """GOSPEL walked: turn, then step; how far the turtle is, after one round, from where its tail ended."""
    turn = p % q; head = 0; H = np.empty(n, dtype=np.int64)
    for j in range(s + n):
        head = (head + turn) % q; turn = turn * 2 % q
        if j >= s: H[j - s] = head
    a = H * (2 * math.pi / q)
    return math.hypot(math.fsum(np.cos(a).tolist()), math.fsum(np.sin(a).tolist()))
def fixed3(x): return str(Decimal(x).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
def prec3(x):
    d = Decimal(x); e = d.adjusted(); return str(d.quantize(Decimal(1).scaleb(e - 2), rounding=ROUND_HALF_UP))
def dist_words(g): return (prec3(g * 1e6) + ' millionths of a step') if g < 0.0005 else (fixed3(g) + ' steps')
WORD = {3: 'three', 5: 'five', 7: 'seven'}
def tw(l): return WORD.get(l, commas(l))

if __name__ == '__main__':
    D = json.load(open('/home/agent2/gospel/referee/clock3/page.json')); out = open('/home/agent2/gospel/referee/clock3/check.out', 'w')
    bad = []; unparsed = []; cnt = dict(turtles=0, even=0, p_not_1=0, above_999=0, home=0, loop=0, away=0, straight=0, f_long=0, f_nomore=0, f_two=0, f_none=0, three_way=0, two_way=0, walked=0, round_said=0, idle_said=0)
    least_gap = 9.0
    for r in D:
        if not r['valid']: continue
        P, Q = r['p'], r['q']; g0 = math.gcd(abs(P), Q); q = Q // g0; p = (P // g0) % q
        s = 0; m = q
        while m % 2 == 0: m //= 2; s += 1
        n = order(m); f = factor(m); say, reason, clock, report = r['say'], r['reason'] or '', r['clock'] or '', r['report']
        cnt['turtles'] += 1; cnt['even'] += q % 2 == 0; cnt['p_not_1'] += p != 1; cnt['above_999'] += q > 999
        if m == 1:
            cnt['straight'] += 1
            if 'walks straight on for ever' not in say or 'never comes home' not in say: bad.append((p, q, 'straight', say[:80]))
            continue
        gain = walk_gain(p, q, s, n); closes = gain < 1e-9
        if not closes: least_gap = min(least_gap, gain)
        # the forecast's first words
        if closes and s == 0:
            cnt['home'] += 1
            if 'it comes home after ' + commas(n) + ' steps' not in say: bad.append((p, q, 'home after n', say[:90]))
        elif closes:
            cnt['loop'] += 1
            if 'never comes home, and never gets away' not in say or 'goes round one loop for ever' not in say: bad.append((p, q, 'loop', say[:90]))
        else:
            cnt['away'] += 1
            if 'it never comes home.' not in say or 'never gets away' in say: bad.append((p, q, 'away', say[:90]))
        # (d) the length of the round, as said
        ms = re.findall(r'(?:Those ([\d,]+) steps are one round|after ([\d,]+) steps: one round|every ([\d,]+) steps)', say)
        said = {x for t in ms for x in t if x}
        if said:
            cnt['round_said'] += 1
            if said != {commas(n)}: bad.append((p, q, 'round length said', sorted(said), n))
        else: unparsed.append((p, q, 'no round length in say', say[:120]))
        # (b), (c) and the report: the distance, digit for digit
        mine = dist_words(gain) if not closes else None
        fm = re.search(r'each one carries the turtle ([\d.,]+ (?:steps|millionths of a step)) further along a straight line', say)
        cm = re.search(r'leaves the turtle ([\d,]+) times that, ([\d.,]+ steps), further on', clock) or re.search(r'a round carries the turtle()\s*([\d.]+ millionths of a step)', clock)
        if closes:
            if fm or cm: bad.append((p, q, 'a distance printed for a round that closes'))
        else:
            F = fm.group(1) if fm else None; C = cm.group(2) if cm else None
            if F != mine or C != mine: bad.append((p, q, 'distance', 'forecast', F, 'clock', C, 'my walk', mine)); 
            else: cnt['two_way'] += 1
            om = re.search(r'balance point, ([\d.]+) of the way from the centre to the rim\. Each round of ([\d,]+) steps? leaves the turtle ([\d,]+) times that', clock)
            if om:
                if om.group(2) != commas(n) or om.group(3) != commas(n): bad.append((p, q, 'n in the caption'))
                if fixed3(n * float(om.group(1))) + ' steps' != C: bad.append((p, q, 'n times the printed balance point is not the printed distance', om.group(1), C))
                if abs(float(om.group(1)) - gain / n) > 0.6 * 10 ** -(len(om.group(1)) - 2): bad.append((p, q, 'balance point', om.group(1), gain / n))
            elif 'millionths' not in clock: unparsed.append((p, q, 'caption', clock[:160]))
            if report is not None:
                cnt['walked'] += 1
                rm = re.search(r'has carried it ([\d.,]+ (?:steps|millionths of a step)) further', report)
                if not rm: unparsed.append((p, q, 'report', report[:140]))
                elif rm.group(1) != mine: bad.append((p, q, 'report distance', rm.group(1), mine))
                else: cnt['three_way'] += 1
        if report is not None and closes:
            cnt['walked'] += 1
            ok = ('home.' in report and s == 0) or ('back where it stood at step ' + commas(s) in report and s > 0) or 'Stopped at step' in report
            if not ok: bad.append((p, q, 'report of a closed round', report[:100]))
        if r.get('fails'): bad.append((p, q, 'the page records a failed check of its own', r['fails']))
        # (a) the test
        odd = 'The odd part of the bottom number, ' if s else ''
        reps = [(l, order(m // l)) for l, e in sorted(f.items()) if e >= 2]
        m1 = re.match(r'The test\. Cross one (\d+) out of the bottom number to get the turtle ([\d,]+)/([\d,]+): its round has ([\d,]+) steps?, and this one has ([\w,]+) times as many, ([\d,]+)\. That is the sign that (it comes home|the round closes)\.( \(Crossing out one ([\d or,and]+) instead leaves the round as long as it is\.\))? The clock below shows why\.$', reason)
        m2 = re.match(r'The test\. Cross one (\d+) out of the bottom number to get the turtle ([\d,]+)/([\d,]+): its round has ([\d,]+) steps?, and this one has no more\. To close it would have to be ([\w,]+) times as long\. The clock below shows why\.$', reason)
        m3 = re.match(r'The test\. Cross one ([\d or,]+) out of the bottom number: the round is no shorter \(([\d,]+) steps each time\)\. To close it would have to be ([\w ,]+) times as long\. The clock below shows why\.$', reason)
        m4 = re.match(r'The test\. (?:The odd part of the bottom number, )?([\d,]+)(?: = [^ ]+(?: × [^ ]+)*)?,? (is itself a prime: no prime comes into it more than once|contains no prime more than once), and without that a round cannot close\. The clock below shows why\.$', reason)
        if m1:
            cnt['f_long'] += 1; l = int(m1.group(1)); A = int(m1.group(2).replace(',', '')); B = int(m1.group(3).replace(',', ''))
            n1 = dict(reps).get(l)
            if n1 is None or B != q // l or A % B != p % B or math.gcd(A, B) != 1 or A >= B and B > 1 or m1.group(4) != commas(n1) or n != l * n1 or m1.group(5) != tw(l) or m1.group(6) != commas(n) or not closes or (m1.group(7) == 'it comes home') != (s == 0):
                bad.append((p, q, 'test: times as many', reason[:160]))
            if m1.group(8):
                cnt['idle_said'] += 1; idle = [int(x) for x in re.findall(r'\d+', m1.group(9))]
                if idle != [l2 for l2, k in reps if k == n] : bad.append((p, q, 'crossing out instead', reason[:200]))
            elif any(k == n for l2, k in reps): bad.append((p, q, 'an idle prime not mentioned (not a falsehood)', reason[:120])) if False else None
        elif m2:
            cnt['f_nomore'] += 1; l = int(m2.group(1)); A = int(m2.group(2).replace(',', '')); B = int(m2.group(3).replace(',', ''))
            if len(reps) != 1 or reps[0][0] != l or B != q // l or A % B != p % B or (A >= B and B > 1) or m2.group(4) != commas(n) or reps[0][1] != n or m2.group(5) != tw(l) or closes: bad.append((p, q, 'test: no more', reason[:160]))
        elif m3:
            cnt['f_two'] += 1; ls = [int(x) for x in re.findall(r'\d+', m3.group(1))]
            if ls != [l for l, k in reps] or len(ls) < 2 or any(k != n for l, k in reps) or m3.group(2) != commas(n) or closes or [w for w in re.findall(r'[\w,]+', m3.group(3)) if w != 'or'] != [tw(l) for l in ls]: bad.append((p, q, 'test: two repeated primes', reason[:170]))
        elif m4:
            cnt['f_none'] += 1
            if reps or int(m4.group(1).replace(',', '')) != m or (m4.group(2).startswith('is itself')) != (len(f) == 1) or closes or (reason.startswith('The test. The odd part') != (s > 0)): bad.append((p, q, 'test: no prime twice', reason[:150]))
        else: unparsed.append((p, q, 'reason', reason[:230]))
    print('counts:', cnt, file=out)
    print('least distance a round that does not close carries the turtle, among these: %.6g' % least_gap, file=out)
    print('faults: %d' % len(bad), file=out)
    for b in bad[:25]: print('  ', b, file=out)
    print('sentences my patterns did not fit: %d' % len(unparsed), file=out)
    for u in unparsed[:12]: print('  ', u, file=out)
    out.close(); print(open('/home/agent2/gospel/referee/clock3/check.out').read()[:6000])
