"""Smell ratings against molecular structure.   usage: python -I aroma.py ratings.csv properties.csv out.json
Rules are in expectations.md.  Two things had to be settled after seeing the table's layout and are marked (*):
(*) a word's slider left untouched by someone who smelled something counts as 0 (no zero is ever entered in the table);
(*) "all ratings given" leaves out the people who said they smelled nothing, also for strength; a second version
    counts them as strength 0 and is reported beside it, not scored."""
import sys, json, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, pearsonr
from rdkit import Chem, RDLogger
from rdkit.Chem import Descriptors
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold
RDLogger.DisableLog('rdApp.*')

df = pd.read_csv(sys.argv[1], low_memory=False)
prop = pd.read_csv(sys.argv[2]).set_index('CID')
WORDS = list(df.columns[18:38])
MAIN = ['strength', 'pleasantness', 'familiarity']
df['smelled'] = ~df['smell'].astype(str).str.contains("can't", case=False)
strong = df[df['dil'] == df.groupby('cid')['dil'].transform('min')].copy()          # the stronger of each molecule's two dilutions
smelled = strong[strong['smelled']].copy()
smelled[WORDS] = smelled[WORDS].fillna(0)                                            # (*)
name = df.groupby('cid')['odor'].first().str.replace(' (replicate)', '', regex=False).str.strip()

M = smelled.groupby('cid')[MAIN + WORDS].mean()
M['n_smelled'] = smelled.groupby('cid').size()
M['share_smelled'] = strong.groupby('cid')['smelled'].mean()
M['strength0'] = strong.assign(s=strong['strength'].fillna(0)).groupby('cid')['s'].mean()           # nobody-smelled counted as 0: not the registered rule
M['dil'] = strong.groupby('cid')['dil'].first()
for w in ('garlic', 'fish'):                                                         # the letter of the rule: only the people who used the word
    M[w + '_users'] = strong.groupby('cid')[w].mean()
    M[w + '_nusers'] = strong.groupby('cid')[w].count()

mols = {c: Chem.MolFromSmiles(prop.loc[c, 'SMILES']) for c in M.index}
assert all(m is not None for m in mols.values())
acid = Chem.MolFromSmarts('[CX3](=O)[OX2H1]')
M['S'] = [any(a.GetSymbol() == 'S' for a in mols[c].GetAtoms()) for c in M.index]
M['N'] = [any(a.GetSymbol() == 'N' for a in mols[c].GetAtoms()) for c in M.index]
M['is_acid'] = [mols[c].HasSubstructMatch(acid) for c in M.index]
M['size'] = [mols[c].GetNumHeavyAtoms() for c in M.index]
M['name'] = [name[c] for c in M.index]
print(f"{len(M)} molecules; {int(M['S'].sum())} contain sulfur, {int(M['N'].sum())} nitrogen, {int(M['is_acid'].sum())} are acids; size {M['size'].min()} to {M['size'].max()} atoms, median {M['size'].median():.0f}")
print(f"at the stronger dilution a molecule was smelled by {100 * M['share_smelled'].median():.0f}% of people at the median (least {100 * M['share_smelled'].min():.0f}%)")
res = {}

ether = Chem.MolFromSmarts('[OX2]([#6])[#6]')
M['ether_or_ester'] = [mols[c].HasSubstructMatch(ether) for c in M.index]
M['fish_touch'] = smelled.assign(t=(smelled['fish'] > 0)).groupby('cid')['t'].mean()
# O1
gap = M.loc[~M['S'], 'pleasantness'].mean() - M.loc[M['S'], 'pleasantness'].mean()
print(f"O1  pleasantness: with sulfur {M.loc[M['S'], 'pleasantness'].mean():.1f}, without {M.loc[~M['S'], 'pleasantness'].mean():.1f}; gap {gap:.1f} points")
# O2, O3
for tag, w, el, k in (("O2", 'garlic', 'S', 20), ("O3", 'fish', 'N', 10)):
    top = M.sort_values(w, ascending=False).head(k)
    print(f"{tag}  the {k} most '{w}': {int(top[el].sum())} contain {'sulfur' if el == 'S' else 'nitrogen'} (in the whole set {int(M[el].sum())} of {len(M)})")
    print("       " + "; ".join(f"{r['name']} {r[w]:.0f}{'*' if r[el] else ''}" for _, r in top.iterrows()))
    top2 = M[M[w + '_nusers'] >= 1].sort_values(w + '_users', ascending=False).head(k)
    print(f"     by the letter (mean over the people who used the word, however few): {int(top2[el].sum())} of {k}; with at least 5 users: "
          f"{int(M[M[w + '_nusers'] >= 5].sort_values(w + '_users', ascending=False).head(k)[el].sum())} of {k}")
    if w == 'fish':
        print(f"     sulfur among the {k} most 'fish': {int(top['S'].sum())}")
# O4-O7
def rho(a, b, sel=None):
    d = M if sel is None else M[sel]
    return float(spearmanr(d[a], d[b])[0])
print(f"O4  familiarity and pleasantness: {rho('familiarity', 'pleasantness'):+.2f}")
print(f"O5  strength and pleasantness: {rho('strength', 'pleasantness'):+.2f}   (strength with nobody-smelled as 0: {rho('strength0', 'pleasantness'):+.2f})")
print(f"O6  size and pleasantness: {rho('size', 'pleasantness'):+.2f}")
print(f"O7  size and strength: {rho('size', 'strength'):+.2f}   (strength with nobody-smelled as 0: {rho('size', 'strength0'):+.2f})")
for dl in sorted(M['dil'].unique()):
    sel = M['dil'] == dl
    print(f"       among the {int(sel.sum())} molecules whose stronger dilution is 1/{int(dl):,}: size and strength {rho('size', 'strength', sel):+.2f}, size and pleasantness {rho('size', 'pleasantness', sel):+.2f}; median size {M.loc[sel, 'size'].median():.0f}")
well = M['share_smelled'] >= 0.8
w = M[M['name'].str.lower().isin(['water', 'sodium phosphate', 'glycerol'])]
print("after the referee: the floor under 'smelled something': " + "; ".join(f"{r['name']} was 'smelled' by {100 * r['share_smelled']:.0f}% (strength {r['strength']:.0f}, pleasantness {r['pleasantness']:.0f})" for _, r in w.iterrows()))
print(f"after the referee: {int((~well).sum())} molecules were smelled by fewer than 80% of people; among the other {int(well.sum())}: familiarity and pleasantness {rho('familiarity', 'pleasantness', well):+.2f}, "
      f"strength and pleasantness {rho('strength', 'pleasantness', well):+.2f}, size and strength {rho('size', 'strength', well):+.2f}, size and pleasantness {rho('size', 'pleasantness', well):+.2f}; "
      f"sulfur gap {M.loc[well & ~M['S'], 'pleasantness'].mean() - M.loc[well & M['S'], 'pleasantness'].mean():.1f}")
k1 = df[(df['dil'] == 1000) & df['smelled']].groupby('cid')['strength'].mean()
both = M.index.intersection(k1.index)
print(f"after the referee: all {len(both)} molecules that were given at 1/1,000, judged at that dilution: size and strength {float(spearmanr(M.loc[both, 'size'], k1[both])[0]):+.2f}")
# O8
P = smelled.groupby(['cid', 'subject'])[MAIN].mean().unstack('subject')             # molecule x person (repeats averaged)
agree = {}
for a in MAIN:
    X = P[a]
    out = []
    for s in X.columns:
        others = X.drop(columns=s).mean(axis=1)
        ok = X[s].notna() & others.notna()
        out.append(pearsonr(X.loc[ok, s], others[ok])[0])
    agree[a] = np.array(out)
print(f"O8  one person against the rest, median over 55 people: strength {np.median(agree['strength']):.2f} (range {agree['strength'].min():.2f} to {agree['strength'].max():.2f}); "
      f"pleasantness {np.median(agree['pleasantness']):.2f} ({agree['pleasantness'].min():.2f} to {agree['pleasantness'].max():.2f}); familiarity {np.median(agree['familiarity']):.2f}")
# O9
top = M.sort_values('pleasantness', ascending=False)
print("O9  the 10 most pleasant: " + "; ".join(f"{r['name']} {r['pleasantness']:.0f}" for _, r in top.head(10).iterrows()))
van = [(r['name'], int(np.where(top.index == c)[0][0]) + 1) for c, r in top.iterrows() if 'vanillin' in str(r['name']).lower()]
print("     vanillins in the set and their rank:", van)
bot = top.tail(10).iloc[::-1]
print("     the 10 least pleasant: " + "; ".join(f"{r['name']} {r['pleasantness']:.0f}{' S' if r['S'] else ''}{' acid' if r['is_acid'] else ''}" for _, r in bot.iterrows()))
print(f"     of those, sulfur or acid: {int((bot['S'] | bot['is_acid']).sum())}")
# O10
feat = pd.DataFrame([Descriptors.CalcMolDescriptors(mols[c]) for c in M.index], index=M.index)
feat = feat.replace([np.inf, -np.inf], np.nan)
feat = feat.fillna(feat.median()).clip(-1e6, 1e6)
feat = feat.loc[:, feat.nunique() > 1]
print(f"O10 model: random forest on {feat.shape[1]} descriptors that vary, ten folds")
def cv(X, y, seed=0):
    pred = np.zeros(len(y))
    for tr, te in KFold(10, shuffle=True, random_state=seed).split(X):
        rf = RandomForestRegressor(n_estimators=500, random_state=seed, n_jobs=16).fit(X[tr], y[tr])
        pred[te] = rf.predict(X[te])
    return float(pearsonr(pred, y)[0]), pred
model = {}
X = feat.values
for a in MAIN + WORDS:
    model[a], pred = cv(X, M[a].values)
    if a in ('pleasantness', 'garlic', 'fish'):
        M[a + '_pred'] = pred
print(f"     pleasantness {model['pleasantness']:.2f}; strength {model['strength']:.2f}; garlic {model['garlic']:.2f}")
print("     not registered, the rest: " + "; ".join(f"{a} {model[a]:.2f}" for a in sorted(model, key=lambda a: -model[a]) if a not in ('pleasantness', 'strength', 'garlic')))
X2 = np.c_[X, np.log10(M['dil'].values)]
r2, _ = cv(X2, M['strength'].values)
r3, _ = cv(np.log10(M['dil'].values)[:, None], M['strength'].values)
r4, _ = cv(X, M['strength0'].values)
print(f"     strength, afterwards: with the dilution added as an input {r2:.2f}; from the dilution alone {r3:.2f}; nobody-smelled as 0, structure only {r4:.2f}")
for seed in (1, 2):
    print(f"     other seeds for folds and forest ({seed}): pleasantness {cv(X, M['pleasantness'].values, seed)[0]:.2f}, strength {cv(X, M['strength'].values, seed)[0]:.2f}, garlic {cv(X, M['garlic'].values, seed)[0]:.2f}")
simple = M[['S', 'N', 'is_acid', 'size']].astype(float).values
print(f"     a four-number model (sulfur, nitrogen, acid, size): pleasantness {cv(simple, M['pleasantness'].values)[0]:.2f}, garlic {cv(simple, M['garlic'].values)[0]:.2f}")
sS = M['S'].values
print(f"     the forest's out-of-fold garlic predictions, among the {int(sS.sum())} sulfur molecules only: {pearsonr(M['garlic_pred'][sS], M['garlic'][sS])[0]:.2f}; fish: {pearsonr(M['fish_pred'][sS], M['fish'][sS])[0]:.2f}; pleasantness: {pearsonr(M['pleasantness_pred'][sS], M['pleasantness'][sS])[0]:.2f}")
sv = M['S'].astype(float)
print(f"after the referee: other yes-or-no facts and pleasantness (Pearson): sulfur {pearsonr(sv, M['pleasantness'])[0]:+.2f}; an ether or ester oxygen {pearsonr(M['ether_or_ester'].astype(float), M['pleasantness'])[0]:+.2f} "
      f"({int(M['ether_or_ester'].sum())} molecules); acid {pearsonr(M['is_acid'].astype(float), M['pleasantness'])[0]:+.2f}; nitrogen {pearsonr(M['N'].astype(float), M['pleasantness'])[0]:+.2f}")
rfg = pearsonr(M['fish'], M['garlic'])[0]; rsf = pearsonr(sv, M['fish'])[0]; rsg = pearsonr(sv, M['garlic'])[0]
print(f"after the referee: fish and garlic across molecules {rfg:.2f}; sulfur and fish {rsf:.2f}, with garlic held fixed {(rsf - rsg * rfg) / np.sqrt((1 - rsg ** 2) * (1 - rfg ** 2)):.2f}")
ft = M.sort_values('fish_touch', ascending=False)
print("after the referee: share of the people who smelled it who moved the 'fish' slider at all: " + "; ".join(f"{r['name']} {100 * r['fish_touch']:.0f}%" for _, r in ft.head(5).iterrows())
      + f"; median sulfur compound {100 * M.loc[M['S'], 'fish_touch'].median():.0f}%; median of all {100 * M['fish_touch'].median():.0f}%")
only_s = M[['S']].astype(float).values
print(f"     sulfur yes or no, nothing else: garlic {pearsonr(only_s[:, 0], M['garlic'])[0]:.2f}, fish {pearsonr(only_s[:, 0], M['fish'])[0]:.2f}, decayed {pearsonr(only_s[:, 0], M['decayed'])[0]:.2f}, pleasantness {pearsonr(only_s[:, 0], M['pleasantness'])[0]:+.2f}")
print(f"     nitrogen yes or no: fish {pearsonr(M['N'].astype(float), M['fish'])[0]:+.2f}, ammonia {pearsonr(M['N'].astype(float), M['ammonia'])[0]:+.2f}")
nos = ~M['S'].values
print(f"     the forest among the {int(nos.sum())} molecules without sulfur: garlic {cv(X[nos], M['garlic'].values[nos])[0]:.2f}, pleasantness {cv(X[nos], M['pleasantness'].values[nos])[0]:.2f}")
# the ceiling: how well one half of the panel predicts the other half
rng = np.random.default_rng(0)
subj = np.array(sorted(smelled['subject'].unique()))
half = {a: [] for a in MAIN + WORDS}
for _ in range(50):
    pick = set(rng.permutation(subj)[:len(subj) // 2])
    m1 = smelled[smelled['subject'].isin(pick)].groupby('cid')[MAIN + WORDS].mean()
    m2 = smelled[~smelled['subject'].isin(pick)].groupby('cid')[MAIN + WORDS].mean()
    both = m1.index.intersection(m2.index)
    for a in MAIN + WORDS:
        half[a].append(pearsonr(m1.loc[both, a], m2.loc[both, a])[0])
half = {a: float(np.mean(v)) for a, v in half.items()}
print("     two random halves of the panel agree (mean of 50 splits): " + "; ".join(f"{a} {half[a]:.2f}" for a in ['pleasantness', 'strength', 'familiarity', 'garlic', 'fish', 'sweet', 'fruit', 'cold', 'warm']))
am = M[M['N']].sort_values('fish', ascending=False)
print("     molecules with nitrogen, most 'fish' first: " + "; ".join(f"{r['name']} {r['fish']:.0f}" for _, r in am.head(8).iterrows()))
print("     amines by name in the set: " + "; ".join(f"{r['name']} (fish {r['fish']:.0f}, ammonia {r['ammonia']:.0f}, pleasant {r['pleasantness']:.0f})" for _, r in M[M['name'].str.contains('amine|piperidine|pyrrolidine|pyridine|indole|putrescine|cadaverine', case=False)].iterrows()))

# afterwards: one person against themself (20 molecules were given twice)
rep = strong.groupby('cid')['vial'].nunique()
rep = rep[rep > 1].index
R = smelled[smelled['cid'].isin(rep)].sort_values('vial')
self_r = {a: [] for a in MAIN}
for s, g in R.groupby('subject'):
    piv = g.groupby(['cid', 'vial'])[MAIN].first().reset_index()
    first = piv.groupby('cid').nth(0).set_index('cid'); second = piv.groupby('cid').nth(1).set_index('cid')
    both = first.index.intersection(second.index)
    if len(both) >= 10:
        for a in MAIN:
            self_r[a].append(pearsonr(first.loc[both, a], second.loc[both, a])[0])
print(f"afterwards: one person against themself on the {len(rep)} molecules given twice (median over {len(self_r['strength'])} people): "
      + "; ".join(f"{a} {np.median(self_r[a]):.2f}" for a in MAIN))
others20 = {}
for a in MAIN:
    X20 = P[a].loc[P[a].index.isin(rep)]
    out = []
    for s in X20.columns:
        o = X20.drop(columns=s).mean(axis=1); ok = X20[s].notna()
        if ok.sum() >= 10:
            out.append(pearsonr(X20.loc[ok, s], o[ok])[0])
    others20[a] = float(np.median(out))
print("            one person against the rest on the same 20 molecules: " + "; ".join(f"{a} {others20[a]:.2f}" for a in MAIN))
firsts, seconds = {}, {}
for sj, g in R.groupby('subject'):
    piv = g.groupby(['cid', 'vial'])[MAIN].first().reset_index()
    firsts[sj] = piv.groupby('cid').nth(0).set_index('cid'); seconds[sj] = piv.groupby('cid').nth(1).set_index('cid')
other1 = {a: [] for a in MAIN}
for sa in firsts:
    for sb in seconds:
        if sa == sb:
            continue
        both = firsts[sa].index.intersection(seconds[sb].index)
        if len(both) >= 10:
            for a in MAIN:
                x, z = firsts[sa].loc[both, a], seconds[sb].loc[both, a]
                if x.std() > 0 and z.std() > 0:
                    other1[a].append(pearsonr(x, z)[0])
print("after the referee: one person's first vial against ANOTHER person's second vial, the same 20 molecules (median over pairs): " + "; ".join(f"{a} {np.median(other1[a]):.2f}" for a in MAIN))
pair = {}
for a in MAIN:
    C = P[a].corr(min_periods=100).values
    pair[a] = float(np.nanmedian(C[np.triu_indices_from(C, 1)]))
    C20 = P[a].loc[P[a].index.isin(rep)].corr(min_periods=10).values
    pair[a + '20'] = float(np.nanmedian(C20[np.triu_indices_from(C20, 1)]))
print("            one person against one other person, median over all pairs: all molecules " + "; ".join(f"{a} {pair[a]:.2f}" for a in MAIN)
      + " | the same 20 molecules " + "; ".join(f"{a} {pair[a + '20']:.2f}" for a in MAIN))
plain = ~M['S'] & ~M['is_acid']
print(f"afterwards: strength and pleasantness among the {int(plain.sum())} molecules with neither sulfur nor an acid group: {rho('strength', 'pleasantness', plain):+.2f}; "
      f"familiarity and pleasantness among them: {rho('familiarity', 'pleasantness', plain):+.2f}")
within = []
for sj in P['pleasantness'].columns:
    a, b = P['familiarity'][sj], P['pleasantness'][sj]
    ok = a.notna() & b.notna()
    within.append(spearmanr(a[ok], b[ok])[0])
print(f"afterwards: familiarity and pleasantness within one person, across molecules: median {np.median(within):+.2f} (range {min(within):+.2f} to {max(within):+.2f}); positive in {int(sum(w > 0 for w in within))} of {len(within)} people")
print(f"afterwards: familiarity and strength across molecules: {rho('familiarity', 'strength'):+.2f}; Pearson for O4 and O5: {pearsonr(M['familiarity'], M['pleasantness'])[0]:+.2f}, {pearsonr(M['strength'], M['pleasantness'])[0]:+.2f}")
# afterwards: which words go with pleasantness
wr = sorted(((rho(w, 'pleasantness'), w) for w in WORDS))
print("afterwards: words and pleasantness: " + "; ".join(f"{w} {r:+.2f}" for r, w in wr))
M.to_csv(sys.argv[3].replace('.json', '-molecules.csv'))
json.dump(dict(model=model, half=half, pair=pair, agree={a: agree[a].tolist() for a in MAIN}, self_r={a: [float(x) for x in self_r[a]] for a in MAIN}, words=[(float(r), w) for r, w in wr]), open(sys.argv[3], 'w'), indent=1)
