"""Second look: are the reader's wordings in the candidates as given?  Counts by command."""
import re, sys, subprocess
D = '/home/agent3/pq2/rule-drafts/limits-post/'
rd = lambda p: open(p, encoding='utf-8').read()
s20 = rd(D + 'section-20.now.md'); note = rd(D + 'note.candidate.md'); signs = rd(D + 'signs.candidate.md')
clock = rd(D + 'clock.candidate.md'); front = rd('/home/agent3/pq2/even-front.md'); lim = rd('/home/agent3/lean/lift-check/even/limit/limits.md')
rep = rd(D + 'reading-of-section-20.md')
norm = lambda t: ' '.join(t.split())
i = note.index('## 20.'); j = note.index('## Files')
print('section-20.now.md equals section 20 of note.candidate.md:', norm(note[i:j]) == norm(s20))
W = {
 'F1 signs': ('(two factors: on an odd modulus n and for a divisor d > 1, if a ≥ 0 elements lie in one residue class modulo d and m − a ≥ 1 do not, the share of signings bad at d is at most c_a·c_(m−a))', signs),
 'F2 signs': ('the limit along even m lies between 0.9364 and 1.2699, the limit along odd m between 0.5251 and 0.8084.', signs),
 'F3 s20': ('At a second look it found the seven made and, beyond them, one sign in §4 that I had made strict and that did not follow as written. Its verdict: not passed as it stood, because one sentence was false as written (on the heavy shape\'s own share; I had copied it from its first report, and a parity was missing); passed with five replacements. Four sentences of its own first report were not exact: that one; "with exact counts" (its exhaustive run had been decided in floating point; repeated with every zero confirmed in integers, same totals); a count for the heavy step; and that a search of the texts found the lemma\'s argument nowhere else (it had missed a forerunner, for fully live prime powers, in section 18\'s first text, that text\'s Lemma F). Of the five replacements two were to sentences of mine (a credit in §4 for four values, two of which are the first text\'s; the strict sign) and one to my account of its first look, where three counts lacked their kind. By its report none touches Theorem L, the Addendum, a proof step or a number in the theorem. They are made in its words where it gave words; the account of the second look in the text\'s §6 is mine', s20),
 'F4 s20': ('**The limits exist; and asymptotically nothing is worse than one heavy element with a bounded decoration, in the sense of the Addendum and with the three qualifiers below.**', s20),
 'F5 s20': ('three qualifiers, in its referee\'s words: "bounded" means bounded for each ε; the comparison is up to ε·c_m, so it says nothing about multisets whose share is far below c_m; and the Addendum compares B with the number K_π(D′)·c_(m−r), not with the share of an actual multiset. (The multiset "m − r copies of 0 beside D′ on Z_L" has a share of at least (1 − o(1))·K_π(D′)·c_(m−r), uniformly over r ≤ R, by the referee\'s sentence as corrected at its second look; and of at most K_π(D′)·c_(m−r), by the inequality of the heavy step.)', s20),
 'F5 signs': ('compared with a number, not with the share of an actual multiset; the heavy shape\'s share is that number up to a factor 1 − o(1), uniformly for a bounded decoration', signs),
 'F6 s20': ('8,670 multisets with two or three heavy elements of Z_n, of 90 to 2012 elements (some are of the heavy shape modulo a proper divisor of n, the one with the largest ratio among them), none with share/c_m above the largest known K of its parity', s20),
 'F7 s20 a': ('By me, by exact counts. The lemma, by trying every signing, on 5,252,918 cases (a case is a multiset, a divisor d > 1 and a residue; every multiset containing 0, of the sizes listed in', s20),
 'F7 s20 b': ('in 1,274,130 the class is occupied, in the others a = 0 and the bound is c_m', s20),
 'F7 s20 c': ('And the count "from below", computed with multiplicities and not by listing signings, for three decorations for each parity (four in all; one of the odd three has K = 0) beside up to 2,002 copies', s20),
 'F8 front': ('the largest share of bad signings that m elements can have on an odd modulus, multiplied by √m, has a limit along even m and one along odd m', norm(front)),
 'F8 row': ('(Theorem L: for β(m), the largest share of bad signings of m elements on an odd modulus, β(m)·√m has a limit', norm(front)),
 'F9 s20': ('of which I read only the result summaries, found no limit of this kind and nothing like the lemma; five of the papers they brought up are named in that file, each of them named already in a report of an earlier search.', s20),
 'F10 clock': ('found no gap in the proof; it required changes, among them two about numbers that I had stated (one was rounded the wrong way; the other did not follow in the way I had derived it and now rests on a sharper figure). At its second look it found one sentence false as written and required five replacements more; they are made in its words, and it has not read them again.', clock),
 'F11 s20': ('a symbol that was not defined. Beside the seven, from its table of verdicts: N₀ ≥ 3 in the proof from above, and a proof of the lower bound in (c), which I had called classical.', s20),
 'F12 signs': ('No fresh instance has searched in print for Theorem L; three quick searches of mine found nothing of the kind (section 20).', signs),
 'plain form clock': ('Exactly: allow any small excess, say a hundredth of the 0.8 divided by √m. Then there is a number, depending only on that allowance, such that, once there are enough marks, no marking has more bad ways than markings of that kind with at most that number of further marks reach in the long run, plus the allowance.', clock),
 'come and stay clock': ('come and stay as near as one likes', clock),
}
for k, (w, t) in W.items():
    print(k, ':', w in t, '| given so in my first report:', w in rep or w.replace("\\'", "'") in rep)
# Theorem L and Addendum copied from limits.md
for head in ('> **Theorem L.**', '> **Addendum (the shape).**'):
    a = lim[lim.index(head):]; a = a[:a.index('\n')]
    b = s20[s20.index(head):]; b = b[:b.index('\n')]
    print(head, 'identical:', a == b, '| identical but for "(§4 of the text)":', a.replace('(§4)', '(§4 of the text)') == b)
# counts
k = clock.index('## What came after, in full'); l = clock.index('## What this does not say')
n = len(clock[k:l].split()); print('clock long section:', n, 'words; round(n, -2) =', int(round(n, -2)), '; page says:', re.search(r'it is long, about ([0-9,]+) words', clock).group(1))
print('limits.md words:', len(lim.split()), '; before §6:', len(lim[:lim.index('## 6.')].split()), '; section 20 says:', re.search(r'about ([0-9,]+) words', s20).group(1))
add = clock[clock.index('[Added @@NOW@@ UTC on 28 November: on clocks with an odd'):]; add = add[:add.index(']') + 1]
print('the addition:', len(add.split()), 'words')
