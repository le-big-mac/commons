"""Diff two files sentence by sentence (or line by line) and print the changed places.

Usage: python -I diff_pages.py BEFORE AFTER [--lines]
Reads the files as data only.
"""
import sys, re, difflib

def split(text, lines=False):
    if lines:
        return text.split("\n")
    # split on sentence ends and on tags that start blocks, keeping everything
    parts = re.split(r'(?<=[.!?])\s+|\n+', text)
    return [p for p in parts if p.strip()]

def main():
    a_path, b_path = sys.argv[1], sys.argv[2]
    lines = "--lines" in sys.argv
    a = split(open(a_path, encoding="utf-8").read(), lines)
    b = split(open(b_path, encoding="utf-8").read(), lines)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    n = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        n += 1
        print("=" * 30, "CHANGE", n, tag, "before[%d:%d]" % (i1, i2), "after[%d:%d]" % (j1, j2))
        ctx = a[max(0, i1 - 1):i1]
        for s in ctx:
            print("  (context before) " + s[:160])
        for s in a[i1:i2]:
            print("  - " + s)
        for s in b[j1:j2]:
            print("  + " + s)
    print("number of changed places:", n)

main()
