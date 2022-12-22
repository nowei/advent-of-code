use regex::Regex;
use std::{collections::HashSet, fs};

static INPUT_FILENAME: &str = "input.txt";

type InputType = HashSet<Block>;

#[derive(Eq, Hash, PartialEq, Copy, Clone, Debug)]
struct Block {
    x: i32,
    y: i32,
    z: i32,
}

impl Block {
    fn check_covered(&self, blocks: &HashSet<Block>) -> i32 {
        let mut sides = 6;
        // x
        if blocks.contains(&Block {
            x: self.x - 1,
            ..*self
        }) {
            sides -= 1
        }
        if blocks.contains(&Block {
            x: self.x + 1,
            ..*self
        }) {
            sides -= 1
        }
        // y
        if blocks.contains(&Block {
            y: self.y - 1,
            ..*self
        }) {
            sides -= 1
        }
        if blocks.contains(&Block {
            y: self.y + 1,
            ..*self
        }) {
            sides -= 1
        }
        // z
        if blocks.contains(&Block {
            z: self.z - 1,
            ..*self
        }) {
            sides -= 1
        }
        if blocks.contains(&Block {
            z: self.z + 1,
            ..*self
        }) {
            sides -= 1
        }
        return sides;
    }

    fn get_adjacent(&self) -> Vec<Block> {
        vec![
            Block {
                x: self.x - 1,
                ..*self
            },
            Block {
                x: self.x + 1,
                ..*self
            },
            Block {
                y: self.y - 1,
                ..*self
            },
            Block {
                y: self.y + 1,
                ..*self
            },
            Block {
                z: self.z - 1,
                ..*self
            },
            Block {
                z: self.z + 1,
                ..*self
            },
        ]
    }

    fn check_adjacent(
        &self,
        blocks: &HashSet<Block>,
        seen: &mut HashSet<Block>,
        boundaries: &(i32, i32, i32, i32, i32, i32),
    ) -> i32 {
        let adjacent_blocks = self.get_adjacent();
        let mut uncovered_surfaces = 0;
        for b in adjacent_blocks {
            match b.check_inside_surfaces(blocks, seen, boundaries) {
                Some(v) => {
                    uncovered_surfaces += v;
                }
                None => {}
            }
        }
        if uncovered_surfaces != 0 {
            println!("uncovered {}", uncovered_surfaces);
        }
        return uncovered_surfaces;
    }

    fn check_inside_surfaces(
        &self,
        blocks: &HashSet<Block>,
        seen: &mut HashSet<Block>,
        boundaries: &(i32, i32, i32, i32, i32, i32),
    ) -> Option<i32> {
        if blocks.contains(self) {
            return Some(0);
        }
        if seen.contains(self) {
            return Some(0);
        }
        let &(x_min, x_max, y_min, y_max, z_min, z_max) = boundaries;
        // Outside bounds
        if (self.x < x_min || self.x > x_max)
            || (self.y < y_min || self.y > y_max)
            || (self.z < z_min || self.z > z_max)
        {
            return None;
        }
        seen.insert(*self);
        let mut sides = 0;
        let mut seen_none = false;
        for b in self.get_adjacent() {
            if blocks.contains(&b) {
                sides += 1;
            } else {
                match b.check_inside_surfaces(blocks, seen, boundaries) {
                    Some(v) => {
                        sides += v;
                    }
                    None => {
                        seen_none = true;
                    }
                }
            }
        }
        if seen_none {
            return None;
        }

        return Some(sides);
    }
}

fn parse_input(input: String) -> InputType {
    let mut result = InputType::new();
    let re = Regex::new(r#"(.*),(.*),(.*)"#).expect("This shouldn't break");

    for line in input.lines() {
        let (x, y, z) = re
            .captures(line)
            .and_then(|cap| {
                let group = (cap.get(1), cap.get(2), cap.get(3));
                match group {
                    (Some(x), Some(y), Some(z)) => Some((
                        x.as_str().parse::<i32>().unwrap(),
                        y.as_str().parse::<i32>().unwrap(),
                        z.as_str().parse::<i32>().unwrap(),
                    )),
                    _ => None,
                }
            })
            .expect("Should work");
        result.insert(Block { x, y, z });
    }
    return result;
}

fn part1(input: InputType) -> i32 {
    let mut result = 0;
    for b in &input {
        result += b.check_covered(&input);
    }
    return result;
}

fn part2(input: InputType) -> i32 {
    let mut result = 0;
    // We just have to check if there are adjacent blocks that are completely covered.
    // We only need to check each adjacent block once, but we need to keep track of blocks
    // that we've seen and if there is empty space, we keep exploring. If we reach the
    // boundaries/beyond then we know that we are not enclosed.
    for b in &input {
        result += b.check_covered(&input);
    }
    // We first get the boundaries of the space;
    let x_min = input.iter().map(|b| b.x).min().expect("should exist");
    let x_max = input.iter().map(|b| b.x).max().expect("should exist");
    let y_min = input.iter().map(|b| b.y).min().expect("should exist");
    let y_max = input.iter().map(|b| b.y).max().expect("should exist");
    let z_min = input.iter().map(|b| b.z).min().expect("should exist");
    let z_max = input.iter().map(|b| b.z).max().expect("should exist");
    let boundaries = (x_min, x_max, y_min, y_max, z_min, z_max);
    println!("boundaries {:?}", boundaries);
    for z in z_min..z_max + 1 {
        println!("layer {} (z)", z);
        for y in y_min..y_max + 1 {
            let mut row = "".to_string();
            for x in x_min..x_max + 1 {
                if input.contains(&Block { x, y, z }) {
                    row.push('#');
                } else {
                    row.push('.');
                }
            }
            println!("{}", row);
        }
    }
    let mut seen: HashSet<Block> = HashSet::new();
    // 1927 is too low
    // 3316 is too high
    let mut air_bubble_surfaces = 0;
    for b in &input {
        air_bubble_surfaces += b.check_adjacent(&input, &mut seen, &boundaries);
    }
    println!("result before {}", result);
    result -= air_bubble_surfaces;
    println!("air bubble surfaces {}", air_bubble_surfaces);
    println!("result after {}", result);
    println!("seen {:?}", seen);
    return result;
}

fn main() {
    let contents_actual =
        fs::read_to_string(INPUT_FILENAME).expect("Should have been able to read the file");
    let parsed_input_actual_1 = parse_input(contents_actual.clone());
    let parsed_input_actual_2 = parse_input(contents_actual);

    let actual_result_1 = part1(parsed_input_actual_1);
    let actual_result_2 = part2(parsed_input_actual_2);

    println!("Day 18 - Part 1");
    println!("The result for the input is: {}", actual_result_1);
    println!("Day 18 - Part 2");
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
        assert_eq!(sample_result_1, 64);
    }

    #[test]
    fn test_part2() {
        let contents_sample = fs::read_to_string(SAMPLE_INPUT_FILENAME)
            .expect("Should have been able to read the file");
        let parsed_input_sample = parse_input(contents_sample);
        let sample_result_2 = part2(parsed_input_sample);
        let contents_sample =
            fs::read_to_string("sample2.txt").expect("Should have been able to read the file");
        let parsed_input_sample = parse_input(contents_sample);
        let sample_result_2 = part2(parsed_input_sample);
        assert_eq!(sample_result_2, 66);
    }
}
