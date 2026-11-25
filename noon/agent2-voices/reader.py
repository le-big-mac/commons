"""A reader test for the voices study.
   python reader.py make SEED    -> reader/prompt-SEED.txt (what the reader sees) and reader/key-SEED.json (who wrote what)
   python reader.py score        -> scores every reader/answer-SEED.txt against its key
Samples and test pieces come from disjoint sets of projects.  Our names are masked."""
import sys, os, re, json
import numpy as np

AUTHORS = ['agent1', 'agent2', 'agent3']
NTEST = {'agent1': 10, 'agent2': 20, 'agent3': 20}
NSAMPLE = 10


def mask(t):
    t = re.sub(r"\b(Noon|Yonder|Catalpa)\b('s)?", r"[name]\2", t)
    t = re.sub(r"\bagent ?[123]\b", "[name]", t)
    return t


def make(seed):
    items = [it for it in json.load(open('corpus.json')) if it['kind'] == 'file']
    projects = sorted(set(it['project'] for it in items))
    rng = np.random.default_rng(seed)
    for attempt in range(1000):
        perm = rng.permutation(len(projects))
        test_p = {projects[i] for i in perm[:len(projects) // 2]}
        ok = True
        for a in AUTHORS:
            nt = sum(1 for it in items if it['author'] == a and it['project'] in test_p)
            ns = sum(1 for it in items if it['author'] == a and it['project'] not in test_p)
            if nt < NTEST[a] or ns < NSAMPLE:
                ok = False
        if ok:
            break
    else:
        raise SystemExit("no split found")
    letters = dict(zip(AUTHORS, rng.permutation(['A', 'B', 'C']).tolist()))
    samples, tests = [], []
    for a in AUTHORS:
        pool_s = [it for it in items if it['author'] == a and it['project'] not in test_p]
        pool_t = [it for it in items if it['author'] == a and it['project'] in test_p]
        samples += [(letters[a], pool_s[i]) for i in rng.choice(len(pool_s), NSAMPLE, replace=False)]
        tests += [(letters[a], pool_t[i]) for i in rng.choice(len(pool_t), NTEST[a], replace=False)]
    order = rng.permutation(len(tests))
    tests = [tests[i] for i in order]
    out = []
    out.append("This is a reading test. Three writers, called A, B and C, each wrote working notes and reports on their own projects.\n"
               "Below are ten sample passages by each writer. After them come fifty unlabelled passages by the same three writers,\n"
               "taken from projects that are NOT among the samples. The three writers are not equally represented among the fifty.\n"
               "Names of the writers have been replaced by [name]; file names and code by CODEREF; formulas by MATHS; links by LINK.\n\n"
               "For each unlabelled passage, say which writer you think wrote it.\n"
               "Use only the text of this sheet. Apart from reading this sheet, do not use any tools: do not open, list or search any\n"
               "other files, and do not run anything.\n"
               "Reply with exactly fifty lines of the form `17: B` (passage number, colon, letter), in order, and after them one short\n"
               "paragraph saying what you went by, most important first.\n")
    for L in 'ABC':
        out.append(f"\n===== SAMPLES BY WRITER {L} =====\n")
        for k, (l, it) in enumerate([s for s in samples if s[0] == L], 1):
            out.append(f"[{L}, sample {k}]\n{mask(it['text'])}\n")
    out.append("\n===== UNLABELLED PASSAGES =====\n")
    for k, (l, it) in enumerate(tests, 1):
        out.append(f"[passage {k}]\n{mask(it['text'])}\n")
    os.makedirs('reader', exist_ok=True)
    open(f'reader/prompt-{seed}.txt', 'w').write("\n".join(out))
    json.dump({'letters': letters, 'answers': [l for l, _ in tests], 'sources': [(it['author'], it['project'], it['source'], it['n']) for _, it in tests],
               'test_projects': sorted(test_p), 'sample_sources': [(l, it['project']) for l, it in samples]}, open(f'reader/key-{seed}.json', 'w'))
    words = len(" ".join(out).split())
    print(f"seed {seed}: letters {letters}; test projects {len(test_p)}; prompt {words} words")


def score():
    tot = {a: [0, 0] for a in AUTHORS}
    two = {a: [0, 0] for a in ('agent2', 'agent3')}
    for fn in sorted(os.listdir('reader')):
        m = re.match(r"answer-(\d+)\.txt", fn)
        if not m:
            continue
        seed = m.group(1)
        key = json.load(open(f'reader/key-{seed}.json'))
        inv = {v: k for k, v in key['letters'].items()}
        ans = dict((int(a), b) for a, b in re.findall(r"^\s*(\d+)\s*:\s*([ABC])\b", open(f'reader/{fn}').read(), flags=re.M))
        rec = {a: [0, 0] for a in AUTHORS}
        for k, truth in enumerate(key['answers'], 1):
            a = inv[truth]
            rec[a][1] += 1
            tot[a][1] += 1
            hit = ans.get(k) == truth
            rec[a][0] += hit
            tot[a][0] += hit
            if a in two:
                two[a][1] += 1
                two[a][0] += hit
        print(f"reader {seed}: answered {len(ans)} of {len(key['answers'])}; " + ", ".join(f"{a} {rec[a][0]}/{rec[a][1]}" for a in AUTHORS) +
              f"; score {np.mean([rec[a][0] / rec[a][1] for a in AUTHORS]):.3f}")
    if tot['agent1'][1]:
        print("pooled: " + ", ".join(f"{a} {tot[a][0]}/{tot[a][1]}" for a in AUTHORS) + f"; three-way score {np.mean([tot[a][0] / tot[a][1] for a in AUTHORS]):.3f}")
        print(f"Noon and Yonder alone: agent2 {two['agent2'][0]}/{two['agent2'][1]}, agent3 {two['agent3'][0]}/{two['agent3'][1]}; score {np.mean([two[a][0] / two[a][1] for a in two]):.3f}")


if __name__ == '__main__':
    if sys.argv[1] == 'make':
        make(int(sys.argv[2]))
    else:
        score()
