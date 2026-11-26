"""The patterns of Z_225 that run225.py had not written when I stopped it (see out225/DEVIATION.txt): each in a process of its own
(run225_one.py, 150 s asked of the solver), stopped from outside at 170 s.  Six at a time.  Appends to out225/z225-c.jsonl.
usage: run225b.py"""
import json, glob, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor
P = json.load(open('predictions-225.json'))
done = set()
for f in glob.glob('out225/z225-[0-5].jsonl'):
    for l in open(f):
        if l.startswith('{'): done.add(','.join(map(str, json.loads(l)['D'])))
todo = ['5,9,75,225', '3,5,45,75', '5,9,15,225', '3,15,25,45']   # the four that run225b.py stopped at 170 s, in its first minute, while my processes were still throttled
lock = threading.Lock(); out = open('out225/z225-c.jsonl', 'a')
def one(k):
    t0 = time.time()
    try:
        r = subprocess.run(['nice', '-n', '12', '/home/agent3/welch/.venv/bin/python', 'run225_one.py', k, '150'], capture_output=True, text=True, timeout=170, env={'OMP_NUM_THREADS': '1', 'PATH': '/usr/bin:/bin'})
        line = next((l for l in r.stdout.split('\n') if l.startswith('{')), None)
        if line is None: line = json.dumps(dict(M=225, D=[int(t) for t in k.split(',') if t], cls=P[k]['cls'], predicted=P[k]['predicted'], status='error', size=None, exact_pattern_ok=None, multiset=None, seconds=round(time.time() - t0, 1), stderr=r.stderr[-300:]))
    except subprocess.TimeoutExpired:
        line = json.dumps(dict(M=225, D=[int(t) for t in k.split(',') if t], cls=P[k]['cls'], predicted=P[k]['predicted'], upper_bound_given=P[k]['predicted'] if P[k]['predicted'] is not None else 450,
                               status='stopped-at-170s', size=None, exact_pattern_ok=None, multiset=None, seconds=round(time.time() - t0, 1)))
    with lock: out.write(line + '\n'); out.flush()
print(len(todo), 'patterns to run', flush=True)
with ThreadPoolExecutor(6) as ex: list(ex.map(one, todo))
print('done', flush=True)
