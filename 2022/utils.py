import subprocess
import toml

days = [4]

def file_contents(d):
    string = """use std::fs;

static SAMPLE_INPUT_FILENAME: &str = "sample.txt";
static INPUT_FILENAME: &str = "input.txt";

type ContentType = Vec<(char, char)>;

fn parse_input(contents: String) -> ContentType {
    let mut result = ContentType::new();
    for line in contents.lines() {
        
    }
    return result;
}

fn puzzle1(contents: &ContentType) -> i32 {
    let mut result = 0;
    return result;
}

fn puzzle2(contents: &ContentType) -> i32 {
    let mut result = 0;
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
    assert_eq!(sample_result_1, 0);
    let actual_result_1 = puzzle1(&parsed_input_actual);
    println!("Day DAYN - Puzzle 1");
    println!("The sample result is: {}", sample_result_1);
    println!("The actual result is: {}", actual_result_1);

    let sample_result_2 = puzzle2(&parsed_input_sample);
    assert_eq!(sample_result_2, 0);
    let actual_result_2 = puzzle2(&parsed_input_actual);
    println!("Day DAYN - Puzzle 2");
    println!("The sample result is: {}", sample_result_2);
    println!("The actual result is: {}", actual_result_2);
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

        with open(day + "/" + "sample.txt", 'w') as f: pass
        with open(day + "/" + "input.txt", 'wb') as f: pass

        if p.returncode == 0:
            with open(day + "/" + 'src/main.rs', 'w') as f:
                f.write(file_contents(d))

            if day not in seen:
                data["workspace"]["members"].append(day)
    
    with open("Cargo.toml", "w") as toml_file:
        toml.dump(data, toml_file)


def main():
    generate_files(days)

if __name__ == '__main__':
    main()
