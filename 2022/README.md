# Advent of Code 2022

Answers written in Rust. Usually answers are what comes
to mind first. If it doesn't work, then something else is tried.
All solutions are best-effort-with-reasonable-attempts.

## short summaries (some spoilers)
day 01 - find largest sum; find sum of 3 largest sums

day 02 - some mod math for rock paper scissors as ints; some more mod math for rock paper scissors but whether we lose, draw, or win.

day 03 - Checking set intersections of half strings; then checking set intersections of 3 strings

day 04 - Checking int range containment; then checking int range overlap

day 05 - Rebuild board, then move via pop and push one at a time in order; move slices around (Simulation)

day 06 - Find end index of first 4 distinct; Find end index of first 14 distinct. Just used a sliding window.

day 07 - Regrets with Rust. The hard part for me was figuring out how to reconstruct directory information from strings initially without references to each other. This meant that we couldn't build the map as we were reading the data due to Rust's ideas of ownership and whatnot. I ended up doing this in two passes, once to collect directory content information and the second to actually create the directory structure and populate it so that it can be traversed. The question itself wasn't even that bad, it was just checking numbers against some other numbers.

