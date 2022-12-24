use std::{collections::HashMap, collections::HashSet, fs};

static INPUT_FILENAME: &str = "input.txt";

type InputType = HashMap<Point, Elf>;

#[derive(Debug, Clone, Copy, Hash, Eq, PartialEq)]
struct Point {
    x: i32,
    y: i32,
}

#[derive(Eq, PartialEq, Hash, Clone, Debug)]
enum Direction {
    North,
    South,
    West,
    East,
}

#[derive(Debug, Clone, Hash, Eq, PartialEq)]
struct Elf {
    location: Point,
}

fn parse_input(input: String) -> InputType {
    let mut result = InputType::new();

    let mut row = 0;
    for line in input.lines() {
        let mut col = 0;
        for i in line.chars() {
            if i == '#' {
                let p = Point { x: col, y: row };
                result.insert(p.clone(), Elf { location: p });
            }
            col += 1;
        }
        row += 1;
    }
    return result;
}

fn simulate(
    elves: &HashMap<Point, Elf>,
    candidate_directions: &mut Vec<Direction>,
) -> HashMap<Point, Elf> {
    let mut collisions: HashSet<Point> = HashSet::new();
    let mut future_elves: HashSet<(Elf, Elf)> = HashSet::new();
    let mut seen: HashSet<Point> = HashSet::new();
    // for y in -2..10 {
    //     for x in -3..11 {
    //         if elves.contains_key(&Point { x, y }) {
    //             print!("#");
    //         } else {
    //             print!(".");
    //         }
    //     }
    //     println!();
    // }

    for pt in elves.keys() {
        let x = pt.x;
        let y = pt.y;
        let nw = Point { x: x - 1, y: y - 1 };
        let n = Point { x: x, y: y - 1 };
        let ne = Point { x: x + 1, y: y - 1 };
        let e = Point { x: x + 1, y };
        let se = Point { x: x + 1, y: y + 1 };
        let s = Point { x: x, y: y + 1 };
        let sw = Point { x: x - 1, y: y + 1 };
        let w = Point { x: x - 1, y };
        // Check if no neighbors
        let elf = elves.get(pt).expect("should exist");
        let (old, new) = if !elves.contains_key(&nw)
            && !elves.contains_key(&n)
            && !elves.contains_key(&ne)
            && !elves.contains_key(&e)
            && !elves.contains_key(&se)
            && !elves.contains_key(&s)
            && !elves.contains_key(&sw)
            && !elves.contains_key(&w)
        {
            (elf.clone(), elf.clone())
        } else {
            // Check north
            let mut elf_tuple = (elf.clone(), elf.clone());
            for d in candidate_directions.iter() {
                let result: Option<(Elf, Elf)> = match d {
                    Direction::North => {
                        if !(elves.contains_key(&nw)
                            || elves.contains_key(&n)
                            || elves.contains_key(&ne))
                        {
                            let mut new_elf = elf.clone();
                            new_elf.location = n.clone();
                            Some((elf.clone(), new_elf))
                        } else {
                            None
                        }
                    }
                    Direction::South => {
                        if !(elves.contains_key(&sw)
                            || elves.contains_key(&s)
                            || elves.contains_key(&se))
                        {
                            let mut new_elf = elf.clone();
                            new_elf.location = s.clone();
                            Some((elf.clone(), new_elf))
                        } else {
                            None
                        }
                    }
                    Direction::West => {
                        if !(elves.contains_key(&sw)
                            || elves.contains_key(&w)
                            || elves.contains_key(&nw))
                        {
                            let mut new_elf = elf.clone();
                            new_elf.location = w.clone();
                            Some((elf.clone(), new_elf))
                        } else {
                            None
                        }
                    }
                    Direction::East => {
                        if !(elves.contains_key(&se)
                            || elves.contains_key(&e)
                            || elves.contains_key(&ne))
                        {
                            let mut new_elf = elf.clone();
                            new_elf.location = e.clone();
                            Some((elf.clone(), new_elf))
                        } else {
                            None
                        }
                    }
                };
                if let Some(new_elf_tuple) = result {
                    elf_tuple = new_elf_tuple;
                    break;
                }
            }
            elf_tuple
        };
        if seen.contains(&new.location) {
            collisions.insert(new.location.clone());
        }
        seen.insert(new.location.clone());
        future_elves.insert((old, new));
    }
    let v = candidate_directions.remove(0);
    candidate_directions.push(v);
    let new_elves: HashMap<Point, Elf> = future_elves
        .iter()
        .map(|(old, new)| {
            if collisions.contains(&new.location) {
                (old.location.clone(), old.clone())
            } else {
                (new.location.clone(), new.clone())
            }
        })
        .collect();
    println!("collision size: {}", collisions.len());
    return new_elves;
}

fn part1(input: InputType) -> i32 {
    let mut result = 0;
    let mut elves = input.clone();

    let mut candidate_directions = vec![
        Direction::North,
        Direction::South,
        Direction::West,
        Direction::East,
    ];
    for round in 0..10 {
        elves = simulate(&elves, &mut candidate_directions);
    }

    let x_min = elves.iter().map(|(p, _)| p.x).min().expect("Should exist");
    let x_max = elves.iter().map(|(p, _)| p.x).max().expect("Should exist");
    let y_min = elves.iter().map(|(p, _)| p.y).min().expect("Should exist");
    let y_max = elves.iter().map(|(p, _)| p.y).max().expect("Should exist");
    let size = (x_max - x_min + 1) * (y_max - y_min + 1);
    println!(
        "x: [{}, {}] y: [{}, {}], size = {}",
        x_min, x_max, y_min, y_max, size
    );
    result = size - elves.len() as i32;
    // 4956 is too high
    // 4855 is too high
    // 2789 is too low
    // num is 3940
    return result;
}

fn part2(input: InputType) -> i32 {
    let mut result = 0;
    let mut elves = input.clone();

    let mut candidate_directions = vec![
        Direction::North,
        Direction::South,
        Direction::West,
        Direction::East,
    ];
    loop {
        let new_elves = simulate(&elves, &mut candidate_directions);
        result += 1;
        if elves.keys().all(|k| new_elves.contains_key(k)) {
            break;
        }
        elves = new_elves;
    }

    return result;
}

fn main() {
    let contents_actual =
        fs::read_to_string(INPUT_FILENAME).expect("Should have been able to read the file");
    let parsed_input_actual_1 = parse_input(contents_actual.clone());
    let parsed_input_actual_2 = parse_input(contents_actual);

    let actual_result_1 = part1(parsed_input_actual_1);
    let actual_result_2 = part2(parsed_input_actual_2);

    println!("Day 23 - Part 1");
    println!("The result for the input is: {}", actual_result_1);
    println!("Day 23 - Part 2");
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
        assert_eq!(sample_result_1, 110);
    }

    #[test]
    fn test_part2() {
        let contents_sample = fs::read_to_string(SAMPLE_INPUT_FILENAME)
            .expect("Should have been able to read the file");
        let parsed_input_sample = parse_input(contents_sample);
        let sample_result_2 = part2(parsed_input_sample);
        assert_eq!(sample_result_2, 20);
    }
}
