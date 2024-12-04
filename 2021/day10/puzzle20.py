sample = True
file = "sample10.txt" if sample else "input10.txt"
valids = []
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
        if not broken:
            valids.append(s)
scores = []
for s in valids:
    curr = 0
    for c in s[::-1]:
        v = 0
        if c == "(":
            v = 1
        elif c == "[":
            v = 2
        elif c == "{":
            v = 3
        elif c == "<":
            v = 4

        curr *= 5
        curr += v
    scores.append(curr)

scores = sorted(scores)
print(scores[len(scores) // 2])
