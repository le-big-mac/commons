"""Mendel's counts, copied by me from the text in mendel.txt, each with a pattern that must be found in that text (verify.py checks it).
(name, group, counts, expected parts, pattern with one group per count, in the order of counts)"""
T = (3, 1)
K27 = [("ABC", 8), ("ABCc", 22), ("ABbCc", 45), ("ABc", 14), ("AbCc", 17), ("aBbCc", 36), ("AbC", 9), ("aBCc", 25), ("AaBCc", 38), ("Abc", 11), ("abCc", 20), ("AabCc", 40),
       ("aBC", 8), ("ABbC", 15), ("AaBbC", 49), ("aBc", 10), ("ABbc", 18), ("AaBbc", 48), ("abC", 10), ("aBbC", 19), ("abc", 7), ("aBbc", 24), ("AaBC", 14), ("AaBbCc", 78),
       ("AaBc", 18), ("AabC", 20), ("Aabc", 16)]          # in the order the printed table reads, left to right and down
K27_COUNTS = tuple(c for _, c in K27); K27_PARTS = tuple(2 ** sum(h in lab for h in ("Aa", "Bb", "Cc")) for lab, _ in K27)
K27_PATTERN = r"(\d+) plants ABC (\d+) plants ABCc (\d+) plants ABbCc " + " ".join(rf'(\d+) " {lab}' for lab, _ in K27[3:])
E = [
 ("form of seed", "seven", (5474, 1850), T, r"Among them were (\d+) round or roundish ones and (\d+) angular wrinkled"),
 ("colour of albumen", "seven", (6022, 2001), T, r"yielded 8023 seeds, (\d+) yellow, and (\d+) green"),
 ("colour of seed-coat", "seven", (705, 224), T, r"Among 929 plants, (\d+) bore violet-red flowers and gray-brown seed-coats; (\d+) had white"),
 ("form of pod", "seven", (882, 299), T, r"Of 1181 plants, (\d+) had them simply inflated, and in (\d+) they were constricted"),
 ("colour of pod", "seven", (428, 152), T, r"trial plants was 580, of which (\d+) had green pods and (\d+) yellow"),
 ("position of flowers", "seven", (651, 207), T, r"Among 858 cases (\d+) had inflorescences axial and (\d+) terminal"),
 ("length of stem", "seven", (787, 277), T, r"Out of 1064 plants, in (\d+) cases the stem was long, and in (\d+) short"),
 ("true-breeding: form of seed", "eight", (372, 193), (2, 1), r"Among 565 plants.{0,90}?(\d+) yielded round seeds only.{0,80}?(\d+), however, gave both", "swap"),
 ("true-breeding: colour of albumen", "eight", (353, 166), (2, 1), r"Of 519 plants.{0,120}?(\d+) yielded exclusively yellow, while (\d+) yielded yellow and green", "swap"),
 ("true-breeding: seed-coat (100 plants)", "eight", (64, 36), (2, 1), r"The offspring of (\d+) plants yielded exclusively gray-brown seed-coats, while of the offspring of (\d+) plants", "swap"),
 ("true-breeding: form of pod (100)", "eight", (71, 29), (2, 1), r"The offspring of (\d+) plants had only simply inflated pods; of the offspring of (\d+),", "swap"),
 ("true-breeding: colour of pod (100)", "eight", (60, 40), (2, 1), r"The offspring of (\d+) plants had only green pods; of the offspring of (\d+) plants", "swap"),
 ("true-breeding: position of flowers (100)", "eight", (67, 33), (2, 1), r"The offspring of (\d+) plants had only axial flowers; of the offspring of (\d+),", "swap"),
 ("true-breeding: length of stem (100)", "eight", (72, 28), (2, 1), r"The offspring of (\d+) plants inherited the long axis, of those of (\d+) plants", "swap"),
 ("true-breeding: colour of pod, repeated (100)", "eight", (65, 35), (2, 1), r"in lieu of the ratio of 60:40, that of (\d+):(\d+) resulted"),
 ("two characters, nine kinds", "nine kinds", (38, 35, 28, 30, 65, 68, 60, 67, 138), (1, 1, 1, 1, 2, 2, 2, 2, 4),
  r"(\d+) plants with the sign AB (\d+) \" \" \" Ab (\d+) \" \" \" aB (\d+) \" \" \" ab (\d+) \" \" \" ABb (\d+) \" \" \" aBb (\d+) \" \" \" AaB (\d+) \" \" \" Aab (\d+) \" \" \" AaBb"),
 ("three characters, 27 kinds", "27 kinds", K27_COUNTS, K27_PARTS, K27_PATTERN),
 ("back-cross 1", "back-crosses", (20, 23, 25, 22), (1, 1, 1, 1), r"(\d+) \d+ round yellow seeds \.+AB (\d+) \d+ round yellow and green seeds \.+ABb (\d+) \d+ round and wrinkled yellow seeds \.+AaB (\d+) \d+ round and wrinkled green and yellow seeds\.AaBb"),
 ("back-cross 3", "back-crosses", (25, 19, 22, 21), (1, 1, 1, 1), r"\d+ (\d+) round yellow seeds \.+AB \d+ (\d+) round yellow and green seeds \.+ABb \d+ (\d+) round and wrinkled yellow seeds \.+AaB \d+ (\d+) round and wrinkled green and yellow seeds\.AaBb"),
 ("back-cross 2", "back-crosses", (31, 26, 27, 26), (1, 1, 1, 1), r"(\d+) \d+ plants of the form AaBb (\d+) \d+ plants of the form Aab (\d+) \d+ plants of the form aBb (\d+) \d+ plants of the form ab"),
 ("back-cross 4", "back-crosses", (24, 25, 22, 27), (1, 1, 1, 1), r"\d+ (\d+) plants of the form AaBb \d+ (\d+) plants of the form Aab \d+ (\d+) plants of the form aBb \d+ (\d+) plants of the form ab"),
 ("back-cross, flower colour and stem", "back-crosses", (47, 40, 38, 41), (1, 1, 1, 1), r"1 violet-red long (\d+) times 2 white long (\d+) \" 3 violet-red short (\d+) \" 4 white short (\d+) \""),
]
# the twenty single plants: the table's ten rows, "plant round angular yellow green"
PLANTS = [(45, 12, 25, 11), (27, 8, 32, 7), (24, 7, 14, 5), (19, 10, 70, 27), (32, 11, 24, 13), (26, 6, 20, 6), (88, 24, 32, 13), (22, 10, 44, 9), (28, 6, 50, 14), (25, 7, 44, 18)]
PLANTS_PATTERN = r"Plants Round Angular Yellow Green " + " ".join(rf"{i} (\d+) (\d+) (\d+) (\d+)" for i in range(1, 11))
for i, (r, a, y, g) in enumerate(PLANTS, 1): E.append((f"plant {i}, form of seed", "twenty plants", (r, a), T, None))
for i, (r, a, y, g) in enumerate(PLANTS, 1): E.append((f"plant {i}, colour of albumen", "twenty plants", (y, g), T, None))
# what Fisher's table says, as I remembered it on the sealed sheet (not from any source)
FISHER = {"seven": (7, 2.1389), "eight": (8, 5.1733), "nine kinds": (8, 2.8110), "27 kinds": (26, 15.3224), "back-crosses": (15, 3.6730), "twenty plants": (20, 12.4870)}
