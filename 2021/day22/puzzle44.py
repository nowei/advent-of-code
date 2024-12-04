sample = False
file = "sample22-b.txt" if sample else "input22.txt"

# Volume Octrees are too expensive:

# class Octree:

#     def __init__(self, x, y, z, val):
#         self.is_val = True
#         self.val = val
#         self.regions = [x, y, z]
#         self.children = []

#     def __str__(self):
#         return 'Octree(regions={}, is_val={}, val={}, contribution={})'.format(str(self.regions), self.is_val, self.val, self.get_volume())
#     def __repr__(self):
#         return 'Octree(regions={}, is_val={}, val={}, contribution={})'.format(str(self.regions), self.is_val, self.val, self.get_volume())

#     def print_recursive(self, level=0):
#         print('    ' * level, self)
#         for c in self.children:
#             c.print_recursive(level + 1)

#     def check_overlap(self, x, y, z):
#         xr, yr, zr = self.regions
#         if not (xr[0] <= x[0] <= xr[1] or xr[0] <= x[1] <= xr[1]):
#             return False
#         if not (yr[0] <= y[0] <= yr[1] or yr[0] <= y[1] <= yr[1]):
#             return False
#         if not (zr[0] <= z[0] <= zr[1] or zr[0] <= z[1] <= zr[1]):
#             return False

#         return True

#     def clamp_bounds(self, x, y, z):
#         xr, yr, zr = self.regions
#         xmin, xmax = max(xr[0], x[0]), min(xr[1], x[1])
#         ymin, ymax = max(yr[0], y[0]), min(yr[1], y[1])
#         zmin, zmax = max(zr[0], z[0]), min(zr[1], z[1])
#         return [[xmin, xmax], [ymin, ymax], [zmin, zmax]]

#     def set_value(self, val, x, y, z):
#         if self.check_overlap(x, y, z):
#             x, y, z = self.clamp_bounds(x, y, z)
#             if self.is_val:
#                 xr, yr, zr = self.regions
#                 if x[0] == xr[0] and x[1] == xr[1] and y[0] == yr[0] and y[1] == yr[1] and z[0] == zr[0] and z[1] == zr[1]:
#                     self.val = val
#                     return
#                 else:
#                     self.is_val = False
#                     x_new = [xr[0], (xr[1] + xr[0]) // 2, (xr[1] + xr[0]) // 2 + 1, xr[1]]
#                     y_new = [yr[0], (yr[1] + yr[0]) // 2, (yr[1] + yr[0]) // 2 + 1, yr[1]]
#                     z_new = [zr[0], (zr[1] + zr[0]) // 2, (zr[1] + zr[0]) // 2 + 1, zr[1]]
#                     for i in range(0, 3, 2):
#                         for j in range(0, 3, 2):
#                             for k in range(0, 3, 2):
#                                 x_child = [x_new[i], x_new[i + 1]]
#                                 y_child = [y_new[j], y_new[j + 1]]
#                                 z_child = [z_new[k], z_new[k + 1]]
#                                 # print('adding {}..{},{}..{},{}..{}'.format(*x_child, *y_child, *z_child))
#                                 self.children.append(Octree(x_child, y_child, z_child, val=self.val))
#             # print(self)
#             for c in self.children:
#                 c.set_value(val, x, y, z)
#         else:
#             return

#     def get_contribution(self):
#         if self.is_val:
#             if self.val:
#                 x,y,z = self.regions
#                 return max(1, (x[1] - x[0] + 1)) * max(1, (y[1] - y[0] + 1)) * max(1,(z[1] - z[0] + 1))
#             else:
#                 return 0
#         else:
#             return 0

#     def get_volume(self):
#         if self.is_val:
#             if self.val:
#                 x,y,z = self.regions
#                 return max(1, (x[1] - x[0] + 1)) * max(1, (y[1] - y[0] + 1)) * max(1,(z[1] - z[0] + 1))
#             else:
#                 return 0
#         else:
#             curr = 0
#             for c in self.children:
#                 curr += c.get_volume()
#             return curr
# def next_power_of_2(x):
#     return 1 if x == 0 else 2**(x - 1).bit_length()
# best = next_power_of_2(best)
# octree = Octree([-best, best], [-best, best], [-best, best], False)
# turn = 0
# for instruction, x, y, z in boundaries:
#     print(turn, instruction, x, y, z)
#     if instruction == 'on':
#         octree.set_value(1, x, y, z)
#     else:
#         octree.set_value(0, x, y, z)
#     turn += 1
# octree.print_recursive()
# ans = octree.get_volume()


def check_within(x, y, z):
    if x[0] < -50 or x[1] > 50:
        return False
    if y[0] < -50 or y[1] > 50:
        return False
    if z[0] < -50 or z[1] > 50:
        return False
    return True


boundaries = []
# best = 0
with open(file, "r") as f:
    for line in f:
        instruction, coords = line.strip().split(" ")
        x, y, z = coords.split(",")
        x_min, x_max = (int(a) for a in x.split("=")[1].split(".."))
        y_min, y_max = (int(a) for a in y.split("=")[1].split(".."))
        z_min, z_max = (int(a) for a in z.split("=")[1].split(".."))
        x = (x_min, x_max)
        y = (y_min, y_max)
        z = (z_min, z_max)
        # best = max(best, abs(x[0]),abs(x[1]), abs(y[0]), abs(y[1]),abs(z[0]), abs(z[1]))
        boundaries.append([instruction, x, y, z])


class VolumeTracker:
    def __init__(self):
        self.boxes = set()

    def add_box(self, val, x, y, z):
        num_boxes_changed = 0
        to_remove = set()
        intercepted_boxes = self._get_intercepted_boxes(x, y, z)
        if intercepted_boxes:
            for box in intercepted_boxes:
                num_boxes_changed += 1
                new_boxes = self._break_box(box, x, y, z)
                to_remove.add(box)
                for nb in new_boxes:
                    self.boxes.add(nb)
                    num_boxes_changed += 1
                # print('breaking {} into {}'.format(box, new_boxes))
            for box in to_remove:
                self.boxes.remove(box)
        if val:
            self.boxes.add((x, y, z))
            num_boxes_changed += 1

        # print('changed {} boxes'.format(num_boxes_changed))

    def _get_intercepted_boxes(self, x, y, z):
        intercepted_boxes = []
        for box in self.boxes:
            xr, yr, zr = box
            if x[0] > xr[1] or x[1] < xr[0]:
                # print('reject x {} by {} {} {}', box, x, y, z)
                continue
            if y[0] > yr[1] or y[1] < yr[0]:
                # print('reject y {} by {} {} {}', box, x, y, z)
                continue
            if z[0] > zr[1] or z[1] < zr[0]:
                # print('reject z {} by {} {} {}', box, x, y, z)
                continue
            intercepted_boxes.append(box)
        return intercepted_boxes

    def _break_box(self, box, x, y, z):
        new_boxes = []
        # break into separate box for each direction and corner/sides
        above = self._break_above(box, x, y, z)
        bottom = self._break_bottom(box, x, y, z)
        front = self._break_front(box, x, y, z)
        back = self._break_back(box, x, y, z)
        left = self._break_left(box, x, y, z)
        right = self._break_right(box, x, y, z)
        if above:
            new_boxes.append(above)
        if bottom:
            new_boxes.append(bottom)
        if front:
            new_boxes.append(front)
        if back:
            new_boxes.append(back)
        if left:
            new_boxes.append(left)
        if right:
            new_boxes.append(right)
        return new_boxes

    def _break_above(self, box, x, y, z):
        xr, yr, zr = box
        if zr[1] <= z[1]:
            return None
        cand = (xr, yr, (z[1] + 1, zr[1]))
        # print('above', cand)
        return cand

    def _break_bottom(self, box, x, y, z):
        xr, yr, zr = box
        if z[0] <= zr[0]:
            return None
        cand = (xr, yr, (zr[0], z[0] - 1))
        # print('bottom', cand)
        return cand

    def _break_front(self, box, x, y, z):
        xr, yr, zr = box
        if xr[1] <= x[1]:
            return None
        nz = (max(z[0], zr[0]), min(z[1], zr[1]))
        cand = ((x[1] + 1, xr[1]), yr, nz)
        # print('front', cand)
        return cand

    def _break_back(self, box, x, y, z):
        xr, yr, zr = box
        if x[0] <= xr[0]:
            return None
        nz = (max(z[0], zr[0]), min(z[1], zr[1]))
        cand = ((xr[0], x[0] - 1), yr, nz)
        # print('back', cand)
        return cand

    def _break_right(self, box, x, y, z):
        xr, yr, zr = box
        if yr[1] <= y[1]:
            return None
        nz = (max(z[0], zr[0]), min(z[1], zr[1]))
        nx = (max(x[0], xr[0]), min(x[1], xr[1]))
        cand = (nx, (y[1] + 1, yr[1]), nz)
        # print('right', cand)
        return cand

    def _break_left(self, box, x, y, z):
        xr, yr, zr = box
        if y[0] <= yr[0]:
            return None
        nz = (max(z[0], zr[0]), min(z[1], zr[1]))
        nx = (max(x[0], xr[0]), min(x[1], xr[1]))
        cand = (nx, (yr[0], y[0] - 1), nz)
        # print('left', cand)
        return cand

    def get_volume(self):
        total = 0
        for box in self.boxes:
            x, y, z = box
            total += (x[1] - x[0] + 1) * (y[1] - y[0] + 1) * (z[1] - z[0] + 1)
        return total

    def get_cubes(self):
        cubes = set()
        for box in self.boxes:
            x, y, z = box
            for i in range(x[0], x[1] + 1):
                for j in range(y[0], y[1] + 1):
                    for k in range(z[0], z[1] + 1):
                        cubes.add((i, j, k))
        return cubes


cubes = set()

vt = VolumeTracker()

turn = 0
for instruction, x, y, z in boundaries:
    # cand = set((i, j, k) for i in range(x[0], x[1] + 1) for j in range(y[0], y[1] + 1) for k in range(z[0], z[1] + 1))
    # if instruction == 'on':
    #     cubes |= cand
    # else:
    #     cubes -= cand
    print(turn, instruction, x, y, z)
    val = 1 if instruction == "on" else 0
    vt.add_box(val, x, y, z)
    print("volume={}".format(vt.get_volume()))
    # print('cube_volume={}'.format(len(cubes)))
    turn += 1

# print(vt.get_cubes() - cubes)


ans = vt.get_volume()
# print(len(cubes), ans)

print(ans)
if sample:
    assert ans == 2758514936282235
