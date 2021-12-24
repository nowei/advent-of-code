# advent-of-code-2021

Answers written in Python3. Usually answers are what comes 
to mind first. If it doesn't work, then something else is tried.
All solutions are best-effort-with-reasonable-attempts.

## short summaries (some spoilers)
day 01 - num increasing / sliding window sum increasing; just a sliding window
day 02 - follow directions / follow directions with scaled up/down movement; just apply the rules
day 03 - most/least common bit / elimination most/least common bits; iterative processing
day 04 - simulation win first / simulation win last; played it out in simulation
day 05 - intersections / intersections with diagonals; simulation
day 06 - brute force list / dp/cohort counting; exponential growth -> dp
day 07 - calculus with median / calculus with mean; math, brute force, math, then brute force again
day 08 - counting unique / elimination rules; process of elimination 
day 09 - sum lowest points / multiply area of lowest basins; just a connected area search
day 10 - detect illegal patterns / score of completing incomplete patterns; iteratively parsing / stack
day 11 - flash together in rounds / all flash together; simulation gang
day 12 - path finding (can't visit small >1 times) / path finding (can visit single small twice, all other small once); DFS with hard-coded rules
day 13 - folding paper once / folding paper multiple times and printing text; used sets
day 14 - brute force evolution / cohort evolution counting; basically dp
day 15 - minimum path / minimum path in repeated squares w/ change; repeated same square but kept track of land offset
day 16 - bit manipulation/extraction / evaluate expressions expressed with bits; iterative development
day 17 - step-wise physics sim / iterate through step-wise physics sim; brute force
day 18 - Nested list parsing and applying rules for eval / best pair and order; iteration and depth
day 19 - beacon reconstruction / manhattan distance between scanners; brute force and resolve at each step
day 20 - bit convolution w/ infinite image / more of the same; brute force
day 21 - deterministic dice rolls / quantum dice splitting results; dp
day 22 - carving spaces in a small, bounded cube / carving space in unbounded volume; ended up splitting each intersected box
day 23 - best way to place 8 people in 4 rooms / best way to place 16 people in 4 rooms; ended up using A*
day 24 - Feels like debugging assembly / Feels like debugging assembly part 2; Just try to zero things out
day 25 - 


## Interesting problems (some spoilers)
12 - it's a twist on normal pathfinding
14 - needs to keep track of counts in a cool way
18 - parsing nested lists is kind of tedious, but applying rules and seeing results is cool
19 - directions are hard, even if limited to 3d and at 90 degree angles
21 - Exponential combinations so using memory to store results, basically dp (tabulation) and expressing the state space, but there's a lot of state so it should be done carefully. Just keeps branching and adding on each step. 
22 - How do we keep track of space and what is the best way to split and keep track of split space? I just ended up splitting up intersected boxes by splitting top and bottom, then front and back, then left and right. - Something to keep in mind: If processing from reverse, if it's on, it'll always stay on. If it's off, then it will always stay off. So we only need to consider new volumes that haven't been carved out yet.  
23 - Basically a search problem if you don't know what you're doing (me). I ended up doing an A* search with a heuristic being the cost to get out + cost to move to the right place + cost to get in. Runtime was a bit bad, but it worked.
24 - It's easy to see that it performs operations. It's harder to trace what the operations actually do. Some conditions are impossible to fulfill, so we just have to let them happen. Always starting from 9s or 1s is a good idea. The trace becomes easier to debug after looking through it for a while.Smart way is to think of \*26 and /26 as pushing and popping and abstracting the parts between the equals checks. Stack should be empty by the end. Brute force after analysis is fine, but after the analysis it becomes arithmetic. 