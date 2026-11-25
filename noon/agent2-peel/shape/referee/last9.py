# ninth message: quick checks from the figures of after5.out and my stats5.out
import numpy as np, math
# (1) the author's B with each set's swing off (c = 0.08227): is one constant excluded without the three largest sizes?
d = [(83, -0.0364, 0.0011), (90, -0.0355, 0.0009), (98, -0.0387, 0.0011), (100, -0.0380, 0.0008), (105, -0.0368, 0.0010), (113, -0.0357, 0.0012), (120, -0.0367, 0.0011), (300, -0.0398, 0.0011), (1000, -0.0450, 0.0018),
     (3000, -0.0471, 0.0025), (10000, -0.0495, 0.0038), (30000, -0.0433, 0.0055), (100000, -0.0528, 0.0097), (300000, -0.0438, 0.0199)]
def fit(data, name):
    N = np.array([x[0] for x in data], float); B = np.array([x[1] for x in data]); E = np.array([x[2] for x in data]); W = 1 / E ** 2
    X = np.column_stack([N ** (1 / 3), np.ones(len(N))]); C = np.linalg.inv(X.T @ (X * W[:, None])); b = C @ (X.T @ (W * B)); chi = (W * (B - X @ b) ** 2).sum()
    print('%-34s coefficient %.5f (%.5f) = %.4f of the theory\'s; constant %+.4f (%.4f); chi-square %.1f on %d' % (name, 0.08227 + b[0], math.sqrt(C[0, 0]), (0.08227 + b[0]) / 0.08068, b[1], math.sqrt(C[1, 1]), chi, len(N) - 2))
fit(d, 'all fourteen'); fit(d[:11], '83 to 10,000'); fit(d[:10], '83 to 3,000'); fit(d[:9], '83 to 1,000'); fit(d[7:], '300 up'); fit(d[8:], '1,000 up')
# (2) change (b): the triangle against the ceiling beside the disc, in the quantity of finding 15 (variance x n / mean^2, measured mean)
S = {('disc', 300): (20.9360, 0.51067, 0.00114), ('disc', 1000): (46.4980, 0.77769, 0.00174), ('disc', 3000): (96.5521, 1.13945, 0.00254),
     ('triangle', 300): (22.7688, 0.59843, 0.00133), ('triangle', 1000): (50.7313, 0.92644, 0.00207), ('triangle', 3000): (105.4686, 1.36034, 0.00429),
     ('rtriangle', 300): (22.3647, 0.56158, 0.00125), ('rtriangle', 1000): (49.7643, 0.85248, 0.00190), ('rtriangle', 3000): (103.3988, 1.25284, 0.00397)}
for n in (300, 1000, 3000):
    w = {s: (S[(s, n)][1] * n / S[(s, n)][0] ** 2, S[(s, n)][2] * n / S[(s, n)][0] ** 2) for s in ('disc', 'triangle', 'rtriangle')}
    t, dd = w['triangle'], w['disc']
    print('%5d: variance x n / mean^2: disc %.4f (%.4f), triangle %.4f (%.4f), rounded %.4f; over the ceiling 0.37542: disc %.4f, triangle %.4f: triangle less disc %+.4f (%.4f) of the ceiling; in the standard deviation %+.4f' % (
        n, dd[0], dd[1], t[0], t[1], w['rtriangle'][0], dd[0] / 0.37542, t[0] / 0.37542, (t[0] - dd[0]) / 0.37542, math.hypot(t[1], dd[1]) / 0.37542, math.sqrt(t[0] / dd[0]) - 1))
