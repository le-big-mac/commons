"""build.py: puck.html from page.src.html and core.js (the arithmetic is inlined, so the page is one file and nothing is fetched).
    python3 -I build.py"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
if __name__ == '__main__':
    src = open(os.path.join(HERE, 'page.src.html'), encoding='utf-8').read(); core = open(os.path.join(HERE, 'core.js'), encoding='utf-8').read()
    assert src.count('/*CORE*/') == 1; open(os.path.join(HERE, 'puck.html'), 'w', encoding='utf-8').write(src.replace('/*CORE*/', core)); print('puck.html: %d bytes' % len(src.replace('/*CORE*/', core).encode('utf-8')))
