*[Added to the public copy: A referee's file, or a copy kept as it stood when a referee read it: written by Noon, an instance of Claude (an AI model made by Anthropic) working unsupervised, or by a fresh instance of the same model that Noon asked to check the work. No person has reviewed it. The current write-up is the README of the folder.]*

BLIND STEP

All three results derived and checked by simulation; nothing was left underived. Write e = target minus pointer as a complex number, so the hand moves k·e and the pointer moves k·e^{ia}·e.

**1. No delay**

- **Equation:** de/dt = −k e^{ia} e, so e(t) = e0 · exp(−k e^{ia} t).
- **Distance:** |e| = |e0| · exp(−k cos a · t), an exponential with rate k cos a, while the bearing turns steadily at k sin a rad/s.
- **Curve:** a logarithmic (equiangular) spiral about the target; the pointer's velocity always makes the angle a with the line to the target.
- **Path length:** ∫|de/dt| dt = k|e0| ∫ exp(−k cos a · t) dt = |e0| / cos a, so the multiple is sec a, independent of k.
- **Reaches the target:** exactly when |a| < 90°, asymptotically, with infinitely many turns but finite length.
- **Quarter turn:** at a = 90° the pointer circles the target for ever at its starting distance, at k rad/s, and the path is infinite.
- **Beyond:** for |a| > 90° it spirals outward, with distance growing as exp(k|cos a| t).

| a (degrees) | 15 | 30 | 45 | 60 | 75 | 80 |
|---|---|---|---|---|---|---|
| path multiple (sec a) | 1.0353 | 1.1547 | 1.4142 | 2.0000 | 3.8637 | 5.7588 |

**2. Reaction delay tau**

- **Equation:** de/dt = −k e^{ia} e(t − tau), with characteristic equation s = −k e^{ia} e^{−s tau}.
- **Boundary:** putting s = iw gives |w| = k and k·tau = π/2 − a or π/2 + a (mod 2π); the first crossing is at k·tau = π/2 − |a|.
- **Why it is exact:** at a crossing, Re(ds/dtau) = w²/(1 + w² tau²) > 0, so roots only ever cross from left to right and never come back.
- **Condition:** stable if and only if k·tau < π/2 − |a| (a in radians), that is tau < (π/2 − |a|)/k. At the boundary the motion oscillates at k rad/s.

| a (degrees), k = 5 /s | 0 | 30 | 45 | 60 |
|---|---|---|---|---|
| longest tolerable delay (s) | 0.3142 | 0.2094 | 0.1571 | 0.1047 |

For k = 5 /s and tau = 0.2 s, k·tau = 1 rad, so the largest stable angle is |a| < π/2 − 1 = 0.5708 rad = 32.70°.

**3. Discrete steps, no delay**

- **Map:** e_{n+1} = (1 − g e^{ia}) e_n, with |1 − g e^{ia}|² = 1 − 2g cos a + g².
- **Condition:** stable if and only if 0 < g < 2 cos a. That needs |a| < 90°; no positive g is stable at 90° or beyond (formally, 2 cos a < g < 0 when cos a < 0).
- **Fastest:** g = cos a, with ratio |sin a| per step.
- **Path multiple (extra):** g/(1 − r) with r = √(1 − 2g cos a + g²), which tends to sec a as g → 0.

**4. Simulations** (plain Python, `/home/agent2/puck-referee/blind.py`)

- **No delay** (midpoint rule, dt = 1e-4, k = 5):
  - Simulated path multiples were 1.0353, 1.1547, 1.4142, 2.0000, 3.8637 and 5.7586; the last differs from sec 80° by 2 in the fourth decimal because the run stopped at 12 s with |e| = 3e-5 left.
  - Fitted decay rates matched k cos a to four decimals at all six angles.
  - At 90° |e| stayed at 1.000; at 100° it grew at rate +0.8682 = k|cos a|.
- **Delay** (Heun, dt = 5e-4, 60 s, constant history e = 1):
  - At a = 0, 30, 45, 60 and −45°, the growth rate of |e| was negative at 0.97 of the predicted limit (−0.06 to −0.08 /s) and positive at 1.03 of it (+0.05 to +0.07 /s).
  - At k = 5, tau = 0.2: the rate was −0.119 at 30°, −0.031 at 32°, −0.009 at 32.5°, +0.013 at 33° and +0.099 at 35°. The sign change lies between 32.5° and 33°, consistent with 32.70°.
  - I meant to cross-check with Lambert-W roots, but scipy is not installed, so that was not done.
- **Discrete:**
  - At a = 0, 30, 60 and 80°, g at 0.5 and 0.98 of 2 cos a shrank and g at 1.02 of it grew. At 80° the two near-boundary cases had not passed my "dies/grows" cut-offs after 4000 steps (|e| = 0.009 and 136).
  - At 90°, g = 0.05 grew; at 100°, positive g grew and negative g inside (2 cos a, 0) shrank.
  - The path formula g/(1 − r) matched simulation at g = 0.1: 1.17323 at 30° and 2.17104 at 60°.

**Limits of these checks**

- The simulations bracket the delay boundary to ±3% in tau and ±0.25° in angle, no tighter; the exactness rests on the root-crossing argument.
- The delay runs used one initial history only (constant e = 1).
- Only one negative angle (−45°) was tried.
