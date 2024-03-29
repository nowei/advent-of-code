use std::{collections::HashMap, fs};

static SAMPLE_INPUT_FILENAME: &str = "sample.txt";
static INPUT_FILENAME: &str = "input.txt";

type InputType = Vec<Monkey>;

struct Monkey {
    index: u32,
    items: Vec<u32>,
    operation: Operation,
    test_num: u32,
    true_monkey: usize,
    false_monkey: usize,
    inspected: i32,
}

impl Monkey {
    fn inspect(&self, old: u32) -> u32 {
        (self.operation)(old.into()).try_into().unwrap()
    }

    fn inspect2(&self, old: u64) -> u64 {
        (self.operation)(old.try_into().unwrap())
            .try_into()
            .unwrap()
    }

    fn test(&self, val: u32) -> bool {
        return val % self.test_num == 0;
    }
}

type Operation = Box<dyn Fn(i64) -> i64>;

fn parse_operation(op_string: &String) -> Operation {
    let args = op_string.split(" ").collect::<Vec<_>>();
    match args[..] {
        ["old", "*", "old"] => return Box::new(move |old| old * old),
        ["old", "*", y] => {
            let y: i64 = y.parse().unwrap();
            return Box::new(move |old| old * y);
        }
        ["old", "+", y] => {
            let y: i64 = y.parse().unwrap();
            return Box::new(move |old| old + y);
        }
        _ => panic!("This shouldn't happen"),
    };
}

// fn evaluate_operation

fn parse_input(input: String) -> InputType {
    let mut result = InputType::new();
    for monkey_string in input.split("Monkey ") {
        if monkey_string.is_empty() {
            continue;
        }
        let mut iter = monkey_string.lines().into_iter();
        let index = iter
            .next()
            .expect("Should exist")
            .strip_suffix(":")
            .expect("this should exist")
            .parse::<u32>()
            .expect("Parsing should work");
        let starting_items = iter
            .next()
            .expect("there should be a next")
            .split("items: ")
            .into_iter()
            .last()
            .expect("This should exist")
            .split(", ")
            .map(|v| v.parse::<u32>().expect("This should parse"))
            .collect::<Vec<u32>>();
        let operation_str = iter
            .next()
            .expect("This should exist")
            .split(" = ")
            .map(|v| v.to_string())
            .collect::<Vec<String>>();
        let operation_string = operation_str.get(1).expect("This should exist");
        let operation = parse_operation(&operation_string);
        let test_num_vec = iter
            .next()
            .expect("This should exist")
            .split(" by ")
            .map(|v| v.to_string())
            .collect::<Vec<String>>();
        let test_num = test_num_vec
            .get(1)
            .expect("This should exist")
            .parse::<u32>()
            .expect("Parse should work");
        let true_monkey = iter
            .next()
            .expect("This should exist")
            .split(" monkey ")
            .into_iter()
            .last()
            .expect("This should exist")
            .parse::<usize>()
            .expect("This should parse");
        let false_monkey = iter
            .next()
            .expect("This should exist")
            .split(" monkey ")
            .into_iter()
            .last()
            .expect("This should exist")
            .parse::<usize>()
            .expect("This should parse");
        result.push(Monkey {
            index: index,
            items: starting_items,
            operation,
            test_num,
            true_monkey,
            false_monkey,
            inspected: 0,
        })
    }
    return result;
}

fn puzzle1(mut input: InputType) -> i32 {
    let mut result = 0;
    for round in 1..21 {
        for i in 0..input.len() {
            let changes = {
                let m = &mut input[i];
                let mut hash_map: HashMap<usize, Vec<u32>> = HashMap::new();
                hash_map.insert(m.true_monkey, Vec::new());
                hash_map.insert(m.false_monkey, Vec::new());
                for old in &m.items {
                    let new = m.inspect(*old) / 3;
                    if m.test(new) {
                        hash_map
                            .get_mut(&m.true_monkey)
                            .expect("This should work")
                            .push(new);
                    } else {
                        hash_map
                            .get_mut(&m.false_monkey)
                            .expect("This should work")
                            .push(new);
                    }
                    m.inspected += 1;
                }
                m.items = vec![];
                hash_map
            };
            for (i, v) in changes {
                let m = &mut input[i];
                m.items.extend(v);
            }
        }
        println!("Round {}", round);
        for m in &input {
            println!("Monkey {}: {:?} {}", m.index, m.items, m.inspected);
        }
    }
    let mut v = input.iter().map(|m| m.inspected).collect::<Vec<i32>>();
    v.sort();
    result = v.iter().rev().take(2).product();
    return result;
}

fn puzzle2(mut input: InputType) -> i64 {
    let mut result = 0i64;
    let rounds = vec![
        1, 20, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000,
    ];
    // We need some sort of modular arithmetic here because we can't compute with large numbers efficiently.
    // Initially had the idea of multiplying the factors together, but was unsure about whether to use that number
    // or a prime larger than that.
    // a % n = b, we keep track of all mods smaller than the largest mod by modding by the product of all prime checks
    // this guarantees that the information for 0..prod capture the mod relation without losing information.
    // Apparently this is also called the Chinese remainder theorem.

    let large_prime: u64 = input.iter().map(|m| m.test_num as u64).product();
    for round in 1..10001 {
        for i in 0..input.len() {
            let changes = {
                let m = &mut input[i];
                let mut hash_map: HashMap<usize, Vec<u32>> = HashMap::new();
                hash_map.insert(m.true_monkey, Vec::new());
                hash_map.insert(m.false_monkey, Vec::new());
                for old in &m.items {
                    let new: u64 = m.inspect2((*old).into()) % large_prime;
                    if m.test(new.try_into().unwrap()) {
                        hash_map
                            .get_mut(&m.true_monkey)
                            .expect("This should work")
                            .push(new.try_into().unwrap());
                    } else {
                        hash_map
                            .get_mut(&m.false_monkey)
                            .expect("This should work")
                            .push(new.try_into().unwrap());
                    }
                    m.inspected += 1;
                }
                m.items = vec![];
                hash_map
            };
            for (i, v) in changes {
                let m = &mut input[i];
                m.items.extend(v);
            }
        }
        if rounds.contains(&round) {
            println!("Round {}", round);
            for m in &input {
                println!("Monkey {}: {:?} {}", m.index, m.items, m.inspected);
            }
        }
    }
    let mut v = input
        .iter()
        .map(|m| m.inspected as i64)
        .collect::<Vec<i64>>();
    v.sort();
    result = v.iter().rev().take(2).product();
    return result;
}

fn main() {
    let contents_sample =
        fs::read_to_string(SAMPLE_INPUT_FILENAME).expect("Should have been able to read the file");
    let contents_actual =
        fs::read_to_string(INPUT_FILENAME).expect("Should have been able to read the file");

    let sample_result_1 = puzzle1(parse_input(contents_sample.clone()));
    assert_eq!(sample_result_1, 10605);
    let sample_result_2 = puzzle2(parse_input(contents_sample.clone()));
    assert_eq!(sample_result_2, 2713310158);

    let actual_result_1 = puzzle1(parse_input(contents_actual.clone()));
    let actual_result_2 = puzzle2(parse_input(contents_actual.clone()));

    println!("Day 11 - Puzzle 1");
    println!("The sample result is: {}", sample_result_1);
    println!("The result for the input is: {}", actual_result_1);
    println!("Day 11 - Puzzle 2");
    println!("The sample result is: {}", sample_result_2);
    println!("The result for the input is: {}", actual_result_2);
}
