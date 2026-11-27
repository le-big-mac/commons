"""test-remake12.py: after the third whole batch (141 faults): the fault that takes the key to the rings away was caught only by the test
stopping, because the test read the words of a caption that was not there. A missing caption now reads as no words, and the assertion on
its words fails.   python -I out27/test-remake12.py [FILE]   (after test-remake11.py)"""
import sys
if __name__ == '__main__':
    P = sys.argv[1] if len(sys.argv) > 1 else '/home/agent2/coin/tools/shot-change.js'; s = open(P, encoding='utf8').read()
    a = """const tx = sel => p.evaluate(s => document.querySelector(s).textContent.replace(/\\s+/g, ' ').trim(), sel),"""
    b = """const tx = sel => p.evaluate(s => { var e = document.querySelector(s); return e ? e.textContent.replace(/\\s+/g, ' ').trim() : ''; }, sel),"""
    assert s.count(a) == 1, s.count(a); s = s.replace(a, b); open(P, 'w', encoding='utf8').write(s); print('test: a caption that is not there reads as no words')
