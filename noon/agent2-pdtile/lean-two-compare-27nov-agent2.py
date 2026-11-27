"""Are the statements in the finished Lean files the statements as fixed before the proofs?   usage: python -I compare.py FOLDER
For each X.as-fixed-before-proof.lean and X.lean: every `theorem NAME ... := by` of the fixed file, with its white space squeezed,
must occur, squeezed, in the finished file; and the finished file must hold no `sorry`, `axiom`, `admit` or `native_decide`.  It also
lists every declaration keyword of the finished file that is not `theorem`/`lemma`/`private`, to be read by eye."""
import sys, os, re
if __name__ == '__main__':
    d = sys.argv[1]; sq = lambda t: re.sub(r'\s+', ' ', t).strip()
    for base in ('Sign', 'Lift2', 'LiftAll'):
        fixed = open(os.path.join(d, base + '.as-fixed-before-proof.lean'), encoding='utf8').read(); done = open(os.path.join(d, base + '.lean'), encoding='utf8').read()
        nocom = re.sub(r'/-.*?-/', '', done, flags=re.S); nocom = re.sub(r'--.*', '', nocom)
        fixed_nc = re.sub(r'/-.*?-/', '', fixed, flags=re.S)      # the header comment of a fixed file may hold the word 'theorem'
        stm = re.findall(r'(theorem\s+\w+.*?):=\s*by\s*\n\s*sorry', fixed_nc, flags=re.S)
        print(base, ':', len(stm), 'statements fixed;', len(done.splitlines()), 'lines finished')
        for t in stm:
            name = re.match(r'theorem\s+(\w+)', t).group(1); ok = sq(t) + ' :=' in sq(done)
            print('   %-28s %s' % (name, 'stands word for word in the finished file' if ok else 'IS NOT in the finished file as fixed'))
        bad = [w for w in ('sorry', 'axiom', 'admit', 'native_decide', 'unsafe', 'implemented_by', 'extern', 'opaque') if re.search(r'\b' + w + r'\b', nocom)]
        other = sorted(set(re.findall(r'^\s*(?:@\[[^\]]*\]\s*)?(instance|notation|macro|syntax|attribute|def|abbrev|structure|class|inductive|local\s+\w+|set_option\s+\S+|open\s+[\w. ]+|import\s+\S+)', nocom, flags=re.M)))
        print('   forbidden words outside comments:', bad or 'none'); print('   other declarations and options:', other)
        imp_f = sorted(re.findall(r'^import\s+(\S+)', fixed, flags=re.M)); imp_d = sorted(re.findall(r'^import\s+(\S+)', done, flags=re.M)); print('   imports fixed', imp_f, '| finished', imp_d)
