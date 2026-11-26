# tip.py -- added on 26 November 2026. The edge-up cube, tilted towards a corner: the curvature of the height of the centre
# of gravity over the centre of buoyancy, by second differences of this study's own height(), beside a closed form.
#   python -I tip.py > tip.out          (numpy; a second or two)
# With an edge up and density d <= 1/2 the part under water is a prism whose section is a right-angled triangle of
# depth sqrt(d), and the water plane is a rectangle 1 by 2 sqrt(d). For a tilt about the short axis of that rectangle
# its stiffness over the volume under water is BM = (2 sqrt(d) / 12) / d = 1 / (6 sqrt(d)), and the centre of gravity
# stands BG = sqrt(2)/2 - (2/3) sqrt(d) above the centre of buoyancy. So
#   BM - BG = (2/3) (sqrt(d) - 1/sqrt(2)) (sqrt(d) - 1/(2 sqrt(2))) / sqrt(d),
# which is negative exactly for 1/8 < d < 1/2 and zero at both ends.
import sys, os, math
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from floating import height

def closed(d):
    x = math.sqrt(d); return (2 / 3) * (x - 1 / math.sqrt(2)) * (x - 1 / (2 * math.sqrt(2))) / x

if __name__ == '__main__':
    up = np.array([1.0, 1.0, 0.0]) / math.sqrt(2)      # a face diagonal vertical: the edge along z is uppermost
    along = np.array([0.0, 0.0, 1.0])                  # towards a corner: "up" leans along that edge
    worst = 0.0
    for d in (0.02, 0.05, 0.10, 0.125, 0.15, 0.20, 0.25, 9 / 32, 0.30, 0.35, 0.40, 0.45, 0.49):
        for eps in (0.003, 0.001):
            h = lambda t: height(math.cos(t) * up + math.sin(t) * along, d)
            c = (h(eps) - 2 * h(0) + h(-eps)) / eps ** 2; worst = max(worst, abs(c - closed(d)))
            print('d = %.5f  step %.3f rad  second difference %+.6f   closed form %+.6f' % (d, eps, c, closed(d)))
    print('largest difference between the two: %.1e' % worst)
    print('closed form at 1/8: %+.1e; at 1/2: %+.1e; at 1/8 + 0.001: %+.6f; at 1/2 - 0.001: %+.6f' % (closed(0.125), closed(0.5), closed(0.126), closed(0.499)))
