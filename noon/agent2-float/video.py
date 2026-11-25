"""A film of the floating cube: its density rises from 0.05 to 0.95 and it takes the lowest attitude at each.
usage: python video.py out.mp4 [frame.png seconds]      (with the last two: write one frame as a picture and stop)
The attitudes are those found in floating.py/sliver.py: face up below (3 - sqrt 3)/6; then leaning by atan sqrt(12 d (1 - d) - 2),
any way round (the film lets the lean wander round to show that); corner up from 0.2269; the mirror image above a half.
The tip from the lean to the corner is drawn as a smooth turn; a real cube would topple."""
import sys, math, itertools, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib

W, H, SS, FPS = 1280, 720, 2, 30
INK, MUTED, NEUTRAL, BLUE, ORANGE = (43, 38, 34), (111, 103, 94), (185, 177, 165), (42, 120, 214), (235, 104, 52)
BG, WOOD, WATER = (251, 250, 247), (226, 192, 141), (156, 195, 238)
FONT = matplotlib.get_data_path() + "/fonts/ttf/DejaVuSans.ttf"
F = {s: ImageFont.truetype(FONT, s * SS) for s in (15, 17, 20, 26, 34)}
D1, D2, D3 = (3 - math.sqrt(3)) / 6, (3 - math.sqrt(2)) / 7, 0.22689      # face up ends; the ring ends; corner up takes over
CORNER = math.atan(math.sqrt(2))

def lean(d):
    return math.atan(math.sqrt(max(0.0, 12 * d * (1 - d) - 2)))

def level(n, d):
    """height of the water plane above the cube's centre, along n, for the share d under water"""
    w = np.abs(n); w = w[w > 1e-6]; k = len(w)
    sums = np.array([sum(c) for r in range(k + 1) for c in itertools.combinations(w, r)]); sign = np.array([(-1) ** r for r in range(k + 1) for _ in itertools.combinations(w, r)])
    V = lambda t: float((sign * np.maximum(0.0, t - sums) ** k).sum() / (math.factorial(k) * np.prod(w)))
    lo, hi = 0.0, float(w.sum())
    for _ in range(50):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if V(mid) < d else (lo, mid)
    return (lo + hi) / 2 - np.abs(n).sum() / 2

def rot_to_vertical(n):
    a = np.cross(n, [0.0, 0.0, 1.0]); s = np.linalg.norm(a)
    if s < 1e-12: return np.eye(3)
    a /= s; ang = math.acos(np.clip(n[2], -1, 1)); K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + math.sin(ang) * K + (1 - math.cos(ang)) * K @ K

# ---- the script of the film: (seconds, function of s in [0, 1] giving density, lean in radians, azimuth in radians, caption)
ease = lambda s: s * s * (3 - 2 * s)
def ring_up(s):
    d = D1 + (D3 - D1) * s; return d, lean(d), math.radians(405 * ease(s)), f"leaning {math.degrees(lean(d)):.0f}°, and as content to lean any way round"
def ring_down(s):
    d = 1 - D3 + (D3 - D1) * s; return d, lean(1 - d), math.radians(45 + 405 * ease(s)), f"leaning {math.degrees(lean(1 - d)):.0f}°, any way round"
SCRIPT = [
    (1.2, lambda s: (0.05, 0.0, 0.0, "face up")),
    (4.0, lambda s: (0.05 + (D1 - 0.05) * s, 0.0, 0.0, "face up")),
    (8.0, ring_up),
    (1.4, lambda s: (D3, lean(D3) + (CORNER - lean(D3)) * ease(s), math.radians(45), "over it goes, onto a corner")),
    (4.5, lambda s: (D3 + (0.5 - D3) * s, CORNER, math.radians(45), "corner up")),
    (1.8, lambda s: (0.5, CORNER, math.radians(45), "corner up, half under: the water line is a regular hexagon")),
    (4.5, lambda s: (0.5 + (0.5 - D3) * s, CORNER, math.radians(45), "corner up")),
    (1.4, lambda s: (1 - D3, CORNER + (lean(D3) - CORNER) * ease(s), math.radians(45), "and back")),
    (8.0, ring_down),
    (4.0, lambda s: (1 - D1 + (0.95 - (1 - D1)) * s, 0.0, 0.0, "face up")),
    (1.6, lambda s: (0.95, 0.0, 0.0, "face up, as ice floats (0.92)")),
]
TOTAL = sum(t for t, _ in SCRIPT)
def state(t):
    for dur, f in SCRIPT:
        if t < dur: return f(t / dur)
        t -= dur
    return SCRIPT[-1][1](1.0)

# ---- drawing
AZ, EL, SCALE, CX, CY = math.radians(-32), math.radians(17), 215, 470, 330
ca, sa, ce, se = math.cos(AZ), math.sin(AZ), math.cos(EL), math.sin(EL)
def view(p):                                        # world -> (screen right, screen up, towards the viewer)
    x = p[..., 0] * ca - p[..., 1] * sa; y = p[..., 0] * sa + p[..., 1] * ca
    return np.stack([x, p[..., 2] * ce + y * se, -y * ce + p[..., 2] * se], -1)
def px(p):
    v = view(np.asarray(p, float)); return [((CX + SCALE * a) * SS, (CY - SCALE * b) * SS) for a, b in v[..., :2].reshape(-1, 2)]
# unit vector from the scene towards the viewer, in world coordinates
TOWARDS = np.linalg.solve(np.array([[ca, -sa, 0], [sa * se, ca * se, ce], [-sa * ce, -ca * ce, se]]), [0, 0, 1.0])
LIGHT = np.array([-0.45, -0.35, 0.82]); LIGHT /= np.linalg.norm(LIGHT)
VERT = np.array(list(itertools.product([-0.5, 0.5], repeat=3)))
FACES = [([0, 1, 3, 2], (-1, 0, 0)), ([4, 6, 7, 5], (1, 0, 0)), ([0, 4, 5, 1], (0, -1, 0)), ([2, 3, 7, 6], (0, 1, 0)), ([0, 2, 6, 4], (0, 0, -1)), ([1, 5, 7, 3], (0, 0, 1))]

def clip(poly, keep_above):
    """the part of a polygon with z >= 0 (or <= 0), and the segment where it meets z = 0"""
    out, cut = [], []; sgn = 1 if keep_above else -1
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]; za, zb = sgn * a[2], sgn * b[2]
        if za >= 0: out.append(a)
        if (za > 0 and zb < 0) or (za < 0 and zb > 0):
            p = a + (b - a) * (za / (za - zb)); p[2] = 0.0; out.append(p); cut.append(p)
    return out, cut

def mix(c, k, other=(0, 0, 0)):
    return tuple(int(round(c[i] * (1 - k) + other[i] * k)) for i in range(3))

def frame(t):
    d, th, ph, cap = state(t)
    n = np.array([math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th)])
    R = rot_to_vertical(n); P = VERT @ R.T; P[:, 2] -= level(n, d)                      # world coordinates, water at z = 0
    im = Image.new("RGB", (W * SS, H * SS), BG); dr = ImageDraw.Draw(im, "RGBA")
    S = 1.3; sq = np.array([[-S, -S, 0], [S, -S, 0], [S, S, 0], [-S, S, 0.0]]); sp = px(sq)
    # the part under water, tinted
    section = []
    for idx, nb in FACES:
        nw = R @ np.array(nb, float); poly = [P[i].copy() for i in idx]
        low, cut = clip(poly, False); section += cut
        if nw @ TOWARDS > 1e-9 and len(low) >= 3:
            shade = 0.70 + 0.30 * max(0.0, nw @ LIGHT)
            dr.polygon(px(low), fill=mix(mix(WOOD, 1 - shade), 0.5, WATER) + (255,), outline=mix(INK, 0.45, WATER) + (255,), width=SS)
    # the water surface
    dr.polygon(sp, fill=WATER + (110,), outline=mix(WATER, 0.25) + (255,))
    # the part above water
    for idx, nb in FACES:
        nw = R @ np.array(nb, float); poly = [P[i].copy() for i in idx]
        up, cut = clip(poly, True)
        if nw @ TOWARDS > 1e-9 and len(up) >= 3:
            shade = 0.70 + 0.30 * max(0.0, nw @ LIGHT)
            dr.polygon(px(up), fill=mix(WOOD, 1 - shade) + (255,))
            dr.line(px(up) + px(up[:1]), fill=INK + (255,), width=int(1.6 * SS), joint="curve")
            if len(cut) == 2: dr.line(px(cut), fill=(255, 255, 255, 255), width=int(2.2 * SS))
    # the water line seen from above
    ox, oy, sc = 1040, 250, 105
    top = lambda q: ((ox + sc * (q[0] * ca - q[1] * sa)) * SS, (oy - sc * (q[0] * sa + q[1] * ca)) * SS)
    hull = P[:, :2]; c = hull.mean(0); ang = np.arctan2(hull[:, 1] - c[1], hull[:, 0] - c[0])
    from scipy.spatial import ConvexHull
    hv = ConvexHull(hull).vertices
    dr.polygon([top(P[i]) for i in hv], outline=NEUTRAL + (255,), width=SS)
    sides = 0
    if section:
        pts = np.array(section); c = pts.mean(0); o = np.argsort(np.arctan2(pts[:, 1] - c[1], pts[:, 0] - c[0])); pts = pts[o]
        keep = [pts[0]]
        for q in pts[1:]:
            if np.linalg.norm(q - keep[-1]) > 1e-6: keep.append(q)
        if len(keep) > 1 and np.linalg.norm(keep[0] - keep[-1]) < 1e-6: keep.pop()
        sides = len(keep)
        if sides >= 3: dr.polygon([top(q) for q in keep], fill=WATER + (255,), outline=INK + (255,), width=int(1.4 * SS))
    dr.text((ox * SS, (oy - 150) * SS), "the water line, from above", font=F[17], fill=INK, anchor="ms")
    dr.text((ox * SS, (oy + 150) * SS), f"{sides} sides", font=F[17], fill=MUTED, anchor="ms")
    # words
    dr.text((60 * SS, 44 * SS), "A uniform cube, made steadily denser", font=F[26], fill=INK, anchor="ls")
    dr.text((60 * SS, 74 * SS), "It takes the attitude in which its centre of gravity is lowest above its centre of buoyancy.", font=F[15], fill=MUTED, anchor="ls")
    dr.text((ox * SS, 470 * SS), f"density {d:.3f}", font=F[34], fill=INK, anchor="ms")
    # the density bar
    x0, x1, yb = 60, W - 60, H - 64; X = lambda v: (x0 + (x1 - x0) * v) * SS
    for a, b, col in ((0, D1, NEUTRAL), (D1, D3, ORANGE), (D3, 1 - D3, BLUE), (1 - D3, 1 - D1, ORANGE), (1 - D1, 1, NEUTRAL)):
        dr.rectangle([X(a) + (SS if a else 0), (yb - 5) * SS, X(b) - SS, (yb + 5) * SS], fill=col + (255,))
    for v, lab in ((0, "0"), (0.219, "0.211 to 0.227"), (0.5, "0.5"), (0.781, "0.773 to 0.789"), (1, "1")):
        dr.text((X(v), (yb + 30) * SS), lab, font=F[15], fill=MUTED, anchor="ms")
    for v, lab in ((0.105, "face up"), (0.36, "corner up"), (0.64, "corner up"), (0.895, "face up")):
        dr.text((X(v), (yb + 30) * SS), lab, font=F[15], fill=INK, anchor="ms")
    dr.polygon([(X(d), (yb - 8) * SS), (X(d) - 8 * SS, (yb - 24) * SS), (X(d) + 8 * SS, (yb - 24) * SS)], fill=INK + (255,))
    dr.text((60 * SS, (yb - 52) * SS), cap, font=F[20], fill=INK, anchor="ls")
    if D1 < d < D3 or 1 - D3 < d < 1 - D1:
        dr.text(((W - 60) * SS, (yb - 52) * SS), "(the film slows down here)", font=F[15], fill=MUTED, anchor="rs")
    return im.resize((W, H), Image.LANCZOS)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        frame(float(sys.argv[3])).save(sys.argv[2]); sys.exit()
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19', '-movflags', '+faststart', sys.argv[1]], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)):
        ff.stdin.write(frame(i / FPS).tobytes())
    ff.stdin.close(); ff.wait(); print(f"{TOTAL:.1f} seconds, {int(TOTAL * FPS)} frames")
