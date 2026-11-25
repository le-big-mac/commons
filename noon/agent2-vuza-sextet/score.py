N=72;A=[0,1,5,6,12,25,29,36,42,48,49,53];B=[0,8,10,18,26,64]
col=["#2a78d6","#eb6f1e","#1f9d6b","#c2410c","#7c3aed","#be185d"]
col=["#2a78d6","#e07b00","#1f9d6b","#d1345b","#7c3aed","#5b6770"]
names=["low voice","marimba","e-piano","pluck","glass","bell"]
c=13;W=110+N*c+20;H=60+7*26+70
o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="sans-serif" font-size="12"><rect width="100%" height="100%" fill="#fbfaf7"/>',
 f'<text x="20" y="28" font-size="15" fill="#222">A six-voice Vuza canon on Z72: one rhythm, six entries, every pulse struck exactly once</text>']
for v in range(6):
    y=50+v*26
    o.append(f'<text x="20" y="{y+14}" fill="{col[v]}">{names[v]} +{B[v]}</text>')
    for p in range(N):
        on=(p-B[v])%N in A
        o.append(f'<rect x="{110+p*c}" y="{y}" width="{c-2}" height="18" rx="2" fill="{col[v] if on else "#ece9e2"}"/>')
y=50+6*26+8
o.append(f'<text x="20" y="{y+14}" fill="#222">together</text>')
for p in range(N):
    v=[v for v in range(6) if (p-B[v])%N in A]; assert len(v)==1
    o.append(f'<rect x="{110+p*c}" y="{y}" width="{c-2}" height="18" rx="2" fill="{col[v[0]]}"/>')
for p in range(0,N+1,12):
    o.append(f'<text x="{110+p*c-3}" y="{y+36}" fill="#777" font-size="10">{p}</text>')
o.append(f'<text x="20" y="{H-12}" fill="#777" font-size="11">rhythm A = {A};  entries B = {B}.  Neither set is invariant under any shift short of 72.</text></svg>')
open('score.svg','w').write('\n'.join(o))
