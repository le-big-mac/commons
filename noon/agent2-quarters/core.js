// The quarters, rung in changes. A clock chime for five bells: every quarter of an hour rings the next rows of an extent of
// Plain Bob Doubles (all 120 orders of five bells, each once), one row at the quarter past, two at the half, three at the quarter to
// and four on the hour, as the Westminster chime does with its five changes on four bells. Ten rows an hour, so the whole extent
// goes by in twelve hours and comes round, 1 2 3 4 5, at noon and at midnight. Then the hour is struck on a deeper bell.
(function (root) {
  'use strict';
  const ROWS = [[1,2,3,4,5],[2,1,4,3,5],[2,4,1,5,3],[4,2,5,1,3],[4,5,2,3,1],[5,4,3,2,1],[5,3,4,1,2],[3,5,1,4,2],[3,1,5,2,4],[1,3,2,5,4],[1,3,5,2,4],[3,1,2,5,4],[3,2,1,4,5],[2,3,4,1,5],[2,4,3,5,1],[4,2,5,3,1],[4,5,2,1,3],[5,4,1,2,3],[5,1,4,3,2],[1,5,3,4,2],[1,5,4,3,2],[5,1,3,4,2],[5,3,1,2,4],[3,5,2,1,4],[3,2,5,4,1],[2,3,4,5,1],[2,4,3,1,5],[4,2,1,3,5],[4,1,2,5,3],[1,4,5,2,3],[1,4,2,5,3],[4,1,5,2,3],[4,5,1,3,2],[5,4,3,1,2],[5,3,4,2,1],[3,5,2,4,1],[3,2,5,1,4],[2,3,1,5,4],[2,1,3,4,5],[1,2,4,3,5],[1,4,2,3,5],[4,1,3,2,5],[4,3,1,5,2],[3,4,5,1,2],[3,5,4,2,1],[5,3,2,4,1],[5,2,3,1,4],[2,5,1,3,4],[2,1,5,4,3],[1,2,4,5,3],[1,2,5,4,3],[2,1,4,5,3],[2,4,1,3,5],[4,2,3,1,5],[4,3,2,5,1],[3,4,5,2,1],[3,5,4,1,2],[5,3,1,4,2],[5,1,3,2,4],[1,5,2,3,4],[1,5,3,2,4],[5,1,2,3,4],[5,2,1,4,3],[2,5,4,1,3],[2,4,5,3,1],[4,2,3,5,1],[4,3,2,1,5],[3,4,1,2,5],[3,1,4,5,2],[1,3,5,4,2],[1,3,4,5,2],[3,1,5,4,2],[3,5,1,2,4],[5,3,2,1,4],[5,2,3,4,1],[2,5,4,3,1],[2,4,5,1,3],[4,2,1,5,3],[4,1,2,3,5],[1,4,3,2,5],[1,3,4,2,5],[3,1,2,4,5],[3,2,1,5,4],[2,3,5,1,4],[2,5,3,4,1],[5,2,4,3,1],[5,4,2,1,3],[4,5,1,2,3],[4,1,5,3,2],[1,4,3,5,2],[1,4,5,3,2],[4,1,3,5,2],[4,3,1,2,5],[3,4,2,1,5],[3,2,4,5,1],[2,3,5,4,1],[2,5,3,1,4],[5,2,1,3,4],[5,1,2,4,3],[1,5,4,2,3],[1,5,2,4,3],[5,1,4,2,3],[5,4,1,3,2],[4,5,3,1,2],[4,3,5,2,1],[3,4,2,5,1],[3,2,4,1,5],[2,3,1,4,5],[2,1,3,5,4],[1,2,5,3,4],[1,2,3,5,4],[2,1,5,3,4],[2,5,1,4,3],[5,2,4,1,3],[5,4,2,3,1],[4,5,3,2,1],[4,3,5,1,2],[3,4,1,5,2],[3,1,4,2,5],[1,3,2,4,5]];                               // the extent, from ../agent2-changes/ (rows[0] is rounds)
  const P = {
    PITCH: { 1: 71, 2: 69, 3: 66, 4: 64, 5: 62 },      // B4 A4 F#4 E4 D4: rounds is the scale coming down
    HOUR: 50,                                          // D3, the bell that counts the hours
    BEAT: 0.42, ROW: 7,                                // seconds between bells; beats a row takes (five bells and a breath)
    WAIT: 1.6, STRIKE: 2.2,                            // seconds after the last row before the first stroke of the hour; between strokes
    PAN: { 1: 0.7, 2: 0.35, 3: 0, 4: -0.35, 5: -0.7 },
    BELL: [[0.5, 0.25, 1.92], [1, 1, 1.49], [2.0, 0.45, 0.96], [2.76, 0.3, 0.587], [4.07, 0.18, 0.373], [5.4, 0.1, 0.213]]   // ratio, level, seconds to fall by e
  };
  // Which rows a chime rings. hour12: 0 to 11, the hour now running (0 is twelve o'clock). quarter: 1, 2, 3 at a quarter past, half past,
  // a quarter to; 4 on the hour that ends it. Returns row numbers 1 to 120 (row 120 is rounds again, written 0 in ROWS).
  function rowsOf(hour12, quarter) {
    const base = 10 * hour12 + [0, 0, 1, 3, 6][quarter], out = [];
    for (let i = 1; i <= quarter; i++) out.push(base + i);
    return out;
  }
  // Everything that sounds in one chime, with times in seconds from its start.
  function chime(hour12, quarter) {
    const rows = rowsOf(hour12, quarter), notes = [];
    rows.forEach((r, i) => ROWS[r % 120].forEach((bell, j) => notes.push({ t: +((i * P.ROW + j) * P.BEAT).toFixed(4), midi: P.PITCH[bell], bell, row: r, place: j + 1, gain: j === 0 ? 0.56 : 0.5, pan: P.PAN[bell], kind: 'bell' })));
    const strikes = quarter === 4 ? ((hour12 + 1) % 12 || 12) : 0, t0 = (rows.length * P.ROW - 2) * P.BEAT + P.WAIT;
    for (let s = 0; s < strikes; s++) notes.push({ t: +(t0 + s * P.STRIKE).toFixed(4), midi: P.HOUR, bell: 0, row: 0, place: s + 1, gain: 0.85, pan: 0, kind: 'hour' });
    return { hour12, quarter, rows, strikes, notes, lasts: +(notes[notes.length - 1].t + 7).toFixed(3) };
  }
  // The chime that belongs to a quarter boundary: given the clock's hour (0 to 23) and minute (0, 15, 30 or 45) at that boundary.
  function at(hour24, minute) {
    const quarter = minute === 0 ? 4 : minute / 15, running = minute === 0 ? (hour24 + 23) % 24 : hour24;      // the hour that the chime belongs to
    return chime(running % 12, quarter);
  }
  // The next boundary after a moment given in milliseconds of local clock time since local midnight-based epoch; returns milliseconds.
  const QUARTER = 15 * 60 * 1000;
  const nextBoundary = ms => (Math.floor(ms / QUARTER) + 1) * QUARTER;
  const api = { P, ROWS, rowsOf, chime, at, nextBoundary, QUARTER, hz: m => 440 * Math.pow(2, (m - 69) / 12) };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.Quarters = api;
})(typeof window !== 'undefined' ? window : globalThis);
