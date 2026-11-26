# Waypoints along the Pacific coast of the Americas, Callao to Ketchikan, written before any lag was computed.
# Coarse (the Gulf of Panama and the mouth of the Gulf of California are crossed in a straight line);
# good to a few per cent. Distance along the line is from La Libertad, north positive, in km.
import math
WAY = [
 ("Callao", -12.07, -77.17), ("", -9.1, -78.6), ("", -5.9, -81.1), ("Talara", -4.6, -81.3),
 ("La Libertad", -2.22, -80.91), ("", -1.05, -80.9), ("", 0.65, -80.1), ("", 1.8, -78.9), ("", 3.8, -77.3),
 ("", 5.5, -77.5), ("", 7.9, -78.4), ("", 7.47, -80.0), ("", 8.03, -82.87), ("Quepos", 9.43, -84.17),
 ("", 9.56, -85.11), ("", 10.9, -85.95), ("", 13.0, -87.7), ("Acajutla", 13.57, -89.84), ("", 14.5, -92.2),
 ("", 16.17, -95.2), ("", 15.65, -96.5), ("Acapulco", 16.84, -99.85), ("", 17.93, -102.18),
 ("Manzanillo", 19.06, -104.3), ("", 20.4, -105.7), ("", 23.2, -106.42), ("Cabo San Lucas", 22.88, -109.91),
 ("", 24.6, -112.1), ("", 26.7, -113.6), ("", 27.85, -115.08), ("", 29.95, -115.8), ("Ensenada", 31.85, -116.63),
 ("San Diego", 32.71, -117.17), ("La Jolla", 32.87, -117.26), ("", 33.72, -118.27), ("Vandenberg", 34.56, -120.61),
 ("", 36.3, -121.9), ("San Francisco", 37.81, -122.47), ("", 38.95, -123.74), ("", 40.44, -124.41),
 ("Crescent City", 41.75, -124.18), ("", 42.84, -124.56), ("South Beach", 44.63, -124.04), ("", 46.25, -124.06),
 ("Neah Bay", 48.37, -124.62), ("Tofino", 49.15, -125.91), ("", 50.78, -128.43), ("Prince Rupert", 54.32, -130.32),
 ("Ketchikan", 55.33, -131.63),
]
def gc(a, b):
    R = 6371.0
    p1, p2 = math.radians(a[0]), math.radians(b[0]); dl = math.radians(b[1] - a[1])
    h = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))
def distances():
    cum = [0.0]
    for i in range(1, len(WAY)):
        cum.append(cum[-1] + gc(WAY[i - 1][1:], WAY[i][1:]))
    i0 = [w[0] for w in WAY].index("La Libertad")
    return {w[0]: cum[i] - cum[i0] for i, w in enumerate(WAY) if w[0]}
# Santa Cruz (Galapagos) is not on the coast: its distance is counted along the equator to the coast
# at 80.1 W and then down to La Libertad, and is given as a negative number.
SANTA_CRUZ_TO_COAST = gc((-0.755, -90.313), (-0.755, -80.5)) + gc((-0.755, -80.5), (-2.22, -80.91))
if __name__ == "__main__":
    for k, v in distances().items(): print(f"{k:<16} {v:8.0f} km")
    print(f"{'Santa Cruz':<16} {-SANTA_CRUZ_TO_COAST:8.0f} km (across open water)")
