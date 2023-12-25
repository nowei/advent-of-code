# Advent of Code 2023

Answers written in `python`. Usually answers are what comes
to mind first. If it doesn't work, then something else is tried.
All solutions are best-effort-with-reasonable-attempts.

## short summaries (some spoilers)

### day 01

The first part is a forwards/backwards string search for digits.

The second part is a forwards/backwards string search for digits or strings representing digits (e.g. 'one', 'two', 'three', ..., 'nine'). I chose to use a trie to do the matching, so I constructed a forwards and backwards trie for matching the values, e.g. 'o' -> 'n' -> 'e' -> 1 or 'e' -> 'n' -> 'o' -> 1.

### day 02

The first part defines a game with colored cubes and asks to check if instances of the game are possible with some number of colored cubes.

The second part just asks us to find the minimum cubes per game, multiply them, and add them together.

### day 03

The first part is parsing numbers from a grid and checking to see if they neighbor any non-`.` and non-digit symbols, e.g. `*`, `@`, `:`, etc... We accomplish by just doing a scan for each row and col. Notice that we will always see the start of the digit if we iterate across the columns on the inner loop. This means that we can check the next columns until we reach the end of the number and then check the adjacent coordinates for non-`.` and non-digit symbols.

The second part instead looks for `*` and for `*` that border exactly two numbers. We notice that a number uniquely borders a `*` based on contiguity along the rows, i.e. if it is contiguous, it is part of the same number. If it is not, it is a new numbers. We reject checking `*` indicies where there were more or less than two bordering numbers. To get the number, we can simply go left and go right as far as we can across the columns given a starting coordinate and read from left to right to reconstruct the number.

### day 04

The first part is just doing like a 2^(num matching - 1) or 0 for each game card and adding them up.

The second part just adds copies of the next game cards based on the number of matching numbers in the current game card. So like if card `n` has 3 matching numbers and we have `c` copies of `n`, then we add `c` more copies of cards `n+1`, `n+2`, `n+3` where `n+x` is capped by the number of cards we started with.

### day 05

The first part was doing number conversions if they fell in a range, given as
`dest, start, range` which can be translated to `a = start, b = start + range - 1, shift = dest - start`
i.e. for `(a, b, shift)`, if for `c` in `a <= c <= b`, we add shift.

The second part was the same as above, but for ranges.
We do this by checking each range and subdividing the range based on the specific
shifts that it is a part of, i.e. overlaps with. For example, if we have a range `[1, 7]` and we have a range shift of `6` inside of `[2, 6]`, we would keep the ranges: `[1, 1], [2+6, 6+6]=[8,12], [7, 7]`. Then finding them minimum was generally trivial by checking the first index. In reality we only care about min edges and min edges of overlaps because all shifts maintain an increasing series.

We originally rabbit-holed on trying to do this by constructing a reverse conversion map by walking the conversion ranges backwards from destination to source, but I eventually learned that this wouldn't work after trying to code this for a while because the shifts are dependent, e.g. it jumps from one range region to another based on the previous one, so the transformations were not easily directly composable or invertible.

Instead of composing them, it's more like tracking how we can get from one region to another over time, e.g. landing on 2 in the given example can hop you to 8. There can be a many-to-one relationship in the conversion layers.

Like

```
1->1
2->2
3->3
4->4
5->5
6->6
```

with a range shift of `2` from `[1, 3]` becomes

```
1->3
2->4
3->5
4->4
5->5
6->6
```

Although the examples given only had swaps between the layers and it was still a 1:1 relationship, but it doesn't necessarily have to be.

### day 06

This is just binary search on the left and right to figure out what the transition points are to no longer score high enough to beat the designated score threshold.

### day 07

Just a parsing/ranking problem based on a string. We consider the hand type and then the individual ranks of cards if there is a tie.

The first part uses 2->A. The second part replaces the Jack with a wildcard Joker. We just enumerate all possibilities with the wildcard since there is a limited set of outcomes. Another way to do this would be to pose this as a search problem and trying out the different ways we can add the cards if we have `x` wildcard jokers, e.g. if we have 2 pairs already, what is the best outcome we can get if we have 1 joker. Or if we have 4 jokers, what is the best possible outcome from our starting point? One observation that could help with this is that it is always optimal to only increment numbers for things we already have, e.g. if we have 3 jokers and `{2: 1, 5: 1}`, we would never put the jokers into something that we didn't already have, e.g. `3`. Another way to make this more complex would be to rank the jokers based on what cards they imitate, assuming optimal ordering.

### day 08

The first part is just following the instructions and cycles.

The second part is doing that and tracking multiple nodes at the same time. The key observation is that there had to be cycles to continuously follow the path or there had to be overlaps (multiple Z's) in the cycles if multiple nodes enter the same cycles. It could've been the latter, because the setting wasn't particularly strict: "the number of nodes with names ending in A is equal to the number ending in Z!" But it wasn't so we got a little lucky.

The next thing to determine is where each cycle starts and when it hits the Z locations wrt the instruction steps (keeping track of the instruction step and locations are important).

Note that the pre-cycle path couldn't have had a different number of nodes from the end-cycle path, since for there to be a cycle, the same number of steps must've been taken/repeated at some point to get to the same number for it to cycle later on. Therefore the cycle start must've been the same for us to detect that there was a cycle.

One other observation is that all the Z nodes started the cycle of instructions over again, i.e. `steps % len(instructions) == 0`, but the result being a multiple of the number of instructions may have been necessary for it to cycle properly based on the number of instructions so it can always get back to the same spot and for us to detect that there was a cycle (by repeating a step with the same instruction).

### day 09

Get diff between consecutive numbers and like their rate(s) of changes and then extrapolating the next number. The next part is the same as the previous by trying to extrapolate the previous number.

### day 10

Create a map and just do a BFS of the possible pipe paths.

Second part was more fun, I ended up expanding the (valid, connected) pipe map so that it was easier to figure out what spaces were actually inside vs. outside of the pipes, e.g. I expanded

```
F
```

into

```
...
.F-
.|.
```

Such that something like

```
F-7
|.|
L-J
```

becomes

```
.........
.F-----7.
.|.....|.
.|.....|.
.|.....|.
.|.....|.
.|.....|.
.L-----J.
.........
```

then we simply had to count all the inside 3x3 squares that were all `I`'s.

Like their example of:

```
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
```

becomes

```
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
```

which when expanded becomes

```
............................................................
....F--------------7..F--7..F--7..F--7..F-----7.............
....|..............|..|..|..|..|..|..|..|.....|.............
....|..............|..|..|..|..|..|..|..|.....|.............
....|..F--------7..|..|..|..|..|..|..|..|..F--J.............
....|..|........|..|..|..|..|..|..|..|..|..|................
....|..|........|..|..|..|..|..|..|..|..|..|................
....|..|.....F--J..|..|..|..|..|..|..|..|..L--7.............
....|..|.....|.....|..|..|..|..|..|..|..|.....|.............
....|..|.....|.....|..|..|..|..|..|..|..|.....|.............
.F--J..L--7..L--7..L--J..L--J..|..|..L--J.....L-----7.......
.|........|.....|..............|..|.................|.......
.|........|.....|..............|..|..|..............|.......
.L--------J.....L--7...........L--J.-S--7..F-----7..L--7....
...................|.................|..|..|.....|.....|....
...................|.................|..|..|.....|.....|....
.............F-----J........F--7..F--J..|..L--7..L--7..L--7.
.............|..............|..|..|.....|.....|.....|.....|.
.............|..............|..|..|.....|.....|.....|.....|.
.............L--7.....F--7..|..|..L--7..|.....L--7..L--7..|.
................|.....|..|..|..|.....|..|........|.....|..|.
................|.....|..|..|..|.....|..|........|.....|..|.
................|..F--J..L--J..|..F--J..|..F--7..|.....L--J.
................|..|...........|..|.....|..|..|..|..........
................|..|...........|..|.....|..|..|..|..........
.............F--J..L-----7.....|..|.....|..|..|..|..........
.............|...........|.....|..|.....|..|..|..|..........
.............|...........|.....|..|.....|..|..|..|..........
.............L-----------J.....L--J.....L--J..L--J..........
............................................................
```

then when marked, it becomes:

```
OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
OOOOF--------------7OOF--7OOF--7OOF--7OOF-----7OOOOOOOOOOOOO
OOOO|IIIIIIIIIIIIII|OO|II|OO|II|OO|II|OO|IIIII|OOOOOOOOOOOOO
OOOO|IIIIIIIIIIIIII|OO|II|OO|II|OO|II|OO|IIIII|OOOOOOOOOOOOO
OOOO|IIF--------7II|OO|II|OO|II|OO|II|OO|IIF--JOOOOOOOOOOOOO
OOOO|II|OOOOOOOO|II|OO|II|OO|II|OO|II|OO|II|OOOOOOOOOOOOOOOO
OOOO|II|OOOOOOOO|II|OO|II|OO|II|OO|II|OO|II|OOOOOOOOOOOOOOOO
OOOO|II|OOOOOF--JII|OO|II|OO|II|OO|II|OO|IIL--7OOOOOOOOOOOOO
OOOO|II|OOOOO|IIIII|OO|II|OO|II|OO|II|OO|IIIII|OOOOOOOOOOOOO
OOOO|II|OOOOO|IIIII|OO|II|OO|II|OO|II|OO|IIIII|OOOOOOOOOOOOO
OF--JIIL--7OOL--7IIL--JIIL--JII|OO|IIL--JIIIIIL-----7OOOOOOO
O|IIIIIIII|OOOOO|IIIIIIIIIIIIII|OO|IIIIIIIIIIIIIIIII|OOOOOOO
O|IIIIIIII|OOOOO|IIIIIIIIIIIIII|OO|II|IIIIIIIIIIIIII|OOOOOOO
OL--------JOOOOOL--7IIIIIIIIIIIL--JI-S--7IIF-----7IIL--7OOOO
OOOOOOOOOOOOOOOOOOO|IIIIIIIIIIIIIIIII|OO|II|OOOOO|IIIII|OOOO
OOOOOOOOOOOOOOOOOOO|IIIIIIIIIIIIIIIII|OO|II|OOOOO|IIIII|OOOO
OOOOOOOOOOOOOF-----JIIIIIIIIF--7IIF--JOO|IIL--7OOL--7IIL--7O
OOOOOOOOOOOOO|IIIIIIIIIIIIII|OO|II|OOOOO|IIIII|OOOOO|IIIII|O
OOOOOOOOOOOOO|IIIIIIIIIIIIII|OO|II|OOOOO|IIIII|OOOOO|IIIII|O
OOOOOOOOOOOOOL--7IIIIIF--7II|OO|IIL--7OO|IIIIIL--7OOL--7II|O
OOOOOOOOOOOOOOOO|IIIII|OO|II|OO|IIIII|OO|IIIIIIII|OOOOO|II|O
OOOOOOOOOOOOOOOO|IIIII|OO|II|OO|IIIII|OO|IIIIIIII|OOOOO|II|O
OOOOOOOOOOOOOOOO|IIF--JOOL--JOO|IIF--JOO|IIF--7II|OOOOOL--JO
OOOOOOOOOOOOOOOO|II|OOOOOOOOOOO|II|OOOOO|II|OO|II|OOOOOOOOOO
OOOOOOOOOOOOOOOO|II|OOOOOOOOOOO|II|OOOOO|II|OO|II|OOOOOOOOOO
OOOOOOOOOOOOOF--JIIL-----7OOOOO|II|OOOOO|II|OO|II|OOOOOOOOOO
OOOOOOOOOOOOO|IIIIIIIIIII|OOOOO|II|OOOOO|II|OO|II|OOOOOOOOOO
OOOOOOOOOOOOO|IIIIIIIIIII|OOOOO|II|OOOOO|II|OO|II|OOOOOOOOOO
OOOOOOOOOOOOOL-----------JOOOOOL--JOOOOOL--JOOL--JOOOOOOOOOO
OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
```

### day 11

This is just manhattan distance with extra steps. Part two is just manhattan distance but crossing certain rows or columns requires additional cost. The second part could've been optimized with like a binary search to get all indicies between the rows, and we can just get the diff to the the number. But I didn't want to fiddle around with the boundaries until it worked so I just ran a range and checked inclusion in the set.

### day 12

This took me too long :skull:. The first thought that came into my head was to try everything permutation, so we used like `itertools.product`, which would've worked, but is slow because this is exponential in the number of permutations, i.e. `2^(# of '?')`. Then I thought about doing it as a search using BFS, then I made another search using DFS where it tried every possibility. Then I was like, "This isn't how it should be done, this is taking too long to run", so I looked up hints on reddit: https://www.reddit.com/r/adventofcode/comments/18hbbxe/2023_day_12python_stepbystep_tutorial_with_bonus/

I didn't read all of it, but part-way into reading it, I learned two major things that helped me get to a solution:

- Each requirement of like `n` `#` symbols requires the next `n` characters to be either `#` or `?` and if it was `.`, we could return early because it was not feasible.
- that I should cache my DFS search with like `functools.lru_cache` to cache values that were visited.

What I realized afterwards:

- I can just skip all the consecutive `.` symbols as well to get to the next ambiguous character `?` or to the next group I need to consider (i.e. all groups start with `#`).
- if more `#` than the sum of reqs, it's not feasible, and we can return early

This meant that the only things I had to track were the current index, `i`, and the current group/requirement index `req_i`, which could've been easily memoized with like a dict, but we use `functools.lru_cache` to cache/memoize the inputs.

The main thing that helped run the large input for part 2 was memoizing the inner dfs search function.

### day 13

Basically just checking for palindrome-like rows/columns. We do this by checking the original and the zipped (flipped) inputs and check each match. Then the second part was checking for like exactly one character off, which we could do by counting the diffs we find when looking for palindromic rows. Basically being able to suffer exactly one mismatch when looking for matching rows/cols.

### day 14

The first part is like a falling rocks simulation problem. Assuming we face north, we cycle by rotating and then shift north which is equivalent to shifting "west", we do this 3 times to simulate a cycle. Then the large number was a hint that this cycled eventually, so we basically just had to find when it started the cycle and when it started to cycle, then simulate `(large number - cycle_start) % cycle_length` in order to get the final orientation + load.

### day 15

Implement a small hashing thing on strings. Then it asks you to only hash part of the string and add or replace labels and values while maintaining order.

The hardest part about this problem was probably reading the problem.

### day 16

Basically a light and mirror problem, but we want to count the number of squares the light crosses.

The second part is the same thing but we change the initial position. This could be parallelized with multiprocessing (work is mostly compute-bound so multithreading will just thrash for execution time).

### day 17

The first part was like a BFS, but we could only go in a certain direction 3 times in a row.

The second part was like the first, but with the requirement that we could only go in a certain direction at least 4 or at most 10 times in a row.

### day 18

This is similar to the pipe one from day 10, but this time instead of space-filling, I checked the horizontal crossings by checking if the above or bottom had a crossing and only switched inside/outside if both a `#` was seen above and below in a sequence of `#`. Then I just counted the number of `#` to get the answer.

The second one had much larger coordinates, so I ended up just using Pick's Theorem + the Shoelace formula to get the answer. Although Pick's theorem says that it's supposed to be `A = i + b/2 - 1` for the area, but my solution involves a `+ 1` instead of a `- 1`. This is probably due to an overcount somewhere, possibly in the perimeter, but that means I overcounted by 4 and I'm unsure where that would come from.

I ended up reading about Green's theorem again and I think I should've taken better notes in Calculus.

### day 19

Part 1 is like sorting groups into accepted or rejected based on their contents and some workflow rules (some part of the group is greater than or less than some number), so like the workflow rules could point to other workflow rules or it can point to accepted or rejected. Everything ends up being accepted or rejected. Then we were just asked to sum all the accepted groups' items

Then part 2 asks us to do the same thing, but for valid ranges `[1, 4000]^4`. So we had to partition the ranges based on the workflow rules and figure out how to properly partition the ranges according to the rules. We did this by doing an iterative algorithm for advancing ranges. E.g. we would do this in levels and evaluating the levels created the next level. The next level was trimmed down by expiring the rejected and accepted lists. This will eventually terminate because all roads lead to acceptance or rejection.

### day 20

The first part was just simulation. The second part required analyzing the input to figure out what triggered the `rx` module. I tried running a simulation and hashed the output to try to find a cycle but after running it for a while and trying an input, I realized that I probably wouldn't be able to find it in time, so I looked at reddit and learned that the input was actually like 4 independent cycles. This let us break the graph into four subgraphs where we could just pay attention to when each subgraph cycle sent a high energy packet to the final `dt` module. Then it just became an LCM problem.

### day 21

The first part can be done with simulation, we make it slightly faster by noticing that we only care about the new neighbors and the old ones will repeat.

What I noticed before I looked for hints:

- Once a single garden square was filled, it would just switch back and forth between two numbers depending on if we're on an even or odd number of steps.
- We can duplicate the garden across infinity by doing a % of the row and col my the max row and max col
- The number of steps was very large, simulating the solution likely isn't the right way to go about it because the number of edges grows really fast.
- The given input left a square that was rotated 45 degrees empty, idk how this is relevant.

I eventually looked for hints on reddit because I was confused about a programmatic solution, but it seems like people solved this analytically so I ended up just looking at their hints because I felt like this was a little over my head.

Specifically, I saw: https://www.reddit.com/r/adventofcode/comments/18nol3m/2023_day_21_a_geometric_solutionexplanation_for/

Things I didn't notice:

- The grid was size 131 x 131
- There was an empty row and column along the middle
- S was at the very center of the grid
- A walk from the center to the edge was a 65 step distance
- full adjacent squares alternate between even or odd steps being full and the number of even or odd squares were squared numbers.
- The number of squares we walk is (26501365 - 65) // 131 = 202300 squares away from the original square.
  - This meant that the after filling all 202300 square in a single direction, we walk 65 more steps, which gets us to the end of that square, leaving behind only corners with squares > 65 away from the center being empty.

Things I realized:

- The diagonals that make up the empty, rotated square in the square were able to be filled in 65 steps, so the corners would always be the same amount of being unfilled.
- Corners matched to create empty corners of full 65-step squares

### day 22

Blocks falling down. This was kind of fun when I realized that I could just do like a scan of (x, y) and see what it would fall on top of. Then we only care about the tallest things it landed on, which was nice. Then the rule for checking whether it was safe to disintegrate was whether all the blocks this block supported had at least two blocks supporting it or if there was nothing above it.

Then for part two, I just copied the blocks and checked all the not-safe-to-disintegrate blocks and added the number of blocks that moved with each change together.

### day 23

Part 1 was just a dfs with some extra encoded steps for handling forced movements `<,>,v,^` and getting the longest path

Part 2 required summarizing the points into a smaller graph based on junctions as verticies and distances as edges. Specifically, the junctions were areas connecting at least 3 possible movements. After that, we just ran a dfs to find the longest path on the smaller junction graph.

### day 24

Part 1 was nice because we just had to convert each hailstone into slope-intercept form to find the intercept point. We could then determine if it was parallel by comparing the slopes after dividing by the gcd between the x and y velocities. Then after that, we can figure out if this is happening before or after by determining whether the intercept time is before or after the initial time we were given.

Part 2 was trickier. I originally tried looking at like minimizing pairwise distance, but things move in weird directions, and over time, so like minimum pairwise distance isn't the right metric for figuring out the order of collision points. Then I wanted to do something with parallel lines and constraints based on parallel lines and like the implications on the speed of the bullet. But there were no parallel lines in my input. 

I eventually realized that the problem was overconstrained in that there were more known variables than free variables and the solution really only needed a handful of hailstones. Then I got stuck on figuring out what equations to use. I eventually got to `(x - xs) / (dxs - dx) = t`, but I didn't know what to do from there. I knew it was supposed to be solved using some system of linear equations, but I wasn't sure about how to set it up since it's been a while. So I looked on reddit: https://www.reddit.com/r/adventofcode/comments/18q40he/2023_day_24_part_2_a_straightforward_nonsolver/ and realized that I can equate `(x - xs) / (dxs - dx) = t = (y - ys) / (dys - dy)`. Then the same could be done for `y,z` and `x,z`. After some manipulation, we could get the known variables on one side and the unknowns on the other. Note that this gave us 3 equations, but there are 6 unknown variables, so we needed at least one more point for consideration. Then we just put it in the numpy linalg solver and we get a number out. Alternatively, we could've used something like `xs * (dx - dx') + dxs * (x - x') = x * dx' - x' * dx` and just did it `y` and `z` and for 2 pairs to get6 equations as well. I don't remember if relating the variables was as important because each direction essentially operates independently.

### day 25

This was just a community-detection problem or a min-cut problem. I messed up implementing min cut twice, once with Karger's and then I gave up on trying with Stoer-Wagner. I eventually realized that this was like a Louvain community detection problem, but I messed myself up writing the algorithm. I eventually just used networkx, but I'll come back and code up the algorithms properly. There were some union find vibes, but that'd still require breaking up the graph.