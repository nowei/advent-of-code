sample = False
file = "sample9.txt" if sample else "input9.txt"
area = []
with open(file, "r") as f:
    for line in f:
        area.append([int(v) for v in line.strip()])
risk_areas = []
# corners
if area[0][0] < area[0][1] and area[0][0] < area[1][0]:
    risk_areas.append(area[0][0])
if area[-1][-1] < area[-1][-2] and area[-1][-1] < area[-2][-1]:
    risk_areas.append(area[-1][-1])
if area[-1][0] < area[-1][1] and area[-1][0] < area[-2][0]:
    risk_areas.append(area[-1][0])
if area[0][-1] < area[1][-1] and area[0][-1] < area[0][-2]:
    risk_areas.append(area[0][-1])

# edges
# cols
for j in range(1, len(area[0]) - 1):
    if (
        area[0][j] < area[0][j - 1]
        and area[0][j] < area[0][j + 1]
        and area[0][j] < area[1][j]
    ):
        risk_areas.append(area[0][j])
    if (
        area[-1][j] < area[-1][j - 1]
        and area[-1][j] < area[-1][j + 1]
        and area[-1][j] < area[-2][j]
    ):
        risk_areas.append(area[-1][j])
# row
for i in range(1, len(area) - 1):
    if (
        area[i][0] < area[i - 1][0]
        and area[i][0] < area[i + 1][0]
        and area[i][0] < area[i][1]
    ):
        risk_areas.append(area[i][0])
    if (
        area[i][-1] < area[i - 1][-1]
        and area[i][-1] < area[i + 1][-1]
        and area[i][-1] < area[i][-2]
    ):
        risk_areas.append(area[i][-1])

# middle
for i in range(1, len(area) - 1):
    for j in range(1, len(area[0]) - 1):
        if (
            area[i][j] < area[i - 1][j]
            and area[i][j] < area[i + 1][j]
            and area[i][j] < area[i][j - 1]
            and area[i][j] < area[i][j + 1]
        ):
            risk_areas.append(area[i][j])

# total
cost = 0
for v in risk_areas:
    cost += v + 1

print(cost)
