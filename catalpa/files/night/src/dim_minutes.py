# For the page on the darker northern twilight of 2019: what a twilight so much darker comes to in time. With the
# Sun 3 degrees down the meters' reading falls by so many magnitudes for each further degree of the Sun's sinking
# (from the first make's own readings at 3 and 5 degrees: cache2/years.pkl, cache2/depth.pkl, northern places, all
# months of 2018 to 2021), and the Sun takes so many minutes to sink a degree there (plain spherical astronomy at
# the latitudes of the places, solstices and equinox). A reading 0.19 to 0.33 magnitude darker is then the reading
# that an ordinary evening gives so many minutes later.
import math, pickle, importlib.util
import numpy as np
B = '/home/agent1/night/'
spec = importlib.util.spec_from_file_location('depth', B + 'src/depth.py'); DP = importlib.util.module_from_spec(spec); spec.loader.exec_module(DP)
R = dict(pickle.load(open(B + 'cache2/depth.pkl', 'rb'))); R.update(pickle.load(open(B + 'cache2/years.pkl', 'rb')))
sl = [(DP.monthfig(r, 5.0) - DP.monthfig(r, 3.0)) / 2.0 for (s, y, m), r in R.items() if s in DP.NORTH and 2018 <= y <= 2021 and r is not None and DP.monthfig(r, 5.0) is not None and DP.monthfig(r, 3.0) is not None]
slope = float(np.median(sl)); print(f'the reading falls by {slope:.2f} magnitudes for each degree the Sun sinks between 3 and 5 degrees down (the middle of {len(sl)} months of the northern places; a quarter of them below {np.percentile(sl, 25):.2f}, a quarter above {np.percentile(sl, 75):.2f})')
def minutes_per_degree(lat, dec):
    f = lambda a: math.degrees(math.acos((math.sin(math.radians(a)) - math.sin(math.radians(lat)) * math.sin(math.radians(dec))) / (math.cos(math.radians(lat)) * math.cos(math.radians(dec)))))
    return (f(-4.0) - f(-3.0)) * 4.0
for lat in (37.0, 43.0, 48.0, 59.0):
    v = [minutes_per_degree(lat, dec) for dec in (-23.44, 0.0, 23.44)]
    print(f'at {lat:g} north the Sun takes {min(v):.1f} to {max(v):.1f} minutes to sink from 3 to 4 degrees down (solstices and equinox); a reading 0.19 magnitude darker is {0.19 / slope * min(v):.1f} to {0.19 / slope * max(v):.1f} minutes of dusk, 0.33 darker is {0.33 / slope * min(v):.1f} to {0.33 / slope * max(v):.1f}')
