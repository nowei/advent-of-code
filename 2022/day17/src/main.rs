use std::{collections::HashSet, fs};

static INPUT_FILENAME: &str = "input.txt";

type InputType = Vec<Direction>;

#[derive(Debug)]
enum TetrisLike {
    HLine,  // Left-most block coord
    Plus,   // Center coord
    FlipL,  // Left-most coord
    VLine,  // Top most coord
    Square, // Top-left most coord
}

#[derive(Debug)]
struct Shape {
    shape_type: TetrisLike,
    points: HashSet<Point>,
    bounds: (i64, i64),
    stopped: bool,
}

impl Shape {
    fn init(shape_type: TetrisLike, bounds: (i64, i64), top_height: i64) -> Shape {
        let left_edge: i64 = bounds.0 + 2;
        let bot_edge: i64 = top_height + 4;
        let points = match shape_type {
            TetrisLike::HLine => vec![
                Point {
                    x: left_edge,
                    y: bot_edge,
                },
                Point {
                    x: left_edge + 1,
                    y: bot_edge,
                },
                Point {
                    x: left_edge + 2,
                    y: bot_edge,
                },
                Point {
                    x: left_edge + 3,
                    y: bot_edge,
                },
            ],
            TetrisLike::Plus => vec![
                Point {
                    x: left_edge,
                    y: bot_edge + 1,
                },
                Point {
                    x: left_edge + 1,
                    y: bot_edge + 2,
                },
                Point {
                    x: left_edge + 1,
                    y: bot_edge + 1,
                },
                Point {
                    x: left_edge + 1,
                    y: bot_edge,
                },
                Point {
                    x: left_edge + 2,
                    y: bot_edge + 1,
                },
            ],
            TetrisLike::FlipL => vec![
                Point {
                    x: left_edge,
                    y: bot_edge,
                },
                Point {
                    x: left_edge + 1,
                    y: bot_edge,
                },
                Point {
                    x: left_edge + 2,
                    y: bot_edge,
                },
                Point {
                    x: left_edge + 2,
                    y: bot_edge + 1,
                },
                Point {
                    x: left_edge + 2,
                    y: bot_edge + 2,
                },
            ],
            TetrisLike::VLine => vec![
                Point {
                    x: left_edge,
                    y: bot_edge,
                },
                Point {
                    x: left_edge,
                    y: bot_edge + 1,
                },
                Point {
                    x: left_edge,
                    y: bot_edge + 2,
                },
                Point {
                    x: left_edge,
                    y: bot_edge + 3,
                },
            ],
            TetrisLike::Square => vec![
                Point {
                    x: left_edge,
                    y: bot_edge,
                },
                Point {
                    x: left_edge + 1,
                    y: bot_edge,
                },
                Point {
                    x: left_edge,
                    y: bot_edge + 1,
                },
                Point {
                    x: left_edge + 1,
                    y: bot_edge + 1,
                },
            ],
        }
        .into_iter()
        .collect();
        Shape {
            shape_type,
            points,
            bounds,
            stopped: false,
        }
    }
    fn mv(&mut self, direction: Direction, blocked: &mut HashSet<Point>) -> bool {
        match direction {
            Direction::Left => {
                if !self.points.iter().any(|&p| {
                    // Checks blocked
                    if p.x - 1 < self.bounds.0 {
                        true
                    } else {
                        if blocked.contains(&Point { x: p.x - 1, ..p }) {
                            return true;
                        }
                        // Not blocked if self-blocked.
                        false
                    }
                }) {
                    self.points = self
                        .points
                        .iter()
                        .map(|&p| Point { x: p.x - 1, ..p })
                        .collect();
                }
            }
            Direction::Right => {
                if !self.points.iter().any(|&p| {
                    // Checks blocked
                    if p.x + 1 > self.bounds.1 {
                        true
                    } else {
                        if blocked.contains(&Point { x: p.x + 1, ..p }) {
                            return true;
                        }
                        false
                    }
                }) {
                    self.points = self
                        .points
                        .iter()
                        .map(|&p| Point { x: p.x + 1, ..p })
                        .collect();
                }
            }
            Direction::Down => {
                if !self.points.iter().any(|&p| {
                    // Checks blocked
                    if p.y - 1 <= 0 {
                        true
                    } else {
                        if blocked.contains(&Point { y: p.y - 1, ..p }) {
                            return true;
                        }
                        false
                    }
                }) {
                    self.points = self
                        .points
                        .iter()
                        .map(|&p| Point { y: p.y - 1, ..p })
                        .collect();
                } else {
                    for p in &self.points {
                        blocked.insert(p.clone());
                    }
                    self.stopped = true;
                }
            }
        }
        return false;
    }
}

#[derive(Debug, Copy, Clone)]
enum Direction {
    Left,
    Right,
    Down,
}

#[derive(Debug, Eq, Hash, PartialEq, Copy, Clone)]
struct Point {
    x: i64,
    y: i64,
}

fn parse_input(input: String) -> InputType {
    let mut result = InputType::new();

    let single_line = input.lines().next().unwrap();
    for c in single_line.chars() {
        result.push(match c {
            '>' => Direction::Right,
            '<' => Direction::Left,
            _ => todo!(),
        });
    }

    return result;
}

fn part1(input: InputType) -> i32 {
    let mut jet_index = 0;
    let mut blocked: HashSet<Point> = HashSet::new();
    for x in 0..7 {
        blocked.insert(Point { x, y: 0 });
    }

    let mut top_height = 0;

    for shape_index in 0..2022 {
        let shape_type = match shape_index % 5 {
            0 => TetrisLike::HLine,
            1 => TetrisLike::Plus,
            2 => TetrisLike::FlipL,
            3 => TetrisLike::VLine,
            4 => TetrisLike::Square,
            _ => panic!("Shouldn't get here"),
        };
        let mut shape = Shape::init(shape_type, (0, 6), top_height);
        let mut jet = true;
        while !shape.stopped {
            if jet {
                shape.mv(*input.get(jet_index).expect("Should be fine"), &mut blocked);
                jet_index = (jet_index + 1) % input.len();
            } else {
                shape.mv(Direction::Down, &mut blocked);
            }
            jet = !jet;
        }
        top_height = shape
            .points
            .iter()
            .map(|p| p.y)
            .max()
            .expect("max should exist")
            .max(top_height);
    }

    return top_height.try_into().unwrap();
}

// Attempt #1 brute-forcing
// Idea #2: Shapes cycle and the flow eventually cycles, how do we detect the cycles?

fn part2(input: InputType) -> i64 {
    let mut jet_index = 0;
    let mut blocked: HashSet<Point> = HashSet::new();
    for x in 0..7 {
        blocked.insert(Point { x, y: 0 });
    }

    let mut top_height: i64 = 0;
    let mut prev_height = 0;
    let mut prev_shape_idx = 0;
    // Cycle detection
    let mut cycle_detector: Vec<i64> = vec![];
    let mut top_heights: Vec<i64> = vec![];
    let mut shape_diffs: Vec<i64> = vec![];

    let goal = 1000000000000i64;
    let mut prev_shape_height = 0;
    'outer: for shape_index in 0..goal {
        let shape_type = match shape_index % 5 {
            0 => TetrisLike::HLine,
            1 => TetrisLike::Plus,
            2 => TetrisLike::FlipL,
            3 => TetrisLike::VLine,
            4 => TetrisLike::Square,
            _ => panic!("Shouldn't get here"),
        };
        let mut shape = Shape::init(shape_type, (0, 6), top_height);
        let mut jet = true;
        let mut to_break = false;
        while !shape.stopped {
            if jet {
                let j_i = jet_index % input.len();
                shape.mv(*input.get(j_i).expect("Should be fine"), &mut blocked);
                jet_index = jet_index + 1;
                if jet_index % input.len() == 0 {
                    // println!(
                    //     "shape index {} {} jet index {} jet iter {} {} {}",
                    //     shape_index,
                    //     shape_index - prev_shape_idx,
                    //     jet_index,
                    //     jet_index / input.len(),
                    //     top_height,
                    //     top_height - prev_height
                    // );
                    let height_diff = top_height - prev_height;
                    if cycle_detector.contains(&height_diff) && jet_index > (input.len() * 1000) {
                        println!("{:?}", cycle_detector);
                        println!("{:?}", top_heights);
                        println!("{:?}", shape_diffs);
                        to_break = true;
                    }
                    cycle_detector.push(top_height - prev_height);
                    shape_diffs.push(shape_index - prev_shape_idx);
                    top_heights.push(top_height);
                    prev_height = top_height;
                    prev_shape_idx = shape_index;
                }
            } else {
                shape.mv(Direction::Down, &mut blocked);
            }
            jet = !jet;
        }
        top_height = shape
            .points
            .iter()
            .map(|p| p.y)
            .max()
            .expect("max should exist")
            .max(top_height);
        if shape_index % 1745 == 0 {
            println!(
                "prev height: {} curr_height: {} diff: {}",
                prev_shape_height,
                top_height,
                top_height - prev_shape_height
            );
            prev_shape_height = top_height;
        }
        if to_break {
            break;
        }
    }

    // Find the first instance of cycle
    // e.g. [15, 8, 16, _12_, 10, 9, 8, 14, _12_, 10, 9, 8, 14, _12_, 10, 9, 8, 14, 12, 10]
    //      [15, 23, 39, _51_, 61, 70, 78, 92, _104_, 114, 123, 131, 145, _157_, 167, 176, 184, 198, 210, 220]
    // Floyd's algorithm
    // Fast pointer, slow pointer
    let mut i = 1;
    let mut j = 2;
    while i == 0 || cycle_detector[i] != cycle_detector[j] {
        i += 1;
        j += 2;
    }
    println!("{} {} {} {}", i, j, cycle_detector[i], cycle_detector[j]);
    i = 0;
    while cycle_detector[i] != cycle_detector[j] {
        j += 1;
        i += 1;
    }
    println!("{} {} {} {}", i, j, cycle_detector[i], cycle_detector[j]);
    j = i + 1;
    while cycle_detector[i] != cycle_detector[j] {
        j += 1;
    }
    println!("{} {} {} {}", i, j, cycle_detector[i], cycle_detector[j]);
    let cycle_length = j - i;
    let mut cycle = vec![];
    let mut shape_cycle = vec![];
    for ind in j..j + cycle_length {
        cycle.push(cycle_detector[ind]);
        shape_cycle.push(shape_diffs[ind]);
    }
    let cycle_start = j;

    println!("cycle {} {:?}", cycle_length, cycle);
    println!("shape {} {:?}", cycle_length, shape_cycle);

    let start_height = top_heights[cycle_start - 1];
    let shape_idx_start: i64 = shape_diffs[..cycle_start].iter().sum();
    let shapes_per_cycle: i64 = shape_cycle.iter().sum();
    let cycle_height_diff: i64 = cycle.iter().sum();
    println!(
        "start_height {} cycle height diff {} shapes_per_cycle {} shape_idx_start {}",
        start_height, cycle_height_diff, shapes_per_cycle, shape_idx_start,
    );
    let cycles = (goal - shape_idx_start) / shapes_per_cycle;
    let remaining_shapes = (goal - shape_idx_start) % shapes_per_cycle;

    let intermediate_height = start_height + cycle_height_diff * cycles;

    println!("{} {} {}", cycles, intermediate_height, remaining_shapes);

    // Grab the last ten rows of the cycle we've found what we've seen so far and move it up so that the total_height
    let mut new_blocked: HashSet<Point> = blocked
        .iter()
        .filter(|p| p.y >= top_height - 20 && p.y <= top_height)
        .map(|p| {
            let diff = top_height - p.y;
            Point {
                x: p.x,
                y: intermediate_height - diff,
            }
        })
        .collect();
    top_height = intermediate_height;

    for shape_index in (goal - remaining_shapes + 1)..goal {
        let shape_type = match shape_index % 5 {
            0 => TetrisLike::HLine,
            1 => TetrisLike::Plus,
            2 => TetrisLike::FlipL,
            3 => TetrisLike::VLine,
            4 => TetrisLike::Square,
            _ => panic!("Shouldn't get here"),
        };
        let mut shape = Shape::init(shape_type, (0, 6), top_height);
        let mut jet = true;
        while !shape.stopped {
            if jet {
                let j_i = jet_index % input.len();
                shape.mv(*input.get(j_i).expect("Should be fine"), &mut new_blocked);
                jet_index = jet_index + 1;
            } else {
                shape.mv(Direction::Down, &mut new_blocked);
            }
            jet = !jet;
        }
        top_height = shape
            .points
            .iter()
            .map(|p| p.y)
            .max()
            .expect("max should exist")
            .max(top_height);
    }

    // 1591977078505 is too tall
    // 1591977075727 is too short
    // 1591977077299 is too short
    // 1591977077305 is not right
    // 1591977077307 is not right
    // 1591977077352 is right?

    return top_height;
}

fn main() {
    let contents_actual =
        fs::read_to_string(INPUT_FILENAME).expect("Should have been able to read the file");
    let parsed_input_actual_1 = parse_input(contents_actual.clone());
    let parsed_input_actual_2 = parse_input(contents_actual);

    let actual_result_1 = part1(parsed_input_actual_1);
    let actual_result_2 = part2(parsed_input_actual_2);

    println!("Day 17 - Part 1");
    println!("The result for the input is: {}", actual_result_1);
    println!("Day 17 - Part 2");
    println!("The result for the input is: {}", actual_result_2);
}

#[cfg(test)]
mod tests {
    use crate::{parse_input, part1, part2};
    use std::fs;

    static SAMPLE_INPUT_FILENAME: &str = "sample.txt";

    #[test]
    fn test_part1() {
        let contents_sample = fs::read_to_string(SAMPLE_INPUT_FILENAME)
            .expect("Should have been able to read the file");
        let parsed_input_sample = parse_input(contents_sample);
        let sample_result_1 = part1(parsed_input_sample);
        assert_eq!(sample_result_1, 3068);
    }

    #[test]
    fn test_part2() {
        let contents_sample = fs::read_to_string(SAMPLE_INPUT_FILENAME)
            .expect("Should have been able to read the file");
        let parsed_input_sample = parse_input(contents_sample);
        let sample_result_2 = part2(parsed_input_sample);
        println!("{}", 1514285714288 - sample_result_2);
        assert_eq!(sample_result_2, 1514285714288);
    }
}
