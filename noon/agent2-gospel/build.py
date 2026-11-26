"""Paste core.js into the page.   usage: python -I build.py page.src.html core.js double.html"""
import sys
if __name__ == '__main__':
    src, core, out = sys.argv[1:4]
    page = open(src, encoding='utf-8').read(); js = open(core, encoding='utf-8').read()
    assert page.count('/*CORE*/') == 1
    open(out, 'w', encoding='utf-8').write(page.replace('/*CORE*/', js))
    print('built', out, len(page.replace('/*CORE*/', js)), 'characters')
