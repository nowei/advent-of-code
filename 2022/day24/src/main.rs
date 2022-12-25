use std::{
    collections::{HashMap, HashSet},
    fs,
};

use priority_queue::PriorityQueue;
use queue::Queue;

static INPUT_FILENAME: &str = "input.txt";

// Board: blizzard
// pos: Point,
// goal: Point,
// walls: HashSet<Point>,
// (#rows, #cols)
// size: (i32, i32),
type InputType = (Board, Point, Point, HashSet<Point>, (i32, i32));

#[derive(Hash, Eq, PartialEq, Clone, Copy, Debug)]
struct Point {
    x: i32,
    y: i32,
}

#[derive(Clone)]
enum Direction {
    Up,
    Right,
    Down,
    Left,
}
#[derive(Clone)]
struct Blizzard {
    pos: Point,
    dir: Direction,
}
#[derive(Clone)]
struct Board {
    bliz: Vec<Blizzard>,
}

impl Board {
    fn step(&self, walls: &HashSet<Point>, size: &(i32, i32)) -> Board {
        let bliz: Vec<Blizzard> = self
            .bliz
            .iter()
            .map(|b| {
                let mut pos = match b.dir {
                    Direction::Up => Point {
                        y: b.pos.y - 1,
                        ..b.pos
                    },
                    Direction::Right => Point {
                        x: b.pos.x + 1,
                        ..b.pos
                    },
                    Direction::Down => Point {
                        y: b.pos.y + 1,
                        ..b.pos
                    },
                    Direction::Left => Point {
                        x: b.pos.x - 1,
                        ..b.pos
                    },
                };
                if walls.contains(&pos) {
                    match b.dir {
                        Direction::Up => pos.y = size.0 - 2,
                        Direction::Right => pos.x = 1,
                        Direction::Down => pos.y = 1,
                        Direction::Left => pos.x = size.1 - 2,
                    }
                }
                Blizzard {
                    pos,
                    dir: b.dir.clone(),
                }
            })
            .collect();
        return Board { bliz };
    }

    fn get_occupied(&self) -> HashSet<Point> {
        let mut set = HashSet::new();
        for b in &self.bliz {
            set.insert(b.pos);
        }
        return set;
    }
}

fn parse_input(input: String) -> InputType {
    // Special handling of first row and last row

    let mut bliz = vec![];
    let mut walls = HashSet::new();

    let blizzard_check = vec!['<', '^', '>', 'v'];

    let mut row = 0;
    let mut col = 0;
    for line in input.lines() {
        col = 0;
        for c in line.chars() {
            if c == '#' {
                walls.insert(Point { x: col, y: row });
            } else if blizzard_check.contains(&c) {
                let b = Blizzard {
                    pos: Point { x: col, y: row },
                    dir: match c {
                        '^' => Direction::Up,
                        '<' => Direction::Left,
                        '>' => Direction::Right,
                        'v' => Direction::Down,
                        _ => panic!("cases should be covered"),
                    },
                };
                bliz.push(b);
            }
            col += 1;
        }
        row += 1;
    }
    let size = (row, col);

    // Init point is empty in first row
    let mut pos = Point { x: 0, y: 0 };
    for i in 0..col {
        if !walls.contains(&Point { x: i, y: 0 }) {
            pos.x = i;
            break;
        }
    }
    // Add a wall above the initial point so that we don't have to worry about that case later on
    walls.insert(Point { y: -1, ..pos });

    // Final point is empty in last row
    let mut goal = Point { x: 0, y: row - 1 };
    for i in 0..col {
        if !walls.contains(&Point { x: i, y: row - 1 }) {
            goal.x = i;
            break;
        }
    }
    walls.insert(Point { y: row, ..goal });

    return (Board { bliz }, pos, goal, walls, size);
}

fn get_valid_next_steps(
    pos: &Point,
    occupied: &HashSet<Point>,
    walls: &HashSet<Point>,
) -> Vec<Point> {
    let directions = vec![
        Direction::Up,
        Direction::Right,
        Direction::Down,
        Direction::Left,
    ];
    // Check staying
    let mut new_positions = vec![];
    if !occupied.contains(&pos) {
        new_positions.push(pos.clone());
    }
    // Check up, down left, right, down
    for new_pos in directions.iter().filter_map(|d| {
        let new_pos = match d {
            Direction::Up => Point {
                y: pos.y - 1,
                ..*pos
            },
            Direction::Right => Point {
                x: pos.x + 1,
                ..*pos
            },
            Direction::Down => Point {
                y: pos.y + 1,
                ..*pos
            },
            Direction::Left => Point {
                x: pos.x - 1,
                ..*pos
            },
        };
        if occupied.contains(&new_pos) {
            return None;
        }
        if walls.contains(&new_pos) {
            return None;
        }
        return Some(new_pos);
    }) {
        new_positions.push(new_pos);
    }
    return new_positions;
}

fn bfs(
    board_tracker: &mut HashMap<i32, (Board, HashSet<Point>)>,
    pos: Point,
    goal: Point,
    walls: HashSet<Point>,
    size: (i32, i32),
) -> i32 {
    let mut queue = Queue::new();
    queue.queue((pos, 1));
    let mut num_evals = 0;
    while let Some((pos, board_index)) = queue.dequeue() {
        if pos == goal {
            return board_index - 1;
        }
        if num_evals % 10000 == 0 {
            println!("{:?} {}", num_evals, queue.len());
        }
        if !board_tracker.contains_key(&board_index) {
            let (prev_board, _) = board_tracker.get(&(board_index - 1)).expect("should exist");
            let new_board = prev_board.step(&walls, &size);
            let occupied = new_board.get_occupied();
            board_tracker.insert(board_index, (new_board, occupied));
        }
        let (board, occupied) = board_tracker
            .get(&board_index)
            .expect("should exist at this point");
        // get valid next states
        for new_pos in get_valid_next_steps(&pos, &occupied, &walls) {
            queue.queue((new_pos, board_index + 1));
        }
        num_evals += 1;
    }

    // Not found
    return -1;
}

fn pq_directed(
    board_tracker: &mut HashMap<i32, (Board, HashSet<Point>)>,
    pos: Point,
    goal: Point,
    walls: &HashSet<Point>,
    size: (i32, i32),
) -> i32 {
    let mut pq = PriorityQueue::new();
    pq.push((pos, 0), 1);
    let mut num_evals = 0;
    let mut best = i32::MAX;
    let mut seen: HashSet<(Point, i32)> = HashSet::new();
    while let Some(((pos, board_index), prio)) = pq.pop() {
        // If we're greater than the best we've found already, it's not worth considering.
        // If number of turns + (-prio) is greater than the best we've found, it's not worth considering
        if board_index - prio >= best {
            continue;
        }
        if pos == goal {
            if board_index < best {
                println!("{:?} {}", pos, board_index);
                best = board_index;
            }
            continue;
        }
        // Ignore positions we've evaluated before to not redo work
        if seen.contains(&(pos, board_index)) {
            continue;
        }
        seen.insert((pos, board_index));
        if num_evals % 100000 == 0 {
            println!("{:?} {} {}, {}", num_evals, pq.len(), board_index, prio);
        }
        if !board_tracker.contains_key(&board_index) {
            let (prev_board, _) = board_tracker.get(&(board_index - 1)).expect("should exist");
            let new_board = prev_board.step(&walls, &size);
            let occupied = new_board.get_occupied();
            board_tracker.insert(board_index, (new_board, occupied));
        }
        let (_, occupied) = board_tracker
            .get(&board_index)
            .expect("should exist at this point");

        for new_pos in get_valid_next_steps(&pos, &occupied, &walls) {
            let prio = (new_pos.x - goal.x).abs() + (new_pos.y - goal.y).abs();
            pq.push((new_pos, board_index + 1), -prio);
        }
        num_evals += 1;
    }
    return best - 1;
}

fn part1(input: InputType) -> i32 {
    let (board, pos, goal, walls, size) = input;
    // Search should be fine? Ideally the search space is limited due to blizzard movement
    // The main idea is to step first, then consider whether we can move in a direction or stay
    // depending on if the updated map overlaps with where we are
    // position, board index

    let mut board_tracker: HashMap<i32, (Board, HashSet<Point>)> = HashMap::new();
    let occupied = board.get_occupied();
    board_tracker.insert(0, (board, occupied));
    // 273 Too high
    return pq_directed(&mut board_tracker, pos, goal, &walls, size);
}

fn part2(input: InputType) -> i32 {
    let mut result = 0;
    let (board, start, goal, walls, size) = input;

    let mut board_tracker: HashMap<i32, (Board, HashSet<Point>)> = HashMap::new();
    let occupied = board.get_occupied();
    board_tracker.insert(0, (board, occupied));
    // go from start -> end
    let board_index = pq_directed(&mut board_tracker, start, goal, &walls, size);
    let (board, occupied) = board_tracker.remove(&(board_index)).expect("Should exist");
    board_tracker.clear();
    board_tracker.insert(0, (board.clone(), occupied.clone()));
    result += board_index;
    // go from end -> start
    let board_index = pq_directed(&mut board_tracker, goal, start, &walls, size);
    let (board, occupied) = board_tracker.remove(&(board_index)).expect("Should exist");
    board_tracker.clear();
    board_tracker.insert(0, (board.clone(), occupied.clone()));
    result += board_index;
    // go from start -> end
    let board_index = pq_directed(&mut board_tracker, start, goal, &walls, size);
    result += board_index;
    return result;
}

fn main() {
    let contents_actual =
        fs::read_to_string(INPUT_FILENAME).expect("Should have been able to read the file");
    let parsed_input_actual_1 = parse_input(contents_actual.clone());
    let parsed_input_actual_2 = parse_input(contents_actual);

    let actual_result_1 = part1(parsed_input_actual_1);
    let actual_result_2 = part2(parsed_input_actual_2);

    println!("Day 24 - Part 1");
    println!("The result for the input is: {}", actual_result_1);
    println!("Day 24 - Part 2");
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
        assert_eq!(sample_result_1, 18);
    }

    #[test]
    fn test_part2() {
        let contents_sample = fs::read_to_string(SAMPLE_INPUT_FILENAME)
            .expect("Should have been able to read the file");
        let parsed_input_sample = parse_input(contents_sample);
        let sample_result_2 = part2(parsed_input_sample);
        assert_eq!(sample_result_2, 54);
    }
}
