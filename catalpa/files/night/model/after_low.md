# One more model run after the fact: a low layer, with and without absorbing particles

Written at 08:27 UTC on 28 November 2026, before the run was started. Not a test: the meters' figure is known (the northern twilight
of late 2019 reads about 0.2 magnitude darker than a year before at every depth of the Sun from 3 to 11 degrees;
`raikoke_night.out`, `check/check-twilight-13.md`). The checker asked what the model gives for a layer at 12 to
16 km, with and without smoke that absorbs light. The model's program is not changed: this run builds the same
atmosphere and then, for the absorbing cases, takes a fifth of the layer's scattering away while leaving its
extinction (a single-scattering albedo of 0.8, the figure the print gives for the Australian smoke).

Cases, all with the layer centred at 14 km and 4 km wide, droplets of median radius 0.22 µm and width 1.4, the
comparison haze 0.005: (a) 0.008 at 550 nm, not absorbing; (b) 0.008, absorbing; (c) 0.016, absorbing.

My guess before the run, as the change of the reading itself (positive: darker): at 3 degrees (a) +0.05 to
+0.10, (b) +0.08 to +0.15, (c) +0.15 to +0.30; at 7 degrees (a) within 0.03 of nothing, (b) +0.02 to +0.08, (c)
+0.05 to +0.15. So I expect the model to give the meters' 0.2 at 3 degrees only with the thicker absorbing layer,
and to give less at 7 degrees than at 3 in every case, where the meters show the same at both.
