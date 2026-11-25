"""Leaf lemmas and dispatch theorems (see gen.py)."""
import json, sys, sympy as sp
from gen import *
HDR=['set_option linter.unusedVariables false','set_option linter.unusedSimpArgs false','set_option linter.unusedTactic false','set_option linter.unreachableTactic false',
     'set_option linter.style.longLine false','set_option maxHeartbeats 1000000','']
ROWS=[c for c in CLS if c!=(0,0)]
def S(e): return sp.sympify(e,locals={'p':p,'q':q})
def P(e): return '('+poly(e,par=False)+')'
def regime_hyps(R): return ' '.join('(hr%d : 0 < %s)'%(i,poly(a,par=False)) for i,a in enumerate(REG[R]))
def regime_args(R): return ' '.join('hr%d'%i for i in range(len(REG[R])))
def bits(Ep,Eq,F):
    Z={(l,0) for l in Ep}|{(0,k) for k in Eq}|set(F)
    return ''.join('1' if o in Z else '0' for o in [(1,0),(2,0),(0,1),(0,2),(1,1),(1,2),(2,1),(2,2)])
def Kstr(Ep,Eq): return '(%s * %s * %s * %s)'%('p' if 1 in Ep else '1','p' if 2 in Ep else '1','q' if 1 in Eq else '1','q' if 2 in Eq else '1')
def leaf(e):
    R=e['regime']; Ep,Eq,F=e['Ep'],e['Eq'],[tuple(x) for x in e['F']]; cat=e['cat']
    Z={(l,0) for l in Ep}|{(0,k) for k in Eq}|set(F)
    rows=[o for o in ROWS if o not in Z]
    y={o:S(e['y']['%d,%d'%o]) for o in rows}; y0=S(e['y']['norm'])
    r={c:sp.together(cc(p,0,c[0])*cc(q,0,c[1])-(y0 if c==(2,2) else 0)-sum(y[o]*cc(p,o[0],c[0])*cc(q,o[1],c[1]) for o in rows)) for c in CLS}
    D=sp.Integer(1)
    for v in list(y.values())+[y0]: D=sp.lcm(D,sp.fraction(sp.together(v))[1])
    Dstr,sg,_=factored(D,R)
    if sg<0: D=-D; Dstr,sg,_=factored(D,R)
    Dstr='('+Dstr+')'
    Y0=sp.cancel(D*y0); Yr={o:sp.cancel(D*y[o]) for o in rows}; Rc={c:sp.cancel(D*r[c]) for c in CLS}
    assert all(sp.fraction(v)[1]==1 for v in list(Yr.values())+[Y0]+list(Rc.values()))
    assert sp.expand(D*Lm[(0,0)]-Y0-sum(Rc[c]*gm[c] for c in CLS)-sum(Yr[o]*Lm[o] for o in rows)-Y0*(gm[(2,2)]-1))==0
    Y0s=P(Y0); name='leaf%s_%s'%(R,bits(Ep,Eq,F))
    rowhyps=' '.join('(hL%d%d : x.L%d%d p q = 0)'%(o+o) for o in rows)
    L=[]
    terms=[]
    for c in CLS:
        if Rc[c]==0: continue
        st,sg,_=factored(Rc[c],R); assert sg>0,(e,c)
        terms.append((c,st))
    defs=', '.join(['Nine.L%d%d'%o for o in CLS]+['Nine.g%d%d'%c for c in CLS])
    body=['  obtain ⟨'+', '.join('a%d'%i for i in range(len(COMMON)))+'⟩ := ha',
          '  obtain ⟨hg00, hg01, hg02, hg10, hg11, hg12, hg20, hg21, hg22e⟩ := hadm',
          '  have hg22 : 0 ≤ x.g22 := by rw [hg22e]; norm_num',
          '  have key : %s * x.L00 p q - %s = %s := by'%(Dstr,Y0s,' + '.join('%s * x.g%d%d'%((st,)+c) for c,st in terms) if terms else '0'),
          '    simp only [%s] at *'%defs,
          '    linear_combination '+' + '.join(['%s * hL%d%d'%((P(Yr[o]),)+o) for o in rows if Yr[o]!=0]+['%s * hg22e'%Y0s])]
    for c,st in terms: body.append('  have t%d%d : (0 : ℝ) ≤ %s * x.g%d%d := by positivity'%(c+(st,)+c))
    body.append('  have hσ : %s ≤ %s * x.L00 p q := by linarith'%(Y0s,Dstr))
    M_=p**2*q**2; ksym=p**len(Ep)*q**len(Eq); K=Kstr(Ep,Eq)
    def fact_eq(expr_str,expr,strict,hname):
        st,sg,_=factored(expr,R); assert sg>0,(e,expr)
        return ['  have %s : (0 : ℝ) %s %s := by'%(hname,'<' if strict else '≤',expr_str),
                '    have e : %s = %s := by ring'%(expr_str,st),'    rw [e]; positivity']
    if cat=='b':
        concl='False'; extra=' (hk : %s ≤ n)'%K
        body+=fact_eq(Y0s,Y0,False,'hY0')
        body+=fact_eq('%s * %s - %s * (p^2*q^2)'%(K,Y0s,Dstr),ksym*Y0-D*M_,True,'hE')
        body+=['  have h1 : n * %s ≤ n * (%s * x.L00 p q) := mul_le_mul_of_nonneg_left hσ hn0.le'%(Y0s,Dstr),
               '  have h2 : %s * %s ≤ n * %s := mul_le_mul_of_nonneg_right hk hY0'%(K,Y0s,Y0s),
               '  have h3 : n * (%s * x.L00 p q) = %s * (p^2*q^2) := by linear_combination %s * hn'%(Dstr,Dstr,Dstr),
               '  linarith']
    elif cat=='H':
        concl='n = p * q'; extra=' (hk : %s ≤ n)'%K
        assert sp.expand(ksym*Y0-D*M_)==0 and sp.expand(ksym-p*q)==0
        body+=fact_eq(Y0s,Y0,True,'hY0')
        body+=['  have hE : %s * %s = %s * (p^2*q^2) := by ring'%(K,Y0s,Dstr),
               '  have h1 : n * %s ≤ n * (%s * x.L00 p q) := mul_le_mul_of_nonneg_left hσ hn0.le'%(Y0s,Dstr),
               '  have h3 : n * (%s * x.L00 p q) = %s * (p^2*q^2) := by linear_combination %s * hn'%(Dstr,Dstr,Dstr),
               '  have hm : n * %s ≤ %s * %s := by linarith'%(Y0s,K,Y0s),
               '  have h4 : n ≤ %s := le_of_mul_le_mul_right hm hY0'%K,
               '  have h5 : n = %s := le_antisymm h4 hk'%K,
               '  rw [h5]; ring']
    else:
        extra=''
        g={c:sp.Integer(0) for c in CLS}
        for key,v in e['gamma'].items(): g[tuple(int(t) for t in key.split(','))]=S(v)
        Dg=sp.Integer(1)
        for c in CLS: Dg=sp.lcm(Dg,sp.fraction(sp.together(g[c]))[1])
        Dgs,sg,_=factored(Dg,R)
        if sg<0: Dg=-Dg; Dgs,sg,_=factored(Dg,R)
        Dgs='('+Dgs+')'
        Gs={}
        for c in CLS:
            if c==(2,2): assert g[c]==1; Gs[c]='%s * u'%Dgs; continue
            if g[c]==0: Gs[c]='0'; continue
            st,sg,dn=factored(sp.cancel(g[c]*Dg),R); assert sg>0 and not dn; Gs[c]='(%s) * u'%st
        wit='(Nine.ofG '+' '.join('(%s)'%Gs[c] for c in CLS)+')'
        rowconcl=' ∧ '.join("x'.L%d%d p q = 0"%o for o in rows)
        if cat=='RP': tail="x'.m00 = 0 ∧ x'.m01 = 0 ∧ x'.m02 = 0"; ntail=3
        elif cat=='RQ': tail="x'.m00 = 0 ∧ x'.m10 = 0 ∧ x'.m20 = 0"; ntail=3
        else: tail="x'.L00 p q * (p*q - 1) = p^2*(q-1) + q^2*(p-1)"; ntail=1
        concl="∃ x' : Nine, x'.Admissible ∧ %s%sn * x'.L00 p q ≤ p^2*q^2 ∧ %s"%(rowconcl,' ∧ ' if rows else '',tail)
        body.append('  have hD : (0 : ℝ) < %s := by positivity'%Dstr)
        body.append('  have hDg : (0 : ℝ) < %s := by positivity'%Dgs)
        body.append('  obtain ⟨u, hu, hu0⟩ : ∃ u : ℝ, %s * u = 1 ∧ 0 < u := ⟨%s⁻¹, mul_inv_cancel₀ (ne_of_gt hDg), inv_pos.2 hDg⟩'%(Dgs,Dgs))
        body.append('  refine ⟨%s, ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩%s, ?_%s⟩'%(wit,', ?_'*len(rows),', ?_'*ntail))
        for c in CLS:
            if c==(2,2): body.append('  · rw [Nine.g22_ofG]; exact hu')
            elif g[c]==0: body.append('  · rw [Nine.g%d%d_ofG]'%c)
            else: body.append('  · rw [Nine.g%d%d_ofG]; positivity'%c)
        for o in rows: body.append('  · rw [Nine.L%d%d_ofG]; ring'%o)
        body+=['  · have hs : %s * %s.L00 p q = %s := by'%(Dstr,wit,Y0s),
               '      rw [Nine.L00_ofG]; linear_combination %s * hu'%Y0s,
               '    have hm : %s * %s.L00 p q ≤ %s * x.L00 p q := by linarith'%(Dstr,wit,Dstr),
               '    have hle : %s.L00 p q ≤ x.L00 p q := le_of_mul_le_mul_left hm hD'%wit,
               '    calc n * %s.L00 p q ≤ n * x.L00 p q := mul_le_mul_of_nonneg_left hle hn0.le'%wit,
               '      _ = p^2*q^2 := hn']
        if cat in ('RP','RQ'): body+=['  · simp [Nine.ofG]']*3
        else: body.append('  · rw [Nine.L00_ofG]; linear_combination (p^2*(q-1) + q^2*(p-1)) * hu')
    L.append('theorem %s (p q n : ℝ) (ha : Atoms p q) %s (x : Nine) (hadm : x.Admissible)'%(name,regime_hyps(R)))
    L.append('    %s (hn : n * x.L00 p q = p^2*q^2) (hn0 : 0 < n)%s :'%(rowhyps,extra))
    L.append('    %s := by'%concl)
    return name,rows,L+body+['']
def certs_files(entries,R,chunk=12):
    todo=[e for e in entries if e['regime']==R and e['cat']!='a']
    files=[]
    for k in range(0,len(todo),chunk):
        fn='Certs%s%02d'%(R,k//chunk); files.append(fn)
        L=['/- GENERATED by ~/p2q2/leangen/gen2.py from certificates_p2q2.json.  Regime %s (%s). -/'%(R,'p < q < p^2' if R=='A' else 'q > p^2'),
           'import P2q2.Atoms','import P2q2.OfG','']+HDR+['namespace P2q2','']
        for e in todo[k:k+chunk]: L+=leaf(e)[2]
        L+=['end P2q2','']
        open(OUT+fn+'.lean','w').write('\n'.join(L))
    return files
def dispatch_file(entries,R,files):
    idx={bits(e['Ep'],e['Eq'],[tuple(x) for x in e['F']]):e for e in entries if e['regime']==R}
    order=[(1,0),(0,1),(2,0),(0,2),(1,1),(1,2),(2,1),(2,2)]
    L=['/- GENERATED by ~/p2q2/leangen/gen2.py.  The case distinction over the 256 zero patterns, regime %s. -/'%R]+['import P2q2.%s'%f for f in files]+['']+HDR+['namespace P2q2','',
       'theorem dispatch%s (p q n : ℝ) (ha : Atoms p q) %s (z01 z02 z10 z11 z12 z20 z21 z22 : Prop) (x : Nine)'%(R,regime_hyps(R)),
       '    (hadm : x.Admissible) (hvan : x.Vanishing p q z01 z02 z10 z11 z12 z20 z21 z22)',
       '    (hn : n * x.L00 p q = p^2*q^2) (hn0 : 0 < n)',
       '    (hk : kfac z10 p * kfac z20 p * kfac z01 q * kfac z02 q ≤ n) :',
       '    Outcome p q n z01 z02 z10 z11 z12 z20 z21 z22 := by',
       '  obtain ⟨v01, v02, v10, v11, v12, v20, v21, v22⟩ := hvan']
    def leafcode(val,ind):
        b=''.join('1' if val[o] else '0' for o in [(1,0),(2,0),(0,1),(0,2),(1,1),(1,2),(2,1),(2,2)])
        e=idx[b]; cat=e['cat']; pad=' '*ind
        if cat=='a':
            def orph(F_,A_,B_):
                if val[A_]: return 'fun _ => Or.inl h%d%d'%A_
                if val[B_]: return 'fun _ => Or.inr h%d%d'%B_
                assert not val[F_]; return 'fun h => absurd h h%d%d'%F_
            def t2(A_,B_,F_):
                if val[F_]: return 'fun _ _ => h%d%d'%F_
                if not val[A_]: return 'fun h _ => absurd h h%d%d'%A_
                assert not val[B_]; return 'fun _ h => absurd h h%d%d'%B_
            ts=[orph((1,1),(1,0),(0,1)),orph((1,2),(1,0),(0,2)),orph((2,1),(2,0),(0,1)),orph((2,2),(2,0),(0,2)),
                t2((1,0),(0,1),(1,1)),t2((1,0),(0,2),(1,2)),t2((2,0),(0,1),(2,1)),t2((2,0),(0,2),(2,2))]
            return [pad+'exact Or.inr (Or.inl ⟨'+', '.join(ts)+'⟩)']
        Z={o for o in order if val[o]}; rows=[o for o in ROWS if o not in Z]
        call='leaf%s_%s p q n ha %s x hadm %s hn hn0'%(R,b,regime_args(R),' '.join('(v%d%d h%d%d)'%(o+o) for o in rows))
        kf='(by rw [kfac_%s z10 p h10, kfac_%s z20 p h20, kfac_%s z01 q h01, kfac_%s z02 q h02] at hk; exact hk)'%tuple('pos' if val[o] else 'neg' for o in [(1,0),(2,0),(0,1),(0,2)])
        if cat=='b': return [pad+'exact (%s %s).elim'%(call,kf)]
        if cat=='H': return [pad+'exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl ⟨%s %s, h10, h22, h12⟩))))'%(call,kf)]
        rs=['r%d%d'%o for o in rows]
        van='⟨'+', '.join(('fun h => absurd h%d%d h'%o) if o in Z else ('fun _ => r%d%d'%o) for o in ROWS)+'⟩'
        if cat in ('RP','RQ'):
            pre='Or.inr (Or.inr (Or.inl ' if cat=='RP' else 'Or.inr (Or.inr (Or.inr (Or.inl '
            post='))' if cat=='RP' else ')))'
            return [pad+"obtain ⟨x', hx', %shle, s0, s1, s2⟩ := %s"%(''.join(r_+', ' for r_ in rs),call),
                    pad+"exact %s⟨x', hx', %s, hle, s0, s1, s2⟩%s"%(pre,van,post)]
        return [pad+"obtain ⟨x', hx', %shle, heq⟩ := %s"%(''.join(r_+', ' for r_ in rs),call),
                pad+"exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr ⟨x', hx', %s, hle, heq⟩))))"%van]
    def rec(k,val,ind):
        if k==2 and not val[(1,0)] and not val[(0,1)]: return [' '*ind+'exact Or.inl ⟨h10, h01⟩']
        if k==8: return leafcode(val,ind)
        o=order[k]; out=[' '*ind+'by_cases h%d%d : z%d%d'%(o+o)]
        for tv in (True,False):
            v2=dict(val); v2[o]=tv; sub=rec(k+1,v2,ind+2)
            out.append(' '*ind+'· '+sub[0].strip()); out+=sub[1:]
        return out
    L+=rec(0,{},2)+['','end P2q2','']
    open(OUT+'Dispatch%s.lean'%R,'w').write('\n'.join(L))
if __name__=='__main__':
    entries=json.load(open('/home/agent2/p2q2/final/certificates_p2q2.json'))
    if len(sys.argv)>1 and sys.argv[1]=='test':
        seen=set(); L=['import P2q2.Atoms','import P2q2.OfG','']+HDR+['namespace P2q2','']
        for e in entries:
            if e['cat']=='a' or (e['regime'],e['cat']) in seen: continue
            seen.add((e['regime'],e['cat'])); L+=leaf(e)[2]
        L+=['end P2q2','']; open('/home/agent2/lean/scratch/LeafTest.lean','w').write('\n'.join(L)); print('test file:',len(seen),'leaves')
    else:
        for R in 'AB':
            if len(sys.argv)>1 and sys.argv[1]=='dispatch':
                n_=len([e for e in entries if e['regime']==R and e['cat']!='a']); files=['Certs%s%02d'%(R,k) for k in range((n_+11)//12)]
            else: files=certs_files(entries,R)
            dispatch_file(entries,R,files); print(R,files)
