"""Checks the page's JavaScript core against the study's Python.   usage: python test-core.py PATH_TO_STUDY     (writes cases.json, runs node, compares)"""
import sys, json, subprocess, math
sys.path.insert(0, sys.argv[1])
import numpy as np, urn
cases = [(1.1, 1.0, 1000, 1.0), (1.1, 0.0, 1000, 1.0), (1.1, 0.5, 999, 1.0), (1.1, 1.5, 1000, 1.0), (2.0, 1.0, 100, 1.0), (1.25, 0.75, 10000, 1.0), (1.1, 1.0, 1000, 10.0), (1.05, 2.0, 10000, 0.3), (1.5, 1.25, 100, 3.0)]
json.dump(cases, open("cases.json", "w")); J = json.loads(subprocess.run(["node", "test-core.js", "cases.json"], capture_output=True, text=True, check=True).stdout); worst = 0.0
for (q, g, N, a), r in zip(cases, J['out']):
    p = urn.dist(q, g, N, a=a); ex = urn.ahead(p); third = float(p[:int(math.ceil(N / 3 - 1e-12))].sum()); d = max(abs(ex - r['ahead']), abs(third - r['third'])); worst = max(worst, d)
    print(f"q = {q}, g = {g}, N = {N:,}, a = {a}: ahead, page {r['ahead']:.10f}, Python {ex:.10f}; share under a third, page {r['third']:.10f}, Python {third:.10f}; the page's probabilities sum to 1 within {abs(r['sum'] - 1):.1e}; {r['ms']} ms")
se = math.sqrt(0.6507 * 0.3493 / J['M']); print(f"the page's sale-by-sale market, {J['M']:,} times at q = 1.1, g = 1, N = 1,000: ahead in {J['sampled']:.4f} (exact 0.6507; standard error {se:.4f})")
print("worst difference:", f"{worst:.1e}", "PASS" if worst < 1e-10 and abs(J['sampled'] - 0.6507) < 3 * se else "FAIL")
