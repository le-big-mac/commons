"""Do the fixed declarations of the skeleton stand character for character in the finished files (shared library copy)?
Each skeleton declaration = text from its doc-comment (or 'instance'/'def'/'theorem' line) up to ':= by\n  sorry' (theorems) or the full
body (def, instance).  Also: forbidden tokens in the three finished files, hashes, and line counts.
usage: python3 -I t1_fixed_decls.py"""
import re, hashlib, sys
SK = '/home/agent3/lean/lift-skeleton/'
FIN = '/srv/commons/agent2-pdtile/lean-tiling/Pnq/'
PRIV = '/home/agent3/lean/lift/Pnq/'
NOTE = '/home/agent3/pq2/rule/lean-lift/'
def rd(p): return open(p, encoding='utf-8').read()
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
ok = True
# hashes of the skeleton against its SHA256 file
for line in rd(SK + 'SHA256').splitlines():
    h, name = line.split()
    same = sha(SK + name) == h
    ok &= same
    print('skeleton hash', name, 'matches SHA256 file:', same)
for name in ('Lift.lean', 'LiftMin.lean'):
    sk, fin = rd(SK + name), rd(FIN + name)
    # split the skeleton into declarations
    parts = re.split(r'\n(?=/-- |instance |def |theorem )', sk)
    decls = []
    for part in parts:
        m = re.search(r'^(instance|def|theorem) (\S+)', part, re.M)
        if not m: continue
        kind, nm = m.group(1), m.group(2)
        body = part
        if kind == 'theorem':
            i = body.index(':= by\n  sorry')
            body = body[:i + len(':= by')]
        else:
            # definition / instance: up to the blank line that ends it
            body = body.split('\n\n')[0]
        # a doc comment directly above an instance/def may be split off: glue handled by regex above
        decls.append((kind, nm, body))
    for kind, nm, body in decls:
        n = fin.count(body)
        ok &= (n == 1)
        print(f'{name}: {kind} {nm}: {len(body)} characters, occurrences in finished file: {n}')
    # the variable line
    for l in sk.splitlines():
        if l.startswith('variable'):
            print(f'{name}: line {l!r} in finished file: {fin.count(l)}')
    # order of the fixed declarations preserved
    pos = [fin.index(b) for _, _, b in decls]
    print(f'{name}: order kept: {pos == sorted(pos)}'); ok &= pos == sorted(pos)
# forbidden tokens
toks = ['sorry', 'admit', 'axiom', 'native_decide', 'unsafe', 'opaque', 'implemented_by', 'set_option', 'notation', 'macro', 'syntax',
        'attribute', '@[', 'local ', 'scoped', 'instance', 'elab', 'open ', 'omit', 'universe', 'deriving', 'macro_rules', 'run_cmd', '#eval', 'decide']
for name in ('Lift.lean', 'Lift1.lean', 'LiftMin.lean'):
    t = rd(FIN + name)
    found = {}
    for tok in toks:
        hits = [i + 1 for i, l in enumerate(t.splitlines()) if tok in l]
        if hits: found[tok] = hits
    print(name, 'tokens found (token: lines):', found)
    print(name, 'lines:', len(t.splitlines()), 'sha256:', sha(FIN + name), '| private copy same:', sha(PRIV + name) == sha(FIN + name),
          '| note folder copy same:', sha(NOTE + name) == sha(FIN + name))
# diff skeleton vs finished outside proofs: header comment and imports
import difflib
for name in ('Lift.lean', 'LiftMin.lean'):
    sk, fin = rd(SK + name).splitlines(), rd(FIN + name).splitlines()
    head_sk = sk[:sk.index('namespace Pnq')]; head_fin = fin[:fin.index('namespace Pnq')]
    d = [l for l in difflib.unified_diff(head_sk, head_fin, lineterm='', n=0) if not l.startswith(('---', '+++', '@@'))]
    print(name, 'header differences (skeleton -> finished):'); [print('   ', l) for l in d]
print('copies in note folder of the fixed files equal the skeleton:', sha(NOTE + 'Lift.as-fixed-before-proof.lean') == sha(SK + 'Lift.lean'),
      sha(NOTE + 'LiftMin.as-fixed-before-proof.lean') == sha(SK + 'LiftMin.lean'))
print('ALL FIXED DECLARATIONS STAND:', ok)
