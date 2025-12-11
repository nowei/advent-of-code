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

### day 04

The first part was counting locations that fit a certain criteria. Then the second part was using those locations and removing them iteratively.

### day 05

The first part was just checking if things fit in a range. The second part was just merging overlapping ranges.

### day 06

Doing some math in columns, then reading the numbers in columns.

### day 07

Splitting beams simulation, then memoization for the second part to consider possible states.

### day 08

Union find gang. Basically ranking connections based on distances between two points, making those connections and continuing to do that `n` times in part 1 and then doing that until everything is connected in part 2 and using the coordinates used for the last connection and doing some math with it.

### day 09

Kind of messed up. The first part was finding the largest area between two points.
The second part was kind of messed up and asked for the largest rectangular area within the shape.
How I originally wanted to do it was to visually inspect the coordinates of the points. But that proved to be not feasible because the size of the input data was around 100k x 100k, which would be ~10000000000 bytes -> which is around 10gb worth of data. So I was like, "Maybe I should just record every point that was within the shape, but then I did some napkin math and found out the min and max x and y coordinates of the shape and learned that the largest shape possible was around 8.1gb or around 8 billion numbers.

So my next idea was to outline the shape by recording every point made by every connection. This was easy to do, but then querying what was inside of these points became difficult. So I decided to break the problem up, line by line. So for every line, I would try to figure out what was inside the shape vs. outside the shape. This proved to also be difficult because there were several cases. Like what happens if we have a mixture of the outline of the shape along with single lines, e.g.

```
....XXXXXX....X..X....
```

What I decided to do instead was build the inside of the shape layer by layer.
The initial case is if the range is made up of the outline of the shape. Then afterwards,
we check the posts of each crossing point and see if the range above it was also part of the shape. If so, this range between the posts is also part of the range. Then I merged the ranges in case there was overlap. This let me build up the mapping of the inside of the shape.

Then what I did afterwards was take every two points and compare them (there are only ~500 points, so 250000 pairs). Then check along the y axis and make sure that every row had an inclusive range (within the shape) that covered the distance between the x coordinates of the two points.

Then I added a heuristic where the pair of coordinates had to have an area at least as big as the largest pair we have seen so far. My final runtime was around 150s.

I imagine that there's a way to do this by storing a representation of the shape in 90k rows and checking every possible pair of points. But what that is escapes me at the moment.

Then I read a comment saying that you can compress the shape by mapping the x coordinates to the index of a sorted list of the x coordinates and the same for the y coordinates. The shape looks like a diamond with a part cut out.

Reworked: With reddit comment for coordinate compression + flood fill, we get the solution in a few seconds.

### day 10

Part 1 was easy, just a bfs to find the matching states.

Part 2 made me cry inside. I first tried dijkstra's. Then I tried A* with my heuristic being the cost * the number of layers. Then I looked at reddit and saw linear algebra and Gaussian elimination so I tried doing it with numpy and scipy. But there were free variables so the matrices weren't square/or they were singular and it's been a while and I did not want to deal with it. Then I read about people using z3 to solve it. So praise z3 👀.
