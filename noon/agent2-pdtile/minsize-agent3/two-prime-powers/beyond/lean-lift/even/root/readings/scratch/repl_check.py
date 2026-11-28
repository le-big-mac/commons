# Check: are the replacements that each second report requires in the texts, word for word
# (white space normalised)?  Passages are cut out of the reports by their line numbers / markers.
import re, sys
R = '/home/agent3/lean/lift-check/even/root/'
def norm(s): return re.sub(r'\s+', ' ', s).strip()
def text(p): return open(R + p, encoding='utf-8').read()
def quote_after(report, marker, nth=1):
    """the first '>' block after the nth occurrence of marker"""
    s = text(report); i = -1
    for _ in range(nth):
        i = s.index(marker, i + 1)
    lines = s[i:].split('\n'); out = []; started = False
    for ln in lines[1:]:
        t = ln.lstrip()
        if t.startswith('>'):
            started = True; out.append(t[1:].strip())
        elif started: break
    return norm(' '.join(out))
def strip_q(s):
    s = s.strip()
    if s.startswith('"') and s.endswith('"'): s = s[1:-1]
    if s.startswith('…'): s = s[1:]
    return norm(s)
def inline_after(report, marker):
    """text between 'by: "' and the closing '"' on the line containing marker"""
    s = text(report)
    i = s.index(marker); ln = s[i:].split('\n')[0]
    j = ln.index('by: "') + 5
    k = ln.rindex('"')
    return norm(ln[j:k])
checks = []
# first text
one = norm(text('one/result.md'))
checks.append(('one 1 (§12, change 2)', strip_q(quote_after('report-referee-one-2.md', '1. **§12, Required change 2.**')), one))
checks.append(('one 2 (§5 sentence)', strip_q(quote_after('report-referee-one-2.md', '2. **§5, new sentence.**')), one))
checks.append(('one 3 (status paragraph)', strip_q(quote_after('report-referee-one-2.md', '**Status paragraph.**')), one))
opt = '(for the two heavy multisets with even m > 61, the computed sum of §6)'
checks.append(('one optional (§9 parenthesis)', opt, one))
# third text
three = norm(text('three/result.md'))
checks.append(('three A (§2)', strip_q(quote_after('report-referee-three-2.md', '**A. §2**')), three))
checks.append(('three B (§3a)', strip_q(quote_after('report-referee-three-2.md', '**B. §3a**')), three))
checks.append(('three C (§9)', strip_q(quote_after('report-referee-three-2.md', '**C. §9**')), three))
# second text
two = norm(text('two/result.md'))
checks.append(('two 1 (§8 Not changed)', inline_after('report-referee-two-2.md', '1. **§8, "Not changed".**'), two))
checks.append(('two 2a (§0 on (c))', inline_after('report-referee-two-2.md', '- In §0 replace "by the referee\'s counts'), two))
checks.append(('two 2b (§6)', inline_after('report-referee-two-2.md', '- In §6 replace'), two))
checks.append(('two 3a (§8 first paragraph)', inline_after('report-referee-two-2.md', '- In §8 replace "The changes below'), two))
checks.append(('two 3b (second line)', 'listed in §8, and read by the referee in a second look', two))
checks.append(('two 3c (six)', '(six, by its second report)', two))
checks.append(('two suggestion 1', 'Theorem Q is not used in any proof any more (§5, which proves nothing, still takes 3/8 and 47/128 from it)', two))
checks.append(('two suggestion 2', 'and none for even h, for every h, by a short proof in the referee\'s second report', two))
for name, pas, body in checks:
    ok = pas in body
    print(('PRESENT ' if ok else 'ABSENT  ') + name + f'  [{len(pas)} chars]')
    if not ok:
        # find longest prefix present
        lo = 0
        for L in range(len(pas), 0, -1):
            if pas[:L] in body: lo = L; break
        print('   passage:', pas[:200], '...')
        print('   longest prefix present:', lo, ' then report has:', repr(pas[lo:lo+80]))
