use std::fs;

static SAMPLE_INPUT_FILENAME: &str = "sample.txt";
static INPUT_FILENAME: &str = "input.txt";

type ContentType = Vec<((u32, u32), (u32, u32))>;

fn parse_input(contents: String) -> ContentType {
    let mut result = ContentType::new();
    for line in contents.lines() {
        let vals = line
            .split(",")
            .into_iter()
            .map(|v| {
                v.split("-")
                    .into_iter()
                    .map(|i| i.parse::<u32>().expect("This should parse properly"))
                    .collect::<Vec<u32>>()
            })
            .collect::<Vec<Vec<u32>>>();
        let a = (vals[0][0], vals[0][1]);
        let b = (vals[1][0], vals[1][1]);
        result.push((a, b));
    }
    return result;
}

fn puzzle1(contents: &ContentType) -> i32 {
    let mut result = 0;
    for ((a_min, a_max), (b_min, b_max)) in contents {
        if (a_min <= b_min && b_max <= a_max) || (b_min <= a_min && a_max <= b_max) {
            result += 1;
        }
    }
    return result;
}

// Two possible cases
// Case 1: a_min <= b_min <= a_max
// a |-----------|
// b          |-----------|
// Case 2: b_min <= a_min <= b_max
// a          |-----------|
// b |-----------|
// Note:
// a     |--|
// b   |------|
// fits case 2
// Also note that it isn't just a_max >= b_min because
// we can have a case like
// a                     |--|
// b         |--|
fn puzzle2(contents: &ContentType) -> i32 {
    let mut result = 0;
    for ((a_min, a_max), (b_min, b_max)) in contents {
        if (a_min <= b_min && b_min <= a_max) || (b_min <= a_min && a_min <= b_max) {
            result += 1;
        }
    }
    return result;
}

fn main() {
    let contents_sample =
        fs::read_to_string(SAMPLE_INPUT_FILENAME).expect("Should have been able to read the file");
    let parsed_input_sample = parse_input(contents_sample);
    let contents_actual =
        fs::read_to_string(INPUT_FILENAME).expect("Should have been able to read the file");
    let parsed_input_actual = parse_input(contents_actual);

    let sample_result_1 = puzzle1(&parsed_input_sample);
    assert_eq!(sample_result_1, 2);
    let actual_result_1 = puzzle1(&parsed_input_actual);
    println!("Day 4 - Puzzle 1");
    println!("The sample result is: {}", sample_result_1);
    println!("The actual result is: {}", actual_result_1);

    let sample_result_2 = puzzle2(&parsed_input_sample);
    assert_eq!(sample_result_2, 4);
    let actual_result_2 = puzzle2(&parsed_input_actual);
    println!("Day 4 - Puzzle 2");
    println!("The sample result is: {}", sample_result_2);
    println!("The actual result is: {}", actual_result_2);
}
