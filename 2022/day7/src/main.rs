use std::{collections::HashMap, fs};

static SAMPLE_INPUT_FILENAME: &str = "sample.txt";
static INPUT_FILENAME: &str = "input.txt";

type ContentType = Directory;

#[derive(Debug)]
struct File {
    _name: String,
    size: u32,
}

#[derive(Debug)]
struct Directory {
    name: String,
    children: HashMap<String, Directory>,
    _files: HashMap<String, File>,
    size: u32,
}

fn parse_input(contents: String) -> ContentType {
    let mut stuff_map: HashMap<String, Vec<String>> = HashMap::new();

    let mut path: Vec<String> = vec!["/".to_string()];
    let mut line_iter = contents.lines().into_iter().peekable();
    while let Some(line) = line_iter.next() {
        let cmd = line.split(" ").collect::<Vec<&str>>();
        assert_eq!(cmd[0], "$");
        if cmd[1] == "cd" {
            match cmd[2] {
                "/" => {}
                ".." => {
                    path.pop();
                    ()
                }
                dir => {
                    let mut name = dir.to_string();
                    name.push_str("/");
                    path.push(name);
                }
            }
        } else if cmd[1] == "ls" {
            let mut stuff = Vec::new();
            let curr_dir_name = path.join("");
            while let Some(next_line) = line_iter.peek() {
                let split = next_line.split(" ").collect::<Vec<&str>>();

                match split[0] {
                    "$" => break,
                    "dir" => {
                        let mut name = curr_dir_name.clone();
                        name.push_str(split[1]);
                        name.push_str("/");
                        stuff.push(format!("dir {}", name));
                    }
                    v => {
                        let mut name = curr_dir_name.clone();
                        name.push_str(split[1]);
                        stuff.push(format!("{} {}", v, name));
                    }
                }
                line_iter.next();
            }
            stuff_map.insert(curr_dir_name, stuff);
        }
    }

    let root = recursive_build_dir(&stuff_map, "/".to_string());
    return root;
}

fn recursive_build_dir(stuff_map: &HashMap<String, Vec<String>>, dir: String) -> Directory {
    let mut children: HashMap<String, Directory> = HashMap::new();
    let mut files: HashMap<String, File> = HashMap::new();
    for v in stuff_map.get(&dir).expect("This should exist") {
        let split: Vec<&str> = v.split(" ").collect();
        match split[0] {
            "dir" => {
                let m = recursive_build_dir(stuff_map, split[1].to_string());
                children.insert(split[1].to_string(), m);
            }
            v => {
                let name = split[1].to_string();
                let size = v.parse::<u32>().expect("This should work");
                files.insert(name.clone(), File { _name: name, size });
            }
        }
    }
    let mut size = 0;
    for f in files.values() {
        size += f.size;
    }
    for d in children.values() {
        size += d.size;
    }
    return Directory {
        name: dir,
        children,
        _files: files,
        size,
    };
}

fn puzzle1(contents: &ContentType) -> u32 {
    fn look_for_sub_100k(dir: &Directory) -> u32 {
        let mut total = 0;
        if dir.size < 100000 {
            total += dir.size;
        }
        for d in dir.children.values() {
            total += look_for_sub_100k(d);
        }
        return total;
    }
    let result = look_for_sub_100k(contents);
    return result;
}

fn puzzle2(contents: &ContentType) -> u32 {
    let mut list: Vec<(u32, String)> = Vec::new();
    fn list_dir_sizes(dir: &Directory, list: &mut Vec<(u32, String)>) {
        let mut name_vec: Vec<&str> = dir.name.split("/").collect();
        name_vec.pop();
        let name = if name_vec.is_empty() {
            "/"
        } else {
            name_vec.pop().expect("This should exist")
        }
        .to_string();
        list.push((dir.size, name));
        for d in dir.children.values() {
            list_dir_sizes(d, list);
        }
    }
    list_dir_sizes(contents, &mut list);

    // Compute memory needed
    let total_disk_space = 70000000;
    let unused_space = total_disk_space - contents.size;
    let amount_to_delete = 30000000 - unused_space;

    list.sort();
    for (size, _name) in list {
        if size > amount_to_delete {
            return size;
        }
    }

    return 0;
}

fn main() {
    let contents_sample =
        fs::read_to_string(SAMPLE_INPUT_FILENAME).expect("Should have been able to read the file");
    let parsed_input_sample = parse_input(contents_sample);
    let contents_actual =
        fs::read_to_string(INPUT_FILENAME).expect("Should have been able to read the file");
    let parsed_input_actual = parse_input(contents_actual);

    let sample_result_1 = puzzle1(&parsed_input_sample);
    assert_eq!(sample_result_1, 95437);
    let actual_result_1 = puzzle1(&parsed_input_actual);
    println!("Day 7 - Puzzle 1");
    println!("The sample result is: {}", sample_result_1);
    println!("The actual result is: {}", actual_result_1);

    let sample_result_2 = puzzle2(&parsed_input_sample);
    assert_eq!(sample_result_2, 24933642);
    let actual_result_2 = puzzle2(&parsed_input_actual);
    println!("Day 7 - Puzzle 2");
    println!("The sample result is: {}", sample_result_2);
    println!("The actual result is: {}", actual_result_2);
}
