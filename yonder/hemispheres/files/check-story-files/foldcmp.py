import sys, re, difflib
cur = open('/home/agent3/site/build/pages/hemispheres.html', encoding='utf-8').read()
old = open('/home/agent3/site/build/pages/hemispheres-before-story.html', encoding='utf-8').read()
i = cur.index('<details class="fold">')
fold = cur[i:]
print('--- head of before-story page')
print(old[:1500])
print('--- line counts', len(fold.splitlines()), len(old.splitlines()))
fl = fold.splitlines()
ol = old.splitlines()
for l in difflib.unified_diff(ol, fl, 'before-story', 'fold', lineterm='', n=0):
    print(l[:3000])
