# summary_t1.py -- tables of the results of t1_setlift.py (JSON lines) and t4_lift_sets.py, for the report.
import json, sys


def rows(fn):
    out = []
    for line in open(fn):
        line = line.strip()
        if line.startswith('{'):
            out.append(json.loads(line))
        elif line and line != 'ALL DONE':
            print("UNEXPECTED LINE in %s: %s" % (fn, line[:200]))
    return out


def t1(fn, title):
    rs = rows(fn)
    print(title)
    print("| N | r | j | group | which w | w tested (hle, hne) | plain lift fails | recipe of the proof fails | random: first lift fails | most random lifts needed | all lifts enumerated | NO lift exists | undecided | excluded (all mult. r^j): cases / conclusion fails | long-division rechecks (bad) |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    tot = dict(tested=0, plain_fail=0, recipe_fail=0, no_witness=0, undecided=0, excluded_hne=0, excluded_hne_fail=0,
               longdiv_checked=0, longdiv_bad=0, random_first_fail=0)
    for r in rs:
        which = 'all' if not r['maxsupp'] and not r['sample'] else ('support <= %d' % r['maxsupp'] if r['maxsupp'] else 'random sample %d' % r['sample'])
        print("| %d | %d | %d | Z_%d | %s | %d | %d | %s | %d | %d | %d | %d | %d | %d / %d | %d (%d) |" % (
            r['N'], r['r'], r['j'], r['G'], which, r['tested'], r['plain_fail'], r['recipe_fail'] if r['r'] != 2 else '-',
            r['random_first_fail'], r['max_tries'], r['exhaustive_used'], r['no_witness'], r['undecided'],
            r['excluded_hne'], r['excluded_hne_fail'], r['longdiv_checked'], r['longdiv_bad']))
        for k in tot:
            tot[k] += r[k]
    print()
    print("cases (N, r, j): %d; largest group: Z_%d; %s" % (len(rs), max(r['G'] for r in rs), json.dumps(tot)))
    nw = [(r['N'], r['r'], r['j'], r['no_witness_list'][:8]) for r in rs if r['no_witness_list']]
    if nw:
        print("w with no lift (first few per case):")
        for x in nw:
            print("  N=%d r=%d j=%d: %s" % x)
    print()


def t4(fn):
    rs = rows(fn)
    print("lifts of multisets of t < Q elements on Z_M to sets on Z_{M s}  (t4_lift_sets.py)")
    print("| M | s | group | Q | sizes t | multisets | which | largest multiplicity | plain lift fails | random: first lift fails | most lifts needed | all lifts enumerated | NO lift | undecided | long-division rechecks (bad) |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    tot = dict(tested=0, plain_fail=0, no_witness=0, undecided=0, longdiv_checked=0, longdiv_bad=0)
    for r in rs:
        print("| %d | %d | Z_%d | %d | 1..%d | %d | %s | %d | %d | %d | %d | %d | %d | %d | %d (%d) |" % (
            r['M'], r['s'], r['G'], r['Q'], r['tmax'], r['tested'], ('all' if not r['sample'] else 'all, or %d random per size' % r['sample']),
            r['maxmult'], r['plain_fail'], r['random_first_fail'], r['max_tries'], r['exhaustive_used'], r['no_witness'],
            r['undecided'], r['longdiv_checked'], r['longdiv_bad']))
        for k in tot:
            tot[k] += r[k]
    print()
    print("pairs (M, s): %d; largest group: Z_%d; %s" % (len(rs), max(r['G'] for r in rs), json.dumps(tot)))
    print()


if __name__ == '__main__':
    import os
    if os.path.exists('t1_setlift_main.out'):
        t1('t1_setlift_main.out', 'exists_set_lift, r odd  (t1_setlift.py)')
    if os.path.exists('t1_setlift_extra.out'):
        t1('t1_setlift_extra.out', 'exists_set_lift, r odd: random samples with supports of every size (t1_setlift.py N r j 0 20000)')
    if os.path.exists('t1_setlift_control.out'):
        t1('t1_setlift_control.out', 'control: r = 2 (excluded by hr)')
    if os.path.exists('t4_lift_sets.out'):
        t4('t4_lift_sets.out')
