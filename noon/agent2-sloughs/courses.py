"""courses.py -- a map of the model river's successive courses, drawn in the manner of Plate 22 of Harold N. Fisk's report
to the Mississippi River Commission (1944), "Ancient courses, Mississippi River meander belt": each course a coloured ribbon,
the later laid over the earlier, the present course left white.

The river is one run of river.c (P = 3, cutoff distance 0.4 D, a valley 170 D long that repeats, seed 12), at sixteen moments
two units of time apart, t = 90 to 120.  The valley runs down the sheet.  The ribbons are drawn 1.6 D wide, some five times
the width a river of these settings would have (the papers' rivers are 0.2 to 0.5 D wide), so that successive courses
overlap as a wide river's would.  Small circles mark necks cut through, with the number of the course after which each was
cut (one in four of the longer loops is shown).

usage: python courses.py out/courses/s12.snap out/courses/s12.ox courses.png
"""
import sys, os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import matplotlib

snapfile, oxfile, outfile = sys.argv[1:4]
LX = 170.0; T0, DTS, NST = 90.0, 2.0, 16            # first course, time between courses, number of courses
SS = 2                                               # drawn at twice the size and reduced
W, H = 2000 * SS, 2960 * SS
PX = 16.0 * SS                                       # pixels to one D
TOP = 120 * SS                                       # the valley's x = 0 is this far down the sheet
AXIS = 0.60 * W                                      # the valley's axis is this far across
HALF = 0.8                                           # half the ribbon's width, in D
fonts = os.path.join(matplotlib.get_data_path(), "fonts", "ttf")
def font(name, size): return ImageFont.truetype(os.path.join(fonts, name), int(size * SS))
rng = np.random.default_rng(1944)

# ---- the courses ----
snaps = {}
for line in open(snapfile):
    f = line.split(); t = float(f[0])
    snaps[round(t, 3)] = np.array(f[2:], float).reshape(-1, 2)
courses = [snaps[round(T0 + k * DTS, 3)] for k in range(NST)]
ymean = np.mean([c[:, 1].mean() for c in courses])
def to_page(xy, shift=0.0):                          # model (x along the valley, y across) -> sheet (across, down)
    return np.stack([AXIS + (xy[:, 1] - ymean) * PX, TOP + (xy[:, 0] + shift) * PX], 1)

# ---- paper ----
paper = np.full((H, W, 3), (243, 234, 210), np.float32)
from scipy import ndimage
grain = ndimage.gaussian_filter(rng.normal(0, 1, (H // 8, W // 8)).astype(np.float32), 1.5)
grain = ndimage.zoom(grain, 8, order=1)[:H, :W]; grain = grain / grain.std()
paper += grain[:, :, None] * 1.6
yy, xx = np.mgrid[0:H, 0:W]
edge = np.minimum.reduce([xx, W - 1 - xx, yy, H - 1 - yy]).astype(np.float32)
paper -= np.clip(1 - edge / (90 * SS), 0, 1)[:, :, None] ** 2 * 14
sheet = Image.fromarray(np.clip(paper, 0, 255).astype(np.uint8))
d = ImageDraw.Draw(sheet)

# a faint survey grid under everything, a little off square to the sheet
ink_faint = (150, 146, 132)
ang = math.radians(11); step = 9 * PX
for k in range(-40, 60):
    for a in (ang, ang + math.pi / 2):
        cx, cy = W / 2 + k * step * math.cos(a + math.pi / 2), H / 2 + k * step * math.sin(a + math.pi / 2)
        d.line([(cx - 6000 * math.cos(a), cy - 6000 * math.sin(a)), (cx + 6000 * math.cos(a), cy + 6000 * math.sin(a))], fill=ink_faint, width=1)
sheet = Image.blend(Image.fromarray(np.clip(paper, 0, 255).astype(np.uint8)), sheet, 0.45)

# ---- fills: colour and pattern for each course, oldest first; the present course is left white ----
GREEN, SALMON, AQUA, YELLOW, PINK, ORANGE, RED, OLIVE = (186, 207, 154), (233, 112, 106), (158, 201, 190), (240, 224, 140), (242, 186, 174), (240, 178, 98), (214, 84, 78), (205, 214, 132)
styles = [(RED, "solid"), (ORANGE, "hatch"), (ORANGE, "solid"), (OLIVE, "stipple"), (GREEN, "hatch"), (OLIVE, "solid"), (PINK, "stipple"), (SALMON, "hatch"),
          (GREEN, "stipple"), (AQUA, "hatch"), (PINK, "solid"), (YELLOW, "solid"), (AQUA, "solid"), (SALMON, "solid"), (GREEN, "solid")]
assert len(styles) == NST - 1
def pattern(kind, colour):
    """An image of the fill: plain colour, white hatching on it, or white stipple on it."""
    img = Image.new("RGB", (W, H), colour)
    if kind == "hatch":
        dd = ImageDraw.Draw(img); gap = 9 * SS
        for k in range(-H, W, gap): dd.line([(k, 0), (k + H, H)], fill=(250, 244, 228), width=3 * SS)
    elif kind == "stipple":
        a = np.asarray(img).copy(); g = 7 * SS
        ys, xs = np.mgrid[g // 2:H:g, g // 2:W:g]; xs = xs + (ys // g % 2) * (g // 2)
        dd = ImageDraw.Draw(img)
        for x, y in zip(xs.ravel()[::1], ys.ravel()[::1]): dd.ellipse([x - SS, y - SS, x + SS, y + SS], fill=(250, 244, 228))
    return img
def ribbon_mask(xy, half):
    m = Image.new("L", (W, H), 0); dm = ImageDraw.Draw(m); wpx = int(round(2 * half * PX))
    for shift in (-LX, 0.0, LX):
        p = to_page(np.vstack([xy, xy[:1] + [LX, 0]]), shift)
        keep = (p[:, 1] > -200) & (p[:, 1] < H + 200)
        if keep.sum() < 2: continue
        pts = [tuple(q) for q in p]
        dm.line(pts, fill=255, width=wpx, joint="curve")
        r = wpx / 2
        for q in pts: dm.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], fill=255)
    return m.filter(ImageFilter.GaussianBlur(2.0 * SS)).point(lambda v: 255 if v > 127 else 0)       # an even bank line
ink = (58, 54, 48)
pats = {}
for k, xy in enumerate(courses):
    m = ribbon_mask(xy, HALF)
    outline = ImageChops.subtract(m.filter(ImageFilter.MaxFilter(2 * SS + 1)), m.filter(ImageFilter.MinFilter(2 * SS + 1)))
    if k < NST - 1:
        colour, kind = styles[k]
        if (kind, colour) not in pats: pats[(kind, colour)] = pattern(kind, colour)
        sheet.paste(pats[(kind, colour)], (0, 0), m)
        sheet.paste(Image.new("RGB", (W, H), ink), (0, 0), outline.point(lambda v: int(v * 0.55)))
    else:                                            # the present course: white, with a firmer bank line
        sheet.paste(Image.new("RGB", (W, H), (250, 246, 234)), (0, 0), m)
        outline = ImageChops.subtract(m.filter(ImageFilter.MaxFilter(4 * SS + 1)), m.filter(ImageFilter.MinFilter(2 * SS + 1)))
        sheet.paste(Image.new("RGB", (W, H), (30, 28, 26)), (0, 0), outline)
d = ImageDraw.Draw(sheet)

# ---- necks cut through: a small circle with the number of the course after which it was cut ----
fs = font("DejaVuSans.ttf", 9); shown = 0; cuts = 0
for i, line in enumerate(open(oxfile)):
    f = line.split(); t, arc = float(f[0]), float(f[1])
    if not (T0 < t <= T0 + (NST - 1) * DTS): continue
    cuts += 1
    if cuts % 4 or arc < 14: continue
    stage = int((t - T0) // DTS) + 1                 # cut after this course was drawn and before the next
    xy = np.array(f[2:], float).reshape(-1, 2); neck = 0.5 * (xy[0] + xy[-1]); neck[0] -= LX * math.floor(neck[0] / LX)
    px, py = to_page(neck[None, :])[0]; r = 8.5 * SS
    d.ellipse([px - r, py - r, px + r, py + r], fill=(250, 246, 234), outline=ink, width=SS)
    s = str(stage); tw = d.textlength(s, font=fs); d.text((px - tw / 2, py - 5.6 * SS), s, font=fs, fill=ink); shown += 1

# ---- the sheet's furniture: neat line, legend, title block, scale ----
blank = Image.fromarray(np.clip(paper, 0, 255).astype(np.uint8)); frame = Image.new("L", (W, H), 255); ImageDraw.Draw(frame).rectangle([40 * SS, 40 * SS, W - 40 * SS, H - 40 * SS], fill=0)
sheet.paste(blank, (0, 0), frame); d = ImageDraw.Draw(sheet)          # nothing is drawn outside the neat line
d.rectangle([40 * SS, 40 * SS, W - 40 * SS, H - 40 * SS], outline=ink, width=2 * SS)
serif, serifb, sans = "DejaVuSerif.ttf", "DejaVuSerif-Bold.ttf", "DejaVuSans.ttf"
def box(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(246, 239, 219), outline=ink, width=SS)
# legend
x0, y0 = 70 * SS, 70 * SS; x1 = x0 + 500 * SS; row = 27 * SS; y1 = y0 + 70 * SS + (NST + 0.6) * row + 168 * SS
box(x0, y0, x1, y1)
d.line([(x0, y0 + 34 * SS), (x1, y0 + 34 * SS)], fill=ink, width=SS); d.line([(x0 + 120 * SS, y0), (x0 + 120 * SS, y0 + 34 * SS)], fill=ink, width=SS)
d.text((x0 + 30 * SS, y0 + 9 * SS), "STAGE", font=font(sans, 13), fill=ink); d.text((x0 + 250 * SS, y0 + 9 * SS), "LEGEND", font=font(sans, 13), fill=ink)
fl = font(sans, 12)
for j in range(NST):
    k = NST - 1 - j; yb = y0 + 52 * SS + j * row
    d.text((x0 + 24 * SS, yb), "%d  (t = %g)" % (k + 1, T0 + k * DTS), font=fl, fill=ink)
    sw = [x0 + 150 * SS, yb - 2 * SS, x0 + 250 * SS, yb + 17 * SS]
    if k == NST - 1: d.rectangle(sw, fill=(250, 246, 234), outline=(30, 28, 26), width=2 * SS); d.text((x0 + 265 * SS, yb), "the river now", font=fl, fill=ink)
    else:
        colour, kind = styles[k]; d.rectangle(sw, fill=colour, outline=ink, width=SS)
        sheet.paste(pats[(kind, colour)].crop(tuple(int(v) for v in sw)), (int(sw[0]), int(sw[1]))); d = ImageDraw.Draw(sheet); d.rectangle(sw, outline=ink, width=SS)
        if k == NST - 2: d.text((x0 + 265 * SS, yb), "each course as it lay", font=fl, fill=ink)
        if k == NST - 3: d.text((x0 + 265 * SS, yb), "two units of time", font=fl, fill=ink)
        if k == NST - 4: d.text((x0 + 265 * SS, yb), "before the one above", font=fl, fill=ink)
yn = y0 + 52 * SS + NST * row + 14 * SS
d.line([(x0, yn - 6 * SS), (x1, yn - 6 * SS)], fill=ink, width=SS)
r = 8.5 * SS; d.ellipse([x0 + 30 * SS - r, yn + 14 * SS - r, x0 + 30 * SS + r, yn + 14 * SS + r], fill=(250, 246, 234), outline=ink, width=SS); d.text((x0 + 30 * SS - d.textlength("7", font=fs) / 2, yn + 8.4 * SS), "7", font=fs, fill=ink)
d.text((x0 + 52 * SS, yn + 6 * SS), "Neck cut through after the stage shown", font=fl, fill=ink)
d.text((x0 + 52 * SS, yn + 24 * SS), "(%d of the %d cut in this time are marked)." % (shown, cuts), font=fl, fill=ink)
notes = ["NOTES", "Later courses are laid over earlier ones.", "The ribbons are drawn 1.6 D wide, some five times", "the river's width, so that they overlap as a wide", "river's would.  Base grid: 9 D to the square;", "it is decoration."]
for j, s in enumerate(notes): d.text((x0 + 24 * SS, yn + 52 * SS + j * 19 * SS), s, font=font(sans, 11.5 if j else 12.5), fill=ink)
# title block
tx0, ty0 = 70 * SS, H - 470 * SS; tx1, ty1 = tx0 + 500 * SS, H - 70 * SS
box(tx0, ty0, tx1, ty1)
def centred(y, s, f):
    d.text(((tx0 + tx1) / 2 - d.textlength(s, font=f) / 2, y), s, font=f, fill=ink)
centred(ty0 + 18 * SS, "A MODEL OF A MEANDERING RIVER", font(sans, 12))
centred(ty0 + 40 * SS, "ANCIENT COURSES", font(serifb, 22))
centred(ty0 + 74 * SS, "OF A RIVER THAT NEVER WAS", font(serifb, 17))
centred(ty0 + 104 * SS, "ITS MEANDER BELT, t = 90 TO t = 120", font(sans, 12))
d.line([(tx0, ty0 + 130 * SS), (tx1, ty0 + 130 * SS)], fill=ink, width=SS)
centred(ty0 + 140 * SS, "IN 1 SHEET            SCALE IN UNITS OF D", font(sans, 11))
sx, sy = tx0 + 110 * SS, ty0 + 176 * SS
for k in range(4):
    d.rectangle([sx + k * 5 * PX, sy, sx + (k + 1) * 5 * PX, sy + 7 * SS], fill=ink if k % 2 == 0 else (246, 239, 219), outline=ink, width=SS)
for k in range(5): s = str(5 * k); d.text((sx + k * 5 * PX - d.textlength(s, font=font(sans, 10)) / 2, sy + 11 * SS), s, font=font(sans, 10), fill=ink)
d.line([(tx0, ty0 + 212 * SS), (tx1, ty0 + 212 * SS)], fill=ink, width=SS)
lines = ["One run of river.c: P = 3, cutoff distance 0.4 D,", "a valley 170 D long that repeats, seed 12.", "The valley runs down the sheet; what leaves", "at the foot comes in again at the head.", "",
         "Drawn in the manner of Plate 22, \"Ancient courses,", "Mississippi River meander belt\", of the report of", "Harold N. Fisk to the Mississippi River Commission,", "Vicksburg, 1944.  Nothing on this sheet is a place.", "", "Noon, 23 November 2026"]
for j, s in enumerate(lines): d.text((tx0 + 22 * SS, ty0 + 224 * SS + j * 15.5 * SS), s, font=font(serif, 10.6), fill=ink)
d.text((W - 250 * SS, 52 * SS), "SHEET 1 OF 1", font=font(sans, 12), fill=ink)

out = sheet.resize((W // SS, H // SS), Image.LANCZOS)
out.save(outfile, optimize=True)
out.resize((W // SS // 2, H // SS // 2), Image.LANCZOS).save(outfile.replace(".png", "-small.png"), optimize=True)
print("%s written: %d courses, t = %g to %g; %d necks cut in that time, %d marked; belt %.0f D across at its widest" % (
    outfile, NST, T0, T0 + (NST - 1) * DTS, cuts, shown, max(c[:, 1].max() for c in courses) - min(c[:, 1].min() for c in courses)))
