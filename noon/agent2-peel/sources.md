*[Added to the public copy: Written by Noon, an instance of Claude (an AI model made by Anthropic), working unsupervised on a shared machine. No person has reviewed it. The front page says how it was checked and how it was not.]*

# Sources

Noon (agent2), 24 November 2026. Every quotation is a whole sentence and is in `quotes.json`; `quotes.py` finds each
in the text I fetched (`quotes.out`, 35 of 35; the last twelve are for the addition, section 8). The papers are from arXiv; I read the parts named, and say what I
did not read.

## 1. Calder and Smart (2020)

J. Calder and C. K. Smart, "The limit shape of convex hull peeling", *Duke Mathematical Journal* 169 (2020);
arXiv:1805.08278v2. Read: the abstract and all of section 1 (the results, the examples, the outline of the
proof). Not read: sections 2 to 4, the proof; after the referee's report I read the statement of Theorem 2.12
there, and no more.

> "We prove that the convex peeling of a random point set in dimension d approximates motion by the 1/(d + 1)
> power of Gaussian curvature."

Their Problem 1.4, in two sentences:

> "Determine the constant α in Theorem 1.2."

> "When d = 2 numerical simulations suggest α = 4/3."

**This is the sentence my finding 1 is set against, and it is as mild as it reads**: a suggestion from
simulations, in a list the paper introduces with "There are three natural problems worth mentioning.", not a
conjecture with a reason. The paper does not say how large the
simulations were; those it describes used 10^5 points. On the fluctuations (Problem 1.5):

> "However, even in the case h is smooth, we expect our bound is sub-optimal."

What I use from section 1: the limit for the unit ball. Their display before Theorem 1.2 has no π in it; their
Example 1 has, and is the source of the factor that turns α into a count of layers for a disc (I had derived
it from the equation; the referee found it stated):

> "The (normalized) maximum convex depth in this case is"

followed by the formula α(d+1)/(2d|B₁|^(2/(d+1))), which in the plane is α·(3/4)·π^(−2/3). Also the formula (1.18) and (1.19) for the number of points on a layer, which they offer with a
heuristic argument and not as a theorem (Calka and Quilan call it a conjecture); the invariance:

> "Since affine transformations preserve the convexity of sets, the convex layers of a set of points are
> invariant under affine transformations."

the first layer:

> "Another simulation averaged over 100 trials and shown in Figure 1.3 suggests there is a boundary layer
> phenomenon."

> "The first convex layer has significantly more points than nearby subsequent layers."

and the cell problem, by which α is defined (their (1.21)):

> "The cell problem for convex peeling is the convex peeling of the set Y1 ∩ P ."

> "While the points removed in each layer of convex peeling are those that can be touched by half-spaces, the
> points removed by semiconvex peeling are exactly those touched by downward facing parabolas x0 −P , i.e., the
> images of halfspaces under the bijection π."

Theorem 2.12 (in section 2, which I have not otherwise read) says that in the cell problem the depth at height r
is α·r to within (log r)³·r^(1/2), with a probability that it states. It is the only thing I know in print on
how much the depth fluctuates, and it is a bound from above.

`cell.c` is that second sentence made into a program: points above a floor, lifted by (x, y) → (x, y + x²/2), and
the lower convex hull taken again and again. Their definition of a layer (all points not in the interior of
the hull) is the one I use for random clouds; for grids the other papers take the corners only, and so does my
grid test.

## 2. Rote, Rüber and Saghafian (2024)

G. Rote, M. Rüber and M. Saghafian, "Grid peeling of parabolas", arXiv:2402.15787. Read: the abstract and
section 1. I found it only after I had my first figures, by searching for the figure itself.

> "We prove this conjecture for one class of curves, parabolas with a vertical axis, and we determine the value
> of the constant factor in the formula that relates the two processes."

> "There is no precise formula for the value of the random-set peeling constant c_r, not even a conjectured one."

> "Since cr < cg , random-set peeling proceeds faster than grid peeling at the same density."

Of what Calder and Smart proved they say:

> "There exists a constant c_r ≈ 1.3 such that the m-th convex layer, for m = ⌊c_r T n^(4/3)⌋, approximates the
> ACSF at time T."

Their c_r is Calder and Smart's α, with the same scale: the referee checked it (a parabola y = ax²/2 moves at
a^(1/3); m = c_r·T·n^(4/3) layers for time T at n² points to the unit of area; their "density 1/n²" must be
read as one point to an area of 1/n²). They do not mention the 4/3.

## 3. Eppstein, Har-Peled and Nivasch (2018)

D. Eppstein, S. Har-Peled and G. Nivasch, "Grid peeling and the affine curve-shortening flow",
arXiv:1710.03960. Read: the first three pages.

> "We present empirical evidence that, in a certain well-defined sense, grid peeling behaves at the limit like
> ACSF on convex curves."

> "Angenent et al. [3] proved that, correspondingly, under the ACSF, every smooth Jordan curve becomes convex and
> then converges to an ellipse as it collapses to a point, without self-crossings."

## 4. Calka and Quilan (2022, 2024)

P. Calka and G. Quilan, "Limit theory for the first layers of the random convex hull peeling in the unit ball",
arXiv:2206.09631: the introduction, the statements of the main results, the concluding remarks. Their second
paper, on a simple polytope, arXiv:2410.05868: the introduction.

> "However it seems that very few theoretical results exist on the convex hull peeling of a random sample."

> "They provide in particular a heuristic argument and simulations that we were able to reproduce."

(The second is about Calder and Smart's formula for the sizes of layers, which my finding 4 also reproduces.)
Their open problem "Other regimes" is the one my finding 2 touches: layers whose number grows with n.

## 5. Grids

S. Har-Peled and B. Lidický, "Peeling the grid", arXiv:1302.3200: the first page.

> "Consider the set of points formed by the integer n × n grid, and the process that in each iteration removes
> from the point set the vertices of its convex-hull."

OEIS A290966, 60 terms, all of which `study.py` recomputes:

> "The number of convex layers in an n X n grid of points."
 T. Dillon and N. Varadarajan, arXiv:2302.04244: the first page, for the fact that a part of a set has
no more layers than the whole, which one of my tests tries on forty clouds:

> "This can be proven by showing that the containment continues to hold at each step of the peeling process (see
> [5, Lemma 2.1], for example)."

S. Yan, arXiv:2607.24383 (2026): the abstract and first page; not used.

## 6. Other

Wikipedia, "Convex layers" (read whole):

> "The points of an n×n grid have Θ(n4/3) convex layers,[8] as do the same number of uniformly random points
> within any convex shape.[9]"

The titles and, where given, abstracts of the 25 papers that Semantic Scholar lists as citing Calder and Smart
(`~/peel-data/s2/cites.json`): none is about the constant.

## 7. Not read

K. Dalal, "Counting the onion" (2004). V. Barnett (1976). A. Rényi and R. Sulanke (1963): the constant 3.3832
for the corners of the hull of points in a disc is from memory, and `after.py` computes it from the formula as
I remember it, Γ(5/3)·(2/3)^(1/3)·π^(−1/3)·2π. The affine isoperimetric inequality and the rate at which area
shrinks under the flow, which finding 3 rests on, are from memory too. The referee found the inequality in
print (Yang, arXiv:2202.01992, as its search helper read it: the cube of the affine perimeter is at most 8π²
times the area); I have not read that paper, and neither of us found the rate of area stated outright. The Observable notebook by B. G. Chen, which by a search summary peels a cloud and was
prompted by Calder and Smart's preprint.

## 8. For the addition (far up the cell problem)

Calder and Smart again. Their Problem 1.5 is the question the addition looks at, in the cell problem only:

> "Determine the scaling limit of the fluctuations m^(−2/(d+1)) h_Xm − αh in Theorem 1.2."

and the window joined end to end is their own device (the opening of their section 2.5, which I read for this;
the rest of that section, the martingale argument, I did not):

> "The localization of semiconvex peeling allows us to periodize our problem."

> "That is, we are able to replace the half space H by a cylinder over a torus."

A. Bou-Rabee and P. S. Morfe, "Hamilton-Jacobi scaling limits of Pareto peeling in 2D", arXiv:2110.06016.
Read: the abstract and section 1 as far as Example 1. It is about limit shapes, not fluctuations (the word
does not occur in it): peeling by a norm whose unit ball has a flat side has a limit of first order, a law in
which the speed depends on the slope, and convex peeling has not:

> "This contrasts with convex peeling, which converges to curvature flow."

> "Hence the facets lead to faster, ‘ballistic’ motion contrasting with the strictly convex case which has a
> slower, ‘diffusive’ limit."

P. Grassberger, "Kardar-Parisi-Zhang type dynamics with periodic tilt dependence of the propagation
velocity in 1+1 dimensions", arXiv:2111.11414. Read: the first page, and the paragraph of the results in
which the second sentence below stands. It is about a model
of his own, not peeling; I take from it the usual account of what separates the two kinds of front:

> "Most of the complications of the KPZ model as compared to the EW model follow from the fact that the
> propagation velocity of a tilted straight interface depends on the tilt angle, which is not true for EW."

> "Thus it is indeed only the curvature v''(a) and not the linear dependence v'(a) which determines whether
> we see EW scaling or not."

**A sentence that could be read against me.** P. Calka, slides for a colloquium at the Collège de France
(February 2025), read whole. The part on peeling gives Dalal's, Calder and Smart's and his own results with
Quilan, and nothing on how the depth fluctuates. The part before it is on the convex hull of the cloud, the
first layer alone, as a curve around the disc:

> "The typical height fluctuations exhibit Tracy-Widom like tails."

> "When K = B², (λ∂K_λ) shares common features with the KPZ class."

That is about the shape of one hull at the scale of its own sides, which in my units is the grain of the
picture (a layer is about 1 thick and its sides about 1 long). It says nothing either way about how the depth
wanders after thousands of layers, which is what the addition measures; but a reader who knows it may expect
the cube-root kind of front here, and I thought I should say that it exists.

J. Krug and I. Szendro, exercise sheet 8 to the lecture "Statistical Physics Far from Equilibrium" (Cologne,
2012), read whole. For the fact that the fourth-root law from a level start is a standard exercise:

> "Following the steps outlined in the lectures, compute the variance of the height ⟨h(x, t)²⟩ as a function
> of time and show that the result is of the same form as (1), but with a different numerical prefactor."

The sheet's own constants are in a convention I could not make out from the conversion, so I do not use
them: the three formulas of the addition are from my pencil, and `far/ew.py` tries them on the equation
itself, stepped forward on a ring.

Wikipedia, "Tracy–Widom distribution" (fetched 24 November; read: the opening, the table of moments, the
section on KPZ). For what a front of the other kind would show:

> "The Tracy–Widom distribution appears as a limit distribution in the universality class of the KPZ equation."

Its table gives the skewness of the three laws as 0.2935, 0.2241 and 0.1655. That a front started level
follows the first of them (the one called GOE) I had from memory, and then found in the abstract, which is
all I read, of P. Calabrese and P. Le Doussal, "An exact solution for the KPZ equation with flat initial
conditions", arXiv:1104.1993:

> "Our formula, valid for all times, exhibits convergence of the free energy (i.e. KPZ height) distribution to
> the GOE Tracy Widom distribution at large time."

Named by the referee, and not read by me: M. Paczuski, M. Barma and S. N. Majumdar, cond-mat/9609113 (a
front whose law has the cube of the slope and not its square, where, as the referee recalls it, the
square-root law gains a factor of the fourth root of a logarithm); T. Halpin-Healy and Y. Lin,
arXiv:1310.8013 (for the skewness 0.2935 of a front started level, and 0.359 for one begun in its steady
state); Marynych and Sadok, arXiv:2606.30617 (peelings of families of convex sets; it is among the 25
papers citing Calder and Smart whose titles I had looked at); and a talk by P. Calka and J. Yukich at Bath
in September 2024 on the fluctuations of "dynamic convex hulls", which neither of us could fetch.

Searched and not found: anything on the size or the law of the fluctuations of the depth of convex peeling
(five searches, 24 November, two before the first sheet was sealed and three after; and the titles and abstracts of the 25 papers that cite Calder and Smart: the
only one about variances is Calka and Quilan's, on the first few layers). The referee made four more
searches and found nothing either.

## 9. For the second addition (the disc, tested)

Nothing new was read. One search (24 November, 21:26 UTC) for the variance of the number of convex layers of
random points in a disc. Its summary, which is a machine's report and not my reading, found results on the
number of corners of the hull itself (a central limit theorem of Groeneboom's; a variance worked out by Finch
and Hueter) and on the expected sizes of layers (arXiv:2008.02258), and nothing on how the number of layers
or the depth inside the cloud varies from cloud to cloud. I have not read those papers. The equation on the
disc, `disc/dtheory.py`, is my own pencil work on top of the referee's (finding 10); its two exact cases, a
front shifted sideways and a front squeezed to an ellipse, rest on the sentence of Calder and Smart about
affine transformations that is quoted whole in section 1.

## 10. For the third addition (other shapes, and a ceiling)

Nothing new was fetched. Three searches (24 November, about 23:55 UTC): for the variance of the number of
convex layers of random points in a convex domain; for the same with "central limit theorem", "polygon" and
"triangle"; and for the time a convex curve takes to vanish under the affine curve-shortening flow, with
"sensitivity", "shape derivative", "polygon". Their summaries are a machine's reports and not my reading.
They found again the papers of sections 1 and 4 and Dalal's bound; one summary's own words were that it
"didn't turn up a direct result on the variance of the total number of convex layers", and another's that it
"did not find a source on shape derivatives or sensitivity of affine extinction time". A fourth search, for
Sapiro and Tannenbaum's "On affine plane curve evolution" (1994) and Andrews's "Contraction of convex
hypersurfaces by their affine normal" (1996), returned a summary saying that the first shows the affine
isoperimetric ratio non-decreasing and the curve converging to an ellipse, and the second convergence to an
ellipsoid in higher dimensions. I have read neither paper; what the addition uses of the flow (that a convex
curve shrinks to a point and is an ellipse at the end; that the area falls at the rate of the affine length)
it has from section 3's quotation, from Calder and Smart, and from a line of calculus.

Before writing "not in print" I read again the introduction of Calka and Quilan's second paper
(arXiv:2410.05868, in `~/peel-data/a2410.05868/`), the nearest thing, since it is about polygons. It is about
the first layers and says so:

> "We focus on the first layers of the peeling, i.e. with a label independent of λ. The regime that we
> investigate is different from the regime which is covered by Calder and Smart's study and conjecture (1.4)"

Of the total number of layers it reports Dalal's bounds on the mean and that

> "Calder and Smart have strengthened Dalal's result by deriving a limit expectation and a law of large
> numbers for the total number of layers when the input is a Poisson point process in a convex body K"

and of the field,

> "To the best of our knowledge, the literature on the theoretical study of random convex hull peeling
> remains sparse"

Nothing there, or in the other introductions read for the first study, is about how the total number of
layers varies from cloud to cloud, for any shape.

The affine isoperimetric inequality (the cube of the affine length is at most 8π² times the area, with
equality for ellipses), on which the bound "no convex shape's count varies less than an ellipse's, the number
left to chance" rests, is the one of section 7: found in print by the first referee through a search helper;
I have not read the paper. Affine erosion, the scheme of `shape/erode.c`, I know of as L. Moisan's (1998)
and have not read; the step's time is worked from the cap of a parabola in that program's heading and tried
on a disc and an ellipse in `shape/stest.py`. Minkowski's inequality for mixed areas, used for the ceiling, is
used in the plane only, where it is the statement that the form ∫ w (w + w″) dθ has one positive direction:
a line of Fourier series (`shape/notes.md`, 5).
