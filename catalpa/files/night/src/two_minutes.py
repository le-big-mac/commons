# How long is the brightening in time? A twilight 50 to 60 per cent brighter passes a given brightness with the Sun
# lower by (the brightening in magnitudes) / (the fall of the twilight in magnitudes for a degree); the Sun sinks at a
# rate that depends on the latitude and the season. For June to August, at the latitudes of the eleven places.
import numpy as np
fall = (14.39 - 13.08)                      # magnitudes for a degree between 6 and 7 degrees down, the eleven places (depth.out)
for pct in (50, 60):
    mag = 2.5 * np.log10(1 + pct / 100); ddeg = mag / fall; row = []
    for lat in (-21, -31, -41):
        for dec in (23.4, 15.0):            # the Sun's declination: late June, and early August
            la, de, h = np.radians(lat), np.radians(dec), np.radians(-6.7)
            cosH = (np.sin(h) - np.sin(la) * np.sin(de)) / (np.cos(la) * np.cos(de)); rate = 15.0 * np.cos(la) * np.cos(de) * np.sqrt(1 - cosH ** 2) / np.cos(h) / 60.0   # degrees a minute
            row.append(ddeg / rate)
    print(f'{pct} per cent brighter = {mag:.2f} magnitude = the Sun {ddeg:.2f} degree lower at the passing; at 21, 31 and 41 degrees south, late June and early August, that takes {min(row):.1f} to {max(row):.1f} minutes')
# and how long after sunset the meters pass their level (the Sun from 0.83 degree down, which is sunset, to 6.5 down)
row = []
for lat in (-21, -31, -41):
    for dec in (23.4, 15.0, 0.0, -23.4):
        la, de = np.radians(lat), np.radians(dec); t = []
        for h in (-0.83, -6.5):
            cosH = (np.sin(np.radians(h)) - np.sin(la) * np.sin(de)) / (np.cos(la) * np.cos(de)); t.append(np.degrees(np.arccos(cosH)) * 4.0)      # minutes of hour angle
        row.append(t[1] - t[0])
print(f'from sunset to the Sun 6.5 degrees down, at 21, 31 and 41 degrees south, through the year: {min(row):.0f} to {max(row):.0f} minutes')
