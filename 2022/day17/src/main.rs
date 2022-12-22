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
//          cycle detection -> with jet cycle
// Implmentation #3: Cycle tracking with bytes?
fn part2(input: InputType) -> i64 {
    let mut jet_index = 0;
    let mut blocked: HashSet<Point> = HashSet::new();
    for x in 0..7 {
        blocked.insert(Point { x, y: 0 });
    }

    let mut top_height: i64 = 0;
    // Cycle detection
    let mut top_heights: Vec<i64> = vec![];

    let goal = 1000000000000i64;
    let mut byte_tracking = vec![];
    for shape_index in 0..goal {
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
                shape.mv(*input.get(j_i).expect("Should be fine"), &mut blocked);
                jet_index = jet_index + 1;
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
        top_heights.push(top_height);
        let mut byte: u8 = 0;
        for x in 0..7u8 {
            if blocked.contains(&Point {
                x: x as i64,
                y: top_height,
            }) {
                byte |= 1 << x;
            }
        }
        byte_tracking.push(byte);
        // Note there are 10092 directions and each piece moves on average 3 times, so
        // we can probably track 3364 shapes at a time. So we may need to repeat this several times, so
        // let us track 3364 * 4 shapes to make sure that we can detect a cycle.
        if byte_tracking.len() == 3364 * 4 {
            break;
        }
    }

    // Find the first instance of cycle
    // e.g. [15, 8, 16, _12_, 10, 9, 8, 14, _12_, 10, 9, 8, 14, _12_, 10, 9, 8, 14, 12, 10]
    //      [15, 23, 39, _51_, 61, 70, 78, 92, _104_, 114, 123, 131, 145, _157_, 167, 176, 184, 198, 210, 220]
    // Floyd's algorithm
    // Fast pointer, slow pointer
    let mut i = 0;
    let mut j = 0;
    let window = 25;
    while i == 0 || (byte_tracking[i..i + window] != byte_tracking[j..j + window]) {
        i += 1;
        j += 2;
    }
    println!("{} {} {} {}", i, j, byte_tracking[i], byte_tracking[j]);
    i = 0;
    while byte_tracking[i..i + window] != byte_tracking[j..j + window] {
        j += 1;
        i += 1;
    }
    println!("{} {} {} {}", i, j, byte_tracking[i], byte_tracking[j]);
    j = i + 1;
    while byte_tracking[i..i + window] != byte_tracking[j..j + window] {
        j += 1;
    }
    println!("{} {} {} {}", i, j, byte_tracking[i], byte_tracking[j]);
    println!("{:?}", &byte_tracking[i..j]);
    println!("{:?}", &byte_tracking[i..2 * j - i]);
    let cycle_length = j - i;
    println!("{}", cycle_length);
    let cycle_start = i;
    let mut height_diffs = vec![];
    let height_start = top_heights[cycle_start - 1];
    let mut last = height_start;
    for idx in cycle_start..cycle_start + cycle_length {
        height_diffs.push(top_heights[idx] - last);
        last = top_heights[idx];
    }
    println!("height diffs: {:?}", height_diffs);
    let cycle_height: i64 = top_heights[i + cycle_length] - top_heights[i];
    let num_cycles = (goal - cycle_start as i64) / cycle_length as i64;
    println!("init height: {}", height_start);
    println!("length of cycle: {}", cycle_length);
    println!("cycle height diff: {}", cycle_height);
    println!("number of cycles remaining: {}", num_cycles);
    let remaining_blocks = (goal - cycle_start as i64) % cycle_length as i64;
    println!("number of blocks remaining: {}", remaining_blocks);
    let height_after_cycles = height_start + cycle_height * num_cycles;
    let remaining_height: i64 = height_diffs[..remaining_blocks as usize].iter().sum();
    let top_height = height_after_cycles + remaining_height;
    println!(
        "result {} {} {}",
        height_after_cycles, remaining_height, top_height
    );

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
