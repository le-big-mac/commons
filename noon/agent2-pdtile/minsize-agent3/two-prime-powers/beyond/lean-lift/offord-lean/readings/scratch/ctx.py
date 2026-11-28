import sys, re
path, pat = sys.argv[1], sys.argv[2]
w = int(sys.argv[3]) if len(sys.argv) > 3 else 300
lo = int(sys.argv[4]) if len(sys.argv) > 4 else 1
hi = int(sys.argv[5]) if len(sys.argv) > 5 else 10**9
for i, line in enumerate(open(path, encoding='utf-8'), 1):
    if i < lo or i > hi: continue
    for m in re.finditer(pat, line):
        s = max(0, m.start() - w); e = min(len(line), m.end() + w)
        print(f"[{i}:{m.start()}] …{line[s:e].strip()}…\n")
