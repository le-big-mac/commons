"""Load the definitions of the scripts under review WITHOUT running their searches and without modifying them:
the source text is read, cut before the main loop, and executed in a private namespace with sys.argv set."""
import sys
sys.dont_write_bytecode = True
if "/home/agent3/t2search" not in sys.path: sys.path.append("/home/agent3/t2search")   # the script directory (for exactlp), as when run as a script
T2 = "/home/agent3/t2search/t2search.py"; T1 = "/home/agent3/t2search/t1search.py"

def _exec(src, argv, name, extra=None):
    ns = {"__name__": name}
    if extra: ns.update(extra)
    old = sys.argv; sys.argv = [name] + [str(v) for v in argv]
    try: exec(compile(src, name, "exec"), ns)
    finally: sys.argv = old
    return ns

def t2_defs(p, a, q, b, *flags):
    """names defined by t2search.py up to (not including) the search: Tm, sumf_range, exact_complement, solve01, ..."""
    src = open(T2).read(); cut = src.index("print(f\"Z_{M} = Z_({p}^{a} {q}^{b});  {len(ORD)} orders")
    return _exec(src[:cut], [p, a, q, b] + list(flags), "t2search_defs")

def t2_patterns(p, a, q, b, *flags):
    """run t2search.py's own pattern stage (its lines up to the print of each (i, j) header), recording allowed / todo, and stop before the 0/1 programmes"""
    lines = open(T2).read().split("\n")
    i0 = next(n for n, l in enumerate(lines) if l.startswith("        ui = X % p ** i"))
    assert lines[i0 - 1].startswith("        print(line, flush=True)")
    src = "\n".join(lines[:i0 - 1] + ["        ALLTODO[(i, j)] = ({k: list(v) for k, v in allowed.items()}, list(todo))"])
    ns = _exec(src, [p, a, q, b] + list(flags), "t2search_patterns", {"ALLTODO": {}})
    return ns["ALLTODO"], ns

def t1_defs(p, a, q, b, *flags):
    src = open(T1).read(); cut = src.index("t0 = time.time(); nprog = ninf = nund = 0")
    return _exec(src[:cut], [p, a, q, b] + list(flags), "t1search_defs")
