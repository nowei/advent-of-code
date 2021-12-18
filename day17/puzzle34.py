sample = False
file = "sample17.txt" if sample else "input17.txt"
with open(file, "r") as f:
    _, _, x_range, y_range = f.readline().strip().split()
    x_target = [int(x) for x in x_range.strip(',').split('=')[1].split('..')]
    y_target = [int(y) for y in y_range.split('=')[1].split('..')]

# idea: Double binary search 
# x-value doesn't matter as long as v_x goes to 0. 
# if we miss from top going down, should we increase or decrease the y-velocity?
# Binary search on y and x??? 
# if undershot (doesn't reach range of x_target), increase x
# if overshot (over range of x_target), decrease x
# if increase and decrease to same amount, give up and try new y because it won't work
# if undershot, increase y
# if overshot, decrease y 

# check to see if possible to to reach x from these positions
possible_v_x = set()
for v_x in range(1, x_target[1] + 1):
    x = 0
    v_init = v_x
    while x < x_target[1] and v_x > 0:
        x += v_x 
        v_x -= 1
        if x_target[0] <= x <= x_target[1]:
            possible_v_x.add(v_init)
print(possible_v_x)

# Highest is sum from 1 to v_y.
# Whether it hits the box depends on whether 
# v_x can get to target and sum from -v_y can get to end
# if v_y greater than abs(y_target[0]), then it's possible to just skip over it

counts = 0
for v_x in possible_v_x:
    for v_y in range(y_target[0], abs(y_target[0]) + 1):
        v_x_i = v_x
        v_y_i = v_y
        x = 0
        y = 0
        seen = False
        while x <= x_target[1] and y >= y_target[0]:
            x += v_x_i
            y += v_y_i
            # if v_x == 6 and v_y == 0:
                # print('what', x, y)
            if x_target[0] <= x <= x_target[1] and y_target[0] <= y <= y_target[1]:
                # print(v_x, v_y)
                seen = True
            if abs(v_x_i) > 0:
                if v_x_i > 0:
                    v_x_i -= 1
                elif v_x_i < 0:
                    v_x_i += 1
            v_y_i -= 1
        if seen:
            counts += 1
ans = counts

print(ans)
if sample:
    assert(ans == 112)