sample = False
file = "sample18.txt" if sample else "input18.txt"
problems = [[]]
with open(file, "r") as f:
    for line in f:
        if not line.strip():
            problems.append([])
        else:
            problems[-1].append(eval(line))


def snail_add(a, b):
    return snail_reduce([a, b])


class NestedIterator:
    def __init__(self, p):
        self.curr_inds = [-1]
        self.p = p

    def next(self):
        while self.curr_inds and self.curr_inds[-1] == 1:
            self.curr_inds.pop()
        if not self.curr_inds:
            return None
        self.curr_inds[-1] += 1
        curr = self.p
        for i in self.curr_inds:
            curr = curr[i]
        while type(curr) == list:
            self.curr_inds.append(0)
            if len(self.curr_inds) != 5:
                curr = curr[0]
            else:
                self.curr_inds.pop()
                break
        return curr, list(self.curr_inds)


def explode_nested(p):
    ni = NestedIterator(p)
    prev, curr, next_v = None, ni.next(), ni.next()
    changed = False
    while next_v != None:
        if type(curr[0]) == list:
            # want to explode
            # if prev on the same level as curr, then we must distribute and add a 0 (right)
            # if next on the same level as curr, we must distribute and add a 0 (left)

            c = p
            for i in curr[1][:-1]:
                c = c[i]
            left, right = c[curr[1][-1]]
            if curr[1][-1] == 1:  # expand right ...[a, [b, c]]...
                c = p
                for i in prev[1][:-1]:
                    c = c[i]
                c[0] += left
                c[1] = 0
                c = p
                for i in next_v[1][:-1]:
                    c = c[i]
                if type(c[next_v[1][-1]]) == list:
                    c[next_v[1][-1]][0] += right
                else:
                    c[next_v[1][-1]] += right
            else:  # expand left ...[[a, b], c]...
                if prev:
                    c = p
                    for i in prev[1][:-1]:
                        c = c[i]
                    if type(c[prev[1][-1]]) == list:
                        c[prev[1][-1]][1] += left
                    else:
                        c[prev[1][-1]] += left
                c = p
                for i in next_v[1][:-1]:
                    c = c[i]
                if type(c[next_v[1][-1]]) == list:
                    c[next_v[1][-1]][0] += right
                else:
                    c[next_v[1][-1]] += right
                c[0] = 0
            changed = True
            break

        prev = curr
        curr = next_v
        next_v = ni.next()
    if not changed and type(curr[0]) == list:
        c = p
        for i in curr[1][:-1]:
            c = c[i]
        left, right = c.pop(1)

        c = p
        for i in prev[1][:-1]:
            c = c[i]
        c[0] += left
        c.append(0)
        changed = True
    return changed


def split_greater(p):
    ni = NestedIterator(p)
    curr = ni.next()
    changed = False
    # At this point there's no numbers that need to be exploded
    while curr and curr[0] < 10:
        curr = ni.next()
    if curr and curr[0] >= 10:
        left = curr[0] // 2
        right = curr[0] // 2 + 1 if curr[0] % 2 else left
        c = p
        for i in curr[1][:-1]:
            c = c[i]
        c[curr[1][-1]] = [left, right]
        changed = True
    return changed


def snail_reduce(p):
    changed = True
    while changed:
        changed = False
        changed = explode_nested(p)
        if changed:
            continue
        changed = split_greater(p)
    return p


def snail_process(problems):
    curr = problems[0]
    for p in problems[1:]:
        curr = snail_add(curr, p)
    return curr


def mag(a):
    left, right = a
    total = 0
    total += 3 * (mag(left) if type(left) == list else left)
    total += 2 * (mag(right) if type(right) == list else right)
    return total


import copy


def get_best_mag(problem):
    best = 0
    for i in range(len(problem)):
        for j in range(i + 1, len(problem)):
            a, b = copy.deepcopy(problem[i]), copy.deepcopy(problem[j])
            curr = mag(snail_add(a, b))
            if curr > best:
                best = curr
                print(problem[i], problem[j], best)
            b, a = copy.deepcopy(problem[i]), copy.deepcopy(problem[j])
            curr = mag(snail_add(a, b))
            if curr > best:
                best = curr
                print(problem[i], problem[j], best)
    return best


problem = problems[-1]
ans = get_best_mag(problem)
print(ans)
if sample:
    assert ans == 3993
