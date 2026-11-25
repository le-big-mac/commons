"""Fetch structures from PubChem for the compound numbers in the ratings table.   usage: python -I structures.py ratings.csv OUTDIR"""
import sys, urllib.request, urllib.parse
import pandas as pd
cids = sorted(set(int(c) for c in pd.read_csv(sys.argv[1], usecols=['cid'])['cid']))
url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/property/SMILES,ConnectivitySMILES,MolecularFormula,MolecularWeight,IUPACName/CSV"
out = []
for i in range(0, len(cids), 100):
    body = urllib.parse.urlencode({'cid': ','.join(str(c) for c in cids[i:i + 100])}).encode()
    req = urllib.request.Request(url, data=body, headers={'User-Agent': 'research-script/1.0'})
    with urllib.request.urlopen(req, timeout=120) as r:
        text = r.read().decode('utf-8')
    lines = text.strip().split('\n')
    out += lines if not out else lines[1:]
open(f"{sys.argv[2]}/properties.csv", 'w').write('\n'.join(out) + '\n')
print(len(cids), "compound numbers asked;", len(out) - 1, "rows received")
