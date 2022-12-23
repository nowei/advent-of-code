use queue::Queue;
use regex::Regex;
use std::{collections::HashMap, fs};

static INPUT_FILENAME: &str = "input.txt";

type InputType = HashMap<String, DependencyMonkey>;

#[derive(Debug)]
struct DependencyMonkey {
    name: String,
    children: Vec<String>,
    parents: Vec<String>,
    value: i64,
    op: Option<(String, String, String)>,
}

impl DependencyMonkey {
    fn can_queue(&self, vals: &HashMap<String, i64>) -> bool {
        for p in &self.parents {
            if !vals.contains_key(p) {
                return false;
            }
        }
        return true;
    }

    fn eval(&self, vals: &HashMap<String, i64>) -> i64 {
        let (a_str, op, b_str) = self
            .op
            .as_ref()
            .expect("This should only be called on op monkeys");
        let a = vals.get(a_str).expect("should exist at this point").clone();
        let b = vals.get(b_str).expect("should exist at this point").clone();
        println!("{} {} {}", a, op, b);
        match op.as_str() {
            "*" => a * b,
            "-" => a - b,
            "+" => a + b,
            "/" => a / b,
            "=" => {
                if a == b {
                    return 1;
                } else {
                    return 0;
                }
            }
            _ => panic!("should just be those options"),
        }
    }

    fn reverse_eval(&self, target_val: i64, vals: &mut HashMap<String, i64>) -> i64 {
        let (a_str, op, b_str) = self
            .op
            .as_ref()
            .expect("This should only be called on op monkeys");
        let unknown_monkey = if vals.contains_key(a_str) {
            b_str
        } else {
            a_str
        };
        // target_val = a [op] b
        // if we know b, then if [op] == +, a = target_val - b
        //                    if [op] == -, a = b + target_val
        //                    if [op] == *, a = target_val / b
        //                    if [op] == /, a = b * target_val
        // if we know a, then if [op] == +, b = target_val - a
        //                    if [op] == -, b = a - target_val
        //                    if [op] == *, b = target_val / a
        //                    if [op] == /, b = a / target_val
        let new_target_val = if unknown_monkey == a_str {
            let b = vals.get(b_str).expect("should exist");
            match op.as_str() {
                "+" => target_val - b,
                "-" => b + target_val,
                "*" => target_val / b,
                "/" => b * target_val,
                _ => panic!("shouldn't get here"),
            }
        } else {
            let a = vals.get(a_str).expect("should exist");
            match op.as_str() {
                "+" => target_val - a,
                "-" => a - target_val,
                "*" => target_val / a,
                "/" => a / target_val,
                _ => panic!("shouldn't get here"),
            }
        };

        // update vals
        vals.insert(unknown_monkey.to_string(), new_target_val);
        return new_target_val;
    }
}

fn parse_input(input: String) -> InputType {
    let mut result = InputType::new();
    let re = Regex::new(r#"(.*): (((.*) (.*) (.*))|(.*))"#).expect("This shouldn't break");

    for line in input.lines() {
        let curr = re
            .captures(line)
            .and_then(|cap| {
                let group = (
                    cap.get(1),
                    cap.get(2),
                    cap.get(3),
                    cap.get(4),
                    cap.get(5),
                    cap.get(6),
                );
                match group {
                    (
                        Some(monkey),
                        Some(_full_group),
                        Some(_full_cap),
                        Some(a),
                        Some(op),
                        Some(b),
                    ) => Some((monkey.as_str(), a.as_str(), op.as_str(), b.as_str())),
                    (Some(monkey), Some(val), None, None, None, None) => {
                        Some((monkey.as_str(), val.as_str(), "", ""))
                    }
                    _ => None,
                }
            })
            .expect("Should work");
        let monkey = match curr {
            (monkey, val, "", "") => DependencyMonkey {
                name: monkey.to_string(),
                children: vec![],
                parents: vec![],
                value: val.parse::<i64>().expect("should parse properly"),
                op: None,
            },
            (monkey, a, op, b) => DependencyMonkey {
                name: monkey.to_string(),
                children: vec![],
                parents: vec![a.to_string(), b.to_string()],
                value: 0,
                op: Some((a.to_string(), op.to_string(), b.to_string())),
            },
            _ => panic!("Shouldn't get here"),
        };
        result.insert(monkey.name.clone(), monkey);
    }

    let keys: Vec<String> = result
        .keys()
        .clone()
        .into_iter()
        .map(|v| v.clone())
        .collect();
    for m in keys {
        let curr_monkey = result.get(&m).expect("monkey should exist");
        for p in curr_monkey.parents.clone() {
            let parent_monkey = result.get_mut(&p).expect("should work");
            parent_monkey.children.push(m.clone());
        }
    }
    return result;
}

fn part1(input: InputType) -> i64 {
    let mut result = 0;
    let mut queue: Queue<String> = Queue::new();
    for (name, monkey) in &input {
        if monkey.parents.is_empty() {
            queue.queue(name.to_string()).expect("should work");
        }
    }

    let mut map_vals: HashMap<String, i64> = HashMap::new();
    while let Some(name) = queue.dequeue() {
        let monkey = input.get(&name).expect("should exist");
        if let Some(op) = &monkey.op {
            let value = monkey.eval(&map_vals);
            map_vals.insert(name, value);
        } else {
            map_vals.insert(name, monkey.value);
        }

        for child in &monkey.children {
            let child_monkey = input.get(child).expect("should be fine");
            if child_monkey.can_queue(&map_vals) {
                queue.queue(child.clone());
            }
        }
    }

    result = *map_vals.get("root").expect("should exist");

    return result;
}

fn part2(input: InputType) -> i64 {
    let mut result = 0;
    // We want to replace humn's value, so we can take it out and evaluate it last so we can determine what values are left that need to be determined.
    // We can work our way down one side of the root monkey

    let mut queue: Queue<String> = Queue::new();
    for (name, monkey) in &input {
        if monkey.parents.is_empty() && name != "humn" {
            queue.queue(name.to_string()).expect("should work");
        }
    }
    let mut map_vals: HashMap<String, i64> = HashMap::new();
    while let Some(name) = queue.dequeue() {
        let monkey = input.get(&name).expect("should exist");
        if let Some(op) = &monkey.op {
            let value = monkey.eval(&map_vals);
            map_vals.insert(name, value);
        } else {
            map_vals.insert(name, monkey.value);
        }

        for child in &monkey.children {
            let child_monkey = input.get(child).expect("should be fine");
            if child_monkey.can_queue(&map_vals) {
                queue.queue(child.clone());
            }
        }
    }

    // We can find the root value we need to match?
    println!("monkeys evaluated: {}", map_vals.len());
    println!("monkeys to be evaluated: {}", input.len() - map_vals.len());
    let root_monkey = input.get("root").expect("should exist");

    let mut unevaluated_parents_order: Vec<String> = vec![];
    let mut target_val = 0;
    for p in &root_monkey.parents {
        if map_vals.contains_key(p) {
            target_val = *map_vals.get(p).expect("should exist");
            println!("{} {}", p, target_val);
        } else {
            println!("We need to find the value of {}", p);
            unevaluated_parents_order.push(p.clone());
        }
    }

    loop {
        let curr = unevaluated_parents_order
            .iter()
            .last()
            .expect("should exist");
        let curr_monkey = input.get(curr).expect("should exist");
        if curr_monkey.parents.len() == 0 {
            // Special case this is actually humn, but we should have a value for this by then?
            break;
        }
        for p in &curr_monkey.parents {
            if map_vals.contains_key(p) {
                println!("{} {}", p, map_vals.get(p).expect("should exist"));
            } else {
                println!("We need to find the value of {}", p);
                unevaluated_parents_order.push(p.clone());
            }
        }
        // reverse eval with the target and known op
        target_val = curr_monkey.reverse_eval(target_val, &mut map_vals);
    }

    result = *map_vals.get("humn").expect("should exist");
    return result;
}

fn main() {
    let contents_actual =
        fs::read_to_string(INPUT_FILENAME).expect("Should have been able to read the file");
    let parsed_input_actual_1 = parse_input(contents_actual.clone());
    let parsed_input_actual_2 = parse_input(contents_actual);

    let actual_result_1 = part1(parsed_input_actual_1);
    let actual_result_2 = part2(parsed_input_actual_2);

    println!("Day 21 - Part 1");
    println!("The result for the input is: {}", actual_result_1);
    println!("Day 21 - Part 2");
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
        assert_eq!(sample_result_1, 152);
    }

    #[test]
    fn test_part2() {
        let contents_sample = fs::read_to_string(SAMPLE_INPUT_FILENAME)
            .expect("Should have been able to read the file");
        let parsed_input_sample = parse_input(contents_sample);
        let sample_result_2 = part2(parsed_input_sample);
        assert_eq!(sample_result_2, 301);
    }
}
