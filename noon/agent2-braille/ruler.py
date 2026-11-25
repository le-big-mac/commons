"""ruler.py: the instrument against the authority. Every example in chapter 10 (Contractions) of the Rules of Unified English
Braille that prints a word or phrase with its braille beside it, put through the translator (liblouis) and compared.
    /usr/bin/python3 -I ruler.py ~/braille-data/rulebook/text.txt   ->  ruler.out (printed), ruler.json
The examples are chosen by the rulebook to show where the rules bite, so the share that disagree here is far above what running
prose would show; it is a list of the translator's known hard places, not its error rate on a novel."""
import json, os, re, sys
import louis
UEB = 'en-ueb-g2.ctb'; B = '⠀-⣿'
def ub(s): return louis.translateString([UEB], s, mode=louis.dotsIO | louis.ucBrl).replace('⠀', ' ')
def pairs(text):
    """(print, braille) for each example of chapter 10: a chunk of a line that is words followed by as many braille words"""
    lines = text.split('\n'); a = max(i for i, l in enumerate(lines) if re.match(r'\s*10\.1\s+Alphabetic wordsigns\s*$', l)); b = max(i for i, l in enumerate(lines) if re.match(r'\s*Section 11\b', l))
    out = []
    for l in lines[a:b]:
        if not re.search('[%s]' % B, l): continue
        for chunk in re.split(r'\s{3,}', l.strip()):
            m = re.match(r"^([A-Za-z][A-Za-z'’.,;:!?\- ]*?)\s+((?:[%s]+ ?)+)$" % B, chunk)
            if not m: continue
            p, br = m.group(1).strip().replace('’', "'"), m.group(2).strip()
            if len(p.split()) == len(br.split()): out.append((p, br))
    return out
if __name__ == '__main__':
    ps = pairs(open(sys.argv[1], encoding='utf-8').read()); seen = set(); same = []; diff = []; emph = []; cut = []
    EMPH = re.compile('[\u2828\u2818\u2838\u2808][\u2802\u2806\u2804\u2836]')      # italic, bold, underline and script indicators: the print had a typeface that the text file has lost
    for p, br in ps:
        if (p, br) in seen: continue
        seen.add((p, br)); mine = ub(p)
        if mine == br: same.append((p, br, mine))
        elif EMPH.search(br): emph.append((p, br, mine))
        elif br.endswith('\u2824') and not p.endswith('-'): cut.append((p, br, mine))     # a word shown divided at a line's end: only its first part is on the line, and a division may change the contraction
        else: diff.append((p, br, mine))
    print('%d examples in chapter 10 with their braille beside them.' % len(seen))
    print('   the translator gives the rulebook\'s braille: %d' % len(same))
    print('   set aside, the print had a typeface (italic, bold) that the text file has lost: %d' % len(emph))
    print('   set aside, a word shown divided at a line\'s end, which a running text never is here: %d (in %d of them the translator\'s whole word begins with the rulebook\'s first part)' % (len(cut), sum(m.startswith(b[:-1]) for _, b, m in cut)))
    print('   the translator gives something else: %d' % len(diff))
    for p, br, mine in diff: print('      %-26s rulebook %-24s translator %s' % (p, br, mine))
    plain = [d for d in diff if d[0].isalpha() and d[0].islower()]
    print('   of those, ordinary words in small letters: %d (%s); the rest have capitals inside, are initials, stammers, spelt-out or syllabled words, or a fragment' % (len(plain), ', '.join(d[0] for d in plain)))
    json.dump(dict(n=len(seen), same=len(same), emphasis=len(emph), divided=len(cut), diff=diff, plain=[d[0] for d in plain]), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ruler.json'), 'w'), ensure_ascii=False, indent=1)
