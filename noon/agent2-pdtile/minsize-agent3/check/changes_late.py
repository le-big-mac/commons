# executed inside make_changes.py: the changes whose wording depends on the referee's own runs.
# Numbers are read from the output files in this folder at build time, so the sentences cannot drift from the outputs.
import re, os, json as _json
H = '/home/agent3/minsize/check'


def _dp(p, q, n, kind, S):
    f = f'{H}/dp-p{p}-q{q}-n{n}-{kind}-S{S}.out'
    d = {}
    for l in open(f):
        m = re.match(r"# (0 not in F \(theorem\)|F all levels|rest of 0 in F \(rule\)): as formula (\d+), differs (\d+), beyond bound (\d+)", l)
        if m: d[m.group(1)[:4]] = (int(m.group(2)), int(m.group(3)), int(m.group(4)))
        m = re.match(r"# sets: patterns with a set (\d+); smallest set = formula (\d+); larger (\d+); smaller (\d+)", l)
        if m: d['sets'] = tuple(int(m.group(i)) for i in range(1, 5))
        m = re.match(r"# author's decided minima \(each solver counted\): same (\d+), different (\d+)", l)
        if m: d['auth'] = (int(m.group(1)), int(m.group(2)))
    return d


def _rule(p, q, n, S):          # (as formula, differs, beyond) for the rule
    return _dp(p, q, n, 'multi', S)['rest']


def _cp(p, q, n):
    f = f'{H}/cpsat-table-p{p}-q{q}-n{n}.out'
    L = [l for l in open(f) if not l.startswith('#') and '| rule ' in l]
    return sum('as formula' in l for l in L), sum('DIFFERS' in l or 'SMALLER' in l for l in L), sum('undecided' in l for l in L), len(L)


full = {96: _rule(2, 3, 5, 144), 162: _rule(3, 2, 4, 162), 250: _rule(5, 2, 3, 250)}
assert full[96] == (992, 0, 0) and full[162] == (240, 0, 0) and full[250] == (56, 0, 0), full
part = {486: _rule(3, 2, 5, 255), 1458: _rule(3, 2, 6, 255), 686: _rule(7, 2, 3, 255), 1250: _rule(5, 2, 4, 255)}
S192 = 144 if os.path.exists(f'{H}/dp-p2-q3-n6-multi-S144.out') else 96
part[192] = _rule(2, 3, 6, S192)
assert all(v[1] == 0 for v in part.values()), part
cp = {28: _cp(2, 7, 2), 63: _cp(3, 7, 2), 44: _cp(2, 11, 2), 56: _cp(2, 7, 3)}
assert all(v[1] == 0 for v in cp.values()), cp
assert cp[28][0] == cp[63][0] == cp[44][0] == 12

add('R17', R,
    "the rule wrong for larger n.",
    "the rule wrong for larger n. The referee looked for one in larger groups, with a recursion over the tree of classes\n"
    "that uses neither of my solvers (`check/dp.c`; each minimum it reports has a witness checked by exact division), and\n"
    f"found none. The rule gives the minimum on all {full[96][0]:,} such patterns of Z_96 (n = 5), on all {full[162][0]:,} of Z_162 (p = 3, q = 2,\n"
    f"n = 4) and on all {full[250][0]:,} of Z_250; on every such pattern it could settle in Z_192, Z_486, Z_1458, Z_686 and Z_1250 (those\n"
    f"with a minimum up to {S192} in Z_192 and up to 255 in the other four: {part[192][0]:,}, {part[486][0]:,}, {part[1458][0]:,}, {part[686][0]:,} and {part[1250][0]:,} patterns); and,\n"
    f"by a CP-SAT model of the referee's own, on the 12 such patterns each of Z_28, Z_63 and Z_44 and on {cp[56][0]} of the {cp[56][3]} of Z_56,\n"
    f"the other {cp[56][2]} undecided (`check/dp-summary.out`, `check/cpsat-table-*.out`). That is q = 2 and 3 for n ≥ 4; for larger q\n"
    "nothing beyond n = 3.",
    "Not a correction: the result of the referee's attempt to break the rule, which the note may want to carry since it says 'a fourth way would make the rule wrong for larger n'. "
    "All numbers are read from the outputs in check/ when changes.json is built.",
    False)

add('R25', R,
    "stays failed (70%): held.",
    "stays failed (70%): held. The sheets promised a Brier score: 0.119 over the fourteen lines of the first sheet that carry\n"
    "a chance (eleven held, three failed), and 0.065 over four lines of the second (its second line speaks only of a miss,\n"
    "and there was none). They also promised a list of what was left out because a solver ran out of time at some size: at\n"
    "order 48 the pattern E = {1, 4}, F = {0, 2, 3} for CP-SAT (HiGHS decided it, and so did a longer CP-SAT run\n"
    "afterwards); at order 135 three patterns for CP-SAT and three for HiGHS; at order 375 one pattern for HiGHS.",
    "expectations.md, 'How it will be scored': 'Patterns where a solver does not finish in its time limit are listed and left out. Brier score over the lines with a stated chance.' "
    "Neither is in the note. Scores and list: check/sheets-scored.out (as the files stood when the note was written). The list as the files stand now, with the long runs stopped, is longer: check/counts-now.out (order 250: two patterns for HiGHS; order 135: five for CP-SAT and three for HiGHS; order 375: three for HiGHS; order 48: one for CP-SAT).",
    True)

orders_done = []
for (p, q, n, S) in [(2, 3, 2, 18), (3, 2, 2, 18), (2, 5, 2, 30), (5, 2, 2, 50), (3, 5, 2, 45), (5, 3, 2, 75), (2, 3, 3, 36), (3, 2, 3, 54), (2, 5, 3, 60), (2, 3, 4, 72)]:
    f = f'{H}/dp-p{p}-q{q}-n{n}-multi-S{S}.out'
    if os.path.exists(f):
        d = _dp(p, q, n, 'multi', S)
        assert d['auth'][1] == 0 and d['0 no'][1] == 0 and d['rest'][1] == 0 and d['0 no'][2] == 0 and d['rest'][2] == 0, (p, q, n, d)
        orders_done.append(p ** n * q)
d250 = _dp(5, 2, 3, 'multi', 250)
assert d250['auth'][1] == 0
olist = ', '.join(str(o) for o in orders_done[:-1]) + ' and ' + str(orders_done[-1])
add('R30', R,
    "*`out/summary.out`. For orders 135, 250 and 375 the solvers had not finished when this was written; the\nrows show what they had decided.*",
    "*`out/summary.out`. For orders 135, 250 and 375 the solvers had not finished when this was written; the\nrows show what they had decided. The referee's recursion has since recomputed, without either solver, every minimum\n"
    f"of orders {olist}, and all 128 of order 250: the same value wherever a solver had decided one, and the\nformulas right on all 128 patterns of order 250 (`check/dp-summary.out`).*",
    "Not a correction. An independent confirmation of the table the note may want to cite; it also completes the row for order 250, where the solvers had decided 29 patterns.",
    False)

add('R29', R,
    "- Small groups only: n ≤ 4, and n = 4 only for (p, q) = (2, 3).",
    "- Small groups only. My solvers: n ≤ 4, and n = 4 only for (p, q) = (2, 3). The referee's recursion, for q = 2 and 3\n"
    "  only: every pattern of Z_96 (n = 5), Z_162 (n = 4) and Z_250, and the patterns with small minima in Z_192, Z_486,\n  Z_1458, Z_686 and Z_1250.\n"
    "- For sets, an observation on ten groups with n ≤ 4 that already fails in Z_96.",
    "Brings the list of limits up to date with what the referee ran, and says of the sets what section 4 now says.",
    False)

add('P05', P,
    "(every pattern for $n\\le 3$ in three groups and for $n=4$ in $\\mathbb{Z}_{48}$)",
    "(by two integer-programming solvers, every pattern for $n=2$ in six groups, for $n=3$ in three and for $n=4$ in\n$\\mathbb{Z}_{48}$; by a referee's independent recursion also every pattern of $\\mathbb{Z}_{96}$, $\\mathbb{Z}_{162}$ and $\\mathbb{Z}_{250}$)",
    "The present wording undercounts n = 2 (six groups were complete) and can now name the larger groups; all 1,024, 256 and 64 patterns with 0 not in F in Z_96, Z_162 and Z_250 have the minimum of the formula (check/dp-summary.out).",
    False)

add('R31', R,
    "search and its reader's files).",
    "search and its reader's files) · `check/` (the referee's scripts and outputs; `check/changes.json` is its list of\nchanges, `check/dp-summary.out` what its recursion computed).",
    "The note now cites files in check/; the list of files should name the folder.",
    False)
