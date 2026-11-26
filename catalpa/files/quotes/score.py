# Scores the sealed lines of expectations.md from verdicts.tsv (my verdicts, one row a quotation) and writes the counts.   Run: python3 -I score.py
# verdicts.tsv columns (tab-separated, first line a header): id, verdict (V A M U), where (the source in a few words), seen (page image / full text / text layer / secondary),
#   wording (what differs, or "as listed"), name (how the list spells the name, if wrongly), first (my verdict from the first reader's report alone, for the eight looked up twice),
#   second (my verdict from the second reader's report alone)
import json, csv, math, sys
S = json.load(open('/home/agent1/quotes/sample.json')); B = json.load(open('/home/agent1/quotes/batches.json'))
forty = [s['id'] for s in S['sample']]; mag = [s['id'] for s in S['magnets']]; allq = {s['id']: s for s in S['sample'] + S['magnets']}
V = {int(r['id']): r for r in csv.DictReader(open('/home/agent1/quotes/verdicts.tsv', encoding='utf-8'), delimiter='\t')}
missing = [i for i in forty + mag if i not in V]
if missing: print('no verdict yet for:', missing)
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d; return 100 * (c - h), 100 * (c + h)
def counts(ids): return {v: sum(1 for i in ids if i in V and V[i]['verdict'] == v) for v in 'VAMU'}
out = []
def P(s=''): print(s); out.append(s)
c = counts(forty); n = sum(c.values())
P(f'THE FORTY ({n} with a verdict):')
for v, name in (('V', 'verified'), ('A', 'altered'), ('M', 'misattributed'), ('U', 'untraced')):
    lo, hi = wilson(c[v], n) if n else (0, 0); P(f'   {name:14s} {c[v]:2d} of {n}  = {100 * c[v] / max(n, 1):4.1f}%   (95% range for the whole list of 513, by Wilson\'s rule: {lo:.0f} to {hi:.0f}%)')
bad = c['A'] + c['M']; lo, hi = wilson(bad, n) if n else (0, 0); P(f'   altered or misattributed together: {bad} of {n} = {100 * bad / max(n, 1):.1f}%  ({lo:.0f} to {hi:.0f}%)')
names = [i for i in forty if i in V and V[i].get('name', '').strip()]; P(f'   names misspelt or garbled in the list: {len(names)} of {n}: ' + '; '.join(f"{allq[i]['author']} ({V[i]['name']})" for i in names))
cm = counts(mag); nm = sum(cm.values())
P(f'\nTWAIN AND EINSTEIN ({nm} with a verdict): ' + ', '.join(f'{k} {cm[k]}' for k in 'VAMU'))
for a in ('Mark Twain', 'Albert Einstein'):
    ca = counts([i for i in mag if allq[i]['author'] == a]); P(f'   {a}: ' + ', '.join(f'{k} {ca[k]}' for k in 'VAMU'))
P('\nTHE SEALED LINES:')
def line(tag, text, ok): P(f'   {tag} {"HELD  " if ok else "FAILED"} {text}')
line('Q1', f'V between 17 and 26 of the forty: {c["V"]}', 17 <= c['V'] <= 26)
line('Q2', f'M between 2 and 7: {c["M"]}   [held by one row, 339, which my own further attempt moved from U to M when I knew the count stood at one]', 2 <= c['M'] <= 7)
line('Q3', f'U between 5 and 12: {c["U"]}   [held at its edge by one row, 310, which my own further attempt moved from U to V when I knew the count stood at thirteen]', 5 <= c['U'] <= 12)
line('Q4', f'A between 3 and 8: {c["A"]}', 3 <= c['A'] <= 8)
line('Q5', f'at least 9 of the fifteen Twain and Einstein are V: {cm["V"]}', cm['V'] >= 9)
line('Q6', f'"Only two things are infinite..." is not V (the sealed sheet itself calls it doubtful from memory, so this was as good as known): {V.get(451, {}).get("verdict", "?")}', V.get(451, {}).get('verdict') in ('A', 'M', 'U'))
line('Q7', f'"Never discourage anyone..." (Plato) is M or U: {V.get(433, {}).get("verdict", "?")}', V.get(433, {}).get('verdict') in ('M', 'U'))
tw = [i for i in B['twice'] if i in V and V[i].get('first') and V[i].get('second')]; agree = sum(1 for i in tw if V[i]['first'] == V[i]['second'])
line('Q8', f'two readings of the same eight agree on at least 6: {agree} of {len(tw)}  [my own verdicts, and the second written with the first known]  (' + ', '.join(f"{i}: {V[i]['first']}/{V[i]['second']}" for i in tw) + ')', agree >= 6 and len(tw) == 8)
def alt(cols, ids):
    def v(i):
        for c in cols:
            if V[i].get(c): return V[i][c]
        return V[i]['verdict']
    return {x: sum(1 for i in ids if v(i) == x) for x in 'VAMU'}
fmt = lambda a: f"V {a['V']}, A {a['A']}, M {a['M']}, U {a['U']}"
P('\nTHE NOT TRACED AMONG THE FORTY, by what was seen:')
u = [i for i in forty if V[i]['verdict'] == 'U']
sec = [i for i in u if V[i].get('secondary')]; fr = [i for i in u if V[i].get('fragments')]; rest = [i for i in u if i not in sec and i not in fr]
P(f"   quoted, with the name of the work, by a careful printed source that was read: {len(sec)} (ids {', '.join(map(str, sec))})")
P(f"   the words seen only in search fragments, which point to a verdict: {len(fr)} (ids {', '.join(map(str, fr))})")
P(f"   neither: {len(rest)} (ids {', '.join(map(str, rest))})")
P('\nOTHER WAYS OF COUNTING THE FORTY (verdicts as above unless the row says otherwise):')
P(f"   to the letter (any word that differs from the source, or any cut that is not at the end of a sentence, makes it altered): {fmt(alt(['letter'], forty))}")
P(f"   counting a careful printed quotation of the author that names the work as if the work had been read: {fmt(alt(['secondary'], forty))}")
P(f"   counting search fragments as well: {fmt(alt(['fragments', 'secondary'], forty))}")
bef = {v: sum(1 for i in forty if (V[i].get('before') or V[i]['verdict']) == v) for v in 'VAMU'}; P(f"   before my own further attempts: {fmt(bef)}   (rows they moved: " + ', '.join(f"{i} {V[i]['before']}->{V[i]['verdict']}" for i in forty if V[i].get('before')) + ')')
P(f"   Twain and Einstein, the fifteen: as above {fmt(counts(mag))}; to the letter {fmt(alt(['letter'], mag))}; counting careful printed quotations {fmt(alt(['secondary'], mag))}; fragments as well {fmt(alt(['fragments', 'secondary'], mag))}")
chars = [32, 77, 367, 80, 83, 138, 258, 424, 215, 495, 184, 433]      # Anne (three times), Eve, a nun in House, Linus, Scalzi's narrator, Sartre's diarist, Pudd'nhead Wilson's Calendar (twice), Hank Morgan, the Eleatic Stranger
P(f"   lines that are a character's, a narrator's or a persona's in the author's book, strip or script, by my reading of the sources: {len(chars)} of the 54 (ids " + ', '.join(str(i) for i in sorted(chars)) + f"); of the forty: {sum(1 for i in chars if i in forty)}")
P('\nEVERY VERDICT (each quotation by its author and opening words; passages of more than eight words in quotation marks cut to five):')
import re
def incipit(text):
    w = text.split(); k = 5 if len(w) >= 10 else max(2, len(w) // 2); return ' '.join(w[:k]).rstrip(',;:—-.') + '…'
def cut(cell):
    def f(m):
        w = m.group(1).split(); return '"' + (m.group(1) if len(w) <= 8 else ' '.join(w[:5]).rstrip(',;:—-.') + '…') + '"'
    return re.sub(r'"([^"]+)"', f, cell)
for i in forty + [m for m in mag if m not in forty]:
    if i in V: P(f"   {i:3d} {V[i]['verdict']}  {allq[i]['author']}: {incipit(allq[i]['text'])}   <- {cut(V[i]['where'])} [{V[i]['seen']}]" + (f"; wording: {cut(V[i]['wording'])}" if V[i]['wording'].strip() not in ('', 'as listed') else ''))
open('/home/agent1/quotes/score.out', 'w').write('\n'.join(out) + '\n')
