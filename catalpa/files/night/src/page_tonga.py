# Assembles ~/site/tonga.html from page/tonga.src.html, the folds kept beside it and the table written by
# src/tonga_page.py, and copies the page's two pictures into the site folder.
B = '/home/agent1/night/'
s = open(B + 'page/tonga.src.html', encoding='utf-8').read()
ALT_MONTHS = "A line chart from 2021 to 2024, month by month. The middle of eleven southern meters stays within 11 per cent of no change through 2021 and to March 2022, rises to 25 in April and May 2022 and to 60, 50 and 49 in June, July and August, drops to 8 in October 2022, is back near 40 in November and December, stays between 17 and 34 until July 2023, and is near no change from September 2023, with 13 below in December 2023. Single southern meters reach 150 per cent and more; one leaps to 75 in November 2021 and sinks to 43 below at the end of 2024. The middle of twenty northern meters stays within 11 of no change throughout. A dashed line marks the eruption of 15 January 2022."
ALT_LATITUDE = "A dot for each of 46 meters by latitude. Eleven southern meters, between 21 and 41 degrees south, stand 17 to 86 per cent brighter. The northern meters, between 28 and 46 degrees north, cluster within 10 of no change; three stand at about 30 to 35, and one, a meter that broke, is off the top of the chart and labelled so. Réunion, at 74, and New Zealand, at 17, are named."
for tag, text in (('<!--ALT_MONTHS-->', ALT_MONTHS), ('<!--ALT_LATITUDE-->', ALT_LATITUDE), ('<!--LO-->', '17'), ('<!--HI-->', '86')):
    assert s.count(tag) == 1, tag; s = s.replace(tag, text)
for tag, fn in (('<!--T_TONGA-->', 't_tonga.html'), ('<!--FOLD_SOUTH-->', 'page/tfold_south.html'), ('<!--FOLD_BETWEEN-->', 'page/tfold_between.html'), ('<!--FOLD_DIM-->', 'page/tfold_dim.html'), ('<!--PLACES_TEXT-->', 'page/tonga_places.html'),
                ('<!--METHOD-->', 'page/tonga_method.html'), ('<!--PRINT-->', 'page/tonga_print.html'), ('<!--SOURCES-->', 'page/tonga_sources.html')):
    assert s.count(tag) == 1, tag; s = s.replace(tag, open(B + fn, encoding='utf-8').read().strip())
TRUST = ' The same copy then read this page against the evidence, and two others read it as visitors on a phone.'
READERS = open(B + 'page/tonga_readers.html', encoding='utf-8').read().strip()
for tag, text in (('<!--READERS-->', READERS), ('<!--TRUST-->', TRUST)):
    assert s.count(tag) == 1, tag; s = s.replace(tag, text)
assert '<!--' not in s, s[s.index('<!--'):s.index('<!--') + 60]
open('/home/agent1/site/tonga.html', 'w', encoding='utf-8').write(s); print('tonga.html', len(s), 'bytes')
import shutil
for f in ('tonga-every-month.png', 'tonga-latitude.png'): shutil.copy(B + 'img/' + f, '/home/agent1/site/img/' + f)
print('pictures copied to the site folder')
