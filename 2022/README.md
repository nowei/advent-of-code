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

day 08 - Rows and Cols got mixed up, but otherwise this was fine. Basically keeping track of things in a grid. 1.) was seeing if we can see the edge in any direction from each position. 2.) was rolling up to the current height in each direction and seeing how many things there are that we can see in our sightline.

day 09 - Following a moving point, basically just checked diffs and clamped; extend it and iterate over changes.

day 10 - Really weird instructions, doing math on some instruction cycles then checking if the current position is close enough to the register value.

day 11 - Simulating monkeys passing things around based on some mult/add ops and mod testing; the second part needed to do some modular arithmetic.

day 12 - started using backtracking, then dp to try to get the cost to get to the goal from any path, but I realized that I was doing a DFS rather than a BFS and didn't actually save the shortest path to a single place due to the order in which things are evaluated, then realized that I could just use a BFS.

day 13 - Nested arrays and comparing nested arrays.

day 14 - Simulation. One grain/one blocked wall piece at a time vs. actually writing out a map/setting for the problem; then the same, but with a floor.

day 15 - Working with ranges and collapsing ranges, then iterating over things, kind of brute-forced for part 2.