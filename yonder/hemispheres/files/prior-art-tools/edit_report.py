"""usage: python -I edit_report.py REPORT.md   -- applies a fixed list of exact replacements, each of which must match once."""
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
R = [
("They are an easy update of Rankin's map, and they rest on one modelled dataset in which, by its own table of inputs, every country on the two slivers enters with a census of 2010 to 2012.",
 "They are an easy update of Rankin's map, and they rest on one modelled dataset in which, by its own table of inputs, the countries on the two slivers enter with censuses of 2005 to 2012."),
("- **Bill Rankin, \"Your Hemisphere\", 2015**,",
 "- **The problem in the abstract** is old: D. S. Johnson and F. P. Preparata, \"The densest hemisphere problem\", Theoretical Computer Science 6 (1978) 93–107: find the hemisphere holding the most of n points on a sphere, with a variant for weighted points. Known to me by title; the search summary of its abstract confirms it; I did not read the paper. It is not about people.\n- **Bill Rankin, \"Your Hemisphere\", 2015**,"),
("- A page at geoawesome.com gives 92.6% for the same map, by the search summary only; I did not fetch it.\n- **The problem in the abstract** is old: D. S. Johnson and F. P. Preparata, \"The densest hemisphere problem\", Theoretical Computer Science 6 (1978) 93–107: find the hemisphere holding the most of n points on a sphere, with a variant for weighted points. Known to me by title; the search summary of its abstract confirms it; I did not read the paper.\n",
 "- A page at geoawesome.com gives 92.6% for the same map, by the search summary only; I did not fetch it.\n"),
("- Rankin's map is of the year 2000, and the study's grid for 2000 also has the Alps on top, by 0.13 points over Berlin, a wider margin than in any later grid. So",
 "- Rankin's map is of the year 2000, and the study's grid for 2000 also has the Alps on top, by 0.13 points over Berlin; in 2010 that lead is 0.03. So"),
("The table of inputs gives the census year for each country: Philippines 2010, Malaysia 2010, Singapore 2010, Indonesia 2010, Brazil 2010, Ecuador 2010, Paraguay 2010, Bolivia 2012. So every grid, the one for 2020 included, is those censuses carried backward and forward by growth rates and scaled to the United Nations' country totals of 2022.",
 "The table of inputs gives the census year for each country: Philippines, Malaysia, Singapore, Indonesia, Thailand, Brazil, Ecuador and Paraguay 2010; Bolivia 2012; Peru 2007; Colombia 2005 (Mexico's row I could not read). So every grid, the one for 2020 included, is those censuses carried backward and forward by growth rates and scaled to the United Nations' country totals of 2022."),
("The move is what the censuses of about 2010, their growth rates and the UN's country series imply.",
 "The move is what censuses of 2005 to 2012, their growth rates and the UN's country series imply."),
("| | Malay Peninsula with Singapore (and Sumatra's coast north of 1° N) | 8.5 | 28.8 |\n| | the rest of mid-Sumatra | 3.6 | 10.5 |\n| | Pacific coast of Mexico, at the other end of the sliver | 0.1 | 0.5 |\n| only in the Alpine half | Brazil's side (São Paulo, Paraná and south, with Paraguay) | 33.2 | 65.0 |\n| | Ecuador with the north of Peru | 6.6 | 16.7 |\n| | Bolivia and inland | 1.4 | 4.7 |\n",
 "| | Malay Peninsula with Singapore (and Sumatra's coast north of 1° N) | 8.5 | 28.8 |\n| | the rest of Sumatra's middle | 3.6 | 10.5 |\n| | west of 60° E, mostly the Pacific coast of Mexico at the sliver's other end | 0.1 | 0.5 |\n| only in the Alpine half | Brazil's side, east of 60° W (São Paulo, Paraná and their neighbours) | 33.2 | 65.0 |\n| | Ecuador with the north of Peru and the south of Colombia | 6.6 | 16.7 |\n| | Bolivia and inland | 1.4 | 4.7 |\n| | elsewhere | 0.1 | 0.2 |\n"),
("published in Geographical Analysis 56 (2024) 514–529 by a later paper's citation. I read the preprint.",
 "published in Geographical Analysis 56 (2024) 514–529 (the journal reference is from a search summary of a later paper's citation). I read the preprint."),
("He credits the idea to Ken Myers (Reddit, 2013) and cites Quah (2015, 2016).",
 "He credits the idea to Ken Myers, on Reddit, and cites Quah (2015, 2016)."),
("The study's centre is 28 km from Arthur's; its radius is 40 km smaller, on different data.",
 "The study's centre is 28 km from Arthur's; its radius is 40 km smaller, on different data and a finer grid."),
("| section 2.5 and the rows of eleven countries read |",
 "| section 2.5 and the rows of fifteen countries read |"),
("by its own documentation every grid, 2020 included, starts from censuses of about 2010 scaled to the United Nations' country totals of 2022.",
 "by its own documentation every grid, 2020 included, starts from censuses of 2005 to 2012 scaled to the United Nations' country totals of 2022."),
("   New: `The population grid is a model (census counts spread over built-up area). Every one of its grids, 2020 included, starts from censuses of about 2010, carried backward and forward by growth rates and scaled to the United Nations' country totals of 2022; the grids for 2025 and 2030 use the UN's medium projection.`",
 "   New: `The population grid is a model (census counts spread over built-up area). Every one of its grids, 2020 included, starts from censuses of about 2010 (2005 to 2012 for the countries on the two slivers), carried backward and forward by growth rates and scaled to the United Nations' country totals of 2022; the grids for 2025 and 2030 use the UN's medium projection.`"),
]
for old, new in R:
    n = s.count(old)
    if n != 1:
        print("NOT APPLIED (matches: %d): %s" % (n, old[:70]))
        continue
    s = s.replace(old, new)
open(p, "w", encoding="utf-8").write(s)
print("done")
