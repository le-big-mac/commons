"""Do the three articles, as they stand now, still say what the notes quote?  Reads the wikitext fetched today and the
revision data (untrusted downloads: read as data).  usage: python -I still_there.py FOLDER"""
import sys, json, os, re
d = sys.argv[1]
titles = {'Letter_frequency': [], 'Land_and_water_hemispheres': [], 'Solar_eclipse_of_August_18,_1868': []}
read = {'Letter_frequency': 1386775465, 'Land_and_water_hemispheres': 1379511027, 'Solar_eclipse_of_August_18,_1868': 1384898663}
quotes = {
 'Letter_frequency': ['13.702', '1.973', '3.927', '1.433', '0.515', '0.937', '0.813', '0.708', '13.101', '1.281', '0.453', '0.136', '2.813', 'Cite check'],
 'Land_and_water_hemispheres': ['is centered in Metropolitan France', 'In 2002, the center of the land hemisphere was calculated as a central area spanning two focal points around Brittany and the Mediterranean Sea between the Balearic Islands and Catalonia', '176-article-15.pdf', '173–174', '43–58'],
 'Solar_eclipse_of_August_18,_1868': ['the French expedition led by', 'Pierre Janssen', 'His calculations were better — by about two seconds — than those of the French astronomers, who acknowledged his accuracy', 'were acknowledged as more precise', 'on 1 October 1868', 'Montes-Bradley', 'Guntur'],
}
for t in titles:
    r = json.load(open(os.path.join(d, t + '.rev.json'), encoding='utf-8'))
    page = next(iter(r['query']['pages'].values())); rev = page['revisions'][0]
    w = open(os.path.join(d, t + '.wiki'), encoding='utf-8').read()
    plain = re.sub(r"'''?|\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", lambda m: m.group(1) or '', w)
    print(t.replace('_', ' '), '| current revision', rev['revid'], rev['timestamp'], '| the revision the note read:', read[t], '| same revision:', rev['revid'] == read[t])
    for q in quotes[t]:
        n = w.count(q) + (plain.count(q) if w.count(q) == 0 else 0)
        print('   ', 'FOUND' if n else 'NOT FOUND', repr(q[:90]))
