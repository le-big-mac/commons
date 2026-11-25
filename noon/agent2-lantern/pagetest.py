"""pagetest.py: build the page, write the states with what lantern.py says of each, and have a headless browser read the page back.
python -I pagetest.py [FOLDER-of-sources] [pictures]      Writes nothing beside this script unless "pictures" is given (shots/page-*.png)."""
import os, subprocess, sys, tempfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1] != 'pictures' else HERE; PICS = 'pictures' in sys.argv
if __name__ == '__main__':
    d = tempfile.mkdtemp(prefix='noon-pagetest-%d-' % os.getpid())
    try:
        html = os.path.join(d, 'lantern.html'); cases = os.path.join(d, 'cases.json')
        r = subprocess.run([sys.executable, '-I', os.path.join(HERE, 'build.py'), SRC, html], capture_output=True, text=True)
        if r.returncode: print('the page does not build: ' + r.stderr[-300:]); sys.exit(1)
        subprocess.run([sys.executable, '-I', os.path.join(HERE, 'pagecases.py'), cases], check=True, capture_output=True)
        env = dict(os.environ, NODE_PATH=os.path.expanduser('~/web/node_modules'), LD_LIBRARY_PATH=os.path.expanduser('~/web/sysroot/usr/lib/x86_64-linux-gnu'))
        if PICS: os.makedirs(os.path.join(HERE, 'shots'), exist_ok=True)
        r = subprocess.run(['node', os.path.join(HERE, 'pagetest.js'), html, cases] + ([os.path.join(HERE, 'shots', 'page')] if PICS else []), capture_output=True, text=True, env=env, timeout=600)
        print(r.stdout, end=''); 
        if r.returncode and not r.stdout.strip().endswith('failed'): print('the test did not finish: ' + r.stderr[-600:])
        sys.exit(r.returncode)
    finally: shutil.rmtree(d, ignore_errors=True)
