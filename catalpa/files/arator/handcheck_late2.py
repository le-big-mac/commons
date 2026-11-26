# Hand check of the five poems added on 26 Nov: 10 lines of each, drawn at 01:29 UTC with random.seed(550) from late2_scans.tsv as it then was (before damaged lines were left
# out, so the same seed now draws other lines).  I scanned the first four feet of each from the text before looking at the scanner's reading; the lines and my scans are kept
# here, and this prints the scanner's present reading of each beside them.
import re
HAND = '''juvencus|SDSS|Sed quid proficient saecli mortalia lucra,
juvencus|DDDD|Atque crucem propriam comitatibus addere nostris
juvencus|SSDS|Inmunda implebat lacerans virtute furoris.
juvencus|SDSD|Incumbens valido nobis violentia tractu.
juvencus|DSSS|Sic genus hoc vero sensu cum degenerarit,
juvencus|DDSS|Interea Mariae sponso miracula mentem
juvencus|SSSS|Iactat; sed nescis, quae sint exordia vocis,
juvencus|DSSS|Rursus in abrupti montis consistere celsis
juvencus|SDSS|Credentes referunt plenam per membra salutem.
juvencus|DDSS|Quae Danihelis habet iussam verissima vocem;
ausonius|DDSS|verba refert mediis concurrens fluctibus echo.
ausonius|SDSD|sic demersa procul durante per intima visu
ausonius|DSDD|cernimus arcanique patet penetrale profundi,
ausonius|SDSS|nec praeferre suos auderet Thybris honores.
ausonius|DSSS|purior hic campis aer Phoebusque sereno
ausonius|DSSD|nec coeunt rictus, haustas sed hiatibus auras
ausonius|DSDS|nobilius permixta tuo sub nomine, quam si
ausonius|SSSS|nec sola antiquos ostentat Roma Catones,
ausonius|DDSD|contulit ad veteris praeconia Quintiliani:
ausonius|DSSS|tempora longarum fers incorrupte morarum,
prudentius|SSDS|mortali de matre hominem, sed cum Patre numen.
prudentius|SDDS|casta, incesta meae patuerunt pectora dextrae,
prudentius|SDDS|intrarat cuneos sociam mentita figuram.
prudentius|DDSS|quadrua vis animat, trinis ingressibus aram
prudentius|DDSD|de tunicae alterius gestamine providus ito,
prudentius|DSDD|Non tamen et solum, quia tu Deus ex Patre, Christe
prudentius|DDSS|orbis Avaritia, sternens centena virorum
prudentius|SSSS|calcatrix mundi mundanis victa fatiscat
prudentius|SSDS|dum sese ostentat, clipeo dum territat auras,
prudentius|DSSS|dum tribuit nosmet dona ad caelestia vexit,
dracontius|DSSD|Scire cupit simplex, et non habet unde requirat:
dracontius|SDDS|Fudit virginei truculentus funeris haeres.
dracontius|DSSS|Reddere mercedem cunctis, quam quisque meretur,
dracontius|DSDD|Praeterea solis datus est locus ille duobus,
dracontius|SDSD|Immortale genus, mortalia dura subivit:
dracontius|SDSS|Nos nobis facimus peccando sponte maligne.
dracontius|SSDD|Conservat natura fidem pietate parentis,
dracontius|SDSD|Per te fetat humus, per te, Deus, herba virescit,
dracontius|DSSD|Amphitheatrales qui non tremuere furores,
dracontius|DDSS|Cum residens caveis inter spectacula festa
corippus|DSSD|Magna viri cervix, nec tardus in ossibus ensis
corippus|DSSS|Faucibus e cunctis campos funduntur in omnes
corippus|DSSD|Torsit et adversi frontem ferit horridus ira
corippus|DDDS|Suscipiens dominus: validis mitescere ventis
corippus|DSSS|Viderat ingentem deiectum vulnere fratrem
corippus|DDSS|Civibus haecne fides? si sic Romana recessit
corippus|DSSS|Quis varias mortes aut dictis explicet hostes
corippus|DSSS|Ausus erit mecum, planis fundetur in arvis:
corippus|DDDD|Ilicet egrediens placidis celer omnia verbis
corippus|DSSS|Ardua pinnati defendunt culmina tecti.'''
rows = [l.rstrip('\n').split('\t') for l in open('/home/agent1/arator/late2_scans.tsv')]
key = lambda s: re.sub(r'[^a-z]', '', s.lower())
now = {(r[0], key(r[5])): r for r in rows}
agree = n = 0
for l in HAND.split('\n'):
    poem, pat, text = l.split('|'); r = now.get((poem, key(text))); n += 1
    if r is None: print(f'{poem:10s} hand {pat}  line no longer in the set   {text}'); continue
    ok = r[1][:4] == pat; agree += ok
    print(f'{poem:10s} hand {pat}  scanner {r[1]:5s} {r[2]:12s} {"agree" if ok else "DIFFER"}   {text}')
print(f'{agree} of {n} agree')
