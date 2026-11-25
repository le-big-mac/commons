"""Second reader, step 9: my Freeth list against agent3's dial.glyph_months(), entry by entry. usage: run9.py"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, '/home/agent3/antikythera'); sys.path.insert(0, '/home/agent3/antikythera/dial')
sys.dont_write_bytecode = True
import lists2, dial
FL, FS, info, cons = lists2.freeth()
l, s = dial.glyph_months()
print('lunar lists equal:', sorted(l) == FL, '; solar lists equal:', sorted(s) == FS)
print('lunar:', FL); print('solar:', FS)
print('lunar-only cells:', len(set(FL) - set(FS)), '; solar-only:', len(set(FS) - set(FL)), '; both:', len(set(FL) & set(FS)))
print('model distance of each lunar glyph month (sorted by distance):', sorted((info[('L', n)][0], n) for n in FL))
print('model distance of each solar glyph month:', sorted((info[('S', n)][0], info[('S', n)][1], n) for n in FS))
