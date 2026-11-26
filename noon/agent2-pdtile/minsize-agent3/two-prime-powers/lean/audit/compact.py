# Compact the pp.all output: collapse whitespace and abbreviate the expression for M = p^n * q^m and ZMod M's ring.
import re, sys
t = open(sys.argv[1], encoding='utf-8').read()
i = t.index('@Pnq.Upset.structure_iff : ∀ {p q n m : Nat} [inst : Fact (Nat.Prime p)] [inst_1 : Fact (Nat.Prime q)]\n')
j = t.index('RAW Pnq.Upset.IsUpSet')
t = t[i:j]
t = re.sub(r'\s+', ' ', t)
pw = lambda b, e: ('(@HPow.hPow.{0, 0, 0} Nat Nat Nat (@instHPow.{0, 0} Nat Nat (@NPow.toPow.{0} Nat (@Monoid.toNPow.{0} Nat Nat.instMonoid))) %s %s)' % (b, e))
M = '(@HMul.hMul.{0, 0, 0} Nat Nat Nat (@instHMul.{0} Nat instMulNat) %s %s)' % (pw('p', 'n'), pw('q', 'm'))
assert M in t
t = t.replace(M, '«M»')
t = t.replace('@Membership.mem.{0, 0} Nat (Finset.{0} Nat) (@SetLike.instMembership.{0, 0} (Finset.{0} Nat) Nat (@Finset.instSetLike.{0} Nat))', '«mem»')
t = t.replace('(@Pnq.Upset.instNeZeroPowMulPow p q n m inst inst_1)', '«instNeZero»')
t = t.replace(' @Pnq.Upset.', '\n\n@Pnq.Upset.')
print(t)
