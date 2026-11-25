#!/usr/bin/env python
"""Second, separate implementation (pandas/floats) to cross-check check.py.
Run as: python -I crosscheck.py /path/to/catalogue.csv . Prints only; writes nothing."""
import sys
import numpy as np
import pandas as pd

df = pd.read_csv(sys.argv[1], dtype=str, keep_default_na=False)
print('rows', len(df))
df = df.drop_duplicates(subset='id', keep='first')
print('after id dedup', len(df))
if not (df['type'] == '').all():
    dropped = df[df['type'].str.strip(' ').str.lower() != 'earthquake']
    print('dropped by type:')
    print(dropped[['time', 'mag', 'depth', 'type', 'place']].to_string())
    df = df[df['type'].str.strip(' ').str.lower() == 'earthquake']
df = df.assign(magn=pd.to_numeric(df['mag'], errors='coerce'),
               t=pd.to_datetime(df['time'], utc=True, errors='coerce'))
lo = pd.Timestamp('2000-01-01T00:00:00.000Z')
hi = pd.Timestamp('2025-12-31T23:59:59.999Z')
df = df[df['magn'].notna() & (df['magn'] >= 5.5) & df['t'].notna() & (df['t'] >= lo) & (df['t'] <= hi)].copy()
N = len(df)
print('N', N)
df['m'] = df['magn'].round(2)
df['year'] = df['t'].dt.year
df['d'] = pd.to_numeric(df['depth'], errors='coerce')
df['lat'] = pd.to_numeric(df['latitude'], errors='coerce')
df['lon'] = pd.to_numeric(df['longitude'], errors='coerce')

print('A1', (df.m >= 6.0).sum(), (df.m >= 6.0).mean(), (df.m >= 7.0).sum(), (df.m >= 7.0).mean())
print('A2', df.m.max(), df.loc[df.m >= 9.0, ['year', 'm', 'place']].values.tolist())
print('A3', (df.lon > 0).sum(), df.lon.notna().sum(), (df.lon > 0).sum() / df.lon.notna().sum())
dv = df.d.round(1).value_counts()
print('A4', dv.head(3).to_dict(), dv.iloc[0] / df.d.notna().sum())
print('A5', (df.m >= 8.0).sum())
print('A6', (df.d < 70).sum(), (df.d < 70).sum() / df.d.notna().sum(),
      (df.d >= 300).sum(), (df.d >= 300).sum() / df.d.notna().sum())
py = df.year.value_counts().reindex(range(2000, 2026), fill_value=0)
print('A7', py.sort_values(ascending=False).head(3).to_dict())
ts = df.t.sort_values()
gaps = ts.diff().dropna().dt.total_seconds().values
print('A8', len(gaps), (gaps < 3600).sum(), (gaps < 3600).mean(), 'zero gaps', (gaps == 0).sum(),
      'closest gaps to 3600:', np.sort(gaps[np.abs(gaps - 3600) < 5]))
p7 = df[df.m >= 7.0].year.value_counts().reindex(range(2000, 2026), fill_value=0)
print('A9 top', p7.sort_values(ascending=False).head(3).to_dict(), 'bottom', p7.sort_values().head(3).to_dict())
print('A10', np.median(df.m.values), 'sorted middle two:', np.sort(df.m.values)[N // 2 - 1: N // 2 + 1])
print('A11', (df.lat < 0).sum(), (df.lat > 0).sum(), (df.lat == 0).sum())
d7 = df.loc[df.m >= 7.0, 'd'].dropna().values
dall = df['d'].dropna().values
print('A12', np.median(d7), len(d7), np.median(dall), len(dall),
      'middle two of all:', np.sort(dall)[len(dall) // 2 - 1: len(dall) // 2 + 1],
      'middle of mag7 (odd n):', np.sort(d7)[len(d7) // 2])
# sensitivities
print('A12 on 1dp depth values:', np.median(np.round(d7, 1)), np.median(np.round(dall, 1)))
print('A12 vs mag<7 only:', np.median(df.loc[df.m < 7.0, 'd'].dropna().values))
print('mag just under thresholds (5.95..6, 6.95..7, 7.95..8, 8.95..9):',
      df.loc[((df.magn > 5.9) & (df.magn < 6.0)) | ((df.magn > 6.9) & (df.magn < 7.0))
             | ((df.magn > 7.9) & (df.magn < 8.0)) | ((df.magn > 8.9) & (df.magn < 9.0)), 'mag'].value_counts().to_dict())
