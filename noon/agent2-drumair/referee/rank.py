from scipy.stats import spearmanr
# added mass (skins) worked from the README's table (density ratio minus one, times radius squared); lift = with air / vacuum - 1 from the same table
rows = [(1.403, 1.145/1.033), (1.433, 1.143/1.033), (1.43, 1.111/1.008), (4, 1.051/1.006), (12, 1.022/1.005), (0.850, 1.313/1.118), (1.43, 1.199/1.071),
        (1.43, 1.179/1.058), (4, 1.108/1.054), (12, 1.072/1.052), (1.063, 1.228/1.076), (3.04, 1.128/1.062), (2.25, 1.193/1.099), (1.588, 1.271/1.135),
        (4.54, 1.182/1.125), (1.10, 1.117/0.996), (1.35, 1.040/0.948), (2.16, 1.006/0.944)]
print("rank correlation of the lift with the added weight, 18 loads (the smooth step left out, weight not given):", round(spearmanr([r[0] for r in rows], [r[1] for r in rows])[0], 3))
