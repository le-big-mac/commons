"""The rule paragraph of "The machine": split after its second sentence, no word changed? And the three added sentences against the folded section.
usage: split.py OLD_SOURCE NEW_SOURCE"""
import re, sys
old, new = (open(p, encoding='utf-8').read() for p in sys.argv[1:3])
po = re.search(r'<p>(The machine defects until.*?)</p>', old, re.S).group(1)
p1 = re.search(r'<p>(The machine defects until.*?)</p>', new, re.S).group(1)
p2 = re.search(r'<p>(So two of these machines.*?)</p>', new, re.S).group(1)
print('old paragraph == new first paragraph + space + new second paragraph:', po == p1 + ' ' + p2)
print('new first paragraph stands before the first picture:', new.index(p1) < new.index('<img src="img/handshake-strip.png"') < new.index(p2))
print('sentences in the new first paragraph:', len(re.split(r'(?<=\.)\s+', p1)))
fold = old[old.index('<h2>Why two defections and not one</h2>'):old.index('<h2>Watch it happen</h2>')]
for s in ('A player who always defects does get through the opening, but gains nothing by it.',
          'If one player defects and the other cooperates, the defector gets 5 points and the cooperator gets nothing; when both cooperate each gets 3, and when both defect each gets 1.',
          'Against this machine the player who always defects collects the 5 only every third round (the third game above) and falls behind.',
          'the player who always defects collects the 5 only every third round (the third game above) and falls behind.'):
    print(repr(s[:60] + '...'), '| in the new open paragraph:', s in new[:new.index('<h2>Why two defections')], '| word for word in the folded section:', s in fold)
print('"gains nothing" anywhere in the old page:', 'gains nothing' in old, '; in the visitor\'s report:', 'gains nothing' in open(sys.argv[3], encoding='utf-8').read())
