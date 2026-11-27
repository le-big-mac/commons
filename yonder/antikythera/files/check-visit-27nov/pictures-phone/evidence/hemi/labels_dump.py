"""Run one of the two programs of the map as it stands (its source is read and run unchanged, writing its picture into my folder),
then ask the drawing itself where it put each number on the lines, each name and each mark, and write that down in the file's pixels.
For each number on a line I also work out, from the grid and by my own interpolation, the loss at the spot where the number stands:
it should be the number.
usage: labels_dump.py PROGRAM.py HEMI_DIR COAST.geojson OUT.png OUT.json"""
import sys, json, math
import numpy as np
prog, hemi, coast, outpng, outjson = sys.argv[1:6]
src = open(prog, encoding='utf-8').read()
sys.argv = [prog, hemi, coast, outpng]
ns = {'__name__': '__main__'}
exec(compile(src, prog, 'exec'), ns)
fig, ax, cs, ext, loss = ns['fig'], ns['ax'], ns['cs'], ns['ext'], ns['loss']
dpi = 230 if 'phone' in prog else 170
fig.canvas.draw()
Wpx, Hpx = fig.get_size_inches() * dpi
def px(x, y):
    X, Y = ax.transData.transform((x, y)) * dpi / fig.dpi
    return float(X), float(Hpx - Y)
def loss_at(x, y):                    # bilinear, on the grid of the file (ext is the same along both axes; loss[row = north, column = east])
    fx = (x - ext[0]) / (ext[1] - ext[0]); fy = (y - ext[0]) / (ext[1] - ext[0])
    i = int(np.clip(math.floor(fx), 0, len(ext) - 2)); j = int(np.clip(math.floor(fy), 0, len(ext) - 2)); a = fx - i; b = fy - j
    return float(loss[j, i] * (1 - a) * (1 - b) + loss[j, i + 1] * a * (1 - b) + loss[j + 1, i] * (1 - a) * b + loss[j + 1, i + 1] * a * b)
out = {'size_px': [float(Wpx), float(Hpx)], 'frame_px': [px(ext[0], ext[-1]), px(ext[-1], ext[0])], 'numbers': [], 'texts': [], 'marks': []}
print(f'{prog}: picture {Wpx:.0f} x {Hpx:.0f}; map frame from {px(ext[0], ext[-1])} to {px(ext[-1], ext[0])}; one km = {(px(ext[-1], 0)[0] - px(ext[0], 0)[0]) / (ext[-1] - ext[0]):.4f} px')
r = fig.canvas.get_renderer()
for t in cs.labelTexts:
    x, y = t.get_position(); bb = t.get_window_extent(r)
    inside = ext[0] <= x <= ext[-1] and ext[0] <= y <= ext[-1]
    e = {'text': t.get_text(), 'km': [float(x), float(y)], 'px': px(x, y), 'rotation': float(t.get_rotation()), 'loss_there': loss_at(x, y) if inside else None,
         'box_px': [bb.x0 * dpi / fig.dpi, Hpx - bb.y1 * dpi / fig.dpi, bb.x1 * dpi / fig.dpi, Hpx - bb.y0 * dpi / fig.dpi]}
    out['numbers'].append(e)
    print(f'  number "{e["text"]}" at ({x:+7.1f}, {y:+7.1f}) km = pixel ({e["px"][0]:6.1f}, {e["px"][1]:6.1f}), turned {e["rotation"]:6.1f} deg; loss on the grid there {e["loss_there"]:.4f}')
for t in ax.texts + fig.texts:
    if t in cs.labelTexts: continue
    bb = t.get_window_extent(r); x, y = t.get_position()
    pa = t.get_bbox_patch(); bbp = pa.get_window_extent(r) if pa is not None else bb
    e = {'text': t.get_text(), 'fontsize': float(t.get_fontsize()), 'box_px': [bbp.x0 * dpi / fig.dpi, Hpx - bbp.y1 * dpi / fig.dpi, bbp.x1 * dpi / fig.dpi, Hpx - bbp.y0 * dpi / fig.dpi],
         'target_km': [float(v) for v in t.xy] if hasattr(t, 'xy') else None}
    out['texts'].append(e)
    print(f'  text {e["text"]!r:60.60s} size {e["fontsize"]:4.1f}; box in pixels x {e["box_px"][0]:6.1f}..{e["box_px"][2]:6.1f}, y {e["box_px"][1]:6.1f}..{e["box_px"][3]:6.1f}' + (f'; joined to ({t.xy[0]:+.1f}, {t.xy[1]:+.1f}) km' if hasattr(t, 'xy') else ''))
for ln in ax.lines:
    if ln.get_marker() in ('o', 's', '^', 'D') and len(ln.get_xdata()) == 1:
        x, y = float(ln.get_xdata()[0]), float(ln.get_ydata()[0])
        out['marks'].append({'marker': ln.get_marker(), 'km': [x, y], 'px': px(x, y), 'size_pt': float(ln.get_markersize())})
        print(f'  mark {ln.get_marker()} at ({x:+7.1f}, {y:+7.1f}) km = pixel ({px(x, y)[0]:6.1f}, {px(x, y)[1]:6.1f}), size {ln.get_markersize()} pt = {ln.get_markersize() * dpi / 72:.1f} px')
json.dump(out, open(outjson, 'w'), indent=1)
