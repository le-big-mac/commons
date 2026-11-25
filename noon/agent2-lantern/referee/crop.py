# crop.py: zoomed crops of Young's Plate XXVIII Fig. 401 with a grid in full-plate pixel coordinates
import sys
from PIL import Image, ImageDraw
SRC='/home/agent2/lantern-referee/sources/young-plate-XXVIII.jpg'
def crop(name,x0,y0,x1,y1,z,step=10):
    im=Image.open(SRC).convert('RGB')
    c=im.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.BICUBIC)
    d=ImageDraw.Draw(c)
    for x in range((x0//step+1)*step,x1,step):
        X=(x-x0)*z; d.line([(X,0),(X,c.size[1])],fill=(255,0,0) if x%(5*step)==0 else (255,170,170),width=1)
        d.text((X+2,2),str(x),fill=(200,0,0))
    for y in range((y0//step+1)*step,y1,step):
        Y=(y-y0)*z; d.line([(0,Y),(c.size[0],Y)],fill=(0,0,255) if y%(5*step)==0 else (170,170,255),width=1)
        d.text((2,Y+2),str(y),fill=(0,0,200))
    c.save('/home/agent2/lantern-referee/'+name+'.png')
if __name__=='__main__':
    crop('zA',860,850,1010,1010,8)      # object E and lens F
    crop('zB',1000,950,1080,1010,14)    # pivots I and L
    crop('zC',1180,730,1240,790,14)     # pivot K
    crop('zD',1290,830,1400,1030,6)     # screen and N
