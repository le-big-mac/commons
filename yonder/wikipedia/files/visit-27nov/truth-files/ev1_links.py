"""Evidence reading 1: the links of the candidate page against the records.
usage: python -I ev1_links.py candidate.html FETCHDIR revisions.txt
Reads the saved answers f1..f11 as data only (no code in them is run)."""
import sys, re, html, os, hashlib, time

cand = open(sys.argv[1], encoding='utf-8').read()
D = sys.argv[2]
revs = open(sys.argv[3], encoding='utf-8').read()

def rd(n):
    return open(os.path.join(D, n), 'rb').read()
def txt(b):
    t = b.decode('utf-8', 'replace')
    t = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', t, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', html.unescape(t))

print('== every link of the candidate, with the words it stands on, and whether it is inside a fold')
depth_marks = [(m.start(), +1) for m in re.finditer(r'<details', cand)] + [(m.start(), -1) for m in re.finditer(r'</details>', cand)]
def in_fold(p):
    return sum(d for q, d in depth_marks if q < p) > 0
links = []
for m in re.finditer(r'<a href="([^"]+)">(.*?)</a>', cand, flags=re.S):
    href = html.unescape(m.group(1)); words = re.sub(r'<[^>]+>', '', html.unescape(m.group(2)))
    links.append((href, words, in_fold(m.start())))
ext = [(h, w, f) for h, w, f in links if h.startswith('http')]
for h, w, f in ext:
    print('  %s | %s | %s' % ('fold' if f else 'OPEN', w[:80], h))
print('  external links: %d (distinct addresses: %d); internal: %d' % (len(ext), len(set(h for h, w, f in ext)), len(links) - len(ext)))

print('\n== the saved answers: times of the files themselves (UTC), sizes, first bytes')
for k in range(1, 12):
    p = os.path.join(D, 'f%d' % k); st = os.stat(p); b = rd('f%d' % k)
    print('  f%-2d %s  %8d bytes  %s  sha256 %s' % (k, time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(st.st_mtime)), st.st_size, b[:8], hashlib.sha256(b).hexdigest()[:16]))

print('\n== f1..f3: the three article revisions')
want = [('Letter_frequency', '1386775465'), ('Land_and_water_hemispheres', '1379511027'), ('Solar_eclipse_of_August_18,_1868', '1384898663')]
for k, (title, rid) in enumerate(want, 1):
    raw = rd('f%d' % k).decode('utf-8', 'replace')
    t = re.search(r'<title>(.*?)</title>', raw, flags=re.S)
    rv = re.findall(r'"wgRevisionId":(\d+)', raw); cur = re.findall(r'"wgCurRevisionId":(\d+)', raw); pn = re.findall(r'"wgPageName":"([^"]*)"', raw)
    asof = re.findall(r'Revision as of ([^<]{5,40})', raw)
    print('  f%d title=%r wgPageName=%s wgRevisionId=%s wgCurRevisionId=%s "Revision as of": %s' % (k, t.group(1) if t else None, pn, rv, cur, asof[:2]))
    print('     wanted: %s %s ; revision id found: %s ; page name matches: %s' % (title, rid, rid in rv, pn == [title]))
    href = 'https://en.wikipedia.org/w/index.php?title=%s&oldid=%s' % (title, rid)
    print('     link on the page: %s' % ([w for h, w, f in ext if h == href]))
    line = [l for l in revs.split('\n') if rid in l]
    print('     revisions.txt: %s' % line)

print('\n== f4, f5: the two rule pages')
for k, short in ((4, 'WP:AITALK'), (5, 'WP:AIBOT')):
    raw = rd('f%d' % k).decode('utf-8', 'replace'); t = txt(rd('f%d' % k))
    ti = re.search(r'<title>(.*?)</title>', raw, flags=re.S)
    pn = re.findall(r'"wgPageName":"([^"]*)"', raw); red = re.findall(r'"wgRedirectedFrom":"([^"]*)"', raw); frag = re.findall(r'"wgInternalRedirectTargetUrl":"([^"]*)"', raw)
    print('  f%d title=%r page=%s redirected from=%s target=%s' % (k, ti.group(1) if ti else None, pn, red, frag))
    for s in ['AI-generated comments are not permitted in discussions', 'are not permitted in discussions', 'always classified as', 'almost certainly be denied', 'almost certainly',
              'explanatory essay', 'This page is a supplement', 'supplement', 'guideline', 'LLM-generated', 'large language model', 'userspace', 'user space', 'approv']:
        print('     %-58r occurs %d' % (s, t.count(s)))
def ctx(t, s, n=260, maxn=3):
    out = []
    for m in list(re.finditer(re.escape(s), t))[:maxn]:
        out.append('...' + t[max(0, m.start() - n):m.end() + n] + '...')
    return out
t4 = txt(rd('f4')); t5 = txt(rd('f5'))
print('\n  -- f4 around "not permitted in discussions":')
for c in ctx(t4, 'not permitted in discussions', 500): print('    ', c)
raw4 = rd('f4').decode('utf-8', 'replace')
for m in re.finditer(r'<(h[2-4])[^>]*id="([^"]*)"[^>]*>(.*?)</\1>', raw4, flags=re.S):
    name = re.sub(r'<[^>]+>', '', m.group(3))
    if re.search(r'LLM|AI|language model|generated', name): print('     heading in f4:', m.group(1), m.group(2), '|', html.unescape(name))
for m in re.finditer(r'id="(AITALK|LLMTALK|[^"]*LLM[^"]*|[^"]*AI[A-Z]*)"', raw4): print('     anchor in f4:', m.group(1))
print('\n  -- f5 head, first 1500 characters of text after the title:')
i5 = t5.find('AI agents and the bot policy'); print('    ', t5[i5:i5 + 1500])
print('\n  -- f5 around "always classified as":')
for c in ctx(t5, 'always classified as', 500): print('    ', c)
print('\n  -- f5 around "almost certainly":')
for c in ctx(t5, 'almost certainly', 500): print('    ', c)
print('\n  -- f5 around "userspace":')
for c in ctx(t5, 'userspace', 300, 4): print('    ', c)

print('\n== f7: Numdam')
raw = rd('f7').decode('utf-8', 'replace'); t7 = txt(rd('f7'))
print('  title:', re.findall(r'<title>(.*?)</title>', raw, flags=re.S))
for s in ['ASENS_1870_1_7__99_0', 'Stephan', 'Voyage de la Commission française', '1870', '99-162', 'Annales scientifiques', 'Tome 7', 'Série 1']:
    print('     %-45r occurs %d' % (s, t7.count(s)))
print('  text head:', t7[:900])

print('\n== f8: the journal page of Supavit\'s article')
raw = rd('f8').decode('utf-8', 'replace'); t8 = txt(rd('f8'))
print('  title:', re.findall(r'<title>(.*?)</title>', raw, flags=re.S))
for m in re.finditer(r'<meta name="(citation_[a-z_]+|DC\.[A-Za-z.]+)"[^>]*content="([^"]*)"', raw):
    if m.group(1) in ('citation_title', 'citation_author', 'citation_journal_title', 'citation_volume', 'citation_issue', 'citation_firstpage', 'citation_lastpage', 'citation_date', 'citation_language', 'citation_pdf_url', 'citation_abstract_html_url', 'DC.Title', 'DC.Title.Alternative', 'DC.Language', 'DC.Identifier.pageNumber'):
        print('     meta %s = %s' % (m.group(1), html.unescape(m.group(2))[:200]))
for s in ['The 1868 Solar Eclipse: Some Considerations about Its Sources and Historiography', 'Supavit', 'Thavaraputta', 'Thammasat Journal of History', '34-57', '250140']:
    print('     %-80r occurs %d' % (s, t8.count(s)))

print('\n== f9 (ADS abstract):', len(rd('f9')), 'bytes; the page links ADS:', any('adsabs' in h or 'ui.adsabs' in h for h, w, f in links))
print('\n== f11: the capture of the web page')
raw = rd('f11').decode('utf-8', 'replace'); t11 = txt(rd('f11'))
print('  title:', re.findall(r'<title>(.*?)</title>', raw, flags=re.S | re.I))
print('  capture stamps in the file:', sorted(set(re.findall(r'web/(\d{14})', raw)))[:12])
for s in ['King Mongkut\'s prediction surpassed those of European scientists.', 'In fact, his calculations were better -- by about two seconds -- than those of the now exhausted French astronomers, who acknowledged his accuracy.',
          'L. Robert Morris, National Post, Toronto, Ontario, Canada, 22 December 2000', 'He died on his birthday, Oct. 18, 1868.', 'Descendants of Danyell Broadley de West Morton', 'Siam Then', 'See Bradley, W.L.']:
    print('     %-60r occurs %d' % (s[:60], t11.count(s)))
if len(sys.argv) > 4:
    old = open(sys.argv[4], 'rb').read()
    print('  saved capture of 26 November: %d bytes; today\'s f11: %d bytes; identical: %s; text identical: %s' % (len(old), len(rd('f11')), old == rd('f11'), txt(old) == t11))
