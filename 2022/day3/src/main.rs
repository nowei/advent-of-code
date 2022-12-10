use std::collections::HashSet;
use std::fs;

static SAMPLE: bool = false;

static FILENAME: &str = match SAMPLE {
    true => "sample.txt",
    false => "input.txt",
};

type ContentType = Vec<String>;

fn parse_input(contents: String) -> ContentType {
    let mut result = ContentType::new();
    for line in contents.lines() {
        result.push(line.to_string());
    }
    return result;
}

fn puzzle6(contents: &ContentType) -> u32 {
    let mut result = 0;
    let large_a_val = 'A' as u32;
    let small_a_val = 'a' as u32;
    for line in contents {
        let half = line.len() / 2;
        let first = String::from(&line[..half]);
        let second = String::from(&line[half..]);
        let mut s1 = HashSet::new();
        for c in first.chars() {
            s1.insert(c);
        }
        let mut s2 = HashSet::new();
        for c in second.chars() {
            s2.insert(c);
        }
        for &c in s1.intersection(&s2) {
            if c.is_uppercase() {
                result += c as u32 - large_a_val + 27;
            } else {
                result += c as u32 - small_a_val + 1;
            }
        }
    }
    println!("The result is:\n{}", result);
    return result;
}

fn puzzle7(contents: &ContentType) -> u32 {
    let mut result = 0;
    let mut iterator = contents.iter();
    let mut i = 0;
    let large_a_val = 'A' as u32;
    let small_a_val = 'a' as u32;
    let mut letters = "abcdefghijklmnopqrstuvwxyz".to_owned();
    letters.push_str(&"abcdefghijklmnopqrstuvwxyz".to_uppercase().to_owned());
    let mut curr_group: HashSet<char> = HashSet::from_iter(letters.chars().into_iter());
    while let Some(s) = iterator.next() {
        let curr_set: HashSet<char> = HashSet::from_iter(s.chars().into_iter());
        curr_group = curr_group
            .intersection(&curr_set)
            .map(|c| *c)
            .collect::<HashSet<char>>();
        i += 1;

        if i % 3 == 0 {
            for &c in curr_group.iter() {
                if c.is_uppercase() {
                    result += c as u32 - large_a_val + 27;
                } else {
                    result += c as u32 - small_a_val + 1;
                }
            }
            curr_group = HashSet::from_iter(letters.chars().into_iter());
        }
    }
    println!("The result is:\n{}", result);
    return result;
}

fn main() {
    let contents = fs::read_to_string(FILENAME).expect("Should have been able to read the file");
    let parsed_input = parse_input(contents.clone());
    let result1 = puzzle6(&parsed_input);
    if SAMPLE {
        assert_eq!(result1, 157);
    }
    let result2 = puzzle7(&parsed_input);
    if SAMPLE {
        assert_eq!(result2, 70);
    }
}
