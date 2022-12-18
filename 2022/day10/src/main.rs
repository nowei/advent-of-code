use std::fs;

static SAMPLE_INPUT_FILENAME: &str = "sample.txt";
static INPUT_FILENAME: &str = "input.txt";

type InputType = Vec<Action>;

#[derive(Debug)]
enum Action {
    NoOp,
    AddX(i32),
}

fn parse_input(input: String) -> InputType {
    let mut result = InputType::new();
    for line in input.lines() {
        if line == "noop" {
            result.push(Action::NoOp);
        } else {
            let split: Vec<&str> = line.split(" ").collect();
            let val = Action::AddX(
                split
                    .get(1)
                    .expect("This should exist")
                    .parse::<i32>()
                    .expect("okay"),
            );
            result.push(val);
        }
    }
    return result;
}

fn puzzle1(input: &InputType) -> i32 {
    let mut result = 0;
    let points = vec![20, 60, 100, 140, 180, 220];
    let mut curr = 1;
    let mut turn = 1;
    for line in input {
        let (turns, v) = if let Action::AddX(val) = line {
            (2, *val)
        } else {
            (1, 0)
        };
        for _ in 0..turns {
            if points.contains(&turn) {
                result += turn * curr;
            }
            turn += 1;
        }
        curr += v;
    }
    return result;
}

fn puzzle2(input: &InputType) -> i32 {
    let mut result = 0;
    let mut curr = 1;
    let mut turn = 0;
    let mut rows = Vec::new();
    let mut curr_row = "".to_string();
    for line in input {
        let (turns, v) = if let Action::AddX(val) = line {
            (2, *val)
        } else {
            (1, 0)
        };
        for _ in 0..turns {
            let pos = (turn) % 40;
            if pos == 0 {
                rows.push(curr_row);
                curr_row = "".to_string();
            }
            if (pos - 1..pos + 2).contains(&curr) {
                curr_row.push('#');
            } else {
                curr_row.push('.');
            }
            turn += 1;
            // println!(
            //     "{}, {}, {}, {:?}, {}",
            //     pos,
            //     curr,
            //     curr_row,
            //     line,
            //     curr_row.len()
            // )
        }
        curr += v;
    }
    rows.push(curr_row);
    println!("{}", rows.len());
    for row in rows {
        println!("{}", row);
    }
    return result;
}

fn main() {
    let contents_sample =
        fs::read_to_string(SAMPLE_INPUT_FILENAME).expect("Should have been able to read the file");
    let parsed_input_sample = parse_input(contents_sample);
    let contents_sample_large =
        fs::read_to_string("larger_sample.txt").expect("Should have been able to read the file");
    let parsed_input_sample_large = parse_input(contents_sample_large);
    let contents_actual =
        fs::read_to_string(INPUT_FILENAME).expect("Should have been able to read the file");
    let parsed_input_actual = parse_input(contents_actual);

    let sample_result_1 = puzzle1(&parsed_input_sample);
    assert_eq!(sample_result_1, 0);
    let sample_result_1_large = puzzle1(&parsed_input_sample_large);
    assert_eq!(sample_result_1_large, 13140);
    // let sample_result_2 = puzzle2(&parsed_input_sample);
    // assert_eq!(sample_result_2, 0);
    let _sample_result_2_large = puzzle2(&parsed_input_sample_large);
    println!();

    let actual_result_1 = puzzle1(&parsed_input_actual);
    let actual_result_2 = puzzle2(&parsed_input_actual);

    println!("Day 10 - Puzzle 1");
    println!("The sample result is: {}", sample_result_1);
    println!("The large sample result is: {}", sample_result_1_large);
    println!("The result for the input is: {}", actual_result_1);
    println!("Day 10 - Puzzle 2");
    // println!("The sample result is: {}", sample_result_2);
    println!("The result for the input is: {}", actual_result_2);
}
