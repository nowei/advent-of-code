# Advent of Code 2024

Answers written in python. Usually the answers are what comes
to mind first. If it doesn't work, then something else is tried.
All solutions are best-effort-with-reasonable-attempts.

To run; use

```
uv run src/app.py --day 1 --execute
```

## short summaries (some spoilers)

### day 01

Just aligning the arrays after sorting or correlating with the count of each instance.

### day 02

Check ascending/descending + make sure it's not jumping by too much. The second part is checking if it's still okay after removing something.

### day 03

Just a regex thing.

### day 04

Looking for a string in certain directions.

### day 05

Checking ordering + some swaps

### day 06

Follow a path, rotate by 90 degrees if we face an obstruction; count number of squares visited.
Part 2 replayed the path taken, but checks for potential loops we can create by adding an obstruction:

- Can't be on the path that was already taken
- Can't be out of bounds
- Can't be a rock that's already there
- Must follow-through to see if it loops or if it just exits the map

### day 07

Walking operators between operands to get to a target by \* or +.

Then do the same for concatenating the numbers with ||.

My :facepalm: for this one was that the target inputs could be repeated, which I didn't account for and got stuck initially.

### day 08

Jumps between nodes of the same type in a 2D space.

Then we extend the jumps between nodes of each group within the boundary.

### day 09

The first one was just greedily filling space; I ended up using an array to represent the memory because using strings for ids kind of messed up and I ran into some edge cases with trying to use the characters and their ordinal values... But filling the space wasn't too bad because you could use two pointers. With the left, track empty space and with the right, track non-empty space. Then we can stop when the two pointers

I ran into a hiccup on the second part because I didn't handle the case of the block moving directly to the left to consolidate the space. This ended up creating a cycle where it would swap the blocks back and forth when I tried to stitch together the moves... In any case, the prompt was generally straightforward, but I didn't handle the right-next-to-block case correctly.

What I ended up doing was kind of like two pointers, but we just keep track of the block's id, size, and free space. The left pointer tracked the first block with an empty space available and the right pointer kept track of the current block we're trying to move. Then we iterate between the left and right pointer to figure out if there is a space we can move the current block into.

If there isn't, then we just move the right pointer over.

If there is a block we can consolidate the candidate block next to, then we:

- move the block's size + free space to the block left of the candidate block
- update the consolidating block's free space to 0 (for the candidate block moves next to it)
- update the candidate block's free space to the consolidating block's free space - the candidate block's size
- splice the array to move the block over
- Keep the evaluation index the same because we shifted stuff over

Then there is the special case where the consolidating block is already directly to the left of the candidate block, in which case

- We wouldn't move the candidate block's size + free space to the block left of the candidate block (because it'll be set to 0), but we just give the consolidating block's free space to the candidate block and call it a day

### day 10

We just do a bfs per trailhead.

I just did a bfs to search to determine the number of distinct 9-height tiles we can reach. Note that the simplification that we can only make 1-level-difference moves and we can only increase the paths made it easier because that means that means we only need to consider the from layer n with value n, layers n + 1 with values n + 1, e.g. for layer 0, we only care about adjacent tiles with value 1 when making layer 1. This meant that the method for consolidating the layers is pretty straightforward.

For the second part, it was just counting the number of different ways to reach the same points. We can do this by tracking: for each node in a new layer, the number of all the different ways to reach a node in the new layer from the current layer. This ends up just being the sum of the ways to reach the nodes in the previous layer. E.g. when two disjoint paths join together, we end up getting 1 + 1, so there are two ways to reach that intersection. Then since there is no backtracking, we can just carry these forward layer by layer until we reach the top of the trailhead.

### day 11

The first part I did it with like a simulation with arrays.

Then I got confused about the second part because it mentioned something about how order was preserved, so I thought that order mattered or something or that there was some pattern with how the numbers split and that we can come up with an equation to model the pattern. During this effort, I found out that a lot of the numbers were repeated.

It made sense that there needed to be a better data structure that could be used rather than just simulating the growing array on each step. While frustrated, I was looking at memes on AOC reddit and kind of spoiled the answer for myself when some comments were talking about how they could use a stack to only evaluate one stone at a time by tracking the step number for each evaluated stone (max stack depth of 75) or how they used memoization and lru caches with recursion or how the hint about how the rocks staying ordered didn't matter. I eventually read a comment that said that the rocks with the same number could be combined to be evaluated together in the next step, which is the solution I ended up with. Instead of trying to evaluate individual rocks for each layer, we can evaluate the group of rocks with all of the same numbers and move them to the next layer.

So the key thing to remember is that if it takes too long to run, think about how can you reuse the work that you've done (memoization) or group the things you're trying to do the work of the group all at once instead of individually.

The work per step is normally bounded by `O(d^s)` where `d` is the branching factor and `s` the number of steps. `d` is at least 1 (stays the same) and at most 2. We can easily say that `d` is at most 2 because during splits, it at most doubles. (Ostensibly, the real bound for `d` is `~1.5`).

Let each number be `n`, we do a unit of `d_n` work per `n` depending on the rules given. Let there be `k` instances of the number `n` in step `s`. In which case the total number amount of work is `sum of d_n * k for n in layer`. When we evaluate it in groups, we only do `sum of d_n for n in layer`; so we reduce the amount of work by the number of instances per number. And the number of instances per number can grow exponentially, so we got rid of an exponential number of growth. The number of distinct numbers is bounded by the rule that if the number of digits is even, we divide the number by 2. Thus, numbers cannot grow too large. For when they grow too large; then there is a split and it becomes a number that is smaller. Once this happens enough times, eventually they consolidate down to the `n` distinct numbers.

There is also an inherent pattern to the growth of the numbers due to the cyclical nature of the rules. The largest number I have seen so far is `409526509568`, so the counters should be bounded within it. The number of possible numbers the stones can take on is also limited by the rules to like single digit numbers and numbers that are a multiple of 2024, or have an odd number of digits.

### day 12

The first part was finding the area + perimeter of regions on a grid.

The second part was finding the area + sides of regions on a grid. We did the sides by grouping the rows and columns of the same regions and then from those regions, detecting the surroundings on the parallels (left/right for columns; top/bot for rows). Then from there, we look for contiguous strips along the parallels that are not part of the region.

### day 13

I just ran it normally the first time by simulating 100 -> 1 button presses on B. I initially tried to some sort of double binary search, but I couldn't figure out how to solve the bounds properly.

Eventually I realized that it was in the form of

```
a_x*a_c + b_x*b_c = p_x
a_y*a_c + b_y*b_c = p_y
```

So I was able to just solve it using some math for solving for the unknowns (the number of times a is pressed and the number of times b is pressed). Then we just needed to round the solution (floating point issues) and confirm that it works (not all machines can reach the prize with integer button presses).

### day 14

The first step was just doing the math to calculate the final position and then modding by the grid size to get the particles into the right place.

The second part was looking for a christmas tree. I ended up being able to find a pattern with poles happened starting at step 98 and repeated every 101 steps. We only print these outputs and eventually found the tree pattern...

```
.....................................................................................................
....................................1111111111111111111111111111111............1....................1
....................................1.............................1..................................
....................................1.............................1..................................
....................................1.............................1..................................
.................................1..1.............................1..................................
....................................1..............1..............1............1.....................
....................................1.............111.............1..................................
....................................1............11111............1..................................
................1...........1.......1...........1111111...........1..................................
....1...............................1..........111111111..........1..................................
....................................1............11111............1..................................
..............................1.....1...........1111111...........1..................................
....................................1..........111111111..........1..................................
..............1.....................1.........11111111111.........1..................................
............1.......................1........1111111111111........1..1...............................
..................................1.1..........111111111..........1..................................
..1...................1.............1.........11111111111.........1...........................1......
....................................1........1111111111111........1...........................1......
....................................1.......111111111111111.......1..................................
....................................1......11111111111111111......1..........1.......................
....................................1........1111111111111........1...............................1..
.......11...........................1.......111111111111111.......1..................................
....................................1......11111111111111111......1............................1...1.
.................................1..1.....1111111111111111111.....1..................................
....................................1....111111111111111111111....1..................................
.....1..............................1.............111.............1..................................
...................1................1.............111.............1..................................
.........................1..........1.............111.............1..1....1..........................
..................1.................1.............................1...............1..................
............................1.......1.............................1..................................
....................................1.............................1..................................
....................................1.............................1..................................
....................................1111111111111111111111111111111..................................
.....................................................................................................
```

### day 15

The first part was just simulation with moving boxes. Moves to "." are easy, we just swap the positions. Moves towards "#" are also easy. We just don't move. Moves towards "O" are a little harder because we just need to check if the direction we move it towards is blocked by a # or not. If it is, we know that we don't need to make a move. If it isn't, then we just move by swapping positions from the last block forward to the "@".

For the second part, it was kind of like a domain expansion where everything became wider. The "O" characters became "[]". The other characters are the same. To handle left and right block moves, we can just keep going while there are "[" or "]" characters; if it stops by a "#", we don't need to move. Otherwise, we swap positions from the last block forward to the "@".

For up and down movements, this was a little more involved because we need to propagate the movements to the "[" if we try to move a "]" and vice versa. Then we have to do that for the next layer of blocks that these blocks touch. If any such layer touches a "#", then we know that no move can be made. If there are only "." above, we can terminate looking for things to move and start moving things. We can move things starting from the last layer down to the first (the "@").

### day 16

Just Dijkstra's to go from the start to end with the optimal cost.

Then it's Dijkstra's but keeping track of multiple paths that have the same, optimal cost.

### day 17

Simulating some assembly instructions. The second part was a little wonky because we needed to replicate the program with the output.

The second part was doing a search to figure out how to construct an input that reproduces the program that it gets run with. Several key observations were necessary for solving this:

- Evaluating the instructions shows that the A register gets // 8 on every loop. This means that the minimum result should be some sum of factors of powers of 8, e.g. a\*8^1 + b\*8^2 + ... = A
- We should evaluate the entries with more matches earlier on than the entries with less matches (to the given problem)
- Heuristic: If the index we are searching for is greater than the number of matches available at that point, then we should give up because that means that there is no way to satisfy the entire program input (there are mismatches earlier on that cannot be resolved by going deeper).

### day 18

Just a BFS to get from start to end.

Keep adding obstructions until we can no longer get to the end. We make an optimization where we do not re-evaluate the path if the new obstruction does not fall onto the current path.

### day 19

The first part was just a search I did with bfs where I jumped the characters that matched usable towels and the next character to check.

The second part wanted all the combinations, so it was just a simple dynamic programming setup where we take O(t \* c) time per towel where t is the length of the towel and c is the number of combinations to evaluate all the combinations. (We store the number of ways (count) to jump to a certain index starting from some previous index as long as they match).

### day 20

Follow a single path + figure out how much time would be saved by skipping a one-width wall. We do this by first following the path so we have a list of tuples that represents the path. Then we determine at each step how far the current tuple is away from the end. Then to find the time saved, it's the distance from the end of the current location minus the distance from the end of the candidate location minus 2 (the time it takes to get across the one-width wall).

Follow the single path, but now instead of skipping a one-width wall; we can have to figure out how much time we can save if we can travel to an unvisited part of the path that is within a manhattan distance of 20. We do this by following the path and at each step, iterating over candidate jump locations on the path and evaluating only those that are within 20 of the current location. Then the time saved is computed in a similar fashion - the distance from the end of the current location minus the distance from the end of the candidate location minus the (manhattan) distance between them (the time it takes to get to that location, while ignoring collisions).

### day 21

This was a doozy. The question had essentially two grids. One keypad input and one directional input.

```
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
\ \ | 0 | A |
\ \ +---+---+

\ \ +---+---+
\ \ | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
```

I started by trying to create all the different optimal paths from one grid position to another grid location (for the keypad and directional grids separately). I did this with dijkstra's but allowing many paths to get from A -> B as long as they were all the same distance. Then eventually I realized that it's more optimal for the latter robots if all the same moves were consecutive, e.g. no `<^<^` but rather `<<^^` or `^^<<` because that would mean a downstream robot would have to switch between `<` and `^` more times than necessary. I considered each pair of `A -> B` a transition from one position to another and the path to be the set of moves to get from `A -> B`.

There were some ties, e.g. `<<^^` and `^^<<`. I ended up optimizing the paths, saying that we preferred characters with a distance from the input key `A` at the end of the sequence such that the transition to the input key is only one step. I set up my order of preference like this

```
distance_from_a = {"<": 3, "^": 1, "v": 2, ">": 1}
...
if distance_from_a[candidate[-1]] < distance_from_a[best[-1]]:
    best = candidate
```

The first part was easy enough to do because even though there were 3 levels of indirection (1 keypad, 2 direction robots, and you) you can still run everything as a string and you can append "A" at the very beginning (starting position) and iterate through every pair to generate the set of moves you need to make for the next level.

To be honest, I was a little confused about how the robot was inputting the numbers by pressing A vs. the first level robot being able to just press the number.

For the second part, instead of 3 levels of indirection, we had 26 (1 keypad, 25 direction robots, and you). This made the string grow quite large, generally exponentially. The first thought I had was to break this down into a counter so that we count the pairs that we cared about on each level to figure out what transitions we cared about on the next level. This worked fine for the first few levels.

Eventually I ran into a snag with this implementation because while for the first few levels we can up with the optimal/correct number of steps, the correct number of steps eventually drifted starting from around the 5th level of indirection. So I gave up on this approach at this point.

I looked at reddit and saw that there were several people who did it with DP where they cached the level and the path that is being evaluated. Then for each path, they try each pair (starting from `A` -> ending at `A`).

One key observation was that every pair starting after the first level of indirection must start at `A` and end at `A` because we must press the `A` button to input the key.

Additionally, instead of trying to find a better shortest path from A -> B, they tried all the paths. I also looked at another solution that used counters. These two solutions provided different results 👀

I ended up trying the DP approach but I only tried the ~equivalent shortest paths from A -> B when there was more than one potential path. This ended up giving the correct answer. This meant that there was something wrong with my counter approach. Eventually, I refactored it a bit so that it doesn't try to build the count of transitions right away but does it in two steps. The first step is mapping the number of transitions `A -> B` to the number of paths (e.g. `>>^^`) that we need to consider. Then the next step is considering the pairs of transitions in the new path, e.g. `A + >>^^ + A = A>>^^A = [(A, >), (>, >), (>, ^), (^, ^), (^, A)]`. After that, for each pair, we add `count` to the value for each pair in the new transitions map. Then we pass this to the next evaluation. Generally, this logic seemed like it should work. But the results diverged after ~the 5th step. I wondered why this was and tried comparing the results to the DP setup, but the formulations were not exactly the most comparable because one was bottom-up (DP) vs. the other being top-down (Counter).

Eventually I played around with the distance from A heuristic:

```
distance_from_a = {"<": 3, "^": 1.2, "v": 2, ">": 1}
```

and this ended up giving results that were consistent with the DP solution. It seems that `^` and `>` were not actually equally favorable. These were the following diffs (left is optimal, right is less)

```
5c5
<   "v": { "<": "<A", ">": ">A", "^": "^A", "v": "A", "A": "^>A" },
---
>   "v": { "<": "<A", ">": ">A", "^": "^A", "v": "A", "A": ">^A" },
27c27
<     "3": "^>A",
---
>     "3": ">^A",
30c30
<     "6": "^^>A",
---
>     "6": ">^^A",
33c33
<     "9": "^^^>A",
---
>     "9": ">^^^A",
42,43c42,43
<     "5": "^>A",
<     "6": "^>>A",
---
>     "5": ">^A",
>     "6": ">>^A",
45,46c45,46
<     "8": "^^>A",
<     "9": "^^>>A",
---
>     "8": ">^^A",
>     "9": ">>^^A",
56c56
<     "6": "^>A",
---
>     "6": ">^A",
59c59
<     "9": "^^>A",
---
>     "9": ">^^A",
84,85c84,85
<     "8": "^>A",
<     "9": "^>>A",
---
>     "8": ">^A",
>     "9": ">>^A",
98c98
<     "9": "^>A",
---
>     "9": ">^A",
```

This actually made some sense, as in order to move up, we have to go left. This means that even though the end position is near A (1 away) on the current level, the downstream position would need to move left, which is 3(!!) blocks away. Compared to if it ended on a >, then it would need to move down (also near A (1 away) on the current level), but that is only 2(!!) steps on the next level. This means that every it would be preferable to end `>` over ending `^`.

These were the optimal directions...

```
{
  "<": { "<": "A", ">": ">>A", "^": ">^A", "v": ">A", "A": ">>^A" },
  ">": { "<": "<<A", ">": "A", "^": "<^A", "v": "<A", "A": "^A" },
  "^": { "<": "v<A", ">": "v>A", "^": "A", "v": "vA", "A": ">A" },
  "v": { "<": "<A", ">": ">A", "^": "^A", "v": "A", "A": "^>A" },
  "A": { "<": "v<<A", ">": "vA", "^": "<A", "v": "<vA" }
}
```

### day 22

Easier than day 21. The first part was just following a sequence that felt similar to hashing to generate pseudorandom numbers. The input was a list of numbers and the goal was to do this operation 2000 times on each number and then sum the results.

The second part was a little more involved because it wanted us to track the one's digit for all these numbers over the 2000 iterations. After that, it wanted us to check the changes between these iterations. Then for these changes, it wanted us to track the first instance of every four consecutive changes at a time for every monkey and the associated amount after these 4 changes. Then at the end of evaluation, we carry this forward to a global tracker that tracks 4 changes -> sum of final amounts after the 4 consecutive changes shows up in each list (0 if it doesn't). Then we just return the best 4 changes we should keep track of in order to maximize the sum of final amounts.

```
create global quad tracker
for each secret number:
    generate list secret number and following 2000 pseudorandom numbers
    get ones digit of every number in list
    get changes between entries
    for every quad of changes:
        mark the first instance and the associated final ones digit in the list
    for every quad of changes and associated amounts:
        add quad to global quad tracker if it doesn't exist
        add the associated amount
return get max associated amount
```

### day 23

The first part was just finding triplets of nodes, so for every node, we had to check every pair of edges that it was connected to. For the nodes on the other side of the edges, we know that it formed a triplet if they shared an edge.

Then the second part wanted to find a maximal clique (a group of nodes where all nodes in the group have an edge between them). We could've started the problem off from the triplets, since the triplets should've been a part of a maximal clique (a clique of size n contains n cliques of size n - 1 (exclude one node and there are n many ways to exclude the nodes)). But that would've been a little more complicated with trying to reason about the data structures and procedures needed to find common neighboring triplets.

In the end, I opted to do a recursive solution where I check every node. Then the maximal clique formed from every node would be all of its neighbors (if it was one, or something smaller (more likely)).

So we start with a candidate set that is the current node. Then I considered each neighbor. If the neighbor was a node connected to all the nodes in the candidate set via an edge, then we could add it to the candidate set, remove it from the list of possible neighbors, and explore the remaining neighbors to see if they fit into the clique (have an edge that is connected to all current members of the clique). At each step, we track the best clique we have found and return that.

We made two optimizations to this process.

- If the neighbor was in the best clique we have seen so far, we don't need to reconsider the clique because the results will be the same + this will lead to a factorial of potential add orderings if not addressed.
- If the neighbor has been visited (as a part of a clique) in some recursion, then this neighbor was not a part of the best clique (first case) and the clique it was in was already evaluated.

### day 24

The first part was relatively straightforward, where we were just doing a topological sort on the dependency graph of XOR/AND/OR logic gates and the inputs then assemble the final output with the results of all the registers that start with z.

The second part was a little rougher because it tells us that the logic gates are supposed to be an adder for the 44-bit numbers. We ended up solving this printing out the inputs, adding them together, and seeing what it's supposed to be and comparing that output with the actual output of the gates. Then the first location that there is an issue should ~roughly be the first digit that there is a mismatch starting from the right. Then we start to debug from there. To help with this, we worked backwards from every equation by replacing its precedents with their precedents until we had an equation that was made up of `y__`, `x__`, and `XOR`/`OR`/`AND` and parentheses. For example,

```
mbj XOR rnp = z03
```

becomes

```
(x03 XOR y03) XOR (((x02 XOR y02) AND ((x01 AND y01) OR ((x00 AND y00) AND (x01 XOR y01)))) OR (x02 AND y02)) = z03
```

From there, we determine the pattern for the adder, which I should've remembered from my computer architecture classes 😅. In any case, we see that there should be only one `x_n XOR y_n` for `z_n`. And the rest should be like `XOR/OR/AND`s of the previous components. From there, I was able to deduce the registers that had the wrong precedents and find where the right precedents were and rewrite their equations s.t. they were correct. Eventually I had to try a few other inputs to make sure that it worked correctly for a few other inputs and it wasn't just happenstance that it was correct.

### day 25

Part 1 was just checking if the key fit in the locks; so like if there were no overlaps between the keys and locks, then it was a fit. This isn't really how keys and locks should work in my opinion, but to each their own. I added up the columns and checked if they were below a number instead of if they didn't have an overlap, which still worked but it was sort of a cop-out since it wasn't clear if there wasn't an overlap or not. I guess another thing I could've done was overlap the keys and locks and checked if there was a `#` block in both at each row and column, which would've been more accurate since just adding the numbers column-wise loses the idea that one is hanging down and one is pointing up.

In any case, I just checked that every column added up to `<=7`
