from math import floor, ceil

sample = False
file = "sample7.txt" if sample else "input7.txt"
with open(file, "r") as f:
    vals = [int(v) for v in f.readline().split(",")]
# These are triangle numbers
# minimize sum(|v_i - x|*(|v_i - x| + 1) for i in range(n))
# minimize sum(|v_i - x|^2 + |v_i - x| for i in range(n))
# minimize sum((v_i - x)^2 + |v_i - x| for i in range(n))

# Then we take the derivative and set it equal to zero.
# 2*(-x)*sum(v_i - x for i in range(n)) + sum(sign(v_i - x) for i in range(n)) = 0
# -2 * x * (sum(v_i for i in range(n)) - n * x) + sum(sign(v_i - x) for i in range(n)) = 0
# -2 * x * sum(v_i for i in range(n)) + 2 * n * x^2 + sum(sign(v_i - x) for i in range(n)) = 0
# 2 * n * x^2 + sum(sign(v_i - x) for i in range(n)) = 2 * x * sum(v_i for i in range(n))
# n * x + sum(sign(v_i - x)) / (2 * x) = sum(v_i for i in range(n))
# x + sum(sign(v_i - x)) / (2 * x * n) = sum(v_i for i in range(n)) / n
# x +/- (1 / (2 * x)) = sum(v_i for i in range(n)) / n
# x +/- ~0 = sum(v_i for i in range(n)) / n
# x ~= sum(v_i for i in range(n)) / n


# Can also binary search for the value
def f(x):
    total = 0
    for v in vals:
        dist = abs(v - x)
        total += dist * (dist + 1) // 2
    return total


mean = sum(vals) / len(vals)
left_x, right_x = floor(mean), ceil(mean)
print(left_x, f(left_x))
print(right_x, f(right_x))

cands = [f(i) for i in range(max(vals))]
ans = min(cands)
print(cands.index(ans), ans)
print(sum(vals) / len(vals))
