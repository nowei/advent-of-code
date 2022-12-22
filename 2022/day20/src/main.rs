use regex::Regex;
use std::fs;

static INPUT_FILENAME: &str = "input.txt";

type InputType = Vec<i32>;

fn parse_input(input: String) -> InputType {
    let mut result = InputType::new();
    let re = Regex::new(r#"(.*)"#).expect("This shouldn't break");

    for line in input.lines() {
        let val = re
            .captures(line)
            .and_then(|cap| {
                let group = cap.get(1);
                match group {
                    (Some(num)) => Some(num.as_str().parse::<i32>().unwrap()),
                    _ => None,
                }
            })
            .expect("Should work");
        result.push(val);
    }
    return result;
}

fn part1(input: InputType, key: i64, times: i32) -> i64 {
    let mut result = 0;
    let length = input.len();
    // It takes length - 1 moves to rotate back to itself.
    // So the total distances should be modded by length - 1?

    // I spent an hour learning that there can be duplicates in the numbers 🤦‍♂️
    let values: Vec<i64> = input.iter().map(|&v| v as i64 * key).collect();
    let mut index: Vec<usize> = (0..length).into_iter().collect();
    for _ in 0..times {
        for (i, &v) in values.iter().enumerate() {
            let curr_pos = index
                .iter()
                .position(|&ind| ind == i)
                .expect("should exist");
            index.remove(curr_pos);
            let mult = curr_pos as i64 + v as i64 as i64;
            let new_pos = mult.rem_euclid(index.len() as i64) as usize;
            index.insert(new_pos, i);
        }
    }

    let new_order: Vec<i64> = index.iter().map(|&i| values[i]).collect();

    let zero_pos = new_order
        .iter()
        .position(|&v| v == 0)
        .expect("should exist");
    let thousandth_val = new_order[(zero_pos + 1000) % new_order.len()];
    let two_thousandth_val = new_order[(zero_pos + 2000) % new_order.len()];
    let three_thousandth_val = new_order[(zero_pos + 3000) % new_order.len()];
    result = thousandth_val + two_thousandth_val + three_thousandth_val;
    return result;
}

fn main() {
    let contents_actual =
        fs::read_to_string(INPUT_FILENAME).expect("Should have been able to read the file");
    let parsed_input_actual_1 = parse_input(contents_actual.clone());
    let parsed_input_actual_2 = parse_input(contents_actual);

    let actual_result_1 = part1(parsed_input_actual_1, 1, 1);
    let actual_result_2 = part1(parsed_input_actual_2, 811589153, 10);

    println!("Day 20 - Part 1");
    println!("The result for the input is: {}", actual_result_1);
    println!("Day 20 - Part 2");
    println!("The result for the input is: {}", actual_result_2);
}

#[cfg(test)]
mod tests {
    use crate::{parse_input, part1};
    use std::fs;

    static SAMPLE_INPUT_FILENAME: &str = "sample.txt";

    #[test]
    fn test_part1() {
        let contents_sample = fs::read_to_string(SAMPLE_INPUT_FILENAME)
            .expect("Should have been able to read the file");
        let parsed_input_sample = parse_input(contents_sample);
        let sample_result_1 = part1(parsed_input_sample, 1, 1);
        assert_eq!(sample_result_1, 3);
    }

    #[test]
    fn test_part2() {
        let contents_sample = fs::read_to_string(SAMPLE_INPUT_FILENAME)
            .expect("Should have been able to read the file");
        let parsed_input_sample = parse_input(contents_sample);
        let sample_result_2 = part1(parsed_input_sample, 811589153, 10);
        assert_eq!(sample_result_2, 1623178306);
    }
}
