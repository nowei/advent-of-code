mapping = [{"0": 0, "1": 0} for _ in range(12)]
with open("input5.txt", "r") as f:
    for line in f:
        for i in range(12):
            mapping[i][line[i]] += 1
best = ["1" if mapping[i]["1"] > mapping[i]["0"] else "0" for i in range(12)]
gamma = "".join(best)
epsilon = "".join(["1" if c == "0" else "0" for c in gamma])
gamma = int(gamma, 2)
epsilon = int(epsilon, 2)
print("gamma = {}, epsilon = {}".format(gamma, epsilon))
print("power consumption = {}".format(gamma * epsilon))
