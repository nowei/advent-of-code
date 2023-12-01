use std::collections::BTreeMap;
use std::fs;

static SAMPLE_INPUT_FILENAME: &str = "sample.txt";
static INPUT_FILENAME: &str = "input.txt";

type ContentType = Vec<String>;

fn parse_input(contents: String) -> ContentType {
    let mut result = ContentType::new();
    for line in contents.lines() {
        result.push(line.to_string());
    }
    return result;
}

fn puzzle1(contents: &ContentType, start_marker: usize) -> Vec<i32> {
    let mut result: Vec<i32> = Vec::new();
    let start = start_marker - 1;
    for line in contents {
        let mut map: BTreeMap<u8, i32> = BTreeMap::new();
        let bytes = line.as_bytes();
        for i in 0..start {
            let key = bytes[i];
            map.insert(key, map.get(&key).unwrap_or(&0) + 1);
        }
        let mut unique = map.len();
        for i in start..bytes.len() {
            let key = bytes[i];
            map.insert(key, map.get(&key).unwrap_or(&0) + 1);
            if *map.get(&key).expect("This should exist") == 1 {
                unique += 1;
            }
            if unique == start_marker {
                result.push((i + 1).try_into().unwrap());
                break;
            }
            let rem_key = bytes[i - start];
            map.insert(rem_key, map.get(&rem_key).expect("This should exist") - 1);
            if *map.get(&rem_key).expect("This should exist") == 0 {
                unique -= 1;
            }
        }
    }
    println!("{:?}", result);
    return result;
}

fn main() {
    let contents_sample =
        fs::read_to_string(SAMPLE_INPUT_FILENAME).expect("Should have been able to read the file");
    let parsed_input_sample = parse_input(contents_sample);
    let contents_actual =
        fs::read_to_string(INPUT_FILENAME).expect("Should have been able to read the file");
    let parsed_input_actual = parse_input(contents_actual);

    let sample_result_1 = puzzle1(&parsed_input_sample, 4);
    assert_eq!(sample_result_1, vec![7, 5, 6, 10, 11]);
    let actual_result_1 = puzzle1(&parsed_input_actual, 4);
    println!("Day 6 - Puzzle 1");
    println!("The sample result is: {:?}", sample_result_1);
    println!("The actual result is: {:?}", actual_result_1);

    let sample_result_2 = puzzle1(&parsed_input_sample, 14);
    assert_eq!(sample_result_2, vec![19, 23, 23, 29, 26]);
    let actual_result_2 = puzzle1(&parsed_input_actual, 14);
    println!("Day 6 - Puzzle 2");
    println!("The sample result is: {:?}", sample_result_2);
    println!("The actual result is: {:?}", actual_result_2);
}
