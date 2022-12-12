use std::fs;

static SAMPLE_INPUT_FILENAME: &str = "sample.txt";
static INPUT_FILENAME: &str = "input.txt";

type InputType = Vec<(char, char)>;

fn parse_input(input: String) -> InputType {
    let mut result = InputType::new();
    for line in input.lines() {}
    return result;
}

fn puzzle1(input: &InputType) -> i32 {
    let mut result = 0;
    return result;
}

fn puzzle2(input: &InputType) -> i32 {
    let mut result = 0;
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
    let sample_result_2 = puzzle2(&parsed_input_sample);
    assert_eq!(sample_result_2, 0);

    let actual_result_1 = puzzle1(&parsed_input_actual);
    let actual_result_2 = puzzle2(&parsed_input_actual);

    println!("Day 10 - Puzzle 1");
    println!("The sample result is: {}", sample_result_1);
    println!("The result for the input is: {}", actual_result_1);
    println!("Day 10 - Puzzle 2");
    println!("The sample result is: {}", sample_result_2);
    println!("The result for the input is: {}", actual_result_2);
}
