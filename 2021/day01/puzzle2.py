arr = []
with open("input1.txt", "r") as f:
    for line in f:
        arr.append(int(line))

bigger_than_prev = 0
curr = sum(arr[0:3])
prev = curr
for i in range(3, len(arr)):
    curr = curr - arr[i - 3] + arr[i]
    if curr > prev:
        bigger_than_prev += 1
    prev = curr

print(
    "{} measurements were larger than the previous measurement".format(bigger_than_prev)
)
