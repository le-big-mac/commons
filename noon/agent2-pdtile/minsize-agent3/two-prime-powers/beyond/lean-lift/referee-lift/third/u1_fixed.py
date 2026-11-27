"""Third pass: do the eight fixed statements of two-skeleton stand character for character in the finished files (two-all, and the copies
that will be posted, lean-lift/two-lean)?  Skeleton hashes against its SHA256 file and against the hash on the board; forbidden tokens; lines.
usage: python -I -B u1_fixed.py"""
import re, hashlib
SK = '/home/agent3/lean/two-skeleton/'; FIN = '/home/agent3/lean/two-all/Pnq/'; POST = '/home/agent3/pq2/rule/lean-lift/two-lean/'
BOARD = '574b8a5d4b302038d6d704ac805556825244ee30dfcc891f41ba3ed0e8be722f'
def rd(p): return open(p, encoding='utf-8').read()
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
print('sha256 of two-skeleton/SHA256 equals the hash in the board post headed 20:51:', sha(SK + 'SHA256') == BOARD)
print('board post contains that hash:', BOARD in rd('/srv/commons/hello-from-agent3.md'))
ok = True
for line in rd(SK + 'SHA256').splitlines():
    h, name = line.split(); same = sha(SK + name) == h; ok &= same
    print('  skeleton file', name, 'matches its line in SHA256:', same)
total = 0
for name in ('Sign.lean', 'Lift2.lean', 'LiftAll.lean'):
    sk, fin = rd(SK + 'Pnq/' + name), rd(FIN + name)
    parts = re.split(r'\n(?=/-- |instance |def |theorem |variable |section |end )', sk); decls = []
    for part in parts:
        m = re.search(r'^theorem (\S+)', part, re.M)
        if m:
            i = part.index(':= by\n  sorry'); decls.append((m.group(1), part[:i + len(':= by')]))
        elif part.startswith(('variable', 'section', 'instance', 'def')):
            decls.append((part.split('\n')[0][:40], part.split('\n\n')[0]))
    pos = []
    for nm, body in decls:
        n = fin.count(body); ok &= (n == 1); pos.append(fin.find(body))
        if body.startswith(('/--', 'theorem')): total += 1
        print(f'{name}: {nm}: {len(body)} characters; occurrences in the finished file: {n}')
    print(f'{name}: order kept: {pos == sorted(pos)}; lines {len(fin.splitlines())}; finished sha256 {sha(FIN + name)[:16]}…; copy to be posted identical: {sha(POST + name) == sha(FIN + name)};'
          f' posted "as fixed" copy identical to skeleton: {sha(POST + name.replace(".lean", ".as-fixed-before-proof.lean")) == sha(SK + "Pnq/" + name)}')
    toks = ['sorry', 'admit', 'axiom', 'native_decide', 'unsafe', 'opaque', 'implemented_by', 'set_option', 'notation', 'macro', 'syntax', 'attribute', '@[', 'local ',
            'scoped', 'instance', 'elab', 'open ', 'omit', 'universe', 'deriving', 'run_cmd', '#eval', 'decide', 'unseal', 'infix', 'prefix', 'postfix', 'private', 'protected', 'abbrev', 'noncomputable']
    found = {}
    for tok in toks:
        hits = [i + 1 for i, l in enumerate(fin.splitlines()) if tok in l]
        if hits: found[tok] = hits[:12]
    print(f'   tokens (token: lines): {found}')
    # header and import differences outside the declarations
    import difflib
    hs, hf = sk.split('namespace Pnq')[0].splitlines(), fin.split('namespace Pnq')[0].splitlines()
    d = [l for l in difflib.unified_diff(hs, hf, lineterm='', n=0) if not l.startswith(('---', '+++', '@@'))]
    print('   header/import differences (skeleton -> finished):', d)
print('fixed theorem statements found:', total, '; ALL STAND:', ok)
