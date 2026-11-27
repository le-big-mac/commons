"""Evidence reading 1: the talk page of "Land and water hemispheres" as saved on 26 November 2026 by a search made for
another study of the same author (read as data): does it speak of what note 2 is about?
usage: python -I ev1_talk.py TALK.wiki"""
import sys, re, os, time
p = sys.argv[1]; t = open(p, encoding='utf-8').read()
print('file:', p, '|', len(t), 'characters | time of the file (UTC):', time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(os.stat(p).st_mtime)))
print('section headings:', re.findall(r'^==+\s*(.*?)\s*==+\s*$', t, flags=re.M))
print('archive boxes or links to archives:', len(re.findall(r'(?i)archive', t)))
print('latest signature dates:', sorted(set(re.findall(r'\d{1,2} \w+ (20\d\d) \(UTC\)', t)))[-3:])
for s in ['Affholder', 'Mediterranean', 'Méditerranée', 'Tarragon', 'Catalonia', 'Balearic', '2002', '2003', '176', '173', 'Monde des Cartes', 'maxim', 'Metropolitan France', 'Dumet', 'Nantes', 'Berget', 'Boggs']:
    print('  %-22r occurs %d' % (s, len(re.findall(re.escape(s), t, flags=re.I))))
