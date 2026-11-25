import numpy as np, matplotlib, subprocess
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from couzin import School
bg="#fbfaf7"; ink="#22211f"
S=[(School(ro=1.0,seed=0),"#eda100","zone width 0: swarm"),(School(ro=3.5,seed=0),"#2a78d6","zone width 2.5: mill"),(School(ro=3.5,seed=1),"#1baf7a","same width, other start: aligned")]
fig,axs=plt.subplots(1,3,figsize=(12.8,4.6),facecolor=bg); plt.subplots_adjust(left=.01,right=.99,top=.88,bottom=.02,wspace=.03)
ff=subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgba','-s','1280x460','-r','30','-i','-','-pix_fmt','yuv420p','-crf','23','shoal.mp4'],stdin=subprocess.PIPE)
Q=[]
for (s,c,t),a in zip(S,axs):
    a.set_facecolor(bg); a.set_xticks([]); a.set_yticks([]); a.set_aspect('equal'); a.set_title(t,color=ink,fontsize=11)
    for sp in a.spines.values(): sp.set_color('#e6e3dc')
    Q.append(a.quiver(s.x[:,0],s.x[:,1],s.v[:,0],s.v[:,1],color=c,scale=30,width=.006,headwidth=3.5,headlength=5,pivot='mid')); a.set_xlim(-16,16); a.set_ylim(-16,16)
cen=[s.x.mean(0) for s,_,_ in S]
for f in range(900):
    for k,(s,c,t) in enumerate(S):
        for _ in range(4): s.step()
        if f%30==0: s.fragments()
        if not hasattr(s,'lab'): s.fragments()
        big=s.lab==np.bincount(s.lab).argmax(); cen[k]=.4*cen[k]+.6*s.x[big].mean(0)   # camera follows the largest group
        Q[k].set_offsets(s.x-cen[k]); Q[k].set_UVC(s.v[:,0],s.v[:,1])
    fig.canvas.draw(); ff.stdin.write(np.asarray(fig.canvas.buffer_rgba()).tobytes())
ff.stdin.close(); ff.wait()
