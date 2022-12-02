import subprocess
import toml
import requests
import os

days = [2]

def file_contents(d):
    string = """use std::fs;

static SAMPLE: bool = true;

static FILENAME: &str = match SAMPLE {
    true => "sample.txt",
    false => "input.txt",
};

type ContentType = Vec<(char, char)>;

fn parse_input(contents: String) -> ContentType {
    let mut result = ContentType::new();
    for line in contents.lines() {
        
    }
    return result;
}

fn puzzleDAYN1(contents: &ContentType) -> i32 {
    let mut result = 0;
    println!("The result is:\n{}", result);
    return result;
}

fn puzzleDAYN2(contents: &ContentType) -> i32 {
    let mut result = 0;
    println!("The result is:\n{}", result);
    return result;
}

fn main() {
    let contents = fs::read_to_string(FILENAME)
        .expect("Should have been able to read the file");
    let parsed_input = parse_input(contents);
    let result1 = puzzleDAYN1(&parsed_input);
    if SAMPLE {
        assert_eq!(result1, 0);
    }
    let result2 = puzzleDAYN2(&parsed_input);
    if SAMPLE {
        assert_eq!(result2, 0);
    }
}

"""
    string = string.replace("DAYN1", str(d * 2))
    string = string.replace("DAYN2", str(d * 2 + 1))
    return string

def generate_files(days):
    data = toml.load("Cargo.toml")
    seen = set(data["workspace"]["members"])
    for d in days:
        day = "day{}".format(d)
        # Note, this crashes if it already exists, so we only hit the input endpoint once
        p = subprocess.run(["cargo", "new", "day{}".format(d), "--bin"])

        with open(day + "/" + "sample.txt", 'w') as f: pass
        req = requests.get(
            "https://adventofcode.com/2022/day/{}/input".format(d),
            cookies={"session": os.environ["AOC_SESSION_ID"]}
        )
        with open(day + "/" + "input.txt", 'wb') as f:
            f.write(req.content)

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
