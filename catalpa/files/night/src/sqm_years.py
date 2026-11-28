# For the record beside the fifteenth sheet: the second make's four southern stations, the fading from 3 to 7 degrees,
# each year from 2019 to 2025 less 2021. Reductions of 2021 to 2025 are those of the thirteenth sheet
# (cache2/sqm_months.pkl); 2019 and 2020 are reduced here from data/sqm2 (fetched by src/sqm_fetch3.py), by the same
# function (src/sqm_depth.py through src/sqm_months.py).
import pickle, importlib.util
import numpy as np
B = '/home/agent1/night/'
spec = importlib.util.spec_from_file_location('sqm_months', B + 'src/sqm_months.py'); SM = importlib.util.module_from_spec(spec); spec.loader.exec_module(SM)
SD = SM.SD; ST = SD.ST
if __name__ == '__main__':
    R = pickle.load(open(B + 'cache2/sqm_months.pkl', 'rb'))
    for c in ST:
        for y in (2019, 2020):
            for m in range(1, 13): R[(c, y, m)] = SD.reduce(c, y, m)
    pickle.dump(R, open(B + 'cache2/sqm_years.pkl', 'wb'))
    def F(c, y, m, dp):
        r = R.get((c, y, m)); a, b = SD.fig(r, dp), SD.fig(r, 3.0); return (a - b) if a is not None and b is not None else None
    YEARS = (2019, 2020, 2022, 2023, 2024, 2025)
    for dp in (7.0, 8.0):
        print(f'the second make: the fading from 3 to {dp:g} degrees, each year less 2021 (the mean over the months both years have, and how many; negative: brighter at depth than in 2021)')
        for c, (name, lat, lon) in ST.items():
            row = []
            for y in YEARS:
                d = [F(c, y, m, dp) - F(c, 2021, m, dp) for m in range(1, 13) if F(c, y, m, dp) is not None and F(c, 2021, m, dp) is not None]
                row.append(f'{y} {np.mean(d):+.2f} ({len(d):2d})' if len(d) >= 3 else f'{y}   .      ')
            print(f"   {name.split(',')[0]:<14} " + '  '.join(row))
        print('   month by month, each station, the month less the same month of 2021 (hundredths):')
        for c, (name, lat, lon) in ST.items():
            for y in (2019, 2020):
                v = [(F(c, y, m, dp) - F(c, 2021, m, dp)) if F(c, y, m, dp) is not None and F(c, 2021, m, dp) is not None else None for m in range(1, 13)]
                if any(x is not None for x in v): print(f"   {name.split(',')[0]:<14} {y}: " + ' '.join(f'{100 * x:+4.0f}' if x is not None else '   .' for x in v))
