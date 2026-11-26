"""A picture of the handshake machine at play, for the public page: four short games, round by round, without noise except one
marked slip. The moves are produced by stepping the machines themselves (the same tables as the study's ipd.py), not typed in.
usage: handshake_strip.py OUT.png      (also writes OUT-older.png, the two-state machine's game)
Colours: two slots of the chart palette (validated as a pair); every square also carries its letter, so colour is not the only cue."""
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
out = sys.argv[1]
SURF, INK, INK2, GREY = '#fcfcfb', '#0b0b0b', '#52514e', '#b4b3ad'
BLUE, ORANGE = '#2a78d6', '#eb6834'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'text.color': INK, 'figure.facecolor': SURF, 'savefig.facecolor': SURF})
# a machine: start state, and for each state (move, next state if the other cooperated, next state if the other defected)
HAND = (0, [('D', 0, 1), ('D', 0, 2), ('C', 2, 0)])      # the handshake
TFT2 = (0, [('D', 0, 1), ('C', 1, 0)])                   # the two-state Tat for Tit
ALLC = (0, [('C', 0, 0)]); ALLD = (0, [('D', 0, 0)])
def play(a, b, rounds, slip=None):
    """slip = (round, player): that player's move comes out the other way in that round."""
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
def draw(games, path, numbers=True):
    h = 0.3 + 3.6 + 3.25 * (len(games) - 1) if numbers else 0.3 + 3.25 * len(games)
    fig, ax = plt.subplots(figsize=(7.6, 0.42 * h + 0.45))
    ax.set_xlim(-4.6, N + 0.4); ax.set_ylim(-0.3, h + 0.9); ax.axis('off'); ax.invert_yaxis()
    y = 0.2
    for gi, (title, na, nb, (ra, rb), slip) in enumerate(games):
        ax.text(-4.5, y, title, fontsize=10.5, fontweight='bold', va='center', ha='left')
        if numbers and gi == 0:
            for i in range(N): ax.text(i + 0.48, y + 0.62, str(i + 1), fontsize=7.5, color=GREY, ha='center', va='center')
        for k, (name, row) in enumerate(((na, ra), (nb, rb))):
            yy = y + (0.95 if (numbers and gi == 0) else 0.6) + k * 1.05
            ax.text(-0.25, yy + 0.45, name, fontsize=9, color=INK2, va='center', ha='right')
            for i, m in enumerate(row):
                ax.add_patch(FancyBboxPatch((i + 0.06, yy + 0.04), 0.84, 0.84, boxstyle='round,pad=0,rounding_size=0.12', fc=BLUE if m == 'C' else ORANGE, ec='none'))
                ax.text(i + 0.48, yy + 0.47, m, fontsize=9, color='white', fontweight='bold', va='center', ha='center')
                if slip == (i + 1, k): ax.add_patch(FancyBboxPatch((i + 0.0, yy - 0.02), 0.96, 0.96, boxstyle='round,pad=0,rounding_size=0.14', fc='none', ec=INK, lw=1.6))
        y += 3.6 if (numbers and gi == 0) else 3.25
    hd = [plt.Line2D([], [], marker='s', ms=11, mfc=BLUE, mec='none', ls='none', label='C: cooperates'), plt.Line2D([], [], marker='s', ms=11, mfc=ORANGE, mec='none', ls='none', label='D: defects')]
    ax.legend(handles=hd, loc='lower left', bbox_to_anchor=(0.0, -0.02), frameon=False, fontsize=9.5, labelcolor=INK2, ncol=2, handletextpad=0.2, columnspacing=1.6)
    fig.subplots_adjust(left=0.02, right=0.99, top=0.99, bottom=0.02)
    fig.savefig(path, dpi=170)
    for title, na, nb, (ra, rb), slip in games: print(title, '|', ''.join(ra), '|', ''.join(rb))
    print('written', path)
draw(GAMES, out)
draw(OLDER, out.replace('.png', '-older.png'), numbers=False)
