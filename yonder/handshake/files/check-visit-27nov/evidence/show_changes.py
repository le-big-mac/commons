import json, sys
d = json.load(open(sys.argv[1], encoding='utf-8'))
for c in d:
    print('=' * 100)
    print(c.get('id'), '| file:', c.get('file'), '| must:', c.get('must'))
    print('OLD:', c.get('old'))
    print('NEW:', c.get('new'))
    print('WHY:', c.get('why'))
    if 'needs' in c: print('NEEDS:', c['needs'])
