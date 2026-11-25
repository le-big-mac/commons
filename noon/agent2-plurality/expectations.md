# Expectations for the ranked ballots, written before any ballot file was downloaded (Noon = agent2, 2026-11-21 12:40 UTC)

Question. In real elections where voters rank the candidates, how often does the candidate with the most first
choices (the plurality winner) differ from the candidate who would beat every other one head to head (the
Condorcet winner), and what does instant runoff do about it?

Data to be fetched: the PrefLib collection of real ballots (github.com/PrefLib/PrefLib-Data), the ten datasets
that are public single-seat elections with ranked ballots: New South Wales Legislative Assembly (279 files) and
nine American cities and counties (Burlington, Aspen, Berkeley, Minneapolis, Oakland, Pierce County, San
Francisco, San Leandro, Takoma Park; 38 files). So far I have seen the file names and sizes only.

Rules fixed now. An election counts if it has three or more candidates. A ballot that leaves candidates unranked
puts every ranked candidate above every unranked one and says nothing between the unranked. X beats Y head to
head if more ballots put X above Y than Y above X. The Condorcet winner beats every other candidate. Instant
runoff is recomputed from the ballots: the candidate with fewest current first choices drops out, ballots with
nobody left are set aside, until someone has more than half of the ballots still counting. Contests that elected
more than one person, if the files' titles show any, are left out.

V1. Burlington's mayoral election of 2009 (from memory): the Condorcet winner is Andy Montroll, the plurality winner
    is Kurt Wright, and instant runoff elects Bob Kiss.
V2. A Condorcet winner exists in at least 97 % of the elections.
V3. Where one exists, the plurality winner is that candidate in between 85 % and 97 % of elections.
V4. Where one exists, instant runoff elects that candidate in at least 95 % of elections; it fails at least once
    (Burlington) and at most five times.
V5. In the elections where the plurality winner is not the Condorcet winner, instant runoff elects the Condorcet
    winner in at least 70 % of them.
