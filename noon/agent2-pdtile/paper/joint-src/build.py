"""Assemble the joint paper from the three standalone notes (weak-pqr, weak-pnq, weak-p2q2).
   Noon's:   ~/paper/weak-pqr.tex                      (labels get the prefix N:)
   Yonder's: /srv/commons/agent2-pdtile/paper/weak-pnq.tex   (labels get the prefix Y:)
The front matter (title, abstract, box, introduction) is in front.tex; everything else is taken from the two
notes section by section, unchanged except for label prefixes, section titles and the references between the two."""
import re, sys, os
HERE=os.path.dirname(os.path.abspath(__file__))
N=open(os.path.join(HERE,'..','weak-pqr.tex')).read()
Y=open(os.path.join(HERE,'..','weak-pnq.tex')).read()
C=open(os.path.join(HERE,'..','weak-p2q2.tex')).read()
def prefix(s,pre):
    labels=set(re.findall(r'\\label\{([^}]*)\}',s))
    def fix(m):
        cmd,arg=m.group(1),m.group(2)
        parts=[(pre+a.strip()) if a.strip() in labels else a for a in arg.split(',')]
        return '\\%s{%s}'%(cmd,','.join(parts))
    return re.sub(r'\\(label|ref|eqref)\{([^}]*)\}',fix,s)
def title_span(p):
    """p starts with \\section{ ; return (title, index just after the closing brace), matching nested braces"""
    i=len('\\section{'); depth=1; j=i
    while depth:
        c=p[j]
        if c=='{': depth+=1
        elif c=='}': depth-=1
        j+=1
    return p[i:j-1], j
def sections(s):
    body=s[s.index(r'\begin{document}'):s.index(r'\begin{thebibliography}')]
    parts=re.split(r'(?m)^(?=\\section\{)',body)
    out={}
    for p in parts[1:]:
        title,_=title_span(p); out[title]=p
    return out
def bib(s):
    b=s[s.index(r'\begin{thebibliography}'):s.index(r'\end{thebibliography}')]
    items=re.split(r'(?m)^(?=\\bibitem\{)',b)[1:]
    return {re.match(r'\\bibitem\{([^}]*)\}',it).group(1):it.rstrip()+'\n' for it in items}
Np=prefix(N,'N:'); Yp=prefix(Y,'Y:'); Cp=prefix(C,'C:')
NS=sections(Np); YS=sections(Yp); CS=sections(Cp)
def retitle(sec,new):
    _,j=title_span(sec)
    return '\\section{'+new+'}'+sec[j:]
def find(d,start):
    ks=[k for k in d if k.startswith(start)]
    assert len(ks)==1,(start,list(d)); return d[ks[0]]
front=open('front.tex').read()
# Yonder's introduction: keep the paragraph that defines E, F, (T1), (T2) for p^n q
yi=find(YS,'Introduction')
a=yi.index('What is proved is that a weak tile'); b=yi.index('The proof has three parts.')
ydefs=yi[a:b]
a2=yi.index('I do not know how to avoid the counting.'); ycannot=yi[a2:].rstrip()+'\n'
assert 'Bounds as in part~(2)' in ycannot
ycannot=ycannot.replace('Bounds as in part~(2)','Upper bounds of the kind of Section~\\ref{Y:sec:bounds}')
out=[]
out.append(front)
out.append(find(NS,'Weak tiles of a cyclic group'))
out.append('\n\\part*{Part I. \\texorpdfstring{$\\Z_{p^nq}$}{Z\\_{p\\^{}nq}} (Yonder)}\n\n')
out.append('\\section{The conditions of Coven and Meyerowitz in \\texorpdfstring{$\\Z_{p^nq}$}{p\\^{}nq}}\\label{Y:sec:cm}\n\n'+ydefs+'\n'+ycannot+'\n')
out.append(find(YS,'The tree of residue classes'))
out.append(find(YS,'Step complements and three upper bounds'))
out.append(find(YS,'Two counting lemmas'))
out.append(retitle(find(YS,'Proof of Theorem'),'Proof of Theorem~\\ref{thm:A}'))
out.append('\n\\part*{Part II. \\texorpdfstring{$\\Z_{pqr}$}{Z\\_{pqr}} (Noon)}\n\n')
out.append(retitle(find(NS,'Notation'),'Notation for Part II'))
out.append(find(NS,'Averaging'))
out.append(find(NS,'Eight numbers'))
out.append(find(NS,'Counting'))
out.append(retitle(find(NS,'The structure theorem'),'The structure theorem and the proof of Theorem~\\ref{thm:B}'))
out.append('\n\\part*{Part III. \\texorpdfstring{$\\Z_{p^2q^2}$}{Z\\_{p\\^{}2q\\^{}2}} (Noon; Lemma~\\ref{C:lem:Y} is Yonder\'s)}\n\n')
out.append(retitle(find(CS,'What is used from'),'Notation for Part III, and what it uses')+'\n')
out.append(find(CS,'Two lemmas on subgroups'))
out.append(find(CS,'The linear programme'))
out.append(find(CS,'A counting lemma'))
out.append(retitle(find(CS,'Proof of Theorem'),'Proof of Theorem~\\ref{thm:C}')+'\\label{C:sec:proofC}\n\n')
out.append('\n\\part*{Part IV. The formal proofs, and remarks}\n\n')
out.append(retitle(find(YS,'The formal proof'),'The formal proof of Theorem~\\ref{thm:A}'))
out.append(retitle(find(NS,'The formal proof'),'The formal proof of Theorem~\\ref{thm:B} and of Section~\\ref{N:sec:general}'))
out.append(retitle(find(CS,'The formal proof'),'The formal proof of Theorem~\\ref{thm:C}'))
out.append(retitle(find(YS,'Remarks'),'Remarks on Part I'))
out.append(retitle(find(NS,'Remarks and questions'),'Remarks on Part II, and questions'))
out.append(retitle(find(CS,'Remarks'),'Remarks on Part III'))
body=''.join(out)
# small adaptations of Noon's text to the joint paper
old_p=r"""For the last sentence of the
theorem: a tile is a pd-tile"""
assert old_p in body, 'proof of thm B closing'
body=body.replace(old_p,r"""For the remark after the two
theorems: a tile is a pd-tile""")
old_y="This proves the\nfirst assertion, and the second follows from the chain of implications in the introduction."
assert old_y in body, 'Yonder closing sentence'
body=body.replace(old_y,"This proves the\ntheorem; that tiles, pd-tiles and weak tiles then coincide follows from the chain of implications in the introduction.")
old_g=r"""the content of Theorem~\ref{N:thm:main}, and of the corresponding theorem for
$\Z_{p^nq}$, is that in those groups the remaining cases can be settled by counting."""
assert old_g in body, 'general closing sentence'
body=body.replace(old_g,r"""the content of Theorems~\ref{thm:A} and~\ref{thm:B} is that in those groups the remaining cases can be settled
by counting.""")
i=body.index(r"\textbf{2.} Yonder's proof that weak tiles of"); j=body.index(r"\textbf{3.} For a set $\mathcal Z$ of orders")
body=body[:i]+body[j:]
body=body.replace(r"\textbf{3.} For a set $\mathcal Z$ of orders",r"\textbf{2.} For a set $\mathcal Z$ of orders").replace(r"\textbf{4.} \emph{Is every weak tile of every cyclic group a tile?}",r"\textbf{3.} \emph{Is every weak tile of every cyclic group a tile?}")
# Part III: references to the joint paper itself
for old,new in [
 (r"\lean{Pqr.zeroAt\_iff\_cnt} of \cite{NY})", r"\lean{Pqr.zeroAt\_iff\_cnt})"),
 (r"The rest is proved in \cite{NY} (Section~2 and Part~I; the absence of orphans is the lower-bound lemma of\nPart~I together with (T1)), and formalised there for every cyclic group or for $p^nq$ as the case may be. We\nalso use the bound (S) of \cite{NY} in a form for two sets:",
  r"The rest is proved in Section~\ref{N:sec:general} and in Part~I (the absence of orphans is\nLemma~\ref{Y:lem:three} together with (T1)), and formalised for every cyclic group or for $p^nq$ as the case may be.\nWe also use the bound (S) of Proposition~\ref{N:prop:SC} in a form for two sets:"),
 (r"built on the libraries \lean{Pqr} and \lean{Pnq} of \cite{NY}:", r"built on the libraries \lean{Pqr} and \lean{Pnq} of Parts~I and~II:"),
 (r"The computations of \cite{NY} (no weak tile", r"The computations reported in the remarks on Part~II (no weak tile"),
 (r"\ref{C:thm:C}", r"\ref{thm:C}"),
]:
    old=old.replace('\\n','\n'); new=new.replace('\\n','\n')
    assert old in body or 'C:thm:C' in old,old[:60]
    body=body.replace(old,new)
assert r'\cite{NY}' not in body, [body[m.start()-80:m.start()+20] for m in re.finditer(r'\\cite\{NY\}',body)]
# references between the notes
body=body.replace(r'\ref{Y:thm:main}',r'\ref{thm:A}').replace(r'\ref{N:thm:main}',r'\ref{thm:B}').replace(r'\ref{N:thm:pnq}',r'\ref{thm:A}')
body=re.sub(r'the companion note~\\cite\{N\}',r'Part~II',body)
body=re.sub(r'~\\cite\{N\}',r' (Part~II)',body)
body=body.replace(r'\cite{N}',r'Part~II')
# bibliography: union, without the two notes citing each other
B=bib(N); B.update({k:v for k,v in bib(Y).items() if k not in B}); B.update({k:v for k,v in bib(C).items() if k not in B})
for k in ('N','NY'): B.pop(k,None)
bibtex='\\begin{thebibliography}{99}\n'+''.join(B[k] for k in sorted(B))+'\\end{thebibliography}\n\n\\end{document}\n'
open('weak-tiles.tex','w').write(body+'\n'+bibtex)
print('sections Noon:',list(NS)); print('sections Yonder:',list(YS)); print('sections p2q2:',list(CS)); print('bib keys:',sorted(B))
