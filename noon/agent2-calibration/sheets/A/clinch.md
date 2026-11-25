# Expectations for the clinching dates, written before any result was read (Noon = agent2, 2026-11-21 11:32 UTC)

Data to be fetched: every match of the English Premier League, ten seasons, 2014-15 to 2023-24, with dates
(football-data.co.uk). So far I have fetched one file to see that it exists and looked at its column names only.

The question. Newspapers say a title, a place or a relegation is "mathematically" settled by a simple count: a
team's largest possible total against the others' current totals. That ignores the fact that the others still
have to play each other. The exact answer needs a small integer programme over the remaining fixtures. How often,
and by how much, is a matter truly settled before the simple count says so?

Four matters, for every team and season, each with a simple and an exact version:
  out of the title (cannot finish level with or above everyone);
  doomed (cannot finish 17th or better);
  safe (certain to finish 17th or better, whatever happens, ties going against it);
  sure of the top four (likewise).
A matter is dated by the day on which it becomes settled. The lead of exact over simple is counted in league
matches played in between, divided by ten ("rounds"), so that a paused season does not inflate it.

L1. For being sure of the title the two always agree (the worst case, the leader losing everything and one rival
    winning everything, is always possible): lead 0 in all ten seasons. A test of my program.
L2. Out of the title: the exact date is earlier than the simple one in between 20 % and 60 % of the 190
    team-seasons that do not win; the largest lead is between 0.5 and 4 rounds.
L3. Safe: exact earlier than simple in between 20 % and 60 % of the team-seasons that end up safe.
L4. Doomed: exact earlier than simple for at least 5 of the 30 relegated teams, and never by more than 2 rounds.
L5. Sure of the top four: exact earlier than simple for at least 10 of the 40.
L6. Nowhere is the lead more than 5 rounds.
