"""Check 5: the working note's body changes against the report's items 1 to 10.

Takes the note before and after, squeezes every run of white space to one space,
applies the report's ten replacements to the 'before' text, and compares the result
with the 'after' text from which the dated head note has been cut.
Also compares the head note's quoted part with the report's note 'For the README'.
"""
import re, difflib

REPORT = "/srv/commons/hemispheres-agent3/prior-art.md"
BEFORE = "/srv/commons/hemispheres-agent3/prior-art-tools/note-before-26nov.txt"
AFTER = "/srv/commons/hemispheres-agent3/README.md"

def sq(s):
    return re.sub(r"\s+", " ", s).strip()

rep_all = open(REPORT, encoding="utf-8").read()
rep = rep_all[rep_all.index("## 4. "):]   # items are numbered in section 4; the note for the README is in section 5
before = sq(open(BEFORE, encoding="utf-8").read())
after_raw = open(AFTER, encoding="utf-8").read()

# the head note: the one line that begins "*Added 02:43 UTC, 26 November"
head_lines = [l for l in after_raw.split("\n") if l.startswith("*Added 02:43 UTC, 26 November")]
print("head-note lines found:", len(head_lines))
head = head_lines[0]
after = sq(after_raw.replace(head + "\n", "", 1))

def item(n):
    m = re.search(r'^%d\. (.*?)(?=^\d+\. |\n\n)' % n, rep, re.S | re.M)
    return m.group(1)

pairs = []
for n in (1, 2, 3, 4, 5, 6, 7, 9):
    t = item(n)
    old = re.search(r'Old: `(.*?)`', t, re.S).group(1)
    new = re.search(r'New: `(.*?)`', t, re.S).group(1)
    pairs.append((n, sq(old), sq(new)))
# item 8: an addition after the row's text
add8 = re.search(r'add `(.*?)`', item(8), re.S).group(1)
old8 = "in the mountains where Sichuan meets Yunnan"
pairs.append((8, old8, old8 + " " + add8))
# item 10: code marks left out in the report
t10 = item(10)
old10 = sq(re.search(r'Old text: (.*?)\n', t10).group(1))
new10 = sq(re.search(r'New text: (.*?)$', t10.strip(), re.S).group(1))
def strip_ticks(s):
    return s.replace("`", "")

work = before
for n, old, new in pairs:
    c = work.count(old)
    print("item %2d: old text occurs %d time(s) in the note before; new text occurs %d time(s) in the note after" % (n, c, after.count(new)))
    if c == 1:
        work = work.replace(old, new)
# item 10 compared without code marks
b10 = strip_ticks(work).count(old10)
a10 = strip_ticks(after).count(new10)
print("item 10 (code marks ignored): old in before %d, new in after %d" % (b10, a10))
work_nt = strip_ticks(work).replace(old10, new10)
after_nt = strip_ticks(after)
print("after applying the ten changes, 'before' equals 'after' (white space and code marks ignored):", work_nt == after_nt)
if work_nt != after_nt:
    sm = difflib.SequenceMatcher(None, work_nt.split(" "), after_nt.split(" "), autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal":
            print("  ", tag, "| expected:", " ".join(work_nt.split(" ")[i1:i2])[:300], "| found:", " ".join(after_nt.split(" ")[j1:j2])[:300])

# code marks of item 10 in the note after
m = re.search(r"the population maps are.*?human-hemisphere`\.", sq(after_raw))
print("item 10 as it stands in the note:", m.group(0) if m else None)

# head note against the report's note for the README
note = re.search(r'\*\*For the README, as a dated note\.\*\*\s*\n\s*\n> \*(.*?)\*\n', rep, re.S).group(1)
print("== head note against the report's note")
a = sq(note).split(" ")
b = sq(head.strip("*")).split(" ")
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != "equal":
        print("  ", tag, "| report:", " ".join(a[i1:i2])[:200], "| head note:", " ".join(b[j1:j2])[:1600])
