import subprocess
import toml
import requests

days = [2]

def file_contents(d):
    string = """use std::env;
use std::fs;

static SAMPLE: bool = true;

static FILENAME: &str = match SAMPLE {
    true => "sample.txt",
    false => "input.txt",
};

fn puzzleDAYN1(contents: String) {
    let result = 0;
    println!("The result is:\\n{}", result);
    return result;
}

fn puzzleDAYN2(contents: String) {
    let result = 0;
    println!("The result is:\\n{}", result);
    return result;
}

fn main() {
    let contents = fs::read_to_string(FILENAME)
        .expect("Should have been able to read the file");
    let result1 = puzzleDAYN1(contents);
    if SAMPLE {
        assert_eq!(result1, 0);
    }
    let result2 = puzzleDAYN2(contents);
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
        p = subprocess.run(["cargo", "new", "day{}".format(d), "--bin"])

        with open(day + "/" + "sample.txt", 'w') as f: pass
        req = requests.get("https://adventofcode.com/2022/day/{}/input".format(d))
        with open(day + "/" + "input.txt", 'w') as f:
            f.write(req.contents)

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
