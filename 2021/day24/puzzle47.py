sample = True
file = "sample24.txt" if sample else "input24.txt"
operations = []
with open(file, "r") as f:
    for line in f:
        operations.append(line.strip().split())


def code_gen(operations):
    mapping = {"x": "0", "y": "0", "z": "0", "w": "0"}
    num = {"x": 0, "y": 0, "z": 0, "w": 0}
    vals = {"x0": 0, "y0": 0, "z0": 0, "w0": 0}
    with open("output24.txt", "w") as f:
        for args in operations:
            op = args[0]
            line = " ".join(args).ljust(12)
            if op == "inp":
                a = args[1]
                mapping[a] = a + str(num[a] + 1)
                line += "{}={}".format(a, mapping[a])
            else:
                a = args[1] + str(num[args[1]])
                b = (
                    str(args[2])
                    if (
                        args[2].isnumeric()
                        or (args[2][0] == "-" and args[2][1:].isnumeric())
                    )
                    else args[2] + str(num[args[2]])
                )
                if op == "add":
                    result = "({}+{})".format(a, b)
                elif op == "mul":
                    if b.isnumeric() and int(b) == 0:
                        result = "0"
                    else:
                        result = "({}*{})".format(a, b)
                elif op == "div":
                    result = "({}//{})".format(a, b)
                elif op == "mod":
                    result = "({}%{})".format(a, b)
                elif op == "eql":
                    result = "({}=={}?1:0)".format(a, b)
                else:
                    print("shouldn't happen")
                try:
                    vals[args[1] + str(num[args[1]] + 1)] = eval(result, vals)
                    print(
                        args[1] + str(num[args[1]] + 1),
                        vals[args[1] + str(num[args[1]] + 1)],
                    )
                    mapping[args[1]] = str(vals[args[1] + str(num[args[1]] + 1)])
                except Exception as e:
                    print(e)
                    mapping[args[1]] = result
                line += (
                    "{}=".format(args[1] + str(num[args[1]] + 1)) + mapping[args[1]]
                ).ljust(20)
            num[args[1]] += 1
            f.write(line + "\n")


# code_gen(operations)

# Some conditions
# cond61 = w3+4 == w4
# cond115 = w6-3 == w7
# cond151 = w8+6 == w9
# cond187 = w10 == w11
# cond205 = (w11+6==w12) or (w7+3==w12) or (w5+1==w12)


def process_op(args, inputs, mapping, num):
    op = args[0]
    line = " ".join(args).ljust(12)
    if op == "inp":
        a = args[1]
        mapping[a] = int(inputs.pop())
        line += "{} = {}".format((a + str(num[a] + 1)).ljust(4), mapping[a]).ljust(12)
    else:
        a = mapping[args[1]]
        b = (
            int(args[2])
            if (args[2].isnumeric() or (args[2][0] == "-" and args[2][1:].isnumeric()))
            else mapping[args[2]]
        )
        label_a = args[1] + str(num[args[1]])
        label_b = (
            str(args[2])
            if (args[2].isnumeric() or (args[2][0] == "-" and args[2][1:].isnumeric()))
            else args[2] + str(num[args[2]])
        )
        if op == "add":
            result = a + b
            line += "{} = {} + {} = {} + {} = {}".format(
                (args[1] + str(num[args[1]] + 1)).ljust(4),
                label_a.rjust(5),
                label_b.ljust(6),
                str(a).rjust(7),
                str(b).ljust(6),
                result,
            ).ljust(12)
        elif op == "mul":
            result = a * b
            line += "{} = {} * {} = {} * {} = {}".format(
                (args[1] + str(num[args[1]] + 1)).ljust(4),
                label_a.rjust(5),
                label_b.ljust(6),
                str(a).rjust(7),
                str(b).ljust(6),
                result,
            ).ljust(12)
        elif op == "div":
            result = a // b
            line += "{} = {} // {} = {} // {} = {}".format(
                (args[1] + str(num[args[1]] + 1)).ljust(4),
                label_a.rjust(5),
                label_b.ljust(5),
                str(a).rjust(7),
                str(b).ljust(5),
                result,
            ).ljust(12)
        elif op == "mod":
            result = a % b
            line += "{} = {} % {} = {} % {} = {}".format(
                (args[1] + str(num[args[1]] + 1)).ljust(4),
                label_a.rjust(5),
                label_b.ljust(6),
                str(a).rjust(7),
                str(b).ljust(6),
                result,
            ).ljust(12)
        elif op == "eql":
            result = 1 if a == b else 0
            line += "{} = {} == {} = {} == {} = {} -------------------".format(
                (args[1] + str(num[args[1]] + 1)).ljust(4),
                label_a.rjust(5),
                label_b.ljust(5),
                str(a).rjust(7),
                str(b).ljust(5),
                result,
            ).ljust(12)
        else:
            print("shouldn't happen")
        mapping[args[1]] = result
    num[args[1]] += 1
    print(line)


def process(operations, inputs):
    mapping = {"x": 0, "y": 0, "z": 0, "w": 0}
    num = {"x": 0, "y": 0, "z": 0, "w": 0}
    for op in operations:
        process_op(op, inputs, mapping, num)
    print(mapping["z"])
    if mapping["z"] == 0:
        return True
    else:
        return False


curr = 99598963999971
print(curr)
cand = list(str(curr))[::-1]
if process(operations, cand):
    print("nani")
ans = curr
print(ans)
