use itertools::Itertools;
use std::fs;

static SAMPLE: bool = false;

static FILENAME: &str = match SAMPLE {
    true => "sample.txt",
    false => "input.txt",
};

type ContentType = Vec<(i32, i32)>;

fn parse_input(contents: String) -> ContentType {
    let mut result = ContentType::new();
    for line in contents.lines() {
        let (a, b) = line
            .split(" ")
            .map(|v| v.chars().nth(0).expect("This should have an character"))
            .collect_tuple()
            .expect("This should work");

        let first = match a {
            'A' => 1,
            'B' => 2,
            'C' => 3,
            _ => 0,
        };
        let second = match b {
            'X' => 1,
            'Y' => 2,
            'Z' => 3,
            _ => 0,
        };
        result.push((first, second));
    }
    return result;
}

fn puzzle4(contents: &ContentType) -> i32 {
    let mut result = 0;
    for (a, b) in contents {
        if a == b {
            result += 3;
        } else {
            if a % 3 + 1 == *b {
                result += 6;
            }
        }
        result += b
    }
    println!("The result is:\n{}", result);
    return result;
}

fn puzzle5(contents: &ContentType) -> i32 {
    let mut result = 0;
    for (a, b) in contents {
        if *b == 1 {
            // lose
            let mut temp = a - 1 % 3;
            if temp == 0 {
                temp = 3;
            }
            result += temp;
        } else if *b == 2 {
            // draw
            result += a + 3;
        } else if *b == 3 {
            // win
            result += (a % 3 + 1) + 6;
        }
    }
    println!("The result is:\n{}", result);
    return result;
}

fn main() {
    let contents = fs::read_to_string(FILENAME).expect("Should have been able to read the file");
    let parsed_input = parse_input(contents);
    let result1 = puzzle4(&parsed_input);
    if SAMPLE {
        assert_eq!(result1, 15);
    }
    let result2 = puzzle5(&parsed_input);
    if SAMPLE {
        assert_eq!(result2, 12);
    }
}
