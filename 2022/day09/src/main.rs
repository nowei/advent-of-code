use std::{
    collections::HashSet,
    fs,
    ops::{Add, AddAssign, Sub, SubAssign},
};

static SAMPLE_INPUT_FILENAME: &str = "sample.txt";
static INPUT_FILENAME: &str = "input.txt";

#[derive(Debug, Clone, Copy)]
struct Position {
    x: i32,
    y: i32,
}

impl Sub for Position {
    type Output = Self;

    fn sub(self, other: Self) -> Self::Output {
        Self {
            x: self.x - other.x,
            y: self.y - other.y,
        }
    }
}

impl Add for Position {
    type Output = Self;

    fn add(self, other: Self) -> Self::Output {
        Self {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

impl AddAssign for Position {
    fn add_assign(&mut self, other: Self) {
        *self = Self {
            x: self.x + other.x,
            y: self.y + other.y,
        };
    }
}

impl SubAssign for Position {
    fn sub_assign(&mut self, other: Self) {
        *self = Self {
            x: self.x - other.x,
            y: self.y - other.y,
        }
    }
}

impl Position {
    fn clamp_to_one(&self) -> Position {
        let x = if self.x > 0 {
            1
        } else if self.x < 0 {
            -1
        } else {
            0
        };
        let y = if self.y > 0 {
            1
        } else if self.y < 0 {
            -1
        } else {
            0
        };
        return Position { x, y };
    }
}

enum Direction {
    LEFT,
    UP,
    RIGHT,
    DOWN,
}

type ContentType = Vec<(Direction, u32)>;

fn parse_input(contents: String) -> ContentType {
    let mut result = ContentType::new();
    for line in contents.lines() {
        let split: Vec<&str> = line.split(" ").collect();
        let direction = match split[0] {
            "U" => Direction::UP,
            "D" => Direction::DOWN,
            "L" => Direction::LEFT,
            "R" => Direction::RIGHT,
            _ => unimplemented!("It shouldn't get here"),
        };
        let steps = split[1].parse::<u32>().expect("This should exist");
        result.push((direction, steps));
    }
    return result;
}

fn puzzle1(contents: &ContentType) -> i32 {
    let mut head_pos = Position { x: 0, y: 0 };
    let mut tail_pos = Position { x: 0, y: 0 };
    const LEFT: Position = Position { x: -1, y: 0 };
    const UP: Position = Position { x: 0, y: 1 };
    const RIGHT: Position = Position { x: 1, y: 0 };
    const DOWN: Position = Position { x: 0, y: -1 };
    let mut pos_tracking: HashSet<(i32, i32)> = HashSet::new();
    for (direction, amount) in contents {
        let delta_pos = match direction {
            Direction::LEFT => LEFT,
            Direction::UP => UP,
            Direction::RIGHT => RIGHT,
            Direction::DOWN => DOWN,
        };
        for _ in 0..*amount {
            head_pos += delta_pos;
            let dist = head_pos - tail_pos;
            if dist.x.abs() >= 2 || dist.y.abs() >= 2 {
                // Move in clamped direction such that it's never more than 1 unit apart
                tail_pos += dist.clamp_to_one();
            }
            pos_tracking.insert((tail_pos.x, tail_pos.y));
        }
    }
    let result = pos_tracking.len();
    assert!(pos_tracking.contains(&(0, 0)));
    return result as i32;
}

fn puzzle2(contents: &ContentType) -> i32 {
    let mut snake = Vec::new();
    for _ in 0..10 {
        snake.push(Position { x: 0, y: 0 });
    }
    const LEFT: Position = Position { x: -1, y: 0 };
    const UP: Position = Position { x: 0, y: 1 };
    const RIGHT: Position = Position { x: 1, y: 0 };
    const DOWN: Position = Position { x: 0, y: -1 };
    let mut pos_tracking: HashSet<(i32, i32)> = HashSet::new();
    for (direction, amount) in contents {
        let delta_pos = match direction {
            Direction::LEFT => LEFT,
            Direction::UP => UP,
            Direction::RIGHT => RIGHT,
            Direction::DOWN => DOWN,
        };
        for _ in 0..*amount {
            // Handle head
            let mut iter = snake.iter_mut();
            let head = iter.next().expect("There should always be a head");
            *head += delta_pos;

            let mut prev = head;
            for curr in iter {
                let dist = *prev - *curr;
                if dist.x.abs() >= 2 || dist.y.abs() >= 2 {
                    // Move in clamped direction such that it's never more than 1 unit apart
                    *curr += dist.clamp_to_one();
                }
                prev = curr;
            }
            // Get tail (new last)
            let tail = snake.last().expect("This should exist");
            pos_tracking.insert((tail.x, tail.y));
        }
    }
    let result = pos_tracking.len();
    assert!(pos_tracking.contains(&(0, 0)));
    return result as i32;
}

fn main() {
    let contents_sample =
        fs::read_to_string(SAMPLE_INPUT_FILENAME).expect("Should have been able to read the file");
    let parsed_input_sample = parse_input(contents_sample);
    let contents_actual =
        fs::read_to_string(INPUT_FILENAME).expect("Should have been able to read the file");
    let parsed_input_actual = parse_input(contents_actual);
    let parsed_extended_sample = parse_input(
        fs::read_to_string("extended_sample.txt").expect("Should have been able to read the file"),
    );

    let sample_result_1 = puzzle1(&parsed_input_sample);
    assert_eq!(sample_result_1, 13);
    let sample_result_2 = puzzle2(&parsed_input_sample);
    assert_eq!(sample_result_2, 1);
    let sample_result_3 = puzzle2(&parsed_extended_sample);
    assert_eq!(sample_result_3, 36);

    let actual_result_1 = puzzle1(&parsed_input_actual);
    let actual_result_2 = puzzle2(&parsed_input_actual);

    println!("Day 9 - Puzzle 1");
    println!("The sample result is: {}", sample_result_1);
    println!("The result for the input is: {}", actual_result_1);
    println!("Day 9 - Puzzle 2");
    println!("The sample result is: {}", sample_result_2);
    println!("The extended sample result is: {}", sample_result_3);
    println!("The result for the input is: {}", actual_result_2);
}
