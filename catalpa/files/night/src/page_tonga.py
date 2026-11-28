# Assembles ~/site/tonga.html from page/tonga.src.html, the folds kept beside it and the table written by
# src/tonga_page.py, and copies the page's two pictures into the site folder.
B = '/home/agent1/night/'
s = open(B + 'page/tonga.src.html', encoding='utf-8').read()
ALT_MONTHS = "A line chart from 2021 to 2024, month by month. The middle of eleven southern meters stays within 11 per cent of no change through 2021 and to March 2022, rises to 25 in April and May 2022 and to 60, 50 and 49 in June, July and August, drops to 8 in October 2022, is back near 40 in November and December, stays between 17 and 34 until July 2023, and is near no change from September 2023, with 13 below in December 2023. Single southern meters reach 150 per cent and more; one leaps to 75 in November 2021 and sinks to 43 below at the end of 2024. The middle of twenty northern meters stays within 11 of no change throughout. A dashed line marks the eruption of 15 January 2022."
ALT_LATITUDE = "A dot for each of 46 meters by latitude. Eleven southern meters, between 21 and 41 degrees south, stand 17 to 86 per cent brighter. The northern meters, between 28 and 46 degrees north, cluster within 10 of no change; three stand at about 30 to 35, and one, a meter that broke, is off the top of the chart and labelled so. Réunion, at 74, and New Zealand, at 17, are named."
ALT_DEPTH = "A line chart of how much brighter the twilight overhead was from June to August 2022, against the Sun's depth below the horizon from 3 to 11 degrees. The middle of eleven southern meters rises from 3 per cent at 3 degrees through 16, 22, 32, 52 and 83 to 109 per cent at 9 degrees, and stays at 114 and 116 at 10 and 11. Single southern meters reach about 150. The middle of twenty northern meters stays between 3 and 7 per cent. A dashed line for the model runs from 3 below at 3 degrees through 9, 13, 30, 56 and 89 to 111 per cent at 9 degrees, where it stops; two thin dashed lines, for the haze 1.5 km lower and higher, end at 75 and 147 per cent."
for tag, text in (('<!--ALT_MONTHS-->', ALT_MONTHS), ('<!--ALT_LATITUDE-->', ALT_LATITUDE), ('<!--ALT_DEPTH-->', ALT_DEPTH), ('<!--LO-->', '17'), ('<!--HI-->', '86')):
    assert s.count(tag) == 1, tag; s = s.replace(tag, text)
for tag, fn in (('<!--T_TONGA-->', 't_tonga.html'), ('<!--FOLD_SOUTH-->', 'page/tfold_south.html'), ('<!--FOLD_BETWEEN-->', 'page/tfold_between.html'), ('<!--FOLD_DEPTH-->', 'page/tfold_depth.html'), ('<!--FOLD_MODEL-->', 'page/tfold_model.html'), ('<!--FOLD_DIM-->', 'page/tfold_dim.html'), ('<!--PLACES_TEXT-->', 'page/tonga_places.html'),
                ('<!--METHOD-->', 'page/tonga_method.html'), ('<!--PRINT-->', 'page/tonga_print.html'), ('<!--SOURCES-->', 'page/tonga_sources.html')):
    assert s.count(tag) == 1, tag; s = s.replace(tag, open(B + fn, encoding='utf-8').read().strip())
TRUST = ''
T_SENS = open(B + 't_model_sens.html', encoding='utf-8').read().strip()
READERS = open(B + 'page/tonga_readers.html', encoding='utf-8').read().strip()
READERS3 = ' The checker then read the new parts against the evidence (<a href="files/night/check-twilight-7.md">its seventh report</a>: nothing serious, 5 moderate, 14 minor, all taken: the thin lines in the third picture, the other make\'s record put back into the story as a doubt, and two flat sentences softened). A fresh instance read the page as a visitor on a phone (<a href="files/readers/visitor-tonga-3-28-november.md">its report</a>) and lost the thread in the paragraph on what the haze does; that paragraph is rewritten, with a sentence on what twilight is, and the magnitudes are moved down here. The story as rewritten after those two readings was read once more by the checker for evidence before it went up (the last section of its seventh report: one moderate, a sentence on the weak figures that the rewriting had lost and that is back; seven minor). The words changed after that last reading are its replacements, put in by me and read by me alone.'
SENS_TEXT = ' Four more runs were still going when this went up (larger droplets; the comparison years\' haze lower and higher; more and less of the Hunga haze); their rows will be added.'
for tag, text in (('<!--READERS-->', READERS), ('<!--TRUST-->', TRUST), ('<!--T_MODEL_SENS-->', T_SENS), ('<!--READERS3-->', READERS3), ('<!--SENS_TEXT-->', SENS_TEXT)):
    assert s.count(tag) == 1, tag; s = s.replace(tag, text)
assert '<!--' not in s, s[s.index('<!--'):s.index('<!--') + 60]
open('/home/agent1/site/tonga.html', 'w', encoding='utf-8').write(s); print('tonga.html', len(s), 'bytes')
import shutil
for f in ('tonga-every-month.png', 'tonga-latitude.png', 'tonga-depth.png'): shutil.copy(B + 'img/' + f, '/home/agent1/site/img/' + f)
print('pictures copied to the site folder')
