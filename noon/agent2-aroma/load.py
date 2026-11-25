"""Read Keller and Vosshall's workbook into one table.   usage: python -I load.py keller2016.xlsx ratings.csv"""
import sys
import openpyxl
import pandas as pd
wb = openpyxl.load_workbook(sys.argv[1], read_only=True, data_only=True)
ws = wb['data']
rows = list(ws.iter_rows(values_only=True))
head = [str(h).strip().replace('\n', ' ') for h in rows[2]]
assert head[2] == 'CID' and head[15] == 'HOW STRONG IS THE SMELL?' and head[37] == 'CHEMICAL', head
names = ['cas', 'catalogue', 'cid', 'odor', 'dilution', 'subject', 'subject_dream', 'gender', 'race', 'ethnicity', 'age', 'vial', 'smell', 'know', 'own_words',
         'strength', 'pleasantness', 'familiarity'] + [h.split('/')[0].lower() for h in head[18:]]
df = pd.DataFrame(rows[3:], columns=names)
df = df[df['cid'].notna()].copy()
# two molecules have their registry number typed in the CID column; their compound numbers are from PubChem's name search
FIX = {'109-19-0': 8038, '3796-70-1': 1549778}                      # isobutyl acetate; 6,10-dimethyl-5,9-undecadien-2-one
df['cid'] = df['cid'].astype(str).str.strip().map(lambda c: FIX.get(c, c))
# found by the referee: the row named omega-6-hexadecenlactone (registry number 7779-50-2) carries compound number 6753,
# which is musk ambrette, a different molecule; PubChem's first compound for that registry number is 3591866
df.loc[df['cas'].astype(str).str.strip() == '7779-50-2', 'cid'] = 3591866
assert not set(FIX.values()) & set(pd.to_numeric(df['cid'][~df['cas'].isin(FIX)], errors='coerce').dropna().astype(int))
for c in ['cid', 'subject', 'vial'] + names[15:]:
    df[c] = pd.to_numeric(df[c], errors='coerce')
df['dilution'] = df['dilution'].astype(str).str.replace(' ', '').str.strip()
df['dil'] = df['dilution'].str.replace(',', '').str.split('/').str[1].astype(float)        # 1/1,000 -> 1000
df.to_csv(sys.argv[2], index=False)
print(len(df), "rows;", df['cid'].nunique(), "molecules;", df['subject'].nunique(), "people;", df['vial'].nunique(), "vials")
print(df['dilution'].value_counts().to_dict())
print(df['smell'].value_counts(dropna=False).to_dict())
print(df['know'].value_counts(dropna=False).to_dict())
