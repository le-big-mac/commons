"""The handshake machine at play, drawn for a narrow screen (27 Nov 2026, agent3): the same four games as
handshake_strip.py beside it, the moves produced in the same way (by stepping the machines), but with each
player's name on a line above its row and not beside it, so that the squares and the lettering can be large.
usage: handshake_strip_phone.py OUT.png      (also writes OUT-older.png)"""
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
out = sys.argv[1]
SURF, INK, INK2, GREY = '#fcfcfb', '#0b0b0b', '#52514e', '#8a8984'
BLUE, ORANGE = '#2a78d6', '#eb6834'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'text.color': INK, 'figure.facecolor': SURF, 'savefig.facecolor': SURF})
HAND = (0, [('D', 0, 1), ('D', 0, 2), ('C', 2, 0)])      # the handshake
TFT2 = (0, [('D', 0, 1), ('C', 1, 0)])                   # the two-state Tat for Tit
ALLC = (0, [('C', 0, 0)]); ALLD = (0, [('D', 0, 0)])
def play(a, b, rounds, slip=None):
    sa, sb = a[0], b[0]; ra, rb = [], []
    for r in range(1, rounds + 1):
        ma, mb = a[1][sa][0], b[1][sb][0]
        if slip == (r, 0): ma = 'D' if ma == 'C' else 'C'
        if slip == (r, 1): mb = 'D' if mb == 'C' else 'C'
        ra.append(ma); rb.append(mb)
        sa = a[1][sa][1 if mb == 'C' else 2]; sb = b[1][sb][1 if ma == 'C' else 2]
    return ra, rb
N = 14
GAMES = [('Two of these machines', 'the machine', 'the machine', play(HAND, HAND, N, slip=(8, 0)), (8, 0)),
         ('Against a player who always cooperates', 'the machine', 'always cooperates', play(HAND, ALLC, N), None),
         ('Against a player who always defects', 'the machine', 'always defects', play(HAND, ALLD, N), None)]
OLDER = [('An older machine, with one defection in its opening', 'the older machine', 'always defects', play(TFT2, ALLD, N), None)]
W_IN = 4.6; UNIT = W_IN / (N + 0.5)                 # one square is one unit wide
def draw(games, path, numbers=True):
    # heights in units: title 1.0; for each player a name line 0.75 and a row 1.0; numbers 0.6 once; gap between games 0.9
    h = sum(1.0 + 2 * 1.75 + 0.9 for _ in games) + (0.6 if numbers else 0) + 1.0
    fig, ax = plt.subplots(figsize=(W_IN, UNIT * h))
    ax.set_xlim(-0.25, N + 0.25); ax.set_ylim(0, h); ax.axis('off'); ax.invert_yaxis()
    y = 0.15
    for gi, (title, na, nb, (ra, rb), slip) in enumerate(games):
        ax.text(0.0, y + 0.45, title, fontsize=10.5, fontweight='bold', va='center', ha='left'); y += 1.0
        for k, (name, row) in enumerate(((na, ra), (nb, rb))):
            ax.text(0.0, y + 0.42, name, fontsize=9.5, color=INK2, va='center', ha='left')
            if numbers and gi == 0 and k == 0:
                ax.text(N, y + 0.42, 'round', fontsize=8.5, color=GREY, va='center', ha='right'); y += 0.75
                for i in range(N): ax.text(i + 0.5, y + 0.25, str(i + 1), fontsize=8.5, color=GREY, ha='center', va='center')
                y += 0.6
            else: y += 0.75
            for i, m in enumerate(row):
                ax.add_patch(FancyBboxPatch((i + 0.06, y + 0.04), 0.88, 0.88, boxstyle='round,pad=0,rounding_size=0.12', fc=BLUE if m == 'C' else ORANGE, ec='none'))
                ax.text(i + 0.5, y + 0.49, m, fontsize=10, color='white', fontweight='bold', va='center', ha='center')
                if slip == (i + 1, k): ax.add_patch(FancyBboxPatch((i + 0.0, y - 0.02), 1.0, 1.0, boxstyle='round,pad=0,rounding_size=0.14', fc='none', ec=INK, lw=1.8))
            y += 1.0
        y += 0.9
    hd = [plt.Line2D([], [], marker='s', ms=11, mfc=BLUE, mec='none', ls='none', label='C: cooperates'), plt.Line2D([], [], marker='s', ms=11, mfc=ORANGE, mec='none', ls='none', label='D: defects')]
    ax.legend(handles=hd, loc='lower left', bbox_to_anchor=(-0.02, -0.01), frameon=False, fontsize=10, labelcolor=INK2, ncol=2, handletextpad=0.2, columnspacing=1.6)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.995, bottom=0.005)
    fig.savefig(path, dpi=170)
    for title, na, nb, (ra, rb), slip in games: print(title, '|', ''.join(ra), '|', ''.join(rb))
    print('written', path)
draw(GAMES, out)
draw(OLDER, out.replace('.png', '-older.png'), numbers=False)
