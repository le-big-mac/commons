# One further attempt for every row left without a page of the author's own: ask the Internet Archive's catalogue for a copy of the named work that can be read without borrowing.
import json, urllib.parse, urllib.request, time, sys
UA = 'reading-check/1.0'
ROWS = [(305, 'Klee', 'title:(tagebücher OR diaries) AND creator:(klee, paul)'), (308, 'Westerfeld', 'title:("last days") AND creator:(westerfeld)'), (414, 'Will', 'title:("statecraft as soulcraft")'),
        (483, 'Deval', 'title:("afin de vivre") AND creator:(deval)'), (185, 'Carter', 'title:("women in the news") AND year:[1980 TO 1982]'), (28, 'La Grange', 'title:(pensées) AND creator:("la grange") AND year:[1870 TO 1880]'),
        (272, 'Rand', 'title:("virtue of selfishness")'), (310, 'Luce', 'title:("vanity fair") AND year:[1930 TO 1931]'), (222, 'Preece', 'title:("lighting by electricity") AND year:[1879 TO 1880]'),
        (140, 'Peter', 'title:("peter prescription")'), (192, 'Einstein', 'title:(gelegentliches) AND creator:(einstein)')]
out = []
for i, who, q in ROWS:
    url = 'https://archive.org/advancedsearch.php?q=' + urllib.parse.quote(q) + '&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=year&fl%5B%5D=collection&fl%5B%5D=mediatype&rows=40&output=json'
    try:
        raw = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60).read()
        open(f'/home/agent1/quotes/lit/second/{i}-ia-catalogue.json', 'wb').write(raw); docs = json.loads(raw)['response']['docs']
    except Exception as e:
        out.append(f'{i} {who}: request failed ({e})'); continue
    texts = [d for d in docs if d.get('mediatype') == 'texts']
    openc = [d for d in texts if not any(c in ('inlibrary', 'printdisabled', 'internetarchivebooks') for c in (d.get('collection') or []))]
    out.append(f"{i} {who}: {len(texts)} text items; readable without borrowing: {len(openc)}" + ''.join(f"\n      {d['identifier']} | {str(d.get('title'))[:70]} | {d.get('year')} | {str(d.get('collection'))[:70]}" for d in openc[:6]))
    time.sleep(1.5)
print('\n'.join(out)); open('/home/agent1/quotes/lit/second/second-attempts-catalogue.out', 'w').write('\n'.join(out) + '\n')
