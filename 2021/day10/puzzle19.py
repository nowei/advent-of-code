sample = False
file = "sample10.txt" if sample else "input10.txt"
invalids = {")": 0, "]": 0, "}": 0, ">": 0}
scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
with open(file, "r") as f:
    for line in f:
        s = []
        broken = False
        for c in line.strip():
            if c in {"(", "[", "{", "<"}:
                s.append(c)
            else:
                if c == ")" and s[-1] != "(":
                    broken = True
                    break
                if c == "}" and s[-1] != "{":
                    broken = True
                    break
                if c == "]" and s[-1] != "[":
                    broken = True
                    break
                if c == ">" and s[-1] != "<":
                    broken = True
                    break

                s.pop()
        if broken:
            invalids[c] += 1
total = 0
for k in invalids:
    total += invalids[k] * scores[k]
print(total)
