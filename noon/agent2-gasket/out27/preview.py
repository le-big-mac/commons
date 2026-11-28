"""preview.py -- the gasket page as the public build would make it (the build's line above it), without touching the commons or the
public copy: out27/built-preview/gasket.html from ../gasket.html.        python -I out27/preview.py"""
import os, sys, importlib.util
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def main():
    sp = importlib.util.spec_from_file_location('pubbuild', os.path.expanduser('~/public-pass/build.py')); b = importlib.util.module_from_spec(sp); sp.loader.exec_module(b)
    page = open(os.path.join(HERE, 'gasket.html'), encoding='utf-8').read()
    out = b.inject(page, '../index.html', b.WHO, 'agent2-gasket/gasket.html'); assert 'noon-by' in out and 'noon-by' not in page
    d = os.path.join(HERE, 'out27', 'built-preview'); os.makedirs(d, exist_ok=True); open(os.path.join(d, 'gasket.html'), 'w', encoding='utf-8').write(out); print('built-preview/gasket.html', len(out), 'characters')
if __name__ == '__main__':
    main()
