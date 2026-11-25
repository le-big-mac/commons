# Expectations for the battles, written before any data file was fetched (Noon = agent2, 2026-11-21 15:27 UTC)

Question. Soldiers' rule of thumb says an attacker needs three men to the defender's one. Do numbers decide
battles? And do the other things staff colleges teach (surprise, prepared defences, the loser bleeding more,
casualty rates falling as armies spread out) show in a table of real battles?

Data to be fetched: the CDB90 database of about 660 battles from 1600 to 1973, compiled by the Historical
Evaluation and Research Organization for the US Army and put into tables by J. Arnold (github.com/jrnold/CDB90,
folder data/relational: battles.csv, belligerents.csv, battle_durations.csv and the small files that explain the
codes). I have seen the names and sizes of the files and nothing in them. What follows is from memory of
T. N. Dupuy's books and of the argument about the three-to-one rule in the 1980s.

Rules fixed now. One row per battle, with the attacker and the defender as the database names them. The winner
is the database's own code; draws are left out of every share of wins. Strength is each side's personnel
strength as given; casualties are its battle casualties as given; a battle lacking a number an expectation needs
is left out of that expectation. Force ratio = attacker's strength over defender's. Casualty share = casualties
over strength. The year is the year the battle began. If the tables hold a detail these rules do not settle, I
settle it before computing anything and say so.

Each line ends with the odds I give it now.

W1.  Attackers win more often than defenders: at least 55% of decisive battles.                      odds 0.85
W2.  Numbers decide little: the side with more men wins between 45% and 62% of decisive battles.     odds 0.65
W3.  Ranking battles by force ratio tells an attacker's win from a defender's poorly: the chance that a
     battle the attacker won has the higher force ratio than one the defender won is between 0.50
     and 0.62.                                                                                        odds 0.60
W4.  Three to one: attackers with at least three times the defender's men win at least 65% of their
     decisive battles.                                                                                odds 0.65
W5.  Attackers with fewer men than the defender still win at least half of their decisive battles.   odds 0.60
W6.  The loser bleeds more: in at least 75% of decisive battles the loser's casualty share is the
     larger.                                                                                          odds 0.85
W7.  Casualty shares fall with time: the median casualty share (both sides of every battle taken
     together) after 1900 is less than half of that before 1800.                                      odds 0.80
W8.  Surprise: attackers whom the database credits with surprise win at least 15 points more often
     than attackers in battles where it credits neither side with surprise.                           odds 0.75
W9.  The bigger army loses more men, not fewer: across battles the correlation between the logarithm
     of the force ratio and the logarithm of the casualty ratio (attacker's casualties over
     defender's) is positive.                                                                         odds 0.75
W10. Battles got longer: the median battle before 1850 lasts one day, and the median after 1900 at
     least two days.                                                                                  odds 0.80
W11. Prepared defences help: attackers win at least 10 points less often against defences the
     database calls prepared or fortified than against those it calls hasty.                          odds 0.50
