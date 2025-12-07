# Advent of Code 2025

Answers written in python. Usually the answers are what comes
to mind first. If it doesn't work, then something else is tried.
All solutions are best-effort-with-reasonable-attempts.

To generate files for a given day,

```
uv run src/app.py --generate --day 1
```

To run; use

```
uv run src/app.py --day 1 --execute
```

## short summaries (some spoilers)

### day 01

Started a few days late, but part 1 was a simple mod. Part 2 was counting the number of times it crosses zero or lands on zero.

### day 02

I accidentally did part 2 during part 1. Part 1 asked for integers where the numbers were duplicated twice, so like `123123`, which repeats `123` twice. Part 2 asked for any number of repeats. I just brute-forced part 2 and iterated through all of the ranges. There probably could've been an easier way to do this with counters and checking if the number of digits in the number are a multiple of two. But I didn't do that, so 👀

### day 03

Part 1 was just finding the largest two-digit number in a string of numbers (respecting order). Part 2 is looking for the largest 12-digit number. So we consider the right 12 digits as the candidate number and consider each digit (starting from the left-most number) and compare them with the remaining numbers to the left to see if moving the candidate number would create a larger number (or gives more options to the other candidate numbers if it's the same).
