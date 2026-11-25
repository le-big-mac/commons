"""Every expectation I sealed with odds on 21 and 22 November 2026, with what happened to it.   usage: python collect.py lines.csv [forecast-medians.csv [ROOT]]
Odds are read from the sealed files themselves.  Outcomes come from the running ledger (the six sheets that forecasters also priced)
or are transcribed below from each study's README, line by line.  1 = held, 0 = failed, blank = void or not settled."""
import sys, re, csv, os
H = sys.argv[3] if len(sys.argv) > 3 else os.path.expanduser('~')      # root under which the sealed files sit: my home folder, or the copies in sealed/
LEDGER = {(r['study'], r['label']): r for r in csv.DictReader(open(f'{H}/calib/ledger.csv'))}
# (study name, order in time, kind, sealed file, ledger name or None, outcomes transcribed from the README)
SOURCES = [
 ('birth months', 1, 'sheet', 'birth/expectations.md', 'birth-months', None),
 ('battles', 2, 'sheet', 'battles/expectations.md', 'battles', None),
 ('transiting planets', 3, 'sheet', 'transits/expectations.md', 'transits', None),
 ('vacancies', 4, 'sheet', 'vacancy/expectations.md', 'vacancy', None),
 ('vacancies', 4, 'bet on my odds', 'vacancy/meta.md', None, dict(Z1=0)),
 ('readers and authors', 5, 'sheet', 'authors/expectations.md', None, dict(R1=1, R2=1, R3=0, R4=1, R5=1)),
 ('readers and authors', 5, 'sheet', 'authors2/expectations.md', None, dict(S1=1, S2=None, S3=None, S4=0, S5=1, S6=0)),
 ('readers and authors', 5, 'sheet', 'authors2/expectations-quick.md', None, dict(Q1=1, Q2=0, Q3=0)),
 ('floating cube', 6, 'sheet', 'float/expectations.md', None, dict(F1=1, F2=1, F3=1, F4=1, F5=0, F6=None, F7=0)),
 ('onset of synchrony', 7, 'sheet', 'onset/expectations.md', 'onset', None),
 ('onset of synchrony', 7, 'bet on my odds', 'onset/meta.md', None, dict(Z1=1)),
 ('onset of synchrony', 7, 'follow-up', 'onset/plateau-prediction.md', None, dict(P1=1, P2=0, P3=1, P4=1)),
 ('onset of synchrony', 7, 'follow-up', 'onset/long-prediction.md', None, dict(L1=1, L2=0)),
 ('onset of synchrony', 7, 'follow-up', 'onset/climb-prediction.md', None, dict(C1=1, C2=1, C3=1)),
 ('onset of synchrony', 7, 'follow-up', 'onset/dip-prediction.md', None, dict(D1=1, D2=1)),
 ('onset of synchrony', 7, 'follow-up', 'onset/long2-prediction.md', None, dict(M1=1, M2=1)),
 ('onset of synchrony', 7, 'follow-up', 'onset/long3-prediction.md', None, dict(N1=1, N2=1)),
 ('onset of synchrony', 7, 'follow-up', 'onset/long4-prediction.md', None, dict(Q1=1, Q2=1, Q3=1, Q4=1)),
 ('onset of synchrony', 7, 'follow-up', 'onset/long5-prediction.md', None, dict(R1=1, R2=1, R3=0, R4=1)),
 ('onset of synchrony', 7, 'follow-up', 'onset/long6-prediction.md', None, dict(S1=1, S2=0)),
 ('onset of synchrony', 7, 'follow-up', 'onset/long7-prediction.md', None, dict(U1=1, U2=1, U3=1)),
 ('taffy pullers', 8, 'sheet', 'taffy/expectations.md', 'taffy', None),
 ('taffy pullers', 8, 'bet on my odds', 'taffy/meta.md', None, dict(Z1=0)),
 ('cannonballs', 9, 'sheet', 'impetus/expectations.md', None, {f'J{i}': 1 for i in range(1, 11)}),
 ('arctic circle', 10, 'sheet', 'aztec/expectations.md', None, dict(A1=0, A2=0, A3=1, A4=0, A5=1, A6=0)),
 ('arctic circle', 10, 'follow-up', 'aztec/corners-prediction.md', None, {f'B{i}': 1 for i in range(1, 7)}),
 ('arctic circle', 10, 'follow-up', 'aztec/tw-prediction.md', None, dict(W1=1, W2=1, W3=1, W4=0, W5=1)),
]
MARKED = ("Marked down", "Same doubt")                       # the sheet says in so many words that the line is marked down
OTHER = ("less sure", "I believe this jump", "memory alone", "guessing", "bet on my memory", "not a calculation")   # doubt worded otherwise; picked by hand from doubts-scan.py
LATE = {}
if len(sys.argv) > 2 and os.path.exists(sys.argv[2]):
    LATE = {(r['file'], r['label']): r['median'] for r in csv.DictReader(open(sys.argv[2]))}
rows = []
for study, order, kind, path, ledger, table in SOURCES:
    text = open(f'{H}/{path}', encoding='utf-8').read()
    found = re.findall(r"^([A-Z]+\d+)\.(.*?)odds (0\.\d+)[ \t]*$", text, re.M | re.S)
    labels = [f[0] for f in found]
    assert len(set(labels)) == len(labels), (path, labels)
    blocks = {b.split('.')[0]: " ".join(b.split()) for b in re.split(r"^(?=[A-Z]+\d+\. )", text, flags=re.M)[1:]}   # a line's own text: from its label to the next label
    assert set(blocks) == set(labels), (path, sorted(set(blocks) ^ set(labels)))
    for lab, _, odds in found:
        body = blocks[lab]
        if ledger:
            L = LEDGER[(ledger, lab)]; assert abs(float(L['my_odds']) - float(odds)) < 1e-9, (path, lab); out = int(float(L['outcome'])); fc = L['forecasters_median']
        else:
            assert lab in table, (path, lab); out = table[lab]; fc = ''
        doubt = 'marked down' if any(p in body for p in MARKED) else 'other named doubt' if any(p in body for p in OTHER) else ''
        mark = 'worked' if ('WORKED' in text or '(worked' in body) and '(guessed' not in body and '(remembered' not in body else 'remembered' if '(remembered' in body else 'guessed' if '(guessed' in body else ''
        rows.append(dict(study=study, order=order, kind=kind, file=path, label=lab, odds=odds, outcome='' if out is None else out, forecasters=fc, forecasters_late=LATE.get((path, lab), ''), named_doubt=doubt, marked=mark))
    if table is not None: assert set(table) == set(labels), (path, sorted(set(table) ^ set(labels)))
with open(sys.argv[1], 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows), "sealed lines with odds;", sum(1 for r in rows if r['outcome'] != ''), "settled;", sum(1 for r in rows if r['outcome'] == 1), "held;", sum(1 for r in rows if r['outcome'] == 0), "failed;", sum(1 for r in rows if r['outcome'] == ''), "void or not settled;", sum(1 for r in rows if r['named_doubt']), "with a named doubt;", sum(1 for r in rows if r['forecasters_late']), "priced afterwards")
