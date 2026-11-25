"""Is each sealed file's sha256 on the shared board?   usage: python hashes.py SEALEDDIR BOARD [more files...]"""
import sys, os, hashlib
board = open(sys.argv[2], encoding='utf-8', errors='replace').read(); n = ok = 0
files = sorted(os.path.join(d, f) for d, _, fs in os.walk(sys.argv[1]) for f in fs if f.endswith('.md')) + sys.argv[3:]
for p in files:
    h = hashlib.sha256(open(p, 'rb').read()).hexdigest(); n += 1; found = h in board; ok += found
    print(f"{'on the board    ' if found else 'NOT on the board'}  {h[:16]}…  {os.path.relpath(p, sys.argv[1]) if p.startswith(sys.argv[1]) else p}")
print(f"{ok} of {n} sealed files have their hash on the board as they stand today")
