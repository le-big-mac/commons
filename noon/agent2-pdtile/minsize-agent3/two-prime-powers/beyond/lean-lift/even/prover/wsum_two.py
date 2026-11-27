"""The count of Theorem D (iii) and why it stops at two odd primes: for a set P of odd primes,
W_P = sum over e* > 1 with primes in P of 2^(-mu(e*)) (product formula, exact, up to t = 60);
pure = sum_p delta_p, delta_p = sum_l 2^(1-(p-1)p^(l-1)) (Lemma Q);  mixed = 2 (W_P - sum_p 1/(2^(p-1) - 1))."""
from fractions import Fraction as F
def Wset(P, T=60):
    def A(t):
        r = 1
        for p in P: r *= 1 + t // (p - 1)
        return r
    return sum(F(A(t) - A(t - 2), 2 ** t) for t in range(2, T + 1, 2))
def delta(p): return sum(F(2, 2 ** ((p - 1) * p ** (l - 1))) for l in range(1, 5))
for P in ((3, 5), (3, 5, 7), (3, 5, 11)):
    W = Wset(P); pure = sum(delta(p) for p in P); mixed = 2 * (W - sum(F(1, 2 ** (p - 1) - 1) for p in P))
    print(P, 'W =', float(W), ' pure (Lemma Q) =', float(pure), ' mixed =', float(mixed), ' total =', float(pure + mixed))
print('sum_{a,b>=1} 2^(1-max(2a,4b)) = 74/225 =', 74 / 225, '; direct:', float(sum(F(2, 2 ** max(2 * a, 4 * b)) for a in range(1, 60) for b in range(1, 30))))
