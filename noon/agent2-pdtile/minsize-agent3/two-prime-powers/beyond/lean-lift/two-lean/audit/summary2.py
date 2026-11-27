# from the t5 outputs: how many (instance, s > 1) pairs have a lifted member, split by whether the least size on the base group
# was proved by the solver; and the same pairs split by parity of s
import re
pr = npr = 0
ev = od = 0
base_pr = base_np = 0
for name in ['t5_cpsat_M28.out', 't5_cpsat_M45.out', 't5_cpsat_M54.out']:
    for line in open(name):
        m = re.search(r'lifted with no new divisor to Z_\(M0\*s\) for s in \[([0-9, ]*)\]', line)
        if not m:
            continue
        ss = [int(x) for x in m.group(1).split(',') if x.strip()]
        if 'proved by the solver' in line:
            pr += len(ss); base_pr += 1
        else:
            npr += len(ss); base_np += 1
        ev += sum(1 for s in ss if s % 2 == 0); od += sum(1 for s in ss if s % 2 == 1)
print(f"base instances: least proved by the solver {base_pr}, not proved {base_np}")
print(f"(instance, s > 1) pairs with a lifted member: base least proved {pr}, base least not proved {npr}; s even {ev}, s odd {od}")
