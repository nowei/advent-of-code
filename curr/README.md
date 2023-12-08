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

### day 10

### day 11

### day 12

### day 13

### day 14

### day 15

### day 16

### day 17

### day 18

### day 19

### day 20

### day 21

### day 22

### day 23

### day 24

### day 25
