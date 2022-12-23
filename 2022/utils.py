import subprocess
import toml

days = [21]

def file_contents(d):
    string = """use std::fs;
use regex::Regex;

static INPUT_FILENAME: &str = "input.txt";

type InputType = Vec<(char, char)>;

fn parse_input(input: String) -> InputType {
    let mut result = InputType::new();
    let re =
        Regex::new(r#"Sensor at x=([-]?[0-9]*), y=([-]?[0-9]*): closest beacon is at x=([-]?[0-9]*), y=([-]?[0-9]*)"#).expect("This shouldn't break");

    for line in input.lines() {
        let _ = re
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
    }
    return result;
}

fn part1(input: InputType) -> i32 {
    let mut result = 0;
    return result;
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

    println!("Day DAYN - Part 1");
    println!("The result for the input is: {}", actual_result_1);
    println!("Day DAYN - Part 2");
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
        assert_eq!(sample_result_1, 0);
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
"""
    string = string.replace("DAYN", str(d))
    return string

def generate_files(days):
    data = toml.load("Cargo.toml")
    seen = set(data["workspace"]["members"])
    for d in days:
        day = "day{}".format(d)
        # Note, this crashes if it already exists, so we only hit the input endpoint once
        p = subprocess.run(["cargo", "new", "day{}".format(d), "--bin"])

        if p.returncode == 0:
            with open(day + "/" + 'src/main.rs', 'w') as f:
                f.write(file_contents(d))

            if day not in seen:
                data["workspace"]["members"].append(day)

            with open(day + "/" + "sample.txt", 'w') as f: pass
            with open(day + "/" + "input.txt", 'wb') as f: pass
    
    with open("Cargo.toml", "w") as toml_file:
        toml.dump(data, toml_file)


def main():
    generate_files(days)

if __name__ == '__main__':
    main()
