"""Key word in context: print each occurrence of the given phrases in a file, with line number and surroundings.
usage: kwic.py FILE WIDTH PHRASE [PHRASE ...]"""
import sys
path, width = sys.argv[1], int(sys.argv[2])
lines = open(path, encoding="utf-8").read().split("\n")
for phrase in sys.argv[3:]:
    print("==", phrase)
    n = 0
    for i, line in enumerate(lines, 1):
        start = 0
        while True:
            j = line.find(phrase, start)
            if j < 0:
                break
            n += 1
            a, b = max(0, j - width), min(len(line), j + len(phrase) + width)
            print(f"  line {i}, col {j}: ...{line[a:b]}...")
            start = j + len(phrase)
    print("  occurrences:", n)
