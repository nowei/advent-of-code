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
