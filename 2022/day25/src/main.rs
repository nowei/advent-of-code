use std::fs;

static INPUT_FILENAME: &str = "input.txt";

type InputType = Vec<String>;

fn parse_input(input: String) -> InputType {
    let mut result = InputType::new();

    for line in input.lines() {
        result.push(line.to_string());
    }
    return result;
}

fn to_decimal(val: String) -> i64 {
    let mut total = 0;
    let base = 5;
    let mut digit_scale = 1;
    for c in val.chars().rev() {
        let v = match c {
            '2' => 2 * digit_scale,
            '1' => 1 * digit_scale,
            '0' => 0 * digit_scale,
            '-' => -1 * digit_scale,
            '=' => -2 * digit_scale,
            _ => panic!("shouldn't get here ever"),
        };
        total += v;
        digit_scale *= base;
    }

    return total;
}

fn to_snafu(val: i64) -> String {
    let mut largest = 0;
    let base = 5;
    let mut digit_scale = 1;
    let mut num_evals = 1;
    // The start of the number should be lower than than the number of things we're at
    while largest < val {
        digit_scale *= base;
        largest = digit_scale * 2;
        num_evals += 1;
    }
    let mut result: Vec<String> = vec![];

    // first digit must either be a 1 or a 2
    // If we can reach the remainder with the remaining range of digits,
    // then this is the path we should go down.
    // 20 => => 1[==] = 13 to 1[22] = 37 (range of 12) (range is +/- 5^n / 2)
    // vs. 0[==] = to -12 to 0[22] = 12 or 2[==] = 38 to 2[22] = 62
    //
    let eval_order = vec!['2', '1', '0', '-', '='];

    let mut curr_val = 0;

    let target = val;

    println!("{}", num_evals);

    while num_evals > 0 {
        let interval = base.pow(num_evals - 1);
        let diff = interval / 2;
        for c in &eval_order {
            let influence = match c {
                '2' => 2 * interval,
                '1' => 1 * interval,
                '0' => 0 * interval,
                '-' => -1 * interval,
                '=' => -2 * interval,
                _ => panic!("Shouldn't get here"),
            };

            let curr_max = curr_val + influence + diff;
            let curr_min = curr_val + influence - diff;
            if target <= curr_max && target >= curr_min {
                println!(
                    "target {} within [{}, {}] num evals remaining {}",
                    target, curr_min, curr_max, num_evals
                );
                curr_val += influence;
                result.push(c.to_string());
                break;
            }
        }
        num_evals -= 1;
    }

    if result.get(0).expect("should exist") == &"0".to_string() {
        result.remove(0);
    }

    return result.join("");
}

fn part1(input: InputType) -> String {
    let mut temp = 0;
    for snafu in input {
        temp += to_decimal(snafu);
    }
    return to_snafu(temp);
}

fn part2(input: InputType) -> i32 {
    let mut result = 0;

    return result;
}

fn main() {
    let contents_actual =
        fs::read_to_string(INPUT_FILENAME).expect("Should have been able to read the file");
    let parsed_input_actual_1 = parse_input(contents_actual.clone());
    let parsed_input_actual_2 = parse_input(contents_actual);

    let actual_result_1 = part1(parsed_input_actual_1);
    let actual_result_2 = part2(parsed_input_actual_2);

    println!("Day 25 - Part 1");
    println!("The result for the input is: {}", actual_result_1);
    println!("Day 25 - Part 2");
    println!("The result for the input is: {}", actual_result_2);
}

#[cfg(test)]
mod tests {
    use crate::{parse_input, part1, part2, to_decimal, to_snafu};
    use std::fs;

    static SAMPLE_INPUT_FILENAME: &str = "sample.txt";

    #[test]
    fn test_to_snafu() {
        assert_eq!(to_snafu(1), "1");
        assert_eq!(to_snafu(2), "2");
        assert_eq!(to_snafu(3), "1=");
        assert_eq!(to_snafu(4), "1-");
        assert_eq!(to_snafu(5), "10");
        assert_eq!(to_snafu(6), "11");
        assert_eq!(to_snafu(7), "12");
        assert_eq!(to_snafu(8), "2=");
        assert_eq!(to_snafu(9), "2-");
        assert_eq!(to_snafu(10), "20");
        assert_eq!(to_snafu(15), "1=0");
        assert_eq!(to_snafu(20), "1-0");
        assert_eq!(to_snafu(2022), "1=11-2");
        assert_eq!(to_snafu(12345), "1-0---0");
        assert_eq!(to_snafu(314159265), "1121-1110-1=0");
    }

    #[test]
    fn test_to_decimal() {
        assert_eq!(to_decimal("1=-0-2".to_string()), 1747);
        assert_eq!(to_decimal("12111".to_string()), 906);
        assert_eq!(to_decimal("2=0=".to_string()), 198);
        assert_eq!(to_decimal("21".to_string()), 11);
        assert_eq!(to_decimal("2=01".to_string()), 201);
        assert_eq!(to_decimal("111".to_string()), 31);
        assert_eq!(to_decimal("20012".to_string()), 1257);
        assert_eq!(to_decimal("112".to_string()), 32);
        assert_eq!(to_decimal("1=-1=".to_string()), 353);
        assert_eq!(to_decimal("1-12".to_string()), 107);
        assert_eq!(to_decimal("12".to_string()), 7);
        assert_eq!(to_decimal("1=".to_string()), 3);
        assert_eq!(to_decimal("122".to_string()), 37);
    }

    #[test]
    fn test_part1() {
        let contents_sample = fs::read_to_string(SAMPLE_INPUT_FILENAME)
            .expect("Should have been able to read the file");
        let parsed_input_sample = parse_input(contents_sample);
        let sample_result_1 = part1(parsed_input_sample);
        assert_eq!(sample_result_1, "2=-1=0");
    }

    #[test]
    fn test_part2() {
        let contents_sample = fs::read_to_string(SAMPLE_INPUT_FILENAME)
            .expect("Should have been able to read the file");
        let parsed_input_sample = parse_input(contents_sample);
        let sample_result_2 = part2(parsed_input_sample);
        assert_eq!(sample_result_2, 0);
    }
}
