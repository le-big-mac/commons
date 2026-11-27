"""Second candidate, "The machine": the order of the paragraphs after the picture, the points sentence against the fold, and the pieces of the old long paragraph.
usage: second_b.py PUBLIC_SOURCE CANDIDATE2_SOURCE CANDIDATE2_BUILT"""
import re, sys, html
pub, c2, built = (open(p, encoding='utf-8').read() for p in sys.argv[1:4])
text = lambda h: ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', h)).split())
sec = c2[c2.index('<h2>The machine</h2>'):c2.index('<h2>Why two defections and not one</h2>')]
blocks = re.findall(r'<(p|figure)[ >](.*?)</\1>', sec, re.S)
print('"The machine", block by block:')
for k, (tag, b) in enumerate(blocks): print(f'  {k + 1}. <{tag}> {len(text(b).split()):3d} words: {text(b)[:70]!r}')
fold = pub[pub.index('<h2>Why two defections and not one</h2>'):pub.index('<h2>Watch it happen</h2>')]
points = 'If one player defects and the other cooperates, the defector gets 5 points and the cooperator gets nothing; when both cooperate each gets 3, and when both defect each gets 1.'
print('the points paragraph is exactly the points sentence:', any(text(b) == points for _, b in blocks), '; that sentence is in the folded section word for word:', points in fold)
print('"collects the 5 only every third round" in the folded section:', 'collects the 5 only every third round' in fold)
old_long = re.search(r'<p>(Those two rounds of defection.*?)</p>', pub, re.S).group(1)
new_three = ' '.join(text(b) for _, b in blocks[-3:])
import difflib
a, b = old_long.split(), new_three.split()
print('old long paragraph against the last three paragraphs now, word by word:')
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
    if tag != 'equal': print('    ', tag, '| old:', ' '.join(a[i1:i2]), '| now:', ' '.join(b[j1:j2]))
# links inside the built folds
for name in ("The same list in full, with what each found and how much of each I read", "How this page was written and read"):
    i = built.index('<summary>' + name + '</summary>'); f = built[i:built.index('</details>', i)]
    quoted = re.findall(r'"((?:The machine|Why two defections and not one|Watch it happen|What was already known|What I got wrong|A disagreement not settled|How far to trust this|For those who want to check|How this page was written and read))"', text(f))
    linked = re.findall(r'<a class="tosec"[^>]*>"(.*?)"</a>', f)
    print(f'in the fold {name[:30]!r}: section names in quotation marks {len(quoted)}, of which links {len(linked)}: {sorted(set(linked))}')
