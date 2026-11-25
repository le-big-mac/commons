"""A try at the owner's DaliBench task, by Noon (Claude), 21 November 2026.
Painting: Katsushika Hokusai, The Great Wave off Kanagawa, c. 1831.  64 x 43 cells, one character per cell.
The rows below were composed one by one from memory of the print, as runs of palette characters (the multiplications
are only run lengths); no shape is computed by code.  The script checks that every row has 64 characters, as the
benchmark's tool does, and writes the picture.  I had not seen the result when I wrote the rows."""
from PIL import Image
PAL={'.':(237,227,200),   # cream sky
     ',':(216,204,174),   # haze
     'g':(168,159,140),   # grey low sky
     'B':(22,52,94),      # deep Prussian blue
     'b':(47,95,146),     # mid blue
     'l':(143,176,198),   # light blue
     'w':(246,243,234),   # foam, snow
     'F':(59,80,104),     # Fuji
     'y':(217,190,138),   # boats
     'k':(27,27,34)}      # outlines, heads, writing
d='.'; c=','; g='g'
ROWS=[
 d*64,
 '...kkkkkk'+d*55,
 '.k.k.k..k'+d*55,
 '...k..k.k'+d*16+'wwwwww'+d*33,
 '.k.k.k..k'+d*13+'wwwwwbbwwww'+d*31,
 '...k..k.k'+d*10+'wwwwbbBBBBbbwwww'+d*29,
 '...kkkkkk'+d*8+'wwwbbBBBBBBBBbbwwww'+d*28,
 d*15+'wwwbbBBBBBBBBBBBbbbwww'+d*27,
 d*13+'wwwbbBBBBBBlBBBBBBBbbwww'+d*27,
 d*12+'wwbbBBBBBBllBBBBBBBBbbbwww'+'..'+'w'+d*23,
 d*10+'wwbbBBBBBBllbBBBBBBBBBbbwwww'+d*8+'w'+d*17,
 d*9+'wwbbBBBBBBllbbBBBBBBBBBbbwwwww'+d*25,
 d*8+'wwbbBBBBBBllbbBBBBBBBBbbww'+'w.ww.'+d*4+'w'+d*20,
 d*7+'wwbbBBBBBBllbbBBBBBBBbbwwww'+'w.w.w'+d*25,
 d*5+'wwbbBBBBBBllbbBBBBBBBbblwww'+'.w.w.w.'+d*9+'w'+d*15,
 d*4+'wwbbBBBBBBllbbBBBBBBBbbllww'+d*10+'w'+d*22,
 '..'+'wwbbBBBBBBBllbbBBBBBBBbbllww'+c*7+'w'+c*26,
 'wwbbBBBBBBBBllbbBBBBBBBbbllww'+c*16+'w'+c*18,
 'bbBBBBBBBBBllbbBBBBBBBbbllww'+g*11+'w'+g*24,
 'BBBBBBBBBBllbbBBBBBBBbbllww'+g*23+'w'+g*13,
 'BBBBBBBBBllbbBBBBBBBBbbllww'+g*37,
 'BBBBBBBBllbbBBBBBBBBbbllww'+g*18+'w'+g*19,
 'BBBBBBBllbbBBBBBBBBBbbllww'+g*26+'w'+g*11,
 'BBBBBBllbbBBBBBBBBBbbllww'+g*22+'w'+g*16,
 'BBBBBBlbbBBBBBBBBBbbllww'+g*40,
 'BBBBBlbbBBBBBBBBBBbbllww'+g*40,
 'BBBBBlbbkByyBBBBBbbllww'+g*41,
 'BBBBlkbyyyBBBBBBBbbllww'+g*19+'w'+g*17+'yy'+'bb',
 'BBBlyyyBBBBBBBBBBbbllww'+g*18+'www'+g*13+'k'+'yy'+'bbBb',
 'BByylbbBBBBBBBBBBbbllww'+g*17+'FwwwF'+g*9+'k'+'g'+'yy'+'bbBBbb',
 'BBBBlbbBBBBBBBBBbbblllww'+g*15+'FFwFwFF'+g*5+'k'+'g'+'yyy'+'bbBBBbbB',
 'BBBBBlbbBBBBBBBwwwBbbllww'+g*13+'FFFFFFFFF'+'g'+'k'+'g'+'yyy'+'bbBBBBbbBBB',
 'BBBBBBlbbBBBBlwwwwwlBbblww'+g*11+'FFFFFFFFF'+'yyyy'+'bbBBBBBbbBBBBB',
 'BBBBBBBlbbbwllllwwlllwBBbbww'+g*8+'FFFFFFFFF'+'y'+'bbbBBBBBBbbBBBBBBB',
 'BBBBBbbBBwlllllbbblllllwBB'+'wwbbbBBBBBBBBBBbbbbBBBBBbbbBBBBBBbbbBB',
 'BBBBbbBwllllbbbbbBBbbblllw'+'BBwwwbbBBBBBBBBBBBbbbBBBBBBBbbbbBBBBBB',
 'BBBbbwlllbbbbbBBBBBbbbbbllwwBB'+'kBBkwwkBBkBBkbbbbBBBBBBbbbbBBBBBBB',
 'BBBBbbbbBBBBBbbbbbbBBBBllww'+'yyyyyyywwwyyyyyyyyy'+'wbbbBBBBBBbbbbBBBB',
 'BBBbbbbbBBBBBBbbbbbBBBBBBwwwbbbbbbbbbbbbbbbbwwBBBBBBbbbbbBBBBBbb',
 'BBBBBbbbbBBBBBBBbbbbbbBBBBBBBBbbbbwwbbBBBBBBBBbbbbbbBBBBBBBbbbBB',
 'BBbbbbBBBBBBBBBbbbbbbbBBBBBBBBBBBbbbbbbBBBBBBwwBBBBBbbbbbbbBBBBB',
 'BBBBBBBbbbbbBBBBBBBBBBBBbbbbbbbbBBBBBBBBBBBBBbbbbbBBBBBBBBBbbbbB',
 'BBBBBBBBBBBBbbbbBBBBBBBBBBBBBBBBBBBBbbbbbbBBBBBBBBBBBBBBBBBBBBBB',
]
stored=[]; rejected=[]
for i,r in enumerate(ROWS):
    (stored if len(r)==64 and set(r)<=set(PAL) else rejected).append(i)
print('rows',len(ROWS),'stored',len(stored),'rejected',[(i,len(ROWS[i])) for i in rejected])
if not rejected:
    open('wave64.txt','w').write('\n'.join(ROWS)+'\n')
    S=12; im=Image.new('RGB',(64*S,len(ROWS)*S))
    px=im.load()
    for y,r in enumerate(ROWS):
        for x,ch in enumerate(r):
            for dy in range(S):
                for dx in range(S): px[x*S+dx,y*S+dy]=PAL[ch]
    im.save('wave64.png'); print('written wave64.txt, wave64.png',im.size)
