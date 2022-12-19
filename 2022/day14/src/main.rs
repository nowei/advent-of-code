use std::{collections::HashSet, fs};

static INPUT_FILENAME: &str = "input.txt";

type InputType = (HashSet<Point>, u32);

#[derive(Hash, Eq, PartialEq, Clone)]
struct Point {
    x: u32,
    y: u32,
}

// Good to be able to query for what's immediately below something?
fn parse_input(input: String) -> InputType {
    let mut y_max = 0;
    let mut blocked = HashSet::new();
    for line in input.lines() {
        let split = line
            .split(" -> ")
            .map(|v| {
                let coords_str: Vec<&str> = v.split(",").collect();
                let x = coords_str[0].parse::<u32>().expect("Should parse");
                let y = coords_str[1].parse::<u32>().expect("Should parse");
                (x, y)
            })
            .collect::<Vec<(u32, u32)>>();
        let mut iter = split.iter();
        let mut prev = iter.next().expect("Should exist");
        while let Some(curr) = iter.next() {
            let x_0 = prev.0.min(curr.0);
            let x_1 = prev.0.max(curr.0) + 1;
            let y_0 = prev.1.min(curr.1);
            let y_1 = prev.1.max(curr.1) + 1;
            for x in x_0..x_1 {
                for y in y_0..y_1 {
                    blocked.insert(Point { x, y });
                }
            }
            prev = curr;
        }
        let y_cand = split
            .iter()
            .map(|v| v.1)
            .max()
            .expect("Some max should exist");
        if y_cand > y_max {
            y_max = y_cand;
        }
    }
    return (blocked, y_max);
}

fn part1(input: InputType) -> i32 {
    let mut result = 0;
    let (mut blocked, y_max) = input;
    // Simulate sand falling down, one grain at a time
    loop {
        let mut curr = Point { x: 500, y: 0 };
        // Move down
        loop {
            // Move down whenever possible
            if !blocked.contains(&Point {
                x: curr.x,
                y: curr.y + 1,
            }) {
                curr.y += 1;
                if curr.y > y_max {
                    break;
                }
            } else {
                // Check left
                if !blocked.contains(&Point {
                    x: curr.x - 1,
                    y: curr.y + 1,
                }) {
                    curr.x -= 1;
                    curr.y += 1;
                } else if !blocked.contains(&Point {
                    x: curr.x + 1,
                    y: curr.y + 1,
                }) {
                    curr.x += 1;
                    curr.y += 1;
                } else {
                    // Blocked in general, break
                    break;
                }
            }
        }
        if curr.y > y_max {
            break;
        } else {
            blocked.insert(curr);
        }
        result += 1;
    }
    return result;
}

fn part2(input: InputType) -> i32 {
    let mut result = 0;
    let (mut blocked, mut y_max) = input;
    // Simulate sand falling down, one grain at a time
    y_max += 2;
    loop {
        let mut curr = Point { x: 500, y: 0 };
        // Move down
        if blocked.contains(&curr) {
            break;
        }
        loop {
            // Move down whenever possible
            if !blocked.contains(&Point {
                x: curr.x,
                y: curr.y + 1,
            }) || curr.y + 1 == y_max
            {
                if curr.y + 1 == y_max {
                    break;
                } else {
                    curr.y += 1;
                }
            } else {
                // Check left
                if !blocked.contains(&Point {
                    x: curr.x - 1,
                    y: curr.y + 1,
                }) {
                    curr.x -= 1;
                    curr.y += 1;
                } else if !blocked.contains(&Point {
                    x: curr.x + 1,
                    y: curr.y + 1,
                }) {
                    curr.x += 1;
                    curr.y += 1;
                } else {
                    // Blocked in general, break
                    break;
                }
            }
        }
        blocked.insert(curr);
        result += 1;
    }
    return result;
}

fn main() {
    let contents_actual =
        fs::read_to_string(INPUT_FILENAME).expect("Should have been able to read the file");
    let parsed_input_actual_1 = parse_input(contents_actual.clone());
    let parsed_input_actual_2 = parse_input(contents_actual);

    let actual_result_1 = part1(parsed_input_actual_1);
    let actual_result_2 = part2(parsed_input_actual_2);

    println!("Day 14 - Part 1");
    println!("The result for the input is: {}", actual_result_1);
    println!("Day 14 - Part 2");
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
        assert_eq!(sample_result_1, 24);
    }

    #[test]
    fn test_part2() {
        let contents_sample = fs::read_to_string(SAMPLE_INPUT_FILENAME)
            .expect("Should have been able to read the file");
        let parsed_input_sample = parse_input(contents_sample);
        let sample_result_2 = part2(parsed_input_sample);
        assert_eq!(sample_result_2, 93);
    }
}
