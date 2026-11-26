"""Angular distances of named places from the woodpecker centre and the land centre, and antipodes of
South American places. usage: python -I places.py   (no input files)"""
import numpy as np

def unit(la, lo):
    la, lo = np.radians(la), np.radians(lo)
    return np.array([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)])

def ang(a, b):
    return float(np.degrees(np.arccos(np.clip(unit(*a) @ unit(*b), -1, 1))))

WP = (43.0, -0.9); LAND = (40.82, 1.72)
asia = [("Delhi", 28.6, 77.2), ("Kathmandu", 27.7, 85.3), ("Kolkata", 22.6, 88.4), ("Colombo", 6.9, 79.9),
        ("Yangon", 16.8, 96.2), ("Bangkok", 13.75, 100.5), ("Hanoi", 21.0, 105.85), ("Vientiane", 17.97, 102.6),
        ("Phnom Penh", 11.56, 104.92), ("Ho Chi Minh City", 10.8, 106.7), ("Da Nang", 16.05, 108.2),
        ("Kunming", 25.04, 102.7), ("Chengdu", 30.66, 104.07), ("Beijing", 39.9, 116.4), ("Shanghai", 31.23, 121.47),
        ("Guangzhou", 23.13, 113.26), ("Hong Kong", 22.3, 114.17), ("Fuzhou", 26.07, 119.3), ("Haikou (Hainan)", 20.04, 110.34),
        ("Taipei", 25.03, 121.57), ("Seoul", 37.57, 126.98), ("Tokyo", 35.68, 139.69), ("Sapporo", 43.06, 141.35),
        ("Kuala Lumpur", 3.14, 101.69), ("Medan", 3.59, 98.67), ("Singapore", 1.35, 103.82), ("Manila", 14.6, 120.98)]
print("distance in degrees from the woodpecker centre 43.0 N, 0.9 W and from the land centre 40.82 N, 1.72 E (inside if under 90)")
for n, la, lo in asia:
    print("  %-20s %7.2f %7.2f" % (n, ang(WP, (la, lo)), ang(LAND, (la, lo))))
sam = [("Caracas", 10.5, -66.9), ("Bogota", 4.7, -74.1), ("Quito", -0.18, -78.47), ("Manaus", -3.1, -60.0),
       ("Iquitos", -3.75, -73.25), ("Lima", -12.05, -77.04), ("Cusco", -13.53, -71.97), ("La Paz", -16.5, -68.15),
       ("Recife", -8.05, -34.9), ("Brasilia", -15.8, -47.9), ("Sao Paulo", -23.55, -46.63), ("Asuncion", -25.3, -57.6),
       ("Buenos Aires", -34.6, -58.38), ("Santiago", -33.45, -70.67), ("Punta Arenas", -53.16, -70.92)]
print("South American places: distance from the woodpecker centre, and the antipode")
for n, la, lo in sam:
    alo = lo + 180
    print("  %-14s %7.2f   antipode %6.2f N %7.2f E" % (n, ang(WP, (la, lo)), -la, alo))
