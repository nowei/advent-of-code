use regex::Regex;
use std::{collections::HashMap, fs};

static INPUT_FILENAME: &str = "input.txt";

type InputType = Vec<SignalBeacon>;

struct Point {
    x: i32,
    y: i32,
}
struct SignalBeacon {
    signal: Point,
    beacon: Point,
}

fn parse_input(input: String) -> InputType {
    let mut result = InputType::new();

    let re =
        Regex::new(r#"Sensor at x=([-]?[0-9]*), y=([-]?[0-9]*): closest beacon is at x=([-]?[0-9]*), y=([-]?[0-9]*)"#).expect("This shouldn't break");

    for line in input.lines() {
        let (sx, sy, bx, by) = re
            .captures(line)
            .and_then(|cap| {
                let group = (cap.get(1), cap.get(2), cap.get(3), cap.get(4));
                match group {
                    (Some(sx), Some(sy), Some(bx), Some(by)) => Some((
                        sx.as_str().parse::<i32>().unwrap(),
                        sy.as_str().parse::<i32>().unwrap(),
                        bx.as_str().parse::<i32>().unwrap(),
                        by.as_str().parse::<i32>().unwrap(),
                    )),
                    _ => None,
                }
            })
            .expect("Should work");
        result.push(SignalBeacon {
            signal: Point { x: sx, y: sy },
            beacon: Point { x: bx, y: by },
        })
    }
    return result;
}

fn part1(input: InputType, y: i32) -> i32 {
    let mut result = 0;
    // Some diff math to see if there can be a beacon there?
    // So basically mark all signal-reaching positions/ranges, then subtract
    // the number of beacons in that row;
    let mut ranges: Vec<(i32, i32)> = input
        .iter()
        .filter_map(|sb| {
            let signal = &sb.signal;
            let beacon = &sb.beacon;
            let manhattan_dist = (signal.x - beacon.x).abs() + (signal.y - beacon.y).abs();
            if (y - signal.y).abs() < manhattan_dist {
                let remaining = manhattan_dist - (y - signal.y).abs();
                Some((signal.x - remaining, signal.x + remaining))
            } else {
                None
            }
        })
        .collect();
    ranges.sort();
    let mut ranges_iter = ranges.iter();
    let mut new_ranges = vec![ranges_iter.next().expect("Should exist").to_owned()];
    while let Some(&(x_min, x_max)) = ranges_iter.next() {
        let (x_min_prev, x_max_prev) = new_ranges.pop().expect("Should be non-empty");
        if x_min <= x_max_prev {
            let val = (x_min_prev, x_max.max(x_max_prev));
            new_ranges.push(val);
        } else {
            new_ranges.push((x_min_prev, x_max_prev));
            new_ranges.push((x_min, x_max));
        }
    }
    println!("{:?}", new_ranges);
    let mut level_beacons: Vec<i32> = input
        .iter()
        .filter_map(|sb| {
            if sb.beacon.y == y {
                Some(sb.beacon.x)
            } else {
                None
            }
        })
        .collect();
    level_beacons.sort();
    level_beacons.dedup();
    for (x_min, x_max) in new_ranges {
        let mut positions = x_max - x_min + 1;
        let r = x_min..x_max + 1;
        for b in &level_beacons {
            if r.contains(b) {
                positions -= 1;
            }
        }
        result += positions;
    }

    return result;
}

fn get_gaps(cand: &Vec<(i32, i32)>) -> Option<i32> {
    let mut iter = cand.iter();
    let prev = iter.next().expect("Should be non-empty");
    while let Some(curr) = iter.next() {
        if curr.0 - prev.1 == 2 {
            return Some(prev.1 + 1);
        }
    }
    return None;
}

fn part2(input: InputType) -> i64 {
    // The distress beacon is not detected by any sensor
    // Beacon must have x and y coordinates [0, 4000000]
    // tuning frequency is x * 4000000 + y;

    // For each beacon, keep track of the ranges in which they can operate
    // Then combine all the ranges, then look for some level of ranges where
    // there is a gap, then return the first tuning frequency with the gap?
    let mut result = 0;
    let mut ranges: HashMap<i32, Vec<(i32, i32)>> = HashMap::new();
    for sb in &input {
        let signal = &sb.signal;
        let beacon = &sb.beacon;
        let manhattan_dist = (signal.x - beacon.x).abs() + (signal.y - beacon.y).abs();
        for y_offset in -manhattan_dist..manhattan_dist + 1 {
            let remaining = manhattan_dist - y_offset.abs();
            let y = signal.y + y_offset;
            if y <= 0 || y >= 4000000 {
                continue;
            }

            let x_range = (
                (signal.x - remaining).max(0),
                (signal.x + remaining).min(4000000),
            );
            ranges.entry(y).or_insert(vec![]).push(x_range);
        }
    }
    let new_ranges: HashMap<i32, Vec<(i32, i32)>> = ranges
        .iter_mut()
        .map(|(k, v)| {
            v.sort();

            let mut ranges_iter = v.iter();
            let mut new_range = vec![ranges_iter.next().expect("Should exist").to_owned()];
            while let Some(&(x_min, x_max)) = ranges_iter.next() {
                let (x_min_prev, x_max_prev) = new_range.pop().expect("Should be non-empty");
                if x_min <= x_max_prev {
                    let val = (x_min_prev, x_max.max(x_max_prev));
                    new_range.push(val);
                } else {
                    new_range.push((x_min_prev, x_max_prev));
                    new_range.push((x_min, x_max));
                }
            }
            (*k, new_range)
        })
        .collect();
    for (y, x_ranges) in new_ranges {
        let gap = get_gaps(&x_ranges);
        match gap {
            Some(val) => {
                println!("{} {}", val, y);
                result = (val as i64) * 4000000 + y as i64;
                println!("Do we ever get there");
                break;
            }
            None => {}
        }
    }
    return result;
}

fn main() {
    let contents_actual =
        fs::read_to_string(INPUT_FILENAME).expect("Should have been able to read the file");
    let parsed_input_actual_1 = parse_input(contents_actual.clone());
    let parsed_input_actual_2 = parse_input(contents_actual);

    let actual_result_1 = part1(parsed_input_actual_1, 2000000);
    let actual_result_2 = part2(parsed_input_actual_2);

    println!("Day 15 - Part 1");
    println!("The result for the input is: {}", actual_result_1);
    println!("Day 15 - Part 2");
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
        let sample_result_1 = part1(parsed_input_sample, 10);
        assert_eq!(sample_result_1, 26);
    }

    #[test]
    fn test_part2() {
        let contents_sample = fs::read_to_string(SAMPLE_INPUT_FILENAME)
            .expect("Should have been able to read the file");
        let parsed_input_sample = parse_input(contents_sample);
        let sample_result_2 = part2(parsed_input_sample);
        assert_eq!(sample_result_2, 56000011);
    }
}
