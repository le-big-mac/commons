# Is the author's bound.py changed in one printed message only?  The compiled file kept in one/__pycache__ was made
# from the source as it stood before (its header records the size of that source).  The new source is compiled in
# memory (not run) and the two code objects are compared constant by constant.  Nothing is executed or written.
import sys, marshal, types, struct
pyc, src = sys.argv[1], sys.argv[2]
raw = open(pyc, "rb").read()
flags, mtime, size = struct.unpack("<III", raw[4:16])
print("compiled file: made from a source of %d bytes; the source now has %d bytes" % (size, len(open(src, "rb").read())))
old = marshal.loads(raw[16:])
new = compile(open(src, "rb").read(), old.co_filename, "exec", dont_inherit=True)
diffs = []
def cmp(a, b, where):
    for attr in ("co_code", "co_names", "co_varnames", "co_freevars", "co_cellvars", "co_argcount", "co_kwonlyargcount",
                 "co_posonlyargcount", "co_flags", "co_name", "co_firstlineno", "co_linetable", "co_exceptiontable"):
        if getattr(a, attr) != getattr(b, attr):
            diffs.append((where, attr))
    if len(a.co_consts) != len(b.co_consts):
        diffs.append((where, "number of constants"))
        return
    for i, (x, y) in enumerate(zip(a.co_consts, b.co_consts)):
        if isinstance(x, types.CodeType) and isinstance(y, types.CodeType):
            cmp(x, y, where + "/" + x.co_name)
        elif x != y or type(x) != type(y):
            diffs.append((where, "constant %d: %r -> %r" % (i, x, y)))
cmp(old, new, "module")
print("differences between the old compiled program and the new source (%d):" % len(diffs))
for d in diffs:
    print("  ", d)
