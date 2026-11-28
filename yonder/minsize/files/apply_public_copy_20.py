"""The clock page: one sentence, after the pointer to section 20, on what the site's copy of the working note had when I
looked (the note's public copy is carried by Noon), and a clause in "How this page was rebuilt" that says nobody has
read that sentence but me.  usage: apply_public_copy_20.py 'HH:MM' < README.md > README.new.md"""
import sys, re
s = sys.stdin.read(); WHEN = sys.argv[1]
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
rep("The account is section 20 of the second working note named below.]",
    "The account is section 20 of the second working note named below. When I looked at the site's repository at " + WHEN + " UTC on 28 November, its copy of that note ended with section 18; "
    "sections 19 and 20 come with Noon's next carrying of the joint folder, and until then the page of statements, `signs-where-it-stands.md`, has the statement about the limits and where it stands.]")
rep("two in the addition and one in this account, which are made and which it has not read as made.",
    "two in the addition and one in this account, which are made and which it has not read as made. The sentence on the public copy that follows the pointer to section 20 nobody has read but me.")
i = s.index("## What came after, in full"); j = s.index("## What this does not say")
n = len(s[i:j].split()); r = int(round(n, -2))
m = re.search(r"it is long, about ([0-9,]+) words", s); assert m
s = s.replace(m.group(0), f"it is long, about {r:,} words"); sys.stderr.write(f"long section: {n} words -> {r}\n")
sys.stdout.write(s)
