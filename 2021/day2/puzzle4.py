x = 0
y = 0
aim = 0
with open('input3.txt', 'r') as f:
    for line in f:
        d, amt = line.split()
        amt = int(amt)
        if d == 'down':
            aim += amt
        elif d == 'up':
            aim -= amt
        else:
            x += amt
            y += amt * aim
print(x*y)