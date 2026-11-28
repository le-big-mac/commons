"""The clock page: a dated sentence, after the one that said what the site's copy of the working note had at 08:11,
that sections 19 and 20 are there since Noon's push; and "the two sentences" in the account of readings.
usage: apply_carried_line.py 'HH:MM' < README.md > README.new.md   (the time at which I looked at the repository)"""
import sys, re
s = sys.stdin.read(); WHEN = sys.argv[1]
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
rep("and until then the page of statements, `signs-where-it-stands.md`, has the statement about the limits and where it stands.]",
    "and until then the page of statements, `signs-where-it-stands.md`, has the statement about the limits and where it stands. Since Noon's push of 09:09 UTC that day they are there: when I looked again at " + WHEN + " UTC, the site's copy of the note had sections 19 and 20.]")
rep("The sentence on the public copy that follows the pointer to section 20 nobody has read but me.",
    "The two sentences on the public copy that follow the pointer to section 20 nobody has read but me.")
i = s.index("## What came after, in full"); j = s.index("## What this does not say")
n = len(s[i:j].split()); r = int(round(n, -2))
m = re.search(r"it is long, about ([0-9,]+) words", s); assert m
s = s.replace(m.group(0), f"it is long, about {r:,} words"); sys.stderr.write(f"long section: {n} words -> {r}\n")
sys.stdout.write(s)
