"""build.py: lantern.html from lantern.src.html, with core.js and page.js put inside it, so that the page is one file.
python -I build.py [FOLDER OUT.html]      (the folder that holds the three sources; by default this one, and lantern.html in it)"""
import os, sys
HERE = sys.argv[1] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(__file__)); OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'lantern.html'); rd = lambda n: open(os.path.join(HERE, n), encoding='utf-8').read()
if __name__ == '__main__':
    src = rd('lantern.src.html'); assert src.count('/*CORE*/') == 1 and src.count('/*PAGE*/') == 1
    assert '</script>' not in rd('core.js') and '</script>' not in rd('page.js'); out = src.replace('/*CORE*/', rd('core.js')).replace('/*PAGE*/', rd('page.js'))
    open(OUT, 'w', encoding='utf-8').write(out); print('%s written: %d bytes' % (os.path.basename(OUT), len(out.encode('utf-8'))))
