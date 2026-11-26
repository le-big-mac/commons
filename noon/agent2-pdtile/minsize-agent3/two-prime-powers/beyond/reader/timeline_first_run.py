"""Reader's reconstruction of when each line of the first Z_225 run was written: the end of the last line of a file is the file's
modification time, and each earlier line ended that many recorded 'seconds' before.   usage: timeline_first_run.py"""
import json, os, datetime
R = '/home/agent3/pq2/rule/out225/'
hm = lambda t: datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime('%H:%M:%S')
def ex(D):
    out = []
    for d in D:
        u = v = 0
        while d % 3 == 0: d //= 3; u += 1
        while d % 5 == 0: d //= 5; v += 1
        out.append(f'{u}{v}')
    return ' '.join(sorted(out))
stop = os.path.getmtime(R + 'z225.done')
print('run began (z225-*.err created):', hm(os.stat(R + 'z225-0.err').st_mtime), '; stopped (z225.done):', hm(stop),
      f'= {(stop - os.stat(R + "z225-0.err").st_mtime) / 60:.1f} minutes into the run')
late = []
for j in range(6):
    f = R + f'z225-{j}.jsonl'; rs = [json.loads(l) for l in open(f) if l.startswith('{')]
    mt = os.path.getmtime(f); start = os.path.getmtime(R + f'z225-{j}.err')
    print(f'z225-{j}.jsonl: {len(rs)} lines; sum of seconds {sum(r["seconds"] for r in rs):.0f}; from start to last line {mt - start:.0f} s; last line written {hm(mt)}; silent for {(stop - mt) / 60:.1f} min at the stop')
    t = mt
    for r in reversed(rs):
        if r['status'] != 'optimal': late.append((t, t - r['seconds'], j, r))
        t -= r['seconds']
late.sort(key=lambda x: x[0])
print('the last six lines of the first run that are not "optimal", with the times they were being solved:')
for end, beg, j, r in late[-6:]:
    print(f'   file {j}: {hm(beg)} to {hm(end)}  {r["D"]} ({ex(r["D"])}; {r["cls"]}; predicted {r["predicted"]}): {r["status"]}, size {r["size"]}, {r["seconds"]} s')
print('second run (z225-b.jsonl) created', hm(os.stat(R + 'z225-b.jsonl').st_birthtime if hasattr(os.stat(R + 'z225-b.jsonl'), 'st_birthtime') else 0), '; last line', hm(os.path.getmtime(R + 'z225-b.jsonl')))
print('third run (z225-c.jsonl) last line', hm(os.path.getmtime(R + 'z225-c.jsonl')))
