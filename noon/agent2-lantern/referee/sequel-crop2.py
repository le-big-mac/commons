# crop2.py: gridded crops of the Britannica page and plate (full-scan pixel coordinates)
import sys
from PIL import Image, ImageDraw
M='/home/agent2/lantern-referee/sequel/materials/'; W='/home/agent2/lantern-referee/sequel/work/'
def crop(src,name,x0,y0,x1,y1,z,grid=True,step=10):
    im=Image.open(M+src).convert('RGB'); c=im.crop((x0,y0,x1,y1)).resize((int((x1-x0)*z),int((y1-y0)*z)),Image.BICUBIC)
    if grid:
        d=ImageDraw.Draw(c)
        for x in range((x0//step+1)*step,x1,step):
            X=(x-x0)*z; d.line([(X,0),(X,c.size[1])],fill=(255,0,0) if x%(5*step)==0 else (255,190,190)); 
            if x%(2*step)==0: d.text((X+2,2),str(x),fill=(200,0,0))
        for y in range((y0//step+1)*step,y1,step):
            Y=(y-y0)*z; d.line([(0,Y),(c.size[0],Y)],fill=(0,0,255) if y%(5*step)==0 else (190,190,255)); 
            if y%(2*step)==0: d.text((2,Y+2),str(y),fill=(0,0,200))
    c.save(W+name+'.png')
if __name__=='__main__':
    crop('eb7-vol16-p514.jp2','text',1640,230,3045,1010,1.0,grid=False)
    crop('eb7-vol16-plate-CCCLXXXVI.jp2','IL',840,3640,1000,3760,7)
    crop('eb7-vol16-plate-CCCLXXXVI.jp2','K',2190,3260,2310,3350,9)
    crop('eb7-vol16-plate-CCCLXXXVI.jp2','N',2730,3710,2870,3850,7)
    crop('eb7-vol16-plate-CCCLXXXVI.jp2','fig',300,3200,2950,4050,0.55,grid=True,step=100)
