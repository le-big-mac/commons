"""Evidence reading 2: the new statements of the second candidate against the records (all downloads read as data).
usage: python -I ev2_records.py"""
import json, os, re, time, hashlib, html, subprocess

D = '/home/agent3/downloads/'
def utc(p): return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(os.stat(p).st_mtime))
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()

print('== "each of the three articles still stood at the revision read here" / "looked up at 12:01 UTC"')
now = D + 'wiki-now-27nov.0Fd5/'
read = {'Letter_frequency': (1386775465, D + 'wiki-Letter_frequency_/page.wiki'), 'Land_and_water_hemispheres': (1379511027, D + 'landhemi-wiki/lw.wiki'),
        'Solar_eclipse_of_August_18,_1868': (1384898663, D + 'wiki-eclipse1868-25nov/page.wiki')}
for t, (rid, saved) in read.items():
    r = json.load(open(now + t + '.rev.json', encoding='utf-8')); rev = next(iter(r['query']['pages'].values()))['revisions'][0]
    same_text = open(now + t + '.wiki', 'rb').read() == open(saved, 'rb').read()
    print('  %-34s current revision %d (of %s); the revision read %d; same: %s; wikitext byte for byte the saved copy: %s; files of %s and %s UTC'
          % (t, rev['revid'], rev['timestamp'], rid, rev['revid'] == rid, same_text, utc(now + t + '.rev.json')[11:], utc(now + t + '.wiki')[11:]))

print('\n== "a scan of about 4 MB"')
w = D + 'affholder-whole.g9UT/176-article-15.pdf'
print('  fetched whole: %d bytes, file of %s UTC; same sha256 as the copy of 21 November: %s' % (os.stat(w).st_size, utc(w), sha(w) == sha(D + 'affholder/affholder2002.pdf')))

print('\n== "the scan\'s machine-read text" (Stephan)')
p = D + 'stephan-1870/paper.pdf'
out = subprocess.run(['pdftotext', '-layout', p, '-'], capture_output=True).stdout
print('  paper.txt is byte for byte what pdftotext -layout gives from the text layer of paper.pdf:', out == open(D + 'stephan-1870/paper.txt', 'rb').read())
info = subprocess.run(['pdfinfo', p], capture_output=True).stdout.decode('utf-8', 'replace')
print('  the PDF\'s own record of who made it:', [l for l in info.split('\n') if l.startswith(('Creator', 'Producer'))])

print('\n== the 2021 paper (saved text): what stands near the heading "King Rama IV\'s Eclipse Calculations"')
t = open('/srv/commons/wander-agent1/lit/orchiston2021/o_raw.txt', encoding='utf-8', errors='replace').read()
t = re.sub(r'\s+', ' ', re.sub(r'-\s*\n\s*', '', t))
for s in ["2.2 King Rama IV’s Eclipse Calculations", "Figure 4: A traditional Thai calculation for the total solar eclipse of 18 August 1868", "The Thai solar eclipse calculation above is not particularly good, it does not predict a total eclipse",
          "the most important eclipse that King Rama IV ever calculated the details of was the total solar eclipse of 18 August 1868", "his calculations of the time of the eclipse having proved extremely correct",
          "first contact according to King Rama IV’s calculation and prediction"]:
    i = t.find(s); print('  %-5s at %6d | %s' % (i >= 0, i, s[:105]))
print('  page footers ("NNN Wayne Orchiston") near them:', [(m.group(1), m.start()) for m in re.finditer(r'(\d{3}) Wayne Orchiston and Darunee', t)][:6])

print('\n== the article (saved wikitext): the lead\'s sentence, and what the calculations are said to be of')
w = open(D + 'wiki-eclipse1868-25nov/page.wiki', encoding='utf-8').read()
i = w.index('whose calculations were acknowledged as more precise'); j = w.index('.', i)
print('  the lead\'s sentence ends: %r' % w[i:j + 60])
print('  a <ref> within the lead\'s sentence or straight after it:', '<ref' in w[w.rfind('\n', 0, i):j + 6])
print('  "The calculations were correct as to the place, time, and type of the solar eclipse that would occur." occurs', w.count('The calculations were correct as to the place, time, and type of the solar eclipse that would occur.'))
print('  citation fields: title "Descendants of Danyell Broadley de West Morton":', w.count('title= Descendants of Danyell Broadley de West Morton'), '; "Siam then" and 1981 in the format field:', bool(re.search(r"format= 964-word excerpt from ''Siam then[^|]*1981", w)), '; author2-link William Lee Bradley:', w.count('author2-link= William Lee Bradley'))

print('\n== the capture: the words before the sentence with the two seconds')
c = open(D + 'wiki-bradley-excerpt-archive/page.html', encoding='utf-8', errors='replace').read()
c = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', c)))
i = c.find('In fact, his calculations'); print('  ...%s' % c[i - 150:i + 60])
print('  "Siam (now Thailand)" occurs', c.count('Siam (now Thailand)'))

print('\n== files the page names, in the built page\'s folder and in the page\'s source folder')
for f in ['visit-27nov/visit-1.md', 'visit-27nov/visit-2.md', 'visit-27nov/still_there.out']:
    print('  %-30s built: %-5s source: %s' % (f, os.path.exists('/home/agent3/site/wiki-new-preview2/wikipedia/files/' + f), os.path.exists('/srv/commons/wikipedia-notes-agent3/' + f)))
