use std::fs;
use std::str;
static SAMPLE_INPUT_FILENAME: &str = "sample.txt";
static INPUT_FILENAME: &str = "input.txt";
use regex::Regex;

#[derive(Clone)]
struct Board {
    state: Vec<Vec<char>>,
}

impl std::fmt::Display for Board {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        let height = self
            .state
            .iter()
            .map(|v| v.len())
            .max()
            .expect("This should exist");
        let mut lines: Vec<String> = Vec::new();
        for i in (0..height - 1).rev() {
            let state: Vec<String> = self
                .state
                .iter()
                .map(|v| {
                    v.get(i)
                        .map(|c| format!("[{}]", c))
                        .unwrap_or("   ".to_string())
                })
                .collect();
            lines.push(state.join(" "))
        }
        let line_numbers = (1..self.state.len() + 1)
            .into_iter()
            .map(|i| format!(" {} ", i))
            .collect::<Vec<String>>()
            .join(" ");
        lines.push(line_numbers);
        write!(f, "{}", lines.join("\n"))
    }
}

struct Move {
    amount: u32,
    from: u32,
    to: u32,
}

struct Moves(pub Vec<Move>);

impl std::fmt::Display for Moves {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        let mut lines = Vec::new();
        for m in self.0.iter() {
            lines.push(format!("move {} from {} to {}", m.amount, m.from, m.to));
        }
        write!(f, "{}", lines.join("\n"))
    }
}

type ContentType = (Board, Moves);

fn parse_input(contents: String) -> ContentType {
    let mut board_setting = Vec::new();
    let mut move_list = Vec::new();
    let mut moves_flag = false;
    for line in contents.lines() {
        if line.is_empty() {
            moves_flag = true;
            continue;
        }
        if moves_flag {
            move_list.push(line);
        } else {
            board_setting.push(line);
        }
    }
    board_setting.reverse();
    let mut board_iterator = board_setting.iter();
    let board_length = board_iterator
        .next()
        .expect("This should exist")
        .split("   ")
        .last()
        .expect("This should exist")
        .trim()
        .parse::<u32>()
        .expect("This should be an integer");

    let state: Vec<Vec<char>> = Vec::new();
    let mut board = Board { state: state };
    for _ in 0..board_length {
        board.state.push(Vec::new());
    }
    while let Some(line) = board_iterator.next() {
        for i in (1..line.len()).step_by(4) {
            let board_index = i / 4;
            let c = line.chars().nth(i).expect("This should exist");
            if c != ' ' {
                board.state[board_index].push(c);
            }
        }
    }

    let re =
        Regex::new(r#"move ([0-9]*) from ([0-9]*) to ([0-9]*)"#).expect("This shouldn't break");

    let moves: Moves = Moves(
        move_list
            .iter()
            .map(|v| {
                let curr_move = re
                    .captures(v)
                    .and_then(|cap| {
                        let groups = (cap.get(1), cap.get(2), cap.get(3));
                        match groups {
                            (Some(amt), Some(from), Some(to)) => Some(Move {
                                amount: amt
                                    .as_str()
                                    .parse::<u32>()
                                    .expect("This should parse correctly"),
                                from: from
                                    .as_str()
                                    .parse::<u32>()
                                    .expect("This should parse correctly"),
                                to: to
                                    .as_str()
                                    .parse::<u32>()
                                    .expect("This should parse correctly"),
                            }),
                            _ => None,
                        }
                    })
                    .expect("This should work");
                curr_move
            })
            .collect::<Vec<Move>>(),
    );

    return (board, moves);
}

fn puzzle1(contents: &ContentType) -> String {
    let (orig_board, moves) = contents;
    let mut board = orig_board.clone().to_owned();
    println!("Before\n{}", board);
    for m in moves.0.iter() {
        // Move m.amount from m.from to m.to one at a time
        for _ in 0..m.amount {
            let val = board.state[(m.from - 1) as usize]
                .pop()
                .expect("There should be a val");
            board.state[(m.to - 1) as usize].push(val);
        }
    }
    let result = board
        .state
        .iter()
        .map(|col| col.last().expect("There should be something here"))
        .collect();
    println!("After\n{}", board);
    return result;
}

fn puzzle2(contents: &ContentType) -> String {
    let (orig_board, moves) = contents;
    let mut board = orig_board.clone().to_owned();
    println!("Before\n{}", board);
    for m in moves.0.iter() {
        // Move m.amount from m.from to m.to one at a time
        let from_length = board.state[(m.from - 1) as usize].len();
        let mut val: Vec<char> = board.state[(m.from - 1) as usize]
            .drain(from_length - m.amount as usize..)
            .collect();
        board.state[(m.to - 1) as usize].append(&mut val);
    }
    let result = board
        .state
        .iter()
        .map(|col| col.last().expect("There should be something here"))
        .collect();
    println!("After\n{}", board);
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
    assert_eq!(sample_result_1, "CMZ".to_string());
    let actual_result_1 = puzzle1(&parsed_input_actual);
    println!("Day 5 - Puzzle 1");
    println!("The sample result is: {}", sample_result_1);
    println!("The actual result is: {}", actual_result_1);

    let sample_result_2 = puzzle2(&parsed_input_sample);
    assert_eq!(sample_result_2, "MCD");
    let actual_result_2 = puzzle2(&parsed_input_actual);
    println!("Day 5 - Puzzle 2");
    println!("The sample result is: {}", sample_result_2);
    println!("The actual result is: {}", actual_result_2);
}
