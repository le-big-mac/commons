# measure.py: profile readings on Young's Plate XXVIII, Fig. 401 (full-plate pixel coordinates)
import numpy as np
from PIL import Image
g=np.asarray(Image.open('/home/agent2/lantern-referee/sources/young-plate-XXVIII.jpg').convert('L')).astype(float)
def colprof(x0,x1,y0,y1):  # mean darkness per column
    return 255-g[y0:y1,x0:x1].mean(axis=0)
def rowprof(x0,x1,y0,y1):
    return 255-g[y0:y1,x0:x1].mean(axis=1)
def show(tag,p,o):
    print(tag,' '.join('%d:%d'%(o+i,v) for i,v in enumerate(p)))
def ridge(xs,ypred,hw=4):   # darkest-row centroid near predicted y for each column x
    out=[]
    for x,yp in zip(xs,ypred):
        y0=int(round(yp))-hw; seg=255-g[y0:y0+2*hw+1,x]; seg=seg-seg.min()
        if seg.max()<40: continue
        out.append((x,y0+(seg*np.arange(len(seg))).sum()/seg.sum()))
    return np.array(out)
if __name__=='__main__':
    show('lens F columns, rows 902-918:',colprof(960,992,902,918),960)
    show('slide pillar columns, rows 895-935:',colprof(856,892,895,935),856)
    show('screen block columns, rows 925-945:',colprof(1296,1388,925,945)[::2],1296)
    # ground line: fit ridge
    xs=np.arange(640,1400,20)
    r=ridge(xs,1100+0.0256*(xs-615)-2*0+0,hw=12)
    if len(r)>3:
        A=np.polyfit(r[:,0],r[:,1],1); print('ground line: slope %.4f, y at x=1000: %.1f, n=%d, rms %.2f'%(A[0],np.polyval(A,1000),len(r),np.std(r[:,1]-np.polyval(A,r[:,0]))))
    # slider rail (top of the arm the lens stands on), rows near 955 between x 905 and 1030
    xs=np.arange(905,1030,5); r=ridge(xs,955+0.0256*(xs-905),hw=6)
    if len(r)>3:
        A=np.polyfit(r[:,0],r[:,1],1); print('lens rail: slope %.4f, n=%d'%(A[0],len(r)))
    # solid rays after the lens
    for tag,(xa,ya,xb,yb) in {'upper solid ray after lens':(1000,899.5,1290,846),'lower solid ray after lens':(1000,927,1290,1008)}.items():
        xs=np.arange(xa,xb,6); r=ridge(xs,ya+(yb-ya)*(xs-xa)/(xb-xa),hw=5)
        A=np.polyfit(r[:,0],r[:,1],1); res=r[:,1]-np.polyval(A,r[:,0]); k=np.abs(res)<1.5
        A=np.polyfit(r[k,0],r[k,1],1); print(tag,': slope %.4f, y at 975: %.1f, y at 1340: %.1f, n=%d'%(A[0],np.polyval(A,975),np.polyval(A,1340),k.sum()))
    for tag,(xa,ya,xb,yb) in {'solid ray falling before lens':(886,899,935,910.5),'solid ray rising before lens':(886,925.5,935,913.5)}.items():
        xs=np.arange(xa,xb,3); r=ridge(xs,ya+(yb-ya)*(xs-xa)/(xb-xa),hw=3)
        A=np.polyfit(r[:,0],r[:,1],1); print(tag,': slope %.4f, y at 870: %.1f, y at 882: %.1f, y at 975: %.1f, n=%d'%(A[0],np.polyval(A,870),np.polyval(A,882),np.polyval(A,975),len(r)))
