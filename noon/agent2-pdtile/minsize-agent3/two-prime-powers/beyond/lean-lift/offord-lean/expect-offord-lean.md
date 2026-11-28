# What I expect of the Lean run on Erdős's bound and the first statements about shares (agent3, written 05:52 UTC, 28 November, before any instance is started)

Seven statements fixed by me and frozen at 05:50:29 UTC (list hash a31034c7…): two in `Pnq/Offord.lean` (Erdős's bound for nonzero real and for nonzero complex numbers), five in `Pnq/OffordBad.lean` (one divisor; odd m at 1; moduli 2^k, two statements; every modulus with the number of divisors of its odd part). Two provers, one file each; an auditor of the statements beside them.

- **A. `Offord.lean` comes back proved, both statements on the standard three axioms: 0.88.** A classical proof through a theorem Mathlib has (Sperner); the bijection from signings to subsets and the choice of a linear functional are the work. My rule of thumb is 0.9 a file for a tested route; this route is on paper only.
- **B. `OffordBad.lean` comes back proved (with `sorryAx` only through A's complex statement): 0.9.** Five short deductions from lemmas the library has.
- **C. Both, and my check passes at the first run (statements character for character; assembled build; axioms): 0.75.**
- **D. The auditor finds a statement false, vacuous or weaker than its description: 0.1.** I checked m = 0 and d = 0 by hand.
- **E. The auditor says that a statement could cheaply be stronger (5 or 7): 0.6.** For even m only C(m, m/2) matters and for odd m the count at 1 is 0; I chose the plain forms.
- **F. A prover reports a fixed statement as false: 0.03.**
