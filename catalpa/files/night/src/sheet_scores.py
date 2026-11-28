# The scores of the eleventh to fourteenth sheets, from the sheets' own odds and the programs' own verdicts.
import re
B = '/home/agent1/night/'
for name, sheet, out in (('eleventh', 'expectations-sqm.md', 'sqm_depth.out'), ('twelfth', 'expectations-decline.md', 'model/decline.out'), ('thirteenth', 'expectations-sqm-months.md', 'sqm_months.out'), ('fourteenth', 'expectations-sqm-fading.md', 'sqm_steep.out')):
    odds = {m.group(1): int(m.group(2)) / 100 for m in re.finditer(r'^\| ([A-Z]\d+) \|.*\| (\d+)% \|\s*$', open(B + sheet, encoding='utf-8').read(), flags=re.M)}
    verdict = {m.group(1): m.group(2) for m in re.finditer(r'^([A-Z]\d+)\. .*?: (held|failed|void)\b', open(B + out, encoding='utf-8').read(), flags=re.M)}
    assert set(odds) == set(verdict), (name, sorted(odds), sorted(verdict))
    sc = [(odds[k] - (1.0 if verdict[k] == 'held' else 0.0)) ** 2 for k in odds if verdict[k] != 'void']
    print(f"the {name} sheet: {sum(v == 'held' for v in verdict.values())} held, {sum(v == 'failed' for v in verdict.values())} failed, {sum(v == 'void' for v in verdict.values())} void; Brier score {sum(sc) / len(sc):.3f} (0.25 is what saying 50% every time would score)")
    print('   ' + '; '.join(f'{k} {int(100 * odds[k])}% {verdict[k]}' for k in sorted(odds, key=lambda s: int(s[1:]))))
