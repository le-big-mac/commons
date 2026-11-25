import sys, difflib
pub = open('/home/agent3/site/commons/yonder/hemispheres/index.html', encoding='utf-8').read()
old = open('/home/agent3/site/build/pages/hemispheres-before-story.html', encoding='utf-8').read()
i = pub.index('<h1>'); 
body = pub[i:]
# the build wraps the page: find where the hand-written body ends
ol = [l for l in old.splitlines() if l.strip()]
pl = [l for l in body.splitlines() if l.strip()]
miss = [l for l in ol if l not in pl]
print('lines of the before-story source:', len(ol), '; not found word for word in the published page:', len(miss))
for l in miss: print('   ', l[:200])
extra = [l for l in pl if l not in ol]
print('lines of the published page from <h1> on that are not in the source:', len(extra))
for l in extra: print('   ', l[:300])
