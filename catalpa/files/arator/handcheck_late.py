# The hand check of Sedulius and Claudian: 12 lines of each, drawn at 23:45 UTC on 25 Nov 2026 with random.seed(430) from late_scans.tsv AS IT THEN WAS
# (before the mends of 26 Nov, and with some lines of an elegiac preface still in the Claudian set, so the same seed on the present file draws other lines).
# The lines are kept here with my division into feet, written out again on 26 Nov; this prints the scanner's present reading of each beside it.
HAND = '''
sedulius|Nam scriptura docet de te mandasse Tonantem,|Nam scrip / tura do / cet de / te man / dasse To / nantem|SDSS
sedulius|A facie terræ, rapidisque volatibus actus|A faci / e ter / rae rapi / disque vo / latibus / actus|DSDD
sedulius|Quod simplex triplicet quodque est triplicabile simplet.|Quod sim / plex tripli / cet quod / qu(e) est tripli / cabile / simplet|SDSD
sedulius|Totum namque lavans uno baptismate mundum:|Totum / namque la / vans u / no bap / tismate / mundum|SDSS
sedulius|Interea dum rite viam sermone levamus|Intere / a dum / rite vi / am ser / mone le / vamus|DSDS
sedulius|Neglegis et regi regum tua regna minaris.|Neglegis / et re / gi re / gum tua / regna mi / naris|DSSD
sedulius|Candida forma nivis Domini de tegmine fulsit.|Candida / forma ni / vis Domi / ni de / tegmine / fulsit|DDDS
sedulius|In vinum convertit aquas: amittere gaudent|In vi / num con / vertit a / quas a / mittere / gaudent|SSDS
sedulius|Tecta diu, Christo nobis veniente, patescit.|Tecta di / u Chris / to no / bis veni / ente pa / tescit|DSSD
sedulius|Pace salutantis sese intulit, atque foratas|Pace sa / lutan / tis se / s(e) intulit / atque fo / ratas|DSSD
sedulius|Carcere constricti non permittemur abire,|Carcere / constric / ti non / permit / temur a / bire|DSSS
sedulius|Haec ventura senes posquam dixere prophetae,|Haec ven / tura se / nes pos / quam dix / ere pro / phetae|SDSS
claudian|Fingere nil maius potuit sopor, altaque vati|Fingere / nil ma / ius potu / it sopor / altaque / vati|DSDD
claudian|Signa movet; iamque ora Padi portusque relinquit|Signa mo / vet iam / qu(e) ora Pa / di por / tusque re / linquit|DSDS
claudian|indiscreta feris? Tales cum saepe parentis|indis / creta fe / ris ta / les cum / saepe pa / rentis|SDSS
claudian|vel coniunx fuerit natarumve agminis una,|vel con / iunx fue / rit na / tarum / v(e) agminis / una|SDSS
claudian|Sots tulerit Martisque vices.  Non funditus armis|So(r)s tule / rit Mar / tisque vi / ces non / funditus / armis|DSDS
claudian|Vidit cornipedes: 'quanam de genre' rogabat|Vidit / cornipe / des qua / nam de / gen(t)e ro / gabat|SDSS
claudian|sed tepido calefacta Noto; ver inde serenum|sed tepi / do cale / facta No / to ver / inde se / renum|DDDS
claudian|cernentes oculos et late pervius humor|cernen / tes ocu / los et / late / pervius / umor|SDSS
claudian|nascendique vices alterna morte rependis,|nascen / dique vi / ces al / terna / morte re / pendis|SDSS
claudian|atque interruptas agnoscit pectinis artes.|atqu(e) in / terrup / tas ag / noscit / pectinis / artes|SSSS
claudian|"Curarum, Cytherea, tibi secreta fatebor.|Cura / rum Cythe / rea ti / bi se / creta fa / tebor|SDDS
claudian|Gratantur durasse diem moderataque laudant|Gratan / tur du / rasse di / em mode / rataque / laudant|SSDD
'''
import re
rows = [l.rstrip('\n').split('\t') for l in open('/home/agent1/arator/late_scans.tsv')]
key = lambda s: re.sub(r'[^a-z]', '', re.sub(r'\s+\d+\s*$', '', s).lower().replace('æ', 'ae'))
now = {(r[0], key(r[5])): r[1] for r in rows}
agree = 0; n = 0; m = 0
for l in HAND.strip().split('\n'):
    poem, text, feet, pat = l.split('|'); n += 1
    got = now.get((poem, key(text)))
    if got is None: print(f'{poem:8s} hand {pat}  no longer in the set (the hexameter of a preface couplet, left out since)   {feet}'); continue
    m += 1; ok = got[:4] == pat; agree += ok
    print(f'{poem:8s} hand {pat}  scanner now {got:5s} {"agree" if ok else "DIFFER"}   {feet}')
print(f'{agree} of the {m} lines still in the set agree ({n} were drawn; all {n} agreed with the scanner\'s reading when drawn)')
