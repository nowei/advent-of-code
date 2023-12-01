use std::fs;

static SAMPLE: bool = false;

static FILENAME: &str = match SAMPLE {
    true => "sample.txt",
    false => "input.txt",
};

fn puzzle1(contents: String) {
    let mut current = 0;
    let mut best = 0;
    for line in contents.lines() {
        match line {
            "" => {
                if current > best {
                    best = current;
                }
                current = 0;
            }
            value => {
                current += value.parse::<i32>().expect("This should be an int");
            }
        }
    }
    if current > best {
        best = current;
    }
    println!();
    println!("Most Calories:\n{}", best);
}

fn puzzle2(contents: String) {
    let mut current = 0;
    let mut entries = Vec::new();
    for line in contents.lines() {
        match line {
            "" => {
                entries.push(current);
                current = 0;
            }
            value => {
                current += value.parse::<i32>().expect("This should be an int");
            }
        }
    }
    entries.push(current);
    entries.sort();
    let top3 = &entries[entries.len() - 3..];
    let total: i32 = top3.iter().sum();
    println!("The 3 elves carrying the most Calories total:\n{:?}", total);
}

fn main() {
    let contents = fs::read_to_string(FILENAME).expect("Should have been able to read the file");

    puzzle1(contents.clone());
    puzzle2(contents);
}
