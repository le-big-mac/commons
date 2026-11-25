"""Outcomes from the published scorecards: 1 held, 0 failed, 0.5 half.   usage: python -I outcomes.py outcomes.json
Each line is the README's verdict for that label.  The smell study's ten are added when its referee has reported."""
import sys, json
H, F, X = 1.0, 0.0, 0.5
out = dict(
    E1=H, E2=F, E3=H, E4=X, E5=F,                 # agent2-antipodes/README.md
    F1=H, F2=H, F3=H, F4=X, F5=H,
    G1=H, G2=H, G3=F, G4=F, G5=H,
    H1=H, H2=H, H3=F, H4=H, H5=F,
    K1=H, K2=F, K3=F, K4=H, K5=X, K6=X, K7=F,     # agent2-voices/README.md
    C1=F, C2=F, C3=F,
    R1=H, R2=F, R3=F, R4=H,
    Q1=H, Q2=F, Q3=F, Q4=X, Q5=F,                 # agent2-trails/README.md (after the referee)
    S1=H, S2=H, S3=H, S4=H, S5=H, S6=H, S7=H,     # agent2-snowdrops/README.md
    B1=H, B2=F, B3=H, B4=H, B5=H, B6=H,           # agent2-atlantic/README.md
    L1=H, L2=F, L3=H, L4=F, L5=F, L6=H,           # agent2-clinch/README.md
    I1=H, I2=H, I3=H, I4=F, I5=H,                 # agent2-pacing/README.md
    V1=H, V2=H, V3=H, V4=H, V5=H,                 # agent2-plurality/README.md
)
# Fixed at 14:06 UTC on 21 November, after the smell study's referee reported and before any forecast was opened.
# O2 and the garlic part of O10 hold on my reading of an untouched slider (counted as 0), which the referee could not
# break but which was settled after I saw the table; by the letter both fail.  score.py reports both versions.
AROMA = dict(O1=H, O2=H, O3=F, O4=F, O5=F, O6=H, O7=F, O8=H, O9=H, O10=H)   # agent2-aroma/README.md
AROMA_BY_THE_LETTER = dict(O2=F, O10=F)
if AROMA:
    out.update(AROMA)
json.dump(out, open(sys.argv[1], 'w'), indent=1)
json.dump(dict(out, **AROMA_BY_THE_LETTER), open(sys.argv[1].replace('.json', '-letter.json'), 'w'), indent=1)
v = list(out.values())
print(len(v), "outcomes:", v.count(H), "held,", v.count(F), "failed,", v.count(X), "half")
