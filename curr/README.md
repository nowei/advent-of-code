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

### day 07

### day 08

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
