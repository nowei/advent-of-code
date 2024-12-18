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

### day 15

The first part was just simulation with moving boxes. Moves to "." are easy, we just swap the positions. Moves towards "#" are also easy. We just don't move. Moves towards "O" are a little harder because we just need to check if the direction we move it towards is blocked by a # or not. If it is, we know that we don't need to make a move. If it isn't, then we just move by swapping positions from the last block forward to the "@".

For the second part, it was kind of like a domain expansion where everything became wider. The "O" characters became "[]". The other characters are the same. To handle left and right block moves, we can just keep going while there are "[" or "]" characters; if it stops by a "#", we don't need to move. Otherwise, we swap positions from the last block forward to the "@".

For up and down movements, this was a little more involved because we need to propagate the movements to the "[" if we try to move a "]" and vice versa. Then we have to do that for the next layer of blocks that these blocks touch. If any such layer touches a "#", then we know that no move can be made. If there are only "." above, we can terminate looking for things to move and start moving things. We can move things starting from the last layer down to the first (the "@").

### day 16

Just Dijkstra's to go from the start to end with the optimal cost.

Then it's Dijkstra's but keeping track of multiple paths that have the same, optimal cost.

### day 17

### day 18

### day 19

### day 20

### day 21

### day 22

### day 23

### day 24

### day 25
