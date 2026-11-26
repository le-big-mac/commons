"""the intended definitions (copied from check_table.py)"""
def divisors(M):
    return [d for d in range(1, M + 1) if M % d == 0]

def is_upset_intended(M, D):
    dv = set(divisors(M))
    if not set(D) <= dv:
        return False
    if 1 in D:
        return False
    for d in D:
        for e in dv:
            if e % d == 0 and e not in D:
                return False
    return True

def corners_intended(M, D):
    non = [d for d in divisors(M) if d not in D]
    out = []
    for c in non:
        # maximal: no other non-member is a proper multiple of c
        if not any(e != c and e % c == 0 for e in non):
            out.append(c)
    return sorted(out)

