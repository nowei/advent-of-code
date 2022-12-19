use std::{cmp::Ordering, fmt, fs};

static INPUT_FILENAME: &str = "input.txt";

type InputType = Vec<(VecOrVal, VecOrVal)>;

#[derive(Debug)]
struct VecOrVal {
    val: i32,
    children: Vec<VecOrVal>,
    is_val: bool,
}
impl VecOrVal {
    fn get_string(&self) -> String {
        if self.is_val {
            return format!("{}", self.val);
        } else {
            let mut v = vec![];
            for child in &self.children {
                v.push(child.get_string());
            }
            return format!("[{}]", v.join(","));
        }
    }
}

impl PartialOrd for VecOrVal {
    fn partial_cmp(&self, other: &VecOrVal) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl PartialEq for VecOrVal {
    fn eq(&self, other: &Self) -> bool {
        self.cmp(other) == Ordering::Equal
    }
}

impl Eq for VecOrVal {}

impl Ord for VecOrVal {
    fn cmp(&self, other: &VecOrVal) -> Ordering {
        if self.is_val && other.is_val {
            if self.val < other.val {
                return Ordering::Less;
            } else if self.val > other.val {
                return Ordering::Greater;
            }
        } else if self.is_val {
            return VecOrVal {
                val: 0,
                children: vec![VecOrVal {
                    val: self.val,
                    children: vec![],
                    is_val: true,
                }],
                is_val: false,
            }
            .cmp(other);
        } else if other.is_val {
            return self.cmp(&VecOrVal {
                val: 0,
                children: vec![VecOrVal {
                    val: other.val,
                    children: vec![],
                    is_val: true,
                }],
                is_val: false,
            });
        } else {
            // Both are lists
            for i in 0..self.children.len().min(other.children.len()) {
                let curr = &self.children[i].cmp(&other.children[i]);
                if *curr != Ordering::Equal {
                    return *curr;
                }
            }
            if self.children.len() < other.children.len() {
                return Ordering::Less;
            } else if self.children.len() > other.children.len() {
                return Ordering::Greater;
            }
        }

        return Ordering::Equal;
    }
}

impl fmt::Display for VecOrVal {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.get_string())
    }
}

// impl IntoIterator for VecOrVal {
//     // (val, (depth, index))
//     type Item = (i32, (usize, usize));
//     type IntoIter = VecOrValIterator;
//     fn into_iter(self) -> Self::IntoIter {
//         VecOrValIterator {
//             obj: self,
//             index: vec![],
//         }
//     }
// }

// pub struct VecOrValIterator {
//     obj: VecOrVal,
//     index: Vec<usize>,
// }

// impl Iterator for VecOrValIterator {
//     type Item = (i32, (usize, usize));
//     fn next(&mut self) -> Option<(i32, (usize, usize))> {
//         let curr = self.obj;
//         if self.index.is_empty() {
//             // init case, we look for a valid value (not an array)
//             while !curr.is_val {

//             }
//         }
//         Some(result)
//     }
// }

fn process_str(input: String) -> VecOrVal {
    let mut levels: Vec<Vec<VecOrVal>> = vec![];
    let mut curr_num = "".to_string();
    let mut result: Option<VecOrVal> = Option::None;
    for c in input.chars() {
        if c == '[' {
            // Start a new array
            levels.push(vec![]);
        } else {
            let mut curr_level = levels.pop().expect("Should be non-empty");
            if c == ']' {
                // End an array
                if !curr_num.is_empty() {
                    curr_level.push(VecOrVal {
                        val: curr_num.parse::<i32>().expect("This should work"),
                        children: vec![],
                        is_val: true,
                    });
                    curr_num = "".to_string();
                }
                if levels.is_empty() {
                    result = Some(VecOrVal {
                        val: 0,
                        children: curr_level,
                        is_val: false,
                    });
                } else {
                    let mut last_level = levels
                        .pop()
                        .expect("We should be able to put it in something");
                    last_level.push(VecOrVal {
                        val: 0,
                        children: curr_level,
                        is_val: false,
                    });
                    levels.push(last_level);
                }
            } else if c == ',' {
                if !curr_num.is_empty() {
                    curr_level.push(VecOrVal {
                        val: curr_num.parse::<i32>().expect("This should work"),
                        children: vec![],
                        is_val: true,
                    });
                    curr_num = "".to_string();
                }
                levels.push(curr_level);
            } else {
                // Still a number
                curr_num.push(c);
                levels.push(curr_level);
            }
        }
    }

    return result.unwrap();
}

fn parse_input(input: String) -> InputType {
    let mut result = InputType::new();
    let mut iter = input.lines().into_iter().peekable();
    while iter.peek().is_some() {
        let left = process_str(iter.next().expect("This should exist").to_string());
        let right = process_str(iter.next().expect("This should exist").to_string());
        result.push((left, right));
        iter.next(); // Should be empty or last line
    }
    return result;
}

fn part1(input: InputType) -> i32 {
    let mut result = 0;
    let mut i = 1;
    for (left, right) in input {
        if left.cmp(&right) == Ordering::Less {
            result += i;
        }
        i += 1;
    }
    return result;
}

fn part2(input: InputType) -> i32 {
    let mut result = 0;
    let mut v = vec![];
    for (left, right) in input {
        v.push(left);
        v.push(right);
    }
    v.push(VecOrVal {
        val: 0,
        children: vec![VecOrVal {
            val: 2,
            children: vec![],
            is_val: true,
        }],
        is_val: false,
    });
    v.push(VecOrVal {
        val: 0,
        children: vec![VecOrVal {
            val: 6,
            children: vec![],
            is_val: true,
        }],
        is_val: false,
    });
    v.sort();
    let two = VecOrVal {
        val: 0,
        children: vec![VecOrVal {
            val: 2,
            children: vec![],
            is_val: true,
        }],
        is_val: false,
    };
    let six = VecOrVal {
        val: 0,
        children: vec![VecOrVal {
            val: 6,
            children: vec![],
            is_val: true,
        }],
        is_val: false,
    };

    let mut two_pos = 0;
    let mut six_pos = 0;
    let mut i = 1;
    for vec_or_val in v {
        if vec_or_val == two {
            two_pos = i;
        }
        if vec_or_val == six {
            six_pos = i;
        }
        i += 1;
    }
    return two_pos * six_pos;
}

fn main() {
    let contents_actual =
        fs::read_to_string(INPUT_FILENAME).expect("Should have been able to read the file");
    let parsed_input_actual_1 = parse_input(contents_actual.clone());
    let parsed_input_actual_2 = parse_input(contents_actual);

    let actual_result_1 = part1(parsed_input_actual_1);
    let actual_result_2 = part2(parsed_input_actual_2);

    println!("Day 13 - Part 1");
    println!("The result for the input is: {}", actual_result_1);
    println!("Day 13 - Part 2");
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
        assert_eq!(sample_result_1, 13);
    }

    #[test]
    fn test_part2() {
        let contents_sample = fs::read_to_string(SAMPLE_INPUT_FILENAME)
            .expect("Should have been able to read the file");
        let parsed_input_sample = parse_input(contents_sample);
        let sample_result_2 = part2(parsed_input_sample);
        assert_eq!(sample_result_2, 140);
    }
}
