"""Make lag-plain.c from lag.c by taking the shortcuts out (see the edits below), so the two can be compared.   usage: python -I plain.py"""
s = open("lag.c").read()
def cut(a, b=""):
    global s
    assert s.count(a) == 1, a[:60]; s = s.replace(a, b)
cut("    if (largest(S, m, P, p) > capK[r]) return -1;\n")                                   # K: the bound on a class's size
i = s.index("  long long cover = 0;"); j = s.index("  return 0;\n}\n\n// The search: returns the guess to send")
s = s[:i] + s[j:]                                                                            # W: the three bounds
cut("  if (mode == 'K' && r == 1) return lastK(S, m, P, p);\n")                              # K: the last guess by pair bit sets
cut("  int useful = (mode == 'K') || (r - 1 >= d + 1);                                      // in W an answer that never arrives in time tells nothing\n", "  int useful = 1;                                                                      // plain: every code is tried at every turn\n")
s = "// lag-plain.c: lag.c with every shortcut taken out (no bound on class sizes, no pair bit sets, no naming-phase count, every code tried at\n// every turn). Made by plain.py from lag.c, to test lag.c against on boards too large for slow.py.\n" + s
open("lag-plain.c", "w").write(s)

# A second copy, lag-plainw.c: the bounds taken out as above, but in W a guess whose answer can no longer be used is still tried only
# if it may be the code. (lag-plain.c tries every code there too, which on the classic board takes hundreds of hours.)
s = open("lag.c").read()
cut("    if (largest(S, m, P, p) > capK[r]) return -1;\n")
i = s.index("  long long cover = 0;"); j = s.index("  return 0;\n}\n\n// The search: returns the guess to send")
s = s[:i] + s[j:]
cut("  if (mode == 'K' && r == 1) return lastK(S, m, P, p);\n")
s = "// lag-plainw.c: lag.c with the bounds and the pair bit sets taken out; in W a guess too late to be answered in time is still tried only\n// if it may be the code. Made by plain.py from lag.c.\n" + s
open("lag-plainw.c", "w").write(s)
