# For the twenty-first sheet: which of the months March, April and May 2020 exist on the first network's share for
# the sixteen photometers of the nineteenth sheet (src/north_fetch.py's list). Requests for existence only (HEAD):
# nothing of any file is fetched. One request every second and a half. Output: data/listing/north_spring2020_probe.txt
import time, importlib.util, urllib.request, urllib.error
B = '/home/agent1/night/'
spec = importlib.util.spec_from_file_location('nf', B + 'src/north_fetch.py'); NF = importlib.util.module_from_spec(spec); spec.loader.exec_module(NF)
out = []
for st in NF.chosen():
    have = []
    for m in (3, 4, 5):
        req = urllib.request.Request(NF.BASE + f'{st}/{st}_2020-{m:02d}.dat', headers={'User-Agent': 'reading-check/1.0'}, method='HEAD')
        try:
            with urllib.request.urlopen(req, timeout=60) as r: have.append(f'2020-{m:02d}')
        except urllib.error.HTTPError as e:
            if e.code != 404: have.append(f'2020-{m:02d}?{e.code}')
        except Exception as e: have.append(f'2020-{m:02d}?{type(e).__name__}')
        time.sleep(1.5)
    out.append(f'{st}: ' + ' '.join(have))
open(B + 'data/listing/north_spring2020_probe.txt', 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
