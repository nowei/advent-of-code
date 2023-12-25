from typing import Any, Optional, List, Tuple, Dict
import argparse
import math

sample_file_path = "test/24.sample"
input_file_path = "test/24.input"

class Hailstone24:
    x: int
    y: int
    z: int
    dx: int
    dy: int
    dz: int

    def __init__(self, x, y, z, dx, dy, dz):
        self.x = x
        self.y = y
        self.z = z
        self.dx = dx
        self.dy = dy
        self.dz = dz
    
    def __repr__(self):
        return f"stone(({self.x}, {self.y}, {self.z}), ({self.dx}, {self.dy}, {self.dz}))"

    def check_parallel_prop(self, other, xy=False) -> Optional[Tuple[int, int]]:
        # factor is the rate at which things are parallel
        if xy:
            self_gcd = math.gcd(self.dx, self.dy)
            self_dx, self_dy = self.dx / self_gcd, self.dy / self_gcd
            other_gcd = math.gcd(other.dx, other.dy)
            other_dx, other_dy = other.dx / other_gcd, other.dy / other_gcd
            if self_dx == other_dx and self_dy == other_dy or (-self_dx == other_dx and -self_dy == other_dy):
                return (self_gcd, other_gcd)
        else:
            self_gcd = math.gcd(math.gcd(self.dx, self.dy), self.dz)
            self_dx, self_dy, self_dz = self.dx / self_gcd, self.dy / self_gcd, self.dz / self_gcd
            other_gcd = math.gcd(math.gcd(other.dx, other.dy), other.dz)
            other_dx, other_dy, other_dz = other.dx / other_gcd, other.dy / other_gcd, other.dz / other_gcd
            if (self_dx == other_dx and self_dy == other_dy and self_dz == other_dz) or (-self_dx == other_dx and -self_dy == other_dy and -self_dz == other_dz):
                return (self_gcd, other_gcd)
        return None

    def intersects(self, other: "Hailstone24", xy=False) -> Optional[List[int]]:
        res = None
        if xy:
            if self.check_parallel_prop(other, xy=True):
                return None
            # get to y=mx+b form from (x, y), (dx, dy)
            # m = dy / dx
            # b = y - (x * m)
            # y = m1x + b1
            # y = m2x + b2
            # m1x + b1 = m2x + b2
            # m2x - m1x = b1 - b2
            # x(m2 - m1) = b1 - b2
            # x = (b1 - b2) / (m2 - m1)
            m1 = self.dy / self.dx
            dt1 = self.x / self.dx
            b1 = self.y - self.x * m1
            m2 = other.dy / other.dx
            dt2 = other.x / other.dx
            b2 = other.y - other.x * m2
            x = (b1 - b2) / (m2 - m1)
            res_x = x
            res_y = x * m1 + b1
            # check if in the past for either stone
            # a stone is in the past if the change (m) is positive and 
            # the result is after the current position
            if res_x / self.dx < dt1:
                return None
            if res_x / other.dx < dt2:
                return None
            res = (res_x, res_y)
        else:
            if self.dx == other.dx and self.dy == other.dy and self.dz == other.dz: 
                return None
        return res

    def dist(self, other):
        return (abs(self.x - other.x) ** 2 + abs(self.y - other.y) ** 2 + abs(self.z - other.z) ** 2) ** 0.5

class Setting24:

    stones: List[Hailstone24]

    def __init__(self, stones):
        self.stones = stones
    
    def dist(self):
        total = 0
        for i in range(len(self.stones) - 1):
            curr = []
            for j in range(i + 1, len(self.stones)):
                curr.append(self.stones[i].dist(self.stones[j]))
            total += min(curr)
        return total

    def step(self) -> "Setting24":
        new_stones = []
        for stone in self.stones:
            new_stones.append(Hailstone24(stone.x + stone.dx, stone.y + stone.dy, stone.z + stone.dz, stone.dx, stone.dy, stone.dz))
        return Setting24(new_stones)

    def get_perfect_stone(self) -> Hailstone24:
        # We have stones with equation
        # (x+dx*t, y+dy*t, z+dz*t), such that we have
        # (x1+dx1*t1, y1+dy1+t1, z1+dz1*t1) - (x_s+dx_s*t1, y_s+dy_s*t1, z_s+dz_s*t1) = (0, 0, 0)
        # With equations
        # p1 + v1 * t1 = ps + vs * t1 # 6 known, 7 unknowns
        # p2 + v2 * t2 = ps + vs * t2 # 12 known, 8 unknowns
        # ...
        # pn + vn * tn = ps + vs * tn # 6n known, 6+n unknowns
        # 
        # []
        # 
        # p + v * t = ps + vs * t
        # p - ps = (vs - v) * t
        # (p - ps) / (vs - v) = t
        # (x - xs) / (dxs - dx) = t
        # (y - ys) / (dys - dy) = t
        # (x - xs) / (dxs - dx) = (y - ys) / (dys - dy)
        # (x - xs) * (dys - dy) = (y - ys) * (dxs - dx)
        # x * (dys - dy) - xs * (dys - dy) = y * (dxs - dx) - ys * (dxs - dx)
        # x * (dys - dy) + ys * (dxs - dx) = y * (dxs - dx) + xs * (dys - dy)
        # x*dys - x*dy + ys*dxs - ys*dx = y*dxs - y*dx + xs * dys - xs * dy
        # ys*dxs - xs*dys = y*dxs - y*dx - xs * dy - x*dys + x*dy + ys*dx
        #                 = x*dy - y*dx + ys*dx - xs * dy + y*dxs - x*dys
        # x*dy - y*dx + ys*dx - xs * dy + y*dxs - x*dys = x'*dy' - y'*dx' + ys*dx' - xs * dy' + y'*dxs - x'*dys
        # dys * (x' - x) + dxs * (y - y') + ys * (dx - dx') + xs * (dy' - dy) = x'*dy' - y' * dx' + y*dx - x*dy
        # xs * (dy' - dy) + ys * (dx - dx') + dxs * (y - y') + dys * (x' - x) = x'*dy' - y' * dx' + y*dx - x*dy
        # ys * (dz - dz') + zs * (dy' - dy) + dys * (z' - z) + dzs * (y - y') = z'*dy' - y' * dz' + y*dx - z*dy
        # xs * (dz - dz') + zs * (dx' - dx) + dxs * (z' - z) + dzs * (x - x') = z'*dx' - x' * dz' + x*dx - z*dx
        # Then we can do this again with y,z and x,z pairs. So we have 6 unknowns and 3 equations, but we can
        # do this again with p'', so we can get 6 equations with 6 unknowns and solve.
        import numpy as np 
        # order of matrix is x, y, z, dx, dy, dz
        p0 = self.stones[0]
        p1 = self.stones[1]
        p2 = self.stones[2]
        A = np.matrix([[p1.dy - p0.dy, p0.dx - p1.dx, 0, p0.y - p1.y, p1.x - p0.x, 0], 
                        [0, p0.dz - p1.dz, p1.dy - p0.dy, 0, p1.z - p0.z, p0.y - p1.y], 
                        [p0.dz - p1.dz, 0, p1.dx - p0.dx, p1.z - p0.z, 0, p0.x - p1.x],
                        [p2.dy - p0.dy, p0.dx - p2.dx, 0, p0.y - p2.y, p2.x - p0.x, 0], 
                        [0, p0.dz - p2.dz, p2.dy - p0.dy, 0, p2.z - p0.z, p0.y - p2.y], 
                        [p0.dz - p2.dz, 0, p2.dx - p0.dx, p2.z - p0.z, 0, p0.x - p2.x], ])
        y = np.matrix([p1.x * p1.dy - p1.y * p1.dx + p0.y * p0.dx - p0.x * p0.dy,
                       p1.z * p1.dy - p1.y * p1.dz + p0.y * p0.dz - p0.z * p0.dy,
                       p1.z * p1.dx - p1.x * p1.dz + p0.x * p0.dz - p0.z * p0.dx,
                       p2.x * p2.dy - p2.y * p2.dx + p0.y * p0.dx - p0.x * p0.dy,
                       p2.z * p2.dy - p2.y * p2.dz + p0.y * p0.dz - p0.z * p0.dy,
                       p2.z * p2.dx - p2.x * p2.dz + p0.x * p0.dz - p0.z * p0.dx,]).T
        x = np.asarray(np.linalg.solve(A, y)).squeeze()


        # Alternatively
        # (x - xs) / (dxs - dx) = t = (x' - xs) / (dxs - dx')
        # (x - xs) * (dxs - dx') = (x' - xs) * (dxs - dx)
        # x * dxs - x * dx' - xs * dxs + xs * dx' = x' * dxs - x' * dx - xs * dxs + xs * dx
        # xs * (dx - dx') + dxs * (x - x') = x * dx' - x' * dx
        
        return Hailstone24(x[0], x[1], x[2], x[3], x[4], x[5])

def parse_file_day24(file_path, example: str = "") -> Any:
    if example:
        lines = [example]
    else:
        with open(file_path, "r") as f:
            lines = f.readlines()
    hailstones = []
    for line in lines:
        curr = line.strip()
        pos, vel = curr.split(" @ ")
        x, y, z = [int(v) for v in pos.split(", ")]
        dx, dy, dz = [int(v) for v in vel.split(", ")]
        hailstones.append(Hailstone24(x,y,z,dx,dy,dz))
    return Setting24(hailstones)

def solve_day24_part1(input: Setting24, range_min, range_max) -> int:
    matches = 0
    for i in range(len(input.stones) - 1):
        hailstone_a = input.stones[i]
        for j in range(i + 1, len(input.stones)):
            hailstone_b = input.stones[j]
            intersect = hailstone_a.intersects(hailstone_b, xy=True)
            if intersect and all([range_min <= v and v <= range_max for v in intersect]):
                matches += 1
    return matches

def solve_day24_part2(input: Setting24) -> int:
    rock = input.get_perfect_stone()
    return rock.x + rock.y + rock.z

def solve_day24(input: Setting24, expected_pt1: Optional[int] = None, expected_pt2: Optional[int] = None):
    if expected_pt1:
        range_min = 7
        range_max = 27
    else:
        range_min = 200000000000000
        range_max = 400000000000000
    out_part1 = solve_day24_part1(input, range_min, range_max)

    if expected_pt1 is not None:
        if out_part1 != expected_pt1:
            print("Sample results do not match")
            print("Sample expected:")
            print(expected_pt1)
        else:
            print("Sample matched")
    print("Part 1 result:")
    print(out_part1)
    print()

    out_part2 = solve_day24_part2(input)
    if expected_pt2 is not None:
        if out_part2 != expected_pt2:
            print("Sample results do not match")
            print("Sample expected:")
            print(expected_pt2)
        else:
            print("Sample matched")
    print("Part 2 result:")
    print(out_part2)
    print()

def main_24(run_all: bool = False, example: Optional[str] = None, answer_only: bool = False):
    if not answer_only:
        if example:
            print("Testing input from cmd line")
            input = parse_file_day24("", example=example)
            solve_day24(input)
            exit(0)

        print("Running script for day 24")
        print("Sample input")
        print("---------------------------------")
        expected_out_part1 = 2
        expected_out_part2 = 47
        print("Input file:", sample_file_path)
        input = parse_file_day24(sample_file_path)
        solve_day24(input, expected_pt1=expected_out_part1, expected_pt2=expected_out_part2)

    if run_all:
        print("---------------------------------")
        print("Actual input")
        print("Input file:", input_file_path)
        input = parse_file_day24(input_file_path)
        solve_day24(input)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--actual', action='store_true')
    parser.add_argument('-e', '--example')
    parser.add_argument('-o', '--answer-only', action='store_true')
    args = parser.parse_args()
    main_24(run_all=args.actual, example=args.example, answer_only=args.answer_only)
