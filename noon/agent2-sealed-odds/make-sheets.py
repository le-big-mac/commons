"""Builds the four files the forecasters see: the sealed sheets with my odds removed and nothing else changed but the sentence that
announces the odds.   usage: python make-sheets.py HOME OUTDIR"""
import sys, re
H, out = sys.argv[1], sys.argv[2]
def strip(path):
    t = open(f"{H}/{path}", encoding='utf-8').read()
    n = len(re.findall(r"odds 0\.\d+[ \t]*$", t, re.M))
    t = re.sub(r"[ \t]*odds 0\.\d+[ \t]*$", "", t, flags=re.M)
    for a, b in (("Each line ends with the odds I give it now, and where I mark one down, why.", "(Noon's own odds, which ended each line, have been removed. Where it marked a line down it says why.)"),
                 ("Each line ends with the\nodds I give it now.", "(Noon's own odds, which ended each line, have been removed.)"),
                 ("Each line ends with the odds I give it now.", "(Noon's own odds, which ended each line, have been removed.)")):
        t = t.replace(a, b)
    assert "odds I give" not in t, path
    assert not re.search(r"odds 0\.\d+[ \t]*$", t, re.M), path
    return t, n
total = 0
for k, paths in enumerate((["authors/expectations.md"], ["authors2/expectations.md"], ["authors2/expectations-quick.md"], ["float/expectations.md", "impetus/expectations.md", "aztec/expectations.md"]), 1):
    parts = []
    for p in paths:
        t, n = strip(p); total += n; parts.append(t.rstrip() + "\n")
    open(f"{out}/sheet-{k}.md", "w", encoding='utf-8').write("\n\n---\n\n".join(parts))
print(total, "odds removed")
