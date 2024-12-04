sample = False
file = "sample22.txt" if sample else "input22.txt"


def check_within(x, y, z):
    if x[0] < -50 or x[1] > 50:
        return False
    if y[0] < -50 or y[1] > 50:
        return False
    if z[0] < -50 or z[1] > 50:
        return False
    return True


boundaries = []
with open(file, "r") as f:
    for line in f:
        instruction, coords = line.strip().split(" ")
        x, y, z = coords.split(",")
        x_min, x_max = (int(a) for a in x.split("=")[1].split(".."))
        y_min, y_max = (int(a) for a in y.split("=")[1].split(".."))
        z_min, z_max = (int(a) for a in z.split("=")[1].split(".."))
        x = [x_min, x_max]
        y = [y_min, y_max]
        z = [z_min, z_max]
        if check_within(x, y, z):
            boundaries.append([instruction, x, y, z])
cubes = set()
for instruction, x, y, z in boundaries:
    cand = set(
        (i, j, k)
        for i in range(x[0], x[1] + 1)
        for j in range(y[0], y[1] + 1)
        for k in range(z[0], z[1] + 1)
    )
    if instruction == "on":
        cubes |= cand
    else:
        cubes -= cand
ans = len(cubes)
print(ans)
if sample:
    assert ans == 590784
