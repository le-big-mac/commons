"""Blind tally of the fifteen scorecards. Referee's own parser; reads nothing in /home/agent2/later/."""
import re, math, sys, json

FILES = [
    ("peas", "/home/agent2/peas/verdicts.out"),
    ("peas2", "/home/agent2/peas/verdicts2.out"),
    ("calve", "/home/agent2/calve/verdicts.out"),
    ("hawk", "/home/agent2/hawk/verdicts.out"),
    ("cutoff", "/home/agent2/cutoff/verdicts.out"),
    ("drum", "/home/agent2/drum/verdicts.out"),
    ("drum2", "/home/agent2/drum/verdicts2.out"),
    ("drum3", "/home/agent2/drum/verdicts3.out"),
    ("outsell", "/home/agent2/outsell/verdicts.out"),
    ("drum12", "/home/agent2/drum12/verdicts.out"),
    ("drumfree", "/home/agent2/drumfree/verdicts.out"),
    ("drumair", "/home/agent2/drumair/verdicts.out"),
    ("prior", "/home/agent2/prior/verdicts.out"),
    ("post", "/home/agent2/post/verdicts.out"),
    ("post2", "/home/agent2/post/verdicts2.out"),
]
PAT = re.compile(r"^([A-Z]+\d+)\s+(.*?)\s*odds\s+([01]\.\d+)\s+(scored FAILED|held|FAILED|HALF|void)\b(.*)$")
VAL = {"held": 1.0, "FAILED": 0.0, "scored FAILED": 0.0, "HALF": 0.5}


def load():
    rows = []
    for sheet, path in FILES:
        for ln in open(path):
            m = PAT.match(ln.rstrip("\n"))
            if not m:
                continue
            label, mark, p, word, rest = m.groups()
            rows.append(dict(sheet=sheet, label=label, mark=mark.strip(), p=float(p), word=word,
                             y=VAL.get(word), rest=rest.strip()))
    return rows


def logit(p):
    return math.log(p / (1 - p))


def expit(x):
    return 1 / (1 + math.exp(-x))


def clip(p):
    return min(0.99, max(0.01, p))


def brier(rows, f=lambda p: p):
    return sum((f(r["p"]) - r["y"]) ** 2 for r in rows) / len(rows)


def fit2(p):
    return clip(expit(0.277 + 1.413 * logit(p)))


def shift(p):
    return clip(expit(logit(p) + 0.581))


def first(mark):
    return mark.split()[0] if mark else "none"


def summary(rows, out, title):
    n = len(rows)
    out.append(f"--- {title}")
    if n == 0:
        out.append("  no lines")
        return
    held = sum(r["y"] == 1 for r in rows); failed = sum(r["y"] == 0 for r in rows); half = sum(r["y"] == 0.5 for r in rows)
    share = sum(r["y"] for r in rows) / n
    mp = sum(r["p"] for r in rows) / n
    out.append(f"  settled {n}: held {held}, failed {failed}, half {half}; share held (half = 0.5) {share:.4f}; "
               f"share strictly held {held / n:.4f}; mean odds {mp:.4f}; gap {share - mp:+.4f}")
    b0, b1, b2 = brier(rows), brier(rows, fit2), brier(rows, shift)
    out.append(f"  Brier as stated {b0:.4f}; two-number fit (0.277 + 1.413 logit) {b1:.4f} ({b1 - b0:+.4f}); "
               f"shift (+0.581) {b2:.4f} ({b2 - b0:+.4f}); 0.5 everywhere {brier(rows, lambda p: 0.5):.4f}; "
               f"base rate everywhere {brier(rows, lambda p: share):.4f}")


def bymark(rows, out):
    out.append(f"  {'mark':<11}{'n':>4}{'held':>6}{'failed':>8}{'half':>6}{'share':>8}{'mean odds':>11}{'Brier':>8}")
    for k in ["worked", "remembered", "guessed", "none"]:
        rr = [r for r in rows if first(r["mark"]) == k]
        if not rr:
            out.append(f"  {k:<11}{0:>4}")
            continue
        n = len(rr)
        out.append(f"  {k:<11}{n:>4}{sum(r['y'] == 1 for r in rr):>6}{sum(r['y'] == 0 for r in rr):>8}"
                   f"{sum(r['y'] == 0.5 for r in rr):>6}{sum(r['y'] for r in rr) / n:>8.3f}"
                   f"{sum(r['p'] for r in rr) / n:>11.4f}{brier(rr):>8.4f}")


if __name__ == "__main__":
    rows = load()
    out = []
    out.append(f"parsed {len(rows)} sealed lines from {len(FILES)} files; void {sum(r['word'] == 'void' for r in rows)}")
    for sheet, _ in FILES:
        rr = [r for r in rows if r["sheet"] == sheet]
        ss = [r for r in rr if r["y"] is not None]
        out.append(f"  {sheet:<9} lines {len(rr):>3} settled {len(ss):>3} held {sum(r['y'] == 1 for r in ss):>3} "
                   f"failed {sum(r['y'] == 0 for r in ss):>3} half {sum(r['y'] == 0.5 for r in ss):>3} "
                   f"mean odds {sum(r['p'] for r in ss) / len(ss):.3f} Brier {brier(ss):.4f}")
    S = [r for r in rows if r["y"] is not None]
    out.append("")
    out.append("1 and 2. All settled lines")
    summary(S, out, "all fifteen files")
    out.append("")
    out.append("3. By the first word of the mark")
    bymark(S, out)
    out.append("")
    out.append("marks seen: " + json.dumps(sorted({r['mark'] for r in rows})))
    open("/home/agent2/later/referee/blind.out", "w").write("\n".join(out) + "\n")
    print("\n".join(out))
