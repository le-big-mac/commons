"""Random domino tilings of the Aztec diamond by domino shuffling, as written in expectations.md.
usage: python aztec.py exhaustive | python aztec.py runs runs.json | python aztec.py picture N SEED out.png | python aztec.py film out.mp4
A tiling of order n is a 2n x 2n array of 0/1 cells: block (i, j) is cells (2i..2i+1, 2j..2j+1) = [[a, b], [c, d]], the dimers on the
north-west, north-east, south-west and south-east sides of that block."""
import sys, json, math, itertools
import numpy as np

def parts(x): return x[0::2, 0::2], x[0::2, 1::2], x[1::2, 0::2], x[1::2, 1::2]
def fillable(x):
    a, b, c, d = parts(x); n = a.shape[0]; empty = ~(a | b | c | d)
    up = np.zeros((n, n), bool); up[1:, :] = (c | d)[:-1, :]            # the block's top corner is touched from the block above
    down = np.zeros((n, n), bool); down[:-1, :] = (a | b)[1:, :]
    left = np.zeros((n, n), bool); left[:, 1:] = (b | d)[:, :-1]
    right = np.zeros((n, n), bool); right[:, :-1] = (a | c)[:, 1:]
    return empty & ~up & ~down & ~left & ~right
def holes(x):
    """the corrected step 4: scanning in reading order, a candidate block is a hole unless the block above it has just been filled.
    (fillable() alone, as the sealed sheet has it, also takes blocks that overlap a hole: see exhaustive-as-sealed.out.)"""
    cand = fillable(x); n = cand.shape[0]; rows = np.arange(n)[:, None] * np.ones((1, n), int)
    last_gap = np.maximum.accumulate(np.where(cand, -1, rows), axis=0)            # the last row at or above that is not a candidate
    return cand & ((rows - last_gap) % 2 == 1)                                     # first, third, fifth ... of each vertical run of candidates
def fill(x, where, toss):
    """toss: one boolean per fillable block, in row order; True = a and d, False = b and c"""
    a, b, c, d = parts(x); diag = np.zeros(where.shape, bool); diag[where] = toss; anti = where & ~diag
    a |= diag; d |= diag; b |= anti; c |= anti
def shuffle(x):
    """steps 1 to 3: embed with a shift of half a block, delete facing pairs, slide"""
    n2 = x.shape[0]; y = np.zeros((n2 + 2, n2 + 2), bool); y[1:-1, 1:-1] = x
    a, b, c, d = parts(y)
    bad = a & d; a[bad] = False; d[bad] = False
    bad = b & c; b[bad] = False; c[bad] = False
    a0, b0 = a.copy(), b.copy(); a[:] = d; d[:] = a0; b[:] = c; c[:] = b0
    return y
def is_tiling(x):
    a, b, c, d = (p.astype(int) for p in parts(x)); n = a.shape[0]
    top = np.zeros((n + 1, n), int); top[:n] += a + b; top[1:] += c + d          # top-and-bottom corners of the blocks
    side = np.zeros((n, n + 1), int); side[:, :n] += a + c; side[:, 1:] += b + d  # left-and-right corners
    return bool((top == 1).all() and (side == 1).all())
def grow(n, rng, readings=None, at=()):
    x = np.zeros((2, 2), bool); w = holes(x); fill(x, w, rng.random(int(w.sum())) < 0.5); tosses = int(w.sum()); out = {}
    for order in range(2, n + 1):
        x = shuffle(x); w = holes(x); k = int(w.sum()); fill(x, w, rng.random(k) < 0.5); tosses += k
        if order in at: out[order] = readings(x, tosses)
    return x, tosses, out

def exhaustive(nmax=5, rule=None):
    rule = rule or holes
    def rec(x, order, target, found):
        if order == target: found.append(x.tobytes()); return is_tiling(x)
        y = shuffle(x) if order else np.zeros((2, 2), bool); w = rule(y); k = int(w.sum()); ok = True
        for toss in itertools.product((False, True), repeat=k):
            z = y.copy(); fill(z, w, np.array(toss, bool)); ok &= rec(z, order + 1, target, found)
        return ok
    res = {}
    for n in range(1, nmax + 1):
        found = []; ok = rec(None, 0, n, found)
        res[n] = dict(sequences=len(found), different=len(set(found)), all_tilings=bool(ok), expected=2 ** (n * (n + 1) // 2))
        print(f"order {n}: {len(found)} sequences of tosses, {len(set(found))} different configurations, every one a tiling: {ok}; 2^(n(n+1)/2) = {2 ** (n * (n + 1) // 2)}", flush=True)
    return res

def readings(x, tosses):
    from scipy.ndimage import label
    a, b, c, d = parts(x); n = a.shape[0]; only = lambda p, q, r, s: p & ~q & ~r & ~s
    oa = only(a, b, c, d); diag = np.diagonal(oa); K = int(np.argmin(diag)) if not diag.all() else n
    frozen = 0
    for mask, corner in ((oa, (0, 0)), (only(b, a, c, d), (0, n - 1)), (only(c, a, b, d), (n - 1, 0)), (only(d, a, b, c), (n - 1, n - 1))):
        lab, _ = label(mask); frozen += int((lab == lab[corner]).sum()) if mask[corner] else 0
    lo, hi = int(0.4 * n), int(0.6 * n); cen = [int(p[lo:hi, lo:hi].sum()) for p in (a, b, c, d)]
    return dict(n=n, K=K, frozen=frozen / n ** 2, centre=[v / sum(cen) for v in cen], tosses=tosses, tiling=is_tiling(x))
def four_corners(x, tosses):
    """K at each of the four corners: the first block along the diagonal from that corner that does not hold exactly that corner's dimer"""
    a, b, c, d = parts(x); n = a.shape[0]; out = []
    for mask in (a & ~b & ~c & ~d, (b & ~a & ~c & ~d)[:, ::-1], (c & ~a & ~b & ~d)[::-1, :], (d & ~a & ~b & ~c)[::-1, ::-1]):
        diag = np.diagonal(mask); out.append(int(np.argmin(diag)) if not diag.all() else n)
    return out
def corner_run(seed):
    rng = np.random.default_rng(seed); _, _, out = grow(1600, rng, four_corners, at=(100, 200, 400, 800, 1600)); return out
def one_run(seed):
    rng = np.random.default_rng(seed); _, _, out = grow(1600, rng, readings, at=(100, 200, 400, 800, 1600)); return out

COL = {'a': (42, 120, 214), 'b': (235, 104, 52), 'c': (27, 175, 122), 'd': (237, 161, 0)}
def draw(x, size, pad=20, bg=(251, 250, 247), nmax=None):
    """the tiling as dominoes, in the usual picture (a diamond): each dimer is a 1 x 2 domino, coloured by its kind"""
    from PIL import Image, ImageDraw
    a, b, c, d = parts(x); n = a.shape[0]; s = (size - 2 * pad) / (2 * (nmax or n) + 2); im = Image.new("RGB", (size, size), bg); dr = ImageDraw.Draw(im)
    P = lambda X, Y: (size / 2 + s * (X - Y) / 2, size / 2 + s * ((X + Y) / 2 - n))        # block-corner coordinates (X across, Y down) -> picture, the diamond's centre in the middle
    for name, arr, (dx1, dy1, dx2, dy2) in (('a', a, (1, 0, 0, 1)), ('b', b, (1, 0, 2, 1)), ('c', c, (0, 1, 1, 2)), ('d', d, (2, 1, 1, 2))):
        for i, j in zip(*np.nonzero(arr)):
            p, q = P(2 * j + dx1, 2 * i + dy1), P(2 * j + dx2, 2 * i + dy2)                # the two cells the domino covers
            x0, x1 = min(p[0], q[0]) - s / 2, max(p[0], q[0]) + s / 2; y0, y1 = min(p[1], q[1]) - s / 2, max(p[1], q[1]) + s / 2
            dr.rectangle([x0 + min(0.5, s / 8), y0 + min(0.5, s / 8), x1 - min(0.5, s / 8), y1 - min(0.5, s / 8)], fill=COL[name])
    return im

if __name__ == '__main__':
    if sys.argv[1] == 'exhaustive': json.dump(exhaustive(), open('exhaustive.json', 'w'))
    elif sys.argv[1] == 'exhaustive-as-sealed': exhaustive(rule=fillable)
    elif sys.argv[1] == 'runs':
        from concurrent.futures import ProcessPoolExecutor
        with ProcessPoolExecutor(max_workers=8) as ex: res = list(ex.map(one_run, range(100, 200)))
        json.dump(res, open(sys.argv[2], 'w')); print(len(res), "runs")
    elif sys.argv[1] == 'corners':                      # python aztec.py corners SEED0 RUNS out.json
        from concurrent.futures import ProcessPoolExecutor
        s0, k = int(sys.argv[2]), int(sys.argv[3])
        with ProcessPoolExecutor(max_workers=8) as ex: res = list(ex.map(corner_run, range(s0, s0 + k)))
        json.dump(res, open(sys.argv[4], 'w')); print(len(res), "runs")
    elif sys.argv[1] == 'picture':
        x, tosses, _ = grow(int(sys.argv[2]), np.random.default_rng(int(sys.argv[3]))); draw(x, 2400).resize((1200, 1200)).save(sys.argv[4]); print("order", sys.argv[2], "tosses", tosses, "tiling", is_tiling(x))
    elif sys.argv[1] == 'film':
        import subprocess
        from PIL import Image, ImageDraw, ImageFont
        import matplotlib
        W, H, SS, FPS, NMAX, PER = 1280, 720, 2, 20, 150, 2                      # two pictures for each order: ten orders a second
        INK, MUTED, BG = (43, 38, 34), (111, 103, 94), (251, 250, 247)
        FONT = matplotlib.get_data_path() + "/fonts/ttf/DejaVuSans.ttf"; F = {k: ImageFont.truetype(FONT, k * SS) for k in (15, 20, 28, 40)}
        rng = np.random.default_rng(11); x = np.zeros((2, 2), bool); w = holes(x); fill(x, w, rng.random(int(w.sum())) < 0.5)
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-movflags', '+faststart', sys.argv[2]], stdin=subprocess.PIPE)
        for order in range(1, NMAX + 1):
            if order > 1: x = shuffle(x); w = holes(x); fill(x, w, rng.random(int(w.sum())) < 0.5)
            im = Image.new("RGB", (W * SS, H * SS), BG); im.paste(draw(x, H * SS, pad=14 * SS, nmax=NMAX), (0, 0)); dr = ImageDraw.Draw(im)
            X0 = 760 * SS
            dr.text((X0, 70 * SS), "The arctic circle", font=F[28], fill=INK, anchor="ls")
            for k, line in enumerate(("A diamond tiled with dominoes, chosen evenly", "from all the ways of tiling it, and grown one", "order at a time by domino shuffling.")):
                dr.text((X0, (104 + 22 * k) * SS), line, font=F[15], fill=MUTED, anchor="ls")
            dr.text((X0, 250 * SS), f"order {order}", font=F[40], fill=INK, anchor="ls")
            digits = int(order * (order + 1) / 2 * math.log10(2)) + 1
            dr.text((X0, 290 * SS), f"{order * (order + 1):,} dominoes", font=F[20], fill=INK, anchor="ls")
            dr.text((X0, 322 * SS), ("the number of tilings has " + f"{digits:,} digits") if digits > 6 else f"{2 ** (order * (order + 1) // 2):,} tilings", font=F[20], fill=INK, anchor="ls")
            for k, (name, lab) in enumerate((('a', "lying; frozen at the top"), ('b', "standing; frozen at the right"), ('c', "standing; frozen at the left"), ('d', "lying; frozen at the bottom"))):
                dr.rectangle([X0, (400 + 30 * k) * SS, X0 + 34 * SS, (417 + 30 * k) * SS], fill=COL[name]); dr.text((X0 + 46 * SS, (414 + 30 * k) * SS), lab, font=F[15], fill=MUTED, anchor="ls")
            for k, line in enumerate(("The four corners freeze, each into one kind", "of domino. What is left unfrozen in the", "middle tends to a circle.")):
                dr.text((X0, (580 + 22 * k) * SS), line, font=F[15], fill=INK, anchor="ls")
            out = im.resize((W, H), Image.LANCZOS).tobytes()
            for _ in range(PER * (10 if order <= 4 else 1) if order < NMAX else 4 * FPS): ff.stdin.write(out)
        ff.stdin.close(); ff.wait(); print("film written; order", NMAX, "is a tiling:", is_tiling(x))
