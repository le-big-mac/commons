# Pogson at Masulipatam, 18 Aug 1868: his timings in local mean time (Nath and Orchiston, JAHH 24(3), 2021, p. 639, Table 1, after Pogson 1869 pp. 7-8) against JPL Horizons,
# for places on the modern map: the middle of the town, the fort, today's district court, and two places further east toward the sea, to see how far east he would have had
# to stand to be as early as Tennant at Guntoor (his station was a "temporary residence" half a mile from the Small Cause Court; its exact place I do not have).
# UT = local mean time - longitude.  Clock correction 4.07 s (Stephenson, Morrison and Hohenkerk).
import sys; sys.path.insert(0, '/home/agent1/wander')
from hz_eclipse import contacts
jd0 = 2403562.5; dt = 4.07
obs_lmt = {'c2': 9 + 34 / 60 + 14.2 / 3600, 'c3': 9 + 40 / 60 + 5.8 / 3600, 'c4': 11 + 4 / 60 + 47.4 / 3600, 'c1est': 8 + 19 / 60 + 22 / 3600}
for name, lon, lat, what in (('masT', 81.1348, 16.1817, 'the town (map node)'), ('masF', 81.1493, 16.1510, 'the fort'), ('masC', 81.1359, 16.1950, 'the district court of today'),
                              ('masE', 81.1699, 16.1510, '2.2 km east of the fort'), ('masL', 81.1797, 16.1538, 'the ruin of the old lighthouse, 3.2 km east of the fort')):
    L = lon / 15.0; o = {k: (v - L) * 3600 for k, v in obs_lmt.items()}
    ev = [('c1', 'c1', 'standard', o['c1est']), ('c2', 'c2', 'smaller', o['c2']), ('c3', 'c3', 'smaller', o['c3']), ('c2s', 'c2', 'standard', o['c2']), ('c3s', 'c3', 'standard', o['c3']), ('c4', 'c4', 'standard', o['c4'])]
    r, dj = contacts(name, lon, lat, 0.005, jd0, dt, ev)
    print(f'Masulipatam, {what} ({lat} N, {lon} E): computed length of totality {r["c3"][0] - r["c2"][0]:.1f} s (smaller Moon), {r["c3s"][0] - r["c2s"][0]:.1f} (standard); Pogson {(obs_lmt["c3"] - obs_lmt["c2"]) * 3600:.1f} s')
    print(f'     seen minus computed: start of totality {o["c2"] - r["c2"][0]:+6.1f} s, end {o["c3"] - r["c3"][0]:+6.1f} (smaller Moon); {o["c2"] - r["c2s"][0]:+6.1f}, {o["c3"] - r["c3s"][0]:+6.1f} (standard); last contact {o["c4"] - r["c4"][0]:+6.1f}; first contact as a second observer estimated it {o["c1est"] - r["c1"][0]:+6.1f}')
