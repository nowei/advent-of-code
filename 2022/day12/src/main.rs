use priority_queue::PriorityQueue;
use std::{collections::HashSet, fs};

static INPUT_FILENAME: &str = "input.txt";

#[derive(PartialEq, Debug, Eq, Hash, Clone, Copy)]
struct Position {
    x: usize,
    y: usize,
}

fn parse_input(input: String) -> (Vec<Vec<u8>>, Position, Position) {
    let mut map = Vec::new();
    let mut start = Position { x: 0, y: 0 };
    let mut end = Position { x: 0, y: 0 };
    let mut y = 0;
    let mut x = 0;
    for line in input.lines() {
        let mut curr_line = vec![];
        let base_val = 'a' as u8;
        for c in line.chars() {
            match c {
                'S' => {
                    start.x = x;
                    start.y = y;
                    curr_line.push(0);
                }
                'E' => {
                    end.x = x;
                    end.y = y;
                    curr_line.push('z' as u8 - base_val);
                }
                v => {
                    curr_line.push(v as u8 - base_val);
                }
            }
            x += 1;
        }
        map.push(curr_line);
        x = 0;
        y += 1;
    }
    return (map, start, end);
}

fn part1((map, start, goal): (Vec<Vec<u8>>, Position, Position)) -> usize {
    let mut pq: PriorityQueue<Position, i32> = PriorityQueue::new();
    pq.push(start, 0);
    let mut seen: HashSet<Position> = HashSet::new();
    let mut best_dist = 0;
    while !pq.is_empty() {
        let (curr_pos, dist) = pq.pop().expect("This should have something");
        if seen.contains(&curr_pos) {
            continue;
        }
        if curr_pos == goal {
            best_dist = -dist;
            break;
        }
        seen.insert(curr_pos);
        let curr_val = map[curr_pos.y][curr_pos.x];
        let mut possible_next_paths = vec![];
        if curr_pos.x > 0 {
            possible_next_paths.push(Position {
                x: curr_pos.x - 1,
                y: curr_pos.y,
            })
        }
        if curr_pos.y > 0 {
            possible_next_paths.push(Position {
                x: curr_pos.x,
                y: curr_pos.y - 1,
            })
        }
        if curr_pos.x < (map[0].len() - 1).try_into().unwrap() {
            possible_next_paths.push(Position {
                x: curr_pos.x + 1,
                y: curr_pos.y,
            })
        }
        if curr_pos.y < (map.len() - 1).try_into().unwrap() {
            possible_next_paths.push(Position {
                x: curr_pos.x,
                y: curr_pos.y + 1,
            })
        }

        possible_next_paths = possible_next_paths
            .into_iter()
            .filter(|v| map[v.y][v.x] <= curr_val + 1)
            .filter(|v| !seen.contains(v))
            .collect();
        for pos in possible_next_paths {
            pq.push(pos, dist - 1);
        }
    }

    return best_dist.try_into().unwrap();
}

fn part2((map, _, goal): (Vec<Vec<u8>>, Position, Position)) -> i32 {
    let mut best_dist = i32::MAX;
    let mut a_potentials = vec![];
    for y in 0..map.len() {
        for x in 0..map[0].len() {
            if map[y][x] == 0 {
                a_potentials.push(Position { x, y });
            }
        }
    }
    for start in a_potentials {
        let mut pq: PriorityQueue<Position, i32> = PriorityQueue::new();
        pq.push(start, 0);
        let mut seen: HashSet<Position> = HashSet::new();
        while !pq.is_empty() {
            let (curr_pos, dist) = pq.pop().expect("This should have something");
            if seen.contains(&curr_pos) {
                continue;
            }
            if curr_pos == goal && -dist < best_dist {
                best_dist = -dist;
                break;
            }
            seen.insert(curr_pos);
            let curr_val = map[curr_pos.y][curr_pos.x];
            let mut possible_next_paths = vec![];
            if curr_pos.x > 0 {
                possible_next_paths.push(Position {
                    x: curr_pos.x - 1,
                    y: curr_pos.y,
                })
            }
            if curr_pos.y > 0 {
                possible_next_paths.push(Position {
                    x: curr_pos.x,
                    y: curr_pos.y - 1,
                })
            }
            if curr_pos.x < (map[0].len() - 1).try_into().unwrap() {
                possible_next_paths.push(Position {
                    x: curr_pos.x + 1,
                    y: curr_pos.y,
                })
            }
            if curr_pos.y < (map.len() - 1).try_into().unwrap() {
                possible_next_paths.push(Position {
                    x: curr_pos.x,
                    y: curr_pos.y + 1,
                })
            }

            possible_next_paths = possible_next_paths
                .into_iter()
                .filter(|v| map[v.y][v.x] <= curr_val + 1)
                .filter(|v| !seen.contains(v))
                .collect();
            for pos in possible_next_paths {
                pq.push(pos, dist - 1);
            }
        }
    }

    return best_dist.try_into().unwrap();
}

fn main() {
    let contents_actual =
        fs::read_to_string(INPUT_FILENAME).expect("Should have been able to read the file");
    let parsed_input_actual_1 = parse_input(contents_actual.clone());
    let parsed_input_actual_2 = parse_input(contents_actual);

    let actual_result_1 = part1(parsed_input_actual_1);
    let actual_result_2 = part2(parsed_input_actual_2);

    println!("Day 12 - Part 1");
    println!("The result for the input is: {}", actual_result_1);
    println!("Day 12 - Part 2");
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
        assert_eq!(sample_result_1, 31);
    }

    #[test]
    fn test_part2() {
        let contents_sample = fs::read_to_string(SAMPLE_INPUT_FILENAME)
            .expect("Should have been able to read the file");
        let parsed_input_sample = parse_input(contents_sample);
        let sample_result_2 = part2(parsed_input_sample);
        assert_eq!(sample_result_2, 29);
    }
}
