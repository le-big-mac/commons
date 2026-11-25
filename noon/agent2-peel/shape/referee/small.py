# last step: my own peeler (pure Python, monotone chain) for small discs: where does the constant set in?
import sys, math, random
def layers(P):
    n = 0
    while P:
        n += 1
        if len(P) <= 3: break            # 1, 2 or 3 points are all corners of their hull
        P.sort(); lo = []; up = []
        for p in P:
            while len(lo) >= 2 and (lo[-1][0]-lo[-2][0])*(p[1]-lo[-2][1]) - (lo[-1][1]-lo[-2][1])*(p[0]-lo[-2][0]) <= 0: lo.pop()
            lo.append(p)
        for p in reversed(P):
            while len(up) >= 2 and (up[-1][0]-up[-2][0])*(p[1]-up[-2][1]) - (up[-1][1]-up[-2][1])*(p[0]-up[-2][0]) <= 0: up.pop()
            up.append(p)
        H = set(lo) | set(up); P = [p for p in P if p not in H]
    return n
N = int(sys.argv[1]); K = int(sys.argv[2]); rng = random.Random(7000 + N); s = s2 = s3 = s4 = 0.0; one = 0; xs = []
for k in range(K):
    P = []
    for i in range(N):
        r = math.sqrt(rng.random()); a = 2 * math.pi * rng.random(); P.append((r * math.cos(a), r * math.sin(a)))
    xs.append(layers(P))
m = sum(xs) / K; v = sum((x - m) ** 2 for x in xs) / (K - 1); m4 = sum((x - m) ** 4 for x in xs) / K; se = math.sqrt((m4 - v * v) / K)
c = 0.08205; th = 0.08068
print('N=%4d K=%6d mean %.4f (%.4f) var %.5f (%.5f)  var - 0.08205 N^(1/3) = %+.4f (%.4f)  [the line has -0.0414]   var - theory 0.08068 N^(1/3) = %+.4f   share in one layer %.5f  mean less 1.3259 (N/pi)^(2/3) 0.75: %+.4f' % (
    N, K, m, math.sqrt(v / K), v, se, v - c * N ** (1 / 3), se, v - th * N ** (1 / 3), sum(1 for x in xs if x == 1) / K, m - 1.3259 * (N / math.pi) ** (2 / 3) * 0.75), flush=True)
