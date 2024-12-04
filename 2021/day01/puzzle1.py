arr = []
with open("input1.txt", "r") as f:
    for line in f:
        arr.append(int(line))

bigger_than_prev = 0
for i in range(1, len(arr)):
    if arr[i - 1] < arr[i]:
        bigger_than_prev += 1

print(
    "{} measurements were larger than the previous measurement".format(bigger_than_prev)
)
