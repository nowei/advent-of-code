from math import floor, ceil

sample = False
file = "sample7.txt" if sample else "input7.txt"
with open(file, "r") as f:
    vals = [int(v) for v in f.readline().split(",")]
# minimize sum(|v_i-x| for i in range(n))
# derivative is sum(sign(v_i - x) for i in range(n))
# this means it is the median because it is only equal to
# zero when there's an equal number of pos and neg (v_i - x)
# minimize by walking from very left value and going to the right, epsilon distance each time and
# computing the gain along each step compared to loss due to being further away from things you've seen
# Also see: https://math.stackexchange.com/questions/113270/the-median-minimizes-the-sum-of-absolute-deviations-the-ell-1-norm
sorted_vals = sorted(vals)
ind = len(vals) / 2
print(sorted_vals, ind)
left_ind = floor(ind)
right_ind = ceil(ind)


# total = sum(vals)
def f(x):
    return sum(abs(v_i - x) for v_i in vals)


print(left_ind, right_ind)
left_x = sorted_vals[left_ind]
right_x = sorted_vals[right_ind]
left_y = f(left_x)
right_y = f(right_x)
print(left_x, left_y)
print(right_x, right_y)
