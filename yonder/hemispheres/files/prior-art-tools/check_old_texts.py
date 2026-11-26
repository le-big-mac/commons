"""usage: python -I check_old_texts.py REPORT.md README.md PAGE.html
Every 'Old: `...`' text in the report must occur exactly once (whitespace-normalised) in the README or the page."""
import sys, re
rep, readme, page = (open(f, encoding="utf-8").read() for f in sys.argv[1:4])
norm = lambda t: re.sub(r"\s+", " ", t)
R, P = norm(readme), norm(page)
for m in re.finditer(r"Old: `([^`]+)`", rep):
    old = norm(m.group(1))
    print("README %d  page %d  | %s" % (R.count(old), P.count(old), old[:90]))
