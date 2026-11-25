import numpy as np, matplotlib, subprocess
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from matplotlib.colors import to_rgb
N=72; PULSE=0.13; FPS=20
A=[0,1,5,6,12,25,29,36,42,48,49,53]; B=[0,8,10,18,26,64]
RH={k:sorted(k*a%N for a in A) for k in (1,5,7,11)}
order=[3,1,0,4,2,5]
plan=[(1,order[:i+1]) for i in range(6)]+[(1,order)]*2+[(5,order)]*2+[(7,order)]*2+[(11,order)]*2+[(1,order)]+[(1,order[i:]) for i in range(1,6)]+[(1,[])]
names=["low voice","marimba","e-piano","pluck","glass","bell"]
col=[to_rgb(c) for c in ["#2a78d6","#eb6834","#1baf7a","#eda100","#e87ba4","#008300"]]
bg=to_rgb("#fbfaf7"); off=to_rgb("#ece9e2"); ink="#22211f"
mix=lambda a,b,t:tuple(a[i]*(1-t)+b[i]*t for i in range(3))
fig=plt.figure(figsize=(12.8,4.0),facecolor=bg); ax=fig.add_axes([.085,.1,.9,.72]); ax.set_facecolor(bg); ax.axis('off'); ax.set_xlim(0,N); ax.set_ylim(7.6,-.4)
rects=[Rectangle((p+.08,v+.12),.84,.76) for v in range(6) for p in range(N)]+[Rectangle((p+.08,6.5),.84,.76) for p in range(N)]
pc=PatchCollection(rects,linewidth=0); ax.add_collection(pc)
for v in range(6): ax.text(-.6,v+.5,names[v],ha='right',va='center',fontsize=9,color=ink)
ax.text(-.6,6.88,'together',ha='right',va='center',fontsize=9,color=ink)
head,=ax.plot([0,0],[-.1,7.4],color=ink,lw=1)
title=fig.text(.085,.9,'',fontsize=12,color=ink)
total=len(plan)*N*PULSE+6
ff=subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgba','-s','1280x400','-r',str(FPS),'-i','-','-i','sextet.mp3','-c:v','libx264','-pix_fmt','yuv420p','-crf','24','-c:a','aac','-b:a','160k','-shortest','sextet-score.mp4'],stdin=subprocess.PIPE)
desc={1:'rhythm A',5:'rhythm 5·A (mod 72)',7:'rhythm 7·A (mod 72), up a fourth',11:'rhythm 11·A (mod 72)'}
for f in range(int(total*FPS)):
    t=f/FPS; c=int(t/(N*PULSE)); ph=t/PULSE-c*N
    k,act=plan[c] if c<len(plan) else (1,[])
    cols=[]; tog=[off]*N
    for v in range(6):
        on={(a+B[v])%N for a in RH[k]} if v in act else set()
        for p in range(N):
            if p in on:
                age=ph-p; glow=np.exp(-age/2.5) if 0<=age else 0
                cc=mix(mix(col[v],bg,.45),col[v],glow) if age<0 or glow<.999 else col[v]
                cc=mix(col[v],bg,.5*(1-glow)); cols.append(cc); tog[p]=cc
            else: cols.append(off)
    pc.set_facecolor(cols+tog); head.set_xdata([ph,ph])
    title.set_text(f'Sextet on a Vuza canon   cycle {min(c+1,len(plan))} of {len(plan)}:  {len(act)} voice{"s" if len(act)!=1 else ""},  {desc[k]}' if c<len(plan) else 'Sextet on a Vuza canon')
    fig.canvas.draw(); ff.stdin.write(np.asarray(fig.canvas.buffer_rgba()).tobytes())
ff.stdin.close(); ff.wait()
