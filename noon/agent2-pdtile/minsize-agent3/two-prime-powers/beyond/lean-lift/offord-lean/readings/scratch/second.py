import re, sys
note = open('/home/agent3/pq2/rule/beyond-up-sets.md', encoding='utf-8').read().split('\n')
def sec(a, b): return '\n'.join(note[a-1:b-1])
s13, s15, s16 = sec(257, 275), sec(293, 313), sec(313, 340)
for name, text, q in [
    ('13', s13, 'the fractions of good signings apart'),
    ('15', s15, 'the shares of good signings apart'),
    ('15', s15, 'The shares of good signings of section 14 (at least 1/2 and 1/4, more than 0.075) are in no Lean statement'),
    ('16', s16, 'I have not asked for them to be'),
]:
    print('section', name, 'has', repr(q[:50]), ':', text.count(q))
# d(n) against 2 d(n')
def d(n): return sum(1 for x in range(1, n + 1) if n % x == 0)
bad = 0
for k in range(0, 7):
    for n1 in range(1, 200, 2):
        a, b = d(2 ** k * n1), 2 * d(n1)
        ok = (b == 2 * a) if k == 0 else (a == b) if k == 1 else (b < a)
        bad += not ok
print('d(n) against 2 d(n\'): cases not as stated:', bad)
board = open('/srv/commons/hello-from-agent3.md', encoding='utf-8').read().split('\n')
for i, l in enumerate(board, 1):
    if l.startswith('**05:52 UTC, 28 Nov') or l.startswith('**06:17 UTC, 28 Nov') or l.startswith('**06:36 UTC, 28 Nov'):
        blk = l
        j = i
        while j < len(board) and board[j].strip() and not board[j].startswith('**0'):
            blk += '\n' + board[j]; j += 1
        print(l[:22], '| "first":', [m.group(0) for m in re.finditer(r'.{0,40}first.{0,40}', blk)][:4], '| SHARES:', 'SHARES' in blk)
print('posts after 06:36:', [l[:40] for l in board if re.match(r'\*\*0[6-9]:[0-9]{2} UTC, 28 Nov', l)][-3:])
