# second_look.py -- the revised sign-four-result.md against the text as refereed.
#  A. Every difference between the two files is one that the author's two replies list: the old and new words are
#     read from the replies themselves (lines "- Old:" / "- New:", the table of the second reply, the insertions),
#     applied in order to the text as refereed, and the result must equal the revised text (white space inside a
#     paragraph aside; the dated paragraph at the head is taken out and printed).
#  B. Each of the referee's replacements, read from the filed report, stands word for word in the revised text.
#  C. Lines that are byte for byte the same / changed (difflib), as a second look at the extent of the changes.
import re, sys, difflib, hashlib

D = "/home/agent3/lean/lift-check/"
old_raw = open(D + "sign-four-result.as-refereed.md", encoding="utf-8").read()
new_raw = open(D + "sign-four-result.md", encoding="utf-8").read()
r1 = open(D + "sign-four-revision-1.md", encoding="utf-8").read()
r2 = open(D + "sign-four-revision-2.md", encoding="utf-8").read()
rep = open(D + "referee-four-report.md", encoding="utf-8").read()
print("sha256 as refereed:", hashlib.sha256(old_raw.encode()).hexdigest())
print("sha256 revised    :", hashlib.sha256(new_raw.encode()).hexdigest())


def norm(t):
    """paragraphs (separated by blank lines) kept apart; inside a paragraph every run of white space is one blank."""
    paras = [" ".join(p.split()) for p in re.split(r"\n\s*\n", t)]
    return "\n\n".join(p for p in paras if p)


def quoted(line, key):
    """the words between the first double quote after key and the last double quote of the line."""
    i = line.index(key) + len(key)
    a = line.index('"', i)
    b = line.rindex('"')
    assert b > a
    return line[a + 1:b]


# ---------- the changes the replies list ----------
changes = []          # (label, old words, new words)
lines1 = r1.splitlines()
i = 0
while i < len(lines1):
    L = lines1[i]
    if L.startswith("- Old: "):
        assert lines1[i + 1].startswith("- New: "), L
        changes.append(("reply 1, " + lines1[i - 1].strip("* ."), quoted(L, "- Old: "), quoted(lines1[i + 1], "- New: ")))
        i += 2
        continue
    if "Added after" in L and L.startswith("**Finding"):
        anchor = quoted(L, "Added after ").lstrip("…")
        assert lines1[i + 1].startswith("- New: "), L
        add = quoted(lines1[i + 1], "- New: ")
        changes.append(("reply 1, " + L.split(".**")[0].strip("* ") + " (added)", anchor, anchor + " " + add))
        i += 2
        continue
    i += 1
lines2 = r2.splitlines()
head_added = None
file_line = None
i = 0
while i < len(lines2):
    L = lines2[i]
    m = re.match(r'^\| (.+?) \| "(.+)" \| "(.+)" \|$', L)
    if m:
        changes.append(("reply 2, table, " + m.group(1), m.group(2), m.group(3)))
    elif L.startswith("- Old: "):
        assert lines2[i + 1].startswith("- New: "), L
        changes.append(("reply 2, Old/New", quoted(L, "- Old: "), quoted(lines2[i + 1], "- New: ")))
        i += 1
    elif "New line after the `even_exact.py` line" in L:
        file_line = quoted(lines2[i + 1], "- ")
        i += 1
    elif "Added before its last sentence" in L:
        head_added = quoted(lines2[i + 1], "- ")
        i += 1
    i += 1
print("\nA. changes read from the two replies: %d pairs of old and new words, one new line for the file list, one dated paragraph" % len(changes))

text = norm(old_raw)
for label, o, n in changes:
    o, n = " ".join(o.split()), " ".join(n.split())
    c = text.count(o)
    print("  %-70s old words found %d time(s)" % (label[:70], c))
    assert c == 1, (label, o)
    text = text.replace(o, n)
# the new line of the file list: after the item that begins "- `even_exact.py`"
a = text.index("- `even_exact.py`")
b = text.index(" - `", a + 5)
text = text[:b] + " - " + file_line + text[b:]
print("  new line of the file list put after the item `even_exact.py`: %s" % file_line[:80])

new_norm = norm(new_raw)
paras = new_norm.split("\n\n")
heads = [p for p in paras if p.startswith("*Refereed, 27 November 2026.*")]
assert len(heads) == 1
head = heads[0]
assert paras.index(head) == 2, paras.index(head)          # title, "Answer to ...", then the dated paragraph
rest = "\n\n".join(p for p in paras if p is not head)
same = rest == text
print("  the text as refereed with these changes applied EQUALS the revised text without its dated paragraph:", same)
if not same:
    sm = difflib.SequenceMatcher(None, text.split(" "), rest.split(" "), autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal":
            print("   DIFFERENCE NOT LISTED:", tag, "|", " ".join(text.split(" ")[i1:i2])[:300], "|", " ".join(rest.split(" ")[j1:j2])[:300])
assert head_added is not None and " ".join(head_added.split()) in head
print("  the dated paragraph contains the sentence quoted in the second reply; it reads:\n")
print("  " + head + "\n")

# ---------- B. the referee's replacements, from the filed report ----------
print("B. the referee's replacements (from referee-four-report.md) in the revised text, word for word")
rl = rep.splitlines()


def find_line(start):
    c = [x for x in rl if x.startswith(start)]
    assert len(c) == 1, (start, len(c))
    return c[0]


items = []
L = find_line("- Replacement for §1: ")
items.append(("1, §1", quoted(L, "Replacement for §1: ")))
L = find_line("- Replacement in the head: ")
items.append(("1, head", re.search(r'Replacement in the head: "(.+?)" for "', L).group(1)))
L = find_line("- Replacement: \"*From the brief")
items.append(("2, From the brief", quoted(L, "- Replacement: ")))
L = find_line("- Replacement for (ii): ")
ii = quoted(L, "Replacement for (ii): ")
L = find_line("Add: \"A caution")
items.append(("3, caution in §6", quoted(L, "Add: ")))
L = find_line("**4. Head, \"Mine (i)\".**")
items.append(("4, Mine (i)", re.search(r'Replacement: "(.+)"\.$', L).group(1)))
L = find_line("**5. §6, \"Large groups\", the pruning.**")
items.append(("5, pruning", re.search(r'add: "(.+)"\.$', L).group(1)))
L = find_line("**6. §4, Remark, last sentence.**")
items.append(("6, Remark of §4", re.search(r'should read "(.+?) …"\.$', L).group(1)))
ok = True
for label, s in items:
    s = " ".join(s.split())
    c = new_norm.count(s)
    # where: the nearest heading before it
    pos = new_norm.find(s)
    sec = [m.group(0) for m in re.finditer(r"## \d+\. [^\n]*|\*\*Whose is what\.\*\*", new_norm[:pos])]
    print("  finding %-20s found %d time(s), after the heading: %s   (%d characters)" % (label, c, sec[-1][:40] if sec else "(head)", len(s)))
    ok &= c >= 1
# (ii): the referee's words up to "is lead 1", then the author's clause
stem = " ".join(ii.split())
assert stem.endswith("is lead 1);")
stem = stem[:-2]
pos = new_norm.find(stem)
print("  finding 2, Mine (ii)        found: %s; what follows the referee's words: %r" % (pos >= 0, new_norm[pos + len(stem):pos + len(stem) + 150]))
ok &= pos >= 0
print("  all present:", ok)

# ---------- C. extent of the changes, line by line ----------
ol, nl = old_raw.splitlines(), new_raw.splitlines()
sm = difflib.SequenceMatcher(None, ol, nl, autojunk=False)
eq = sum(i2 - i1 for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag == "equal")
hunks = [(tag, i1, i2, j1, j2) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal"]
print("\nC. lines: %d as refereed, %d revised; %d lines the same byte for byte; %d places changed" % (len(ol), len(nl), eq, len(hunks)))
# numbers: every token with a digit, outside the dated paragraph, the added caution, the clause and the new file line
def digits(t):
    return sorted(re.findall(r"[^\s]*\d[^\s]*", t))
t_new = rest
for label, o, n in changes:
    pass
print("   tokens with a digit: as refereed %d, revised without the dated paragraph %d" % (len(digits(norm(old_raw))), len(digits(rest))))
added = sorted(set(digits(rest)) - set(digits(norm(old_raw))))
gone = sorted(set(digits(norm(old_raw))) - set(digits(rest)))
print("   tokens with a digit that are new in the revised text:", added)
print("   tokens with a digit that are gone from it:", gone)
