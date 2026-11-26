"""Placebo for run_proof.py: the same peeling on multisets that do NOT have the required divisors (a point added to a sum of
cosets).  The double-difference identity, or a later check, should fail in nearly every case with D not empty.   usage: placebo.py"""
import random, subprocess, sys, re
src = open('run_proof.py').read()
src = src.replace("            orig = A[:]; pieces = []", "            A[random.randrange(M)] += 1\n            orig = A[:]; pieces = []")
src = src.replace("            for k in range(n, -1, -1):", "            try:\n              for k in range(n, -1, -1):")
body_start = src.index("                assert periodic(A, M, N[k + 1] % M), 'not periodic under the period'")
body_end = src.index("            assert periodic(A, M, 1)")
body = src[body_start:body_end]
src = src[:body_start] + '\n'.join(('  ' + l) if l.strip() else l for l in body.split('\n')) + src[body_end:]
src = src.replace("            assert periodic(A, M, 1)                                # what is left is constant",
                  "              ok_runs = globals().get('ok_runs', 0) + (1 if D else 0); globals()['ok_runs'] = ok_runs\n            except AssertionError:\n              fails = globals().get('fails', 0) + 1; globals()['fails'] = fails; continue\n            assert periodic(A, M, 1)")
src = src.replace("print(f'{groups} groups, {tot} multisets peeled as the proof says; every check held')",
                  "print(f\"placebo: {globals().get('fails', 0)} multisets failed a check; {globals().get('ok_runs', 0)} with D not empty passed every check\")")
exec(compile(src, 'placebo-run', 'exec'))
