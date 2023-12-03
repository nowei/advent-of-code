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

### day 05

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
