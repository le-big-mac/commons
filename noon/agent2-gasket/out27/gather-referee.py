"""gather-referee.py -- copies the referee's own programs and what they printed from its working folder (~/referee-gasket-27, mine,
not published) into referee27/its-files/, and writes there a list of what is copied and what is not.   python -I out27/gather-referee.py
Not copied: its files of counts (649 MB), the paper's source it downloaded, its copies of my page (whole, and with one thing broken:
each change is described in its reports), and the page's answers it saved for its comparisons (5 MB each time)."""
import os, shutil
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); SRC = os.path.expanduser('~/referee-gasket-27'); DST = os.path.join(HERE, 'referee27', 'its-files')
WANT = [
 ('', ['gasket.c', 'analyse.py', 'check_geo.py', 'q5check.py', 'setcheck.py', 'types.py'], 'the blind step: its enumerator in C, the reading of its count files, two checks of the enumerator (circles placed in the plane; an undirected search on sets of curvatures), the recount of circles by size, and its working of the types'),
 ('out>printed', ['analysis_1e6_final.txt', 'analysis_1e7_final.txt', 'analysis_1e8.txt', 'analysis_3e7.txt', 'sporadic_1e6.txt', 'sporadic_1e7.txt'], 'what those printed: the tables of its blind report, and its lists for (-3, 5, 8, 8)'),
 ('read', ['drive.js', 'compare.py', 'compare.out', 'quick.js', 'testruns.log'], 'the reading: its script that drives the page, its comparison of what the page printed with its own program (46,949 comparisons), and the log of my test run on its broken copies'),
 ('read3', ['compare3.py', 'compare3.out', 'quick3.js', 'quick4.js', 'testruns.log', 'corner.png'], 'the check of the mending: the comparison run again, the corner case (the picture dragged past a corner of the outer circle), its broken copies run against my test'),
 ('read4', ['compare4.py', 'compare4.out', 'quick5.js', 'quick5.out', 'testruns.log'], 'the last check: the comparison run again with the edge views and the five forms of the fourth-power passage'),
 ('read5', ['compare5.py', 'compare5.out', 'quick6.js', 'quick6.out', 'testruns.log'], 'the fifth report: the comparison on the page as it now stands (47,115 comparisons)'),
]
def main():
    os.makedirs(DST, exist_ok=True); lines = ['# The referee\'s own files', '', 'Copied by `out27/gather-referee.py` from the referee\'s working folder, as it left them. The programs are the referee\'s (a fresh instance of the model), not mine; I have changed nothing in them. Paths inside them are those of the machine they ran on.', '']
    n = 0
    for sub, names, what in WANT:
        sub, to = (sub.split('>') + [sub])[:2] if '>' in sub else (sub, sub)      # the referee's folder `out` is kept here as `printed` (the public build leaves out folders named out)
        os.makedirs(os.path.join(DST, to), exist_ok=True); lines.append('- `%s`: %s. Files: %s.' % (to + '/' if to else '(top)', what, ', '.join('`%s`' % x for x in names)))
        for x in names: shutil.copyfile(os.path.join(SRC, sub, x), os.path.join(DST, to, x)); n += 1
    lines += ['', 'Not copied: its files of counts (649 MB; the tables above are what it read from them), the source of the paper that it downloaded, its copies of my page whole and with one thing broken (each change is described in its reports), and the page\'s answers that it saved for its comparisons (about 5 MB each time).', '']
    open(os.path.join(DST, 'CONTENTS.md'), 'w', encoding='utf-8').write('\n'.join(lines)); print(n, 'files copied to referee27/its-files/')
if __name__ == '__main__':
    main()
