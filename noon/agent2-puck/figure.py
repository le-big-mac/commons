"""figure.py: the paths of a hand that only chases, from the middle to a dot straight above, at five turns.
    ~/vuza/.venv/bin/python -I figure.py  ->  spirals.png"""
import cmath, math
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
INK, MUTED, BG, RULE = '#2b2622', '#6a625a', '#fcfcfb', '#e4dfd6'
def path(deg, T=60.0, dt=0.002):
    """the ring's places: its offset r from the dot obeys r' = -R(a) r; the ring starts at the middle, the dot is one unit above"""
    rot = cmath.exp(1j * math.radians(deg)); r = complex(0, -1); pts = [r]
    for _ in range(int(T / dt)):
        r += -rot * r * dt; pts.append(r)
        if abs(r) < 0.004 or abs(r) > 3: break
    return [(p.real, p.imag + 1) for p in pts]          # as places on the board: the dot at (0, 1), the middle at (0, 0)
if __name__ == '__main__':
    fig, ax = plt.subplots(figsize=(9.6, 6.0), dpi=120); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    shades = {0: '#9fb9dc', 30: '#6f9ad0', 60: '#3f7bc0', 80: '#1c5cab', 90: '#c8622a'}
    for deg in (0, 30, 60, 80, 90):
        pts = path(deg, T=8 if deg == 90 else 60); ax.plot([p[0] for p in pts], [p[1] for p in pts], color=shades[deg], lw=2.2 if deg != 90 else 2.0, ls='-' if deg != 90 else (0, (5, 3)), solid_capstyle='round')
    ax.scatter([0], [1], s=260, color='#c8622a', zorder=5, edgecolors=BG, linewidths=2); ax.scatter([0], [0], s=60, color=MUTED, zorder=5)
    ax.text(0.06, -0.06, 'the middle, where the ring starts', color=MUTED, fontsize=11, va='top'); ax.text(0.1, 1.02, 'the dot', color=MUTED, fontsize=11, va='center')
    names = {0: 'no turn: straight', 30: 'a twelfth of a turn: 1.15 times as long', 60: 'a sixth of a turn: twice as long', 80: '80 degrees: 5.8 times as long', 90: 'a quarter turn: round and round for ever'}
    for n, deg in enumerate((0, 30, 60, 80, 90)):                     # a legend beside the picture: a stroke of each line and its name, in ink
        y = 1.75 - 0.24 * n; ax.plot([1.3, 1.62], [y, y], color=shades[deg], lw=2.4, ls='-' if deg != 90 else (0, (5, 3))); ax.text(1.72, y, names[deg], color=INK, fontsize=11.5, va='center')
    ax.set_aspect('equal'); ax.set_xlim(-1.15, 4.2); ax.set_ylim(-0.25, 2.15); ax.axis('off')
    ax.set_title('A hand that only chases the dot, when its pointer is turned', loc='left', fontsize=13, color=INK)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.93, bottom=0.02); fig.savefig('spirals.png', facecolor=BG); print('spirals.png')
