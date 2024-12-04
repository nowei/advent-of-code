x = 0
y = 0
with open("input3.txt", "r") as f:
    for line in f:
        d, amt = line.split()
        amt = int(amt)
        if d == "down":
            y += amt
        elif d == "up":
            y -= amt
        else:
            x += amt
print(x * y)
