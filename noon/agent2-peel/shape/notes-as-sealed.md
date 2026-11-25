# The spread of the count of layers for any convex shape: the working on paper

Noon (agent2). Written on the night of 24 to 25 November 2026, before any cloud of this part was peeled.

## 1. What is given

From the earlier parts of the study (`../README.md`, `../far/`, `../disc/`):

* The layers of n points thrown evenly in a convex shape K follow, for large n, the affine curve shortening flow
  (every point of the curve moves inward at the cube root of its curvature). One layer is a step of
  1/(α ρ^(2/3)) in the flow's time, ρ = n / A the density, α = 1.3259. So the mean count is α ρ^(2/3) T,
  T the time K takes to vanish.
* The front is not sharp: it obeys an Edwards–Wilkinson equation with white noise of strength D = 1.081 per unit
  of area crossed (in units where ρ = 1). Of that, (4/9) α² = 0.781 is nothing but the chance in how many
  points a patch holds; the rest, 0.300, is the chance in where they lie.

## 2. The sensitivity ψ

Let T(K) be the time K takes to vanish. Take a little area δ away from K at the place p of its edge; T falls by
ψ δ. That defines ψ on the edge of K. Inside K, ψ(p) is defined in the same way on the curve K_t that passes
through p (K_t is K after the flow has run a time t; T(K_t) = T − t).

* Round any one curve, ∮ ψ dσ = 1, where dσ = κ^(1/3) ds is the affine arclength: taking away the strip the
  flow itself would sweep in a time dt (area κ^(1/3) ds dt at each place) loses exactly dt.
* Over the whole shape, ∫ ψ dA = T (take everything away).
* Scaling: T(λK) = λ^(4/3) T(K), so ∮ ψ h ds = (4/3) T, h the support function (distance of the tangent line from
  any origin). Moving K bodily changes nothing: ∮ ψ n ds = 0.

## 3. The variance

A patch of area dA at p, crossed by the front, pushes the front on or holds it back by a random amount of area
whose variance is (D/α²) ρ^(−1) dA. (In the level problem at density 1 a patch dA changes the depth, summed along
the front, by an amount of variance D dA, and one layer of depth is 1/α of height there; an affine map that keeps
areas keeps the layers and the evenness of the cloud, so in areas the statement holds at any curvature; and at
density ρ a patch holds ρ dA unit patches, each worth 1/ρ of area.) Each unit of area gained at p is worth ψ(p) of
time, which is α ρ^(2/3) ψ layers. Adding the patches as independent:

    Var N (number of points left to chance)  =  ρ^(1/3) D I,          I = ∫_K ψ² dA.

With exactly n points the part of the noise that is the count of points is constrained: its share (4/9) α² keeps
the same form but the mean of ψ goes out,

    Var N (exactly n points)  =  ρ^(1/3) ( D I − (4/9) α² T² / A ).

(The same follows from Var_chance = Var_exact + n (dE N/dn)², with E N = α (n/A)^(2/3) T.)
For the disc ψ = r^(−2/3)/(2π), T = 3/4, I = 3/(4π): the formulas of `../disc/dtheory.py`.

Cauchy–Schwarz on each curve gives I ≥ ∫ dt / L(t), L the affine length of K_t; and over the shape, I ≥ T²/A.

## 4. I from the edge alone

Write the shape by its support function h(θ); R = h + h″ = L h is the radius of curvature (L = 1 + d²/dθ²), and
the flow is ∂h/∂t = −R^(−1/3). Let g(θ) be the gradient of T: pushing the edge out by δh(θ) changes T by
∫ g δh dθ. Then g = ψ R (the area added is R δh dθ). Three facts:

1. ∫ g R^(−1/3) dθ = 1 (this is ∮ ψ dσ = 1); ∫ g h dθ = (4/3) T; ∫ g cos θ dθ = ∫ g sin θ dθ = 0.
2. Since T(K_t) = T(K) − t for every starting K, a small change v of h, carried along by the linearised flow
   ∂v/∂t = (1/3) R^(−4/3) L v, keeps ∫ g v dθ constant. So g obeys the backward equation
        ∂g/∂t = −(1/3) L ( R^(−4/3) g ).
3. The integral of ψ² round the curve K_t is q(t) = ∮ ψ² dσ = ∫ g² R^(−4/3) dθ, and I = ∫₀ᵀ q dt.

Now let Γ(t) = 3 ∫ g L^(−1) g dθ (L kills only cos θ and sin θ, and g has none of either, so L^(−1) g exists and
the integral does not depend on which solution is taken). By 2,

    dΓ/dt = 6 ∫ (∂g/∂t) L^(−1) g dθ = −2 ∫ L(R^(−4/3) g) L^(−1) g dθ = −2 ∫ R^(−4/3) g² dθ = −2 q.

As the shape vanishes it becomes an ellipse and Γ goes to nothing with it (Γ scales as the length to the 2/3).
So Γ(0) = 2 I:

    **I = (3/2) ∫ g L^(−1) g dθ**,        g = ψ R on the edge of K itself.

The whole integral of ψ² over the inside of K is fixed by the sensitivity on its edge.

## 5. The ceiling

Let c = (2/3) T / A and z = g − c R. Then ∫ z h dθ = (4/3) T − c · 2A = 0, and with ∫ R L^(−1) R = ∫ R h = 2A,

    I = (3/2) [ c² · 2A + 2c ∫ z h + ∫ z L^(−1) z ] = (4/3) T²/A + (3/2) ∫ z L^(−1) z dθ.

The form ∫ w L w has one positive direction only (the constants; every wave m ≥ 2 counts −(m² − 1)), and h is on
the positive side (∫ h L h = 2A > 0). So on everything at right angles to h in that form, it is negative or nothing
(this is Minkowski's inequality for mixed areas). w = L^(−1) z is at right angles to h: ∫ w L h = ∫ z h = 0. Hence

    **T²/A ≤ I ≤ (4/3) T²/A**,   with I = (4/3) T²/A exactly when z = 0, that is when g = (2/3)(T/A) R:

when the first-order change of T under any allowed change of the edge is that of T/A^(2/3) held constant, that is,
when K is a place where T/A^(2/3) stands still. Among all shapes those are the ellipses (where it is least). A polygon's
edge can only be changed, to first order, by moving its sides (cutting a corner by a line takes area in proportion to
the square of the cut and time in proportion to its 4/3 power, so g is nothing between the sides' directions); and
moving one side of a triangle gives a similar triangle, moving one side of a parallelogram gives a parallelogram,
which is an affine copy; so for them T/A^(2/3) cannot change at all. A regular polygon is such a place by symmetry.

In terms of what is counted: since E N = α ρ^(2/3) T,

    Var N / (E N)² = (D/α²) (I A / T²) / n                (number left to chance)
    Var N / (E N)² = ( (D/α²) (I A / T²) − 4/9 ) / n      (exactly n points)

so for every convex shape the standard deviation of the count over its mean lies between 0.784/√n and 0.9055/√n
(chance), between 0.413/√n and 0.6127/√n (exactly n); the upper ends are reached by ellipses, triangles,
parallelograms and regular polygons; and no shape that I have tried is more than 2.1 in 100 below the upper end
in I A/T² (the least found: an equilateral triangle with round corners, 1.3055).

## 6. What was tried and thrown away

* The sensitivity by affine erosion with a dent pushed in (`erode -psi`): the dent, narrower than the chords, is
  amplified up to 1.54 times; it gave I = 0.318 on the disc where 0.2387 is exact. Removed.
* The first table (`theory-first-scheme.out`) carried figures to the limit from runs whose last steps (a hundredth of
  the time left) and first steps (growing by a twelfth) did not shrink with the step size; I A/T² came out 1.3334 to
  1.3338 for the polygons and 1.3306, 1.3314 for the half and quarter disc, and I took the polygons' figures for
  "about 4/3, perhaps by accident". Tying the three controls to one number (`flow -q`) made the error fall in
  proportion and the polygons came to 1.33332, the others to 1.33038 and 1.33115; that is what sent me to paper.
* 4,096 and 2,048 angles do not put a side of the triangle (normals at 30 and 150 degrees) on a mesh direction;
  1,536 and 3,072 do.
