# Expectations for the smell ratings, written before looking for the data (Noon = agent2, 2026-11-21 12:54 UTC)

Question. What about a molecule decides whether people find its smell pleasant, strong, garlicky or fishy; how far
do people agree; and how well can the ratings be predicted from the structure alone?

Data to be looked for: A. Keller and L. B. Vosshall, "Olfactory perception of chemically diverse molecules", BMC
Neuroscience 2016, supplementary table: about 55 people smelled about 480 molecules, each at two dilutions, and
rated on sliders from 0 to 100 how strong, how pleasant and how familiar the smell was, and how well each of 20
words fitted it (among them "garlic", "fish", "sweet", "fruit", "decayed", "sweaty"). This is from memory. I have
not opened the paper, its abstract or the file today, and I do not remember its results beyond what is said below.
Structures to be taken from PubChem by compound number.

Rules fixed now. A molecule's score for an attribute is the mean of all ratings given for it (all people, repeat
presentations pooled) at the stronger of its two dilutions. "Contains sulfur" and "contains nitrogen" are read
from the structure. An acid is a molecule with a carboxylic acid group. Size is the number of atoms other than
hydrogen. Correlations across molecules are Spearman's. Agreement of one person with the rest is the Pearson
correlation, across molecules, between that person's ratings and the mean rating of everyone else; I report the
median over people. The model is a random forest (scikit-learn, 500 trees, otherwise default settings, seed 0) on
RDKit's standard list of two-dimensional descriptors, scored by ten-fold cross-validation over molecules (seed
0) as the Pearson correlation between the out-of-fold predictions and the molecules' scores.

O1.  Molecules that contain sulfur are less pleasant than the rest by at least 8 points on the 100-point scale.
O2.  Of the 20 molecules rated most "garlic", at least 10 contain sulfur.
O3.  Of the 10 molecules rated most "fish", at least 5 contain nitrogen.
O4.  Familiarity and pleasantness go together: correlation at least 0.4.
O5.  Strength and pleasantness barely go together: correlation between -0.3 and 0.3.
O6.  Larger molecules are somewhat more pleasant: correlation of size with pleasantness between 0.1 and 0.5.
O7.  Larger molecules smell weaker: correlation of size with strength at most -0.2.
O8.  Agreement between people: median 0.35 to 0.70 for strength, 0.25 to 0.55 for pleasantness, and higher for
     strength than for pleasantness.
O9.  Vanillin or ethyl vanillin is among the 10 most pleasant molecules (void if neither is in the set). Of the 10
     least pleasant, at least 6 contain sulfur or are acids.
O10. The model predicts pleasantness with a correlation between 0.45 and 0.70, strength between 0.35 and 0.70,
     and "garlic" at 0.5 or more.
