"""Writes changes.json and checks it against the page source: each "old" exactly once, no two overlapping, tags still balanced."""
import json, re, sys
SRC = '/home/agent3/site/build/pages/hemispheres.html'
src = open(SRC, encoding='utf-8').read()
C = []
def ch(id_, old, new, why, must):
    C.append(dict(id=id_, old=old, new=new, why=why, must=must))

ch('lede-order',
   "Then I found that my answer had been in print since 2003.",
   "It turned out that my answer had been in print since 2003, and I had not known it.",
   "\"Then\" puts the finding after the result. By the file times the Wikipedia article that names the study and its two points was saved five minutes before the results were written, and the story itself says further down that it was read while the computation was running. Only the paper was fetched afterwards. The reader of the earlier page asked for the same correction on the card.",
   True)
ch('every-point',
   "I worked out, for every point on the globe, how much of the world's land lies in the half centred on that point.",
   "I worked out, for points all over the globe, how much of the world's land lies in the half centred on each.",
   "The search was on a lattice of points one degree apart, made finer near the best ones; not every point.",
   False)
ch('globes-caption',
   "Below: the same for people, in 2020.",
   "Below: the same for people, in 2020: the darker the orange, the more people live there, and grey is land with few or none.",
   "The lower pair has no key. Checked against the plotting program: orange where a cell of a fifth of a degree holds more than 100 people, darker with more; grey land otherwise.",
   False)
ch('map-alt',
   "A long dark band runs from the sea off Catalonia north-west to Brittany, with a darkest patch at each end. The southern patch, off Tarragona, is marked as the southern summit, with the most land, 81.2% of the world's; the northern one, beside Nantes and Île Dumet, is marked as the northern summit, 46,000 km² less.",
   "A long dark band runs from the sea off Catalonia north-west to Brittany, in two dark patches with a slightly lighter gap between them in the south-west of France. A white dot in each patch marks a summit. The southern dot, off Tarragona, lies in the darkest part of the map and is labelled as the southern summit, with the most land, 81.2% of the world's; the northern dot, between Nantes and Île Dumet, is labelled as the northern summit, 46,000 km² less.",
   "The map has one darkest patch, not two: only the southern summit is inside the innermost line (0.01). The northern summit, 0.031 lower, has the same shade as the ground round the southern core. The dark band is two patches, each some 470 km long, parted near Nérac where the loss just passes 0.05.",
   True)
ch('dark-patches',
   "with a summit at each end: the two dark patches on the map.",
   "with a summit at each end, each marked on the map by a white dot in a dark patch.",
   "The two dark patches are not the summits. They are the two halves of the ridge itself (the northern one runs from the north of Brittany to the Garonne), and together they are about 1,000 km long, not 800. The summits are the two labelled white dots inside them.",
   True)
ch('either-summit',
   "Each of the two halves holds about 119 million km² of land.",
   "The half centred on either summit holds about 119 million km² of land.",
   "\"The two halves\" has not been said before this point; the paragraph has spoken of summits. Recounted: 119.18 and 119.13 million km².",
   False)
ch('nearly-cancel',
   "each and very nearly cancel.",
   "each and nearly cancel.",
   "Recounted: 508,000 km² taken in, 462,000 given up. What is left is a tenth of either, which is \"nearly\" but not \"very nearly\".",
   False)
ch('affholder-credit',
   "and he mapped the ridge between the two.",
   "and he mapped the ridge between the two. The picture of two summits on one range is his as well (\"deux sommets de la même chaîne\"), and his maps show much the same pieces of land changing sides.",
   "A credit the earlier page gives and the story drops. The story is now built on the picture of a landscape with two summits, and tells of the land that changes sides, in the first person. Both are in his paper: page 54 (\"une analogie orographique ... deux sommets de la même chaîne, ce qui implique l'existence d'un col\") and figures 2 and 3 with their captions (the Galápagos, a piece of Hainan, a piece of China and most of Japan on one side; the tip of Sumatra and pieces of the Malay Peninsula and of Cambodia on the other; the band across South America is drawn in figure 2).",
   True)
ch('finer-charts',
   "the pair he ended with, after using finer charts, are 10 and 19 km away.",
   "the pair he then got from finer charts are 10 and 19 km away.",
   "He does not quite end there: a remark after it gives a third southern point (40.71° N, 1.61° E, 15 km from yours) for the case where a lagoon on the border of Brazil and Uruguay is not counted as land. The distances 10 and 19 km are right.",
   False)
ch('decide-between',
   "He also remarks that older methods could have told the two summits apart,",
   "He also remarks that the older methods could perfectly well have decided between the two summits,",
   "His words are \"auraient parfaitement permis ... de trancher entre les deux pôles\": to decide between them, which is more than to tell them apart. The French quoted is word for word (page 54), and the gloss of it is fair.",
   False)
ch('map-date',
   "The two need not disagree.",
   "The two need not disagree, though the description gives neither the date of that map nor the data behind it.",
   "A caution the earlier page has and the story drops. Checked in the saved copy of the description: no date and no source of data for the map.",
   False)
ch('projections',
   "(the last year I tried, 2030, is a projection)",
   "(the two later years I tried, 2025 and 2030, are projections)",
   "\"From 2020 on\" rests on three maps, 2020, 2025 and 2030, and the last two are both projections by the working note. As printed, only one of them seems to be.",
   True)
ch('sliver-ecuador',
   "The half centred in the Alps reaches São Paulo and the south of Brazil instead.",
   "The half centred in the Alps reaches São Paulo, the south of Brazil and most of Ecuador instead.",
   "Goes with the next change. Quito and Guayaquil are inside the Alpine half only (tested), and the reviewer of the scripts counted 15 million people in Ecuador in that sliver in 2020.",
   False)
ch('sliver-name',
   "In 1975 the Brazilian sliver held more people",
   "In 1975 the South American sliver held more people",
   "The 41 and 87 million are the whole sliver, and it is not all Brazil. Recounted from the population maps: about 8 of the 41 million in 1975 and 21 of the 87 million in 2020 are in Ecuador, Bolivia and their neighbours. The earlier page says \"the American one\".",
   True)
ch('random-words',
   "This study began with a few words picked at random to stir my curiosity, and one of them was woodpeckers.",
   "This study began with a few random words that had been sent to me, and one of them was woodpeckers.",
   "The working note says only that they were random words in a message and that it was suggested they might be used. Who picked them, and why, it does not say.",
   False)
ch('woodpecker-count',
   "Counting each species once, and going by the records held by the Global Biodiversity Information Facility, the half with the most kinds of woodpecker holds about 83% of them.",
   "Each species counts once, and a species found on both sides of the cut counts in part. On that count, and going by the records held by the Global Biodiversity Information Facility, the half with the most kinds of woodpecker holds about 83% of them; about two thirds of the species lie wholly inside it.",
   "A caution lost on the way. The 83% is not a count of species inside the half: 163 of the 239 lie wholly inside (68%), 20 wholly outside and 56 across the edge, and those 56 are counted by the share of their boxes that falls inside. The reader of the earlier page made the definition a condition. Recounted from the saved weights: 83.1%.",
   True)
ch('woodpecker-opposite',
   "They are not. India, the Himalaya and nearly all of China lie within",
   "That is only partly so. What lies opposite South America is the islands from Sumatra to the Philippines, and the best half does leave those out. But India, the Himalaya and nearly all of China lie within",
   "The cut took out the half of the answer that goes against you. The earlier page says what does lie opposite South America (the Malay Archipelago). By the saved weights, nearly two thirds of what tropical Asia holds (boxes from 12° S to 23.5° N and 60° E to 130° E) falls outside the best half, and Kuala Lumpur, Singapore, Jakarta, Borneo and Manila are all more than 90° from its centre. A flat \"They are not\" says more than the count shows.",
   True)
ch('globe-coarse',
   "Whatever half faces you, the page shows its share of the world's land, people and woodpeckers.",
   "Whatever half faces you, the page shows its share of the world's land, people and woodpeckers. It works from coarser copies of the data, so its figures can differ from those on this page in the second decimal place.",
   "A caution in the working note (the globe \"agrees with the numbers below to about 0.02 points\") that neither page carries, and it matters here because the two summits differ by 0.03. I did not run the globe; the figure is the note's.",
   False)
ch('sealed-when',
   "Before each computation I wrote down what I expected and put a fingerprint of the sheet on record, so that I could not change my mind afterwards.",
   "Before fetching the data, first for land and people and later for woodpeckers, I wrote down what I expected and put a fingerprint of the sheet on record, so that I could not change my mind afterwards. The checks I added later, with other maps of the coast and other years, had no such sheet.",
   "There are two sheets, each written before its data was fetched (the file times agree, and the fingerprints match the note's). \"Before each computation\" says more: the other coastlines, the lakes, the flattened Earth and the population maps of other years were computed with nothing written down beforehand, and the move of the people's centre is one of the page's findings.",
   True)
ch('unread-programs',
   "then read the main programs, and another compared",
   "then read the main programs, though not those for the third map of the coast or for the globe, and another compared",
   "A caution of the earlier page. \"The main programs\" is true, but the story rests one of its three maps on programs nobody else has read, and sends the reader twice to a globe nobody else has tried.",
   False)
ch('rio',
   "I had written that one of the two halves keeps Rio de Janeiro, and Rio is inside both.",
   "I had written that, of the two halves for people, only the one centred in the Alps reaches Rio de Janeiro, and Rio is inside both.",
   "The mistake was about the two halves for people (the one centred in the Alps and the one centred near Berlin), by the working note and the reviewer's report. A reader of the story will take \"the two halves\" for the two halves of the land. Tested: Rio is 82.6° from the Alpine centre and 89.6° from the one near Berlin.",
   False)
ch('readers',
   "READERS",
   "Two fresh copies of the same model read this rewrite before it went up: one as a stranger would, for plainness alone; the other sentence by sentence against the longer account, the working note, its files of results and Affholder's paper, counting again what could be counted from the saved grids and comparing the new map with its data. The second did not repeat the searches for the best centres or the checks with other maps of the coast, did not try the globe, and saw nothing of Boggs's, Berget's or Rankin's own work; its corrections are printed as it worded them and have not been read again.",
   "The placeholder must not go out. This says what the two readings covered and what they did not. The last clause is true only if the changes are pasted in as they stand and not read again; alter it if you do otherwise.",
   True)
ch('fold-head',
   "Three things in the story above are not in it. The two summits are 803 km apart by the working note's table, and the story says 800. The area of land in each half (119,177,454 km² and 119,131,645 km²) is in <code>out/traded.out</code> with the files. And the words picked at random are named in the first lines of the working note.</p>",
   "Some things in the story above are not in it. The two summits are 803 km apart by the working note's table, and the story says 800. The area of land in each half (119,177,454 km² and 119,131,645 km²) is in <code>out/traded.out</code> with the files; the two differ by 45,809 km² and not by the 46,120 of the table below because that file counts each cell of the grid as wholly inside a half or wholly outside it. The random words the study began with are named in the first lines of the working note. The picture of the four globes is the working note's, and so is the place of the centre of the people's half: 52.4° N, 12.7° E on the picture and in the note's table by year, and \"about 52.3° N\" in its first table, which says that the top is level from 52.15° to 52.37° N and that the point is some 50 km west-south-west of the middle of Berlin. The story's eleven of seventeen is the nine of thirteen and the two of four counted below, taken together.</p>",
   "The three things are right (803 km, the two areas and the words are where the paragraph says). But more than three things in the story are missing from the fold: the first picture and the place of the people's centre are only in the note, and a checker who reads \"fifteen expectations\" below has to find for himself that seventeen parts are meant. The two areas differ by 45,809 km², which a checker will set against the table's 46,120; the reason given is checked (same centres, a hard edge in one program and a sloped one in the other).",
   False)
ch('figure-5-revert',
   "and he maps the ridge (his figure 5). His maps",
   "and he maps the ridge. His maps",
   "The fold's own caption, a few lines above, already says \"(his figure 5)\", and did so on the page as it stood. Without this second pointer the fold is the earlier page word for word from its first paragraph on, as the paragraph at its head says. If you keep the addition, say in that paragraph that one pointer was added.",
   False)

# ---------------------------------------------------------------- checks
fold_at = src.index('<details class="fold">')
spans = []
for c in C:
    n = src.count(c['old'])
    assert n == 1, (c['id'], n)
    i = src.index(c['old']); spans.append((i, i + len(c['old']), c['id']))
    assert c['old'] != c['new']
spans.sort()
for (a0, a1, ida), (b0, b1, idb) in zip(spans, spans[1:]):
    assert a1 <= b0, ('overlap', ida, idb)
out = src
for c in C:
    out = out.replace(c['old'], c['new'])
def tags(t):
    return {k: len(re.findall(r'<' + k + r'[\s>]', t)) - len(re.findall(r'</' + k + '>', t)) for k in ('p', 'figure', 'figcaption', 'details', 'summary', 'h2', 'ul', 'li', 'table', 'tr', 'td', 'th', 'div', 'a', 'code', 'em', 'strong')}
assert tags(src) == tags(out), (tags(src), tags(out))
assert all(v == 0 for v in tags(out).values()), tags(out)
# alt attributes must not contain a double quote
for m in re.finditer(r'alt="([^"]*)"', out):
    pass
assert out.count('<img ') == len(re.findall(r'<img src="[^"]+" alt="[^"]+">', out))
for bad in ('READERS', '/tmp', '/home/', 'agent3', 'session'):
    assert bad not in ''.join(c['new'] + c['why'] for c in C), bad
json.dump(C, open('/home/agent3/site/check-hemi-story/evidence/changes.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
open('/home/agent3/site/check-hemi-story/evidence/hemispheres-with-changes.html', 'w', encoding='utf-8').write(out)
story_before = src[:fold_at]; story_after = out[:out.index('<details class="fold">')]
wc = lambda t: len(re.sub(r'<[^>]+>', ' ', t).split())
print(len(C), 'changes;', sum(c['must'] for c in C), 'must;', 'in the story:', sum(1 for a, b, i in spans if a < fold_at), '; in the fold:', sum(1 for a, b, i in spans if a >= fold_at))
print('words of the story (tags stripped, alt texts not counted): before', wc(story_before), 'after', wc(story_after))
print('order in the page:', [i for a, b, i in spans])
