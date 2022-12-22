use queues::{IsQueue, Queue};
use regex::Regex;
use std::{collections::HashSet, fs};

static INPUT_FILENAME: &str = "input.txt";

type InputType = Vec<Blueprint>;

// e.g.
// Blueprint 1:
//   Each ore robot costs 4 ore.
//   Each clay robot costs 2 ore.
//   Each obsidian robot costs 3 ore and 14 clay.
//   Each geode robot costs 2 ore and 7 obsidian.
struct Blueprint {
    blueprint_num: u32,
    // 0 is ore robot
    // 1 is clay robot
    // 2 is obsidian robot
    // 3 is geode robot
    costs: Vec<(u32, u32, u32)>,
}

#[derive(Hash, Eq, PartialEq, Clone, Debug)]
struct State {
    time: u32,
    workers: Vec<u32>,
    resources: Vec<u32>,
}

impl Blueprint {
    // Idea #1: BFS; there's an error with how this explores state, something is missing
    fn evaluate(&self, robots: Vec<u32>, time_limit: u32) -> u32 {
        let mut queue = Queue::new();
        queue
            .add(State {
                time: 0,
                workers: robots.clone(),
                resources: vec![0, 0, 0, 0],
            })
            .expect("should add");
        let mut seen: HashSet<State> = HashSet::new();
        let mut best_geodes = 0;

        let ore_per_turn = self.costs.iter().map(|c| c.0).max().expect("Should exist");
        let clay_per_turn = self.costs.iter().map(|c| c.1).max().expect("Should exist");
        let obsidian_per_turn = self.costs.iter().map(|c| c.2).max().expect("Should exist");
        let max_cost_per_turn = vec![ore_per_turn, clay_per_turn, obsidian_per_turn];
        while let Ok(state) = queue.remove() {
            if seen.contains(&state) {
                continue;
            }
            seen.insert(state.clone());
            if state.time == time_limit {
                let curr_geodes = state.resources[3];
                if curr_geodes > best_geodes {
                    println!("{} {:?} {}", self.blueprint_num, state, queue.size());
                    best_geodes = curr_geodes;
                }
                continue;
            }
            // idea #1: Check if we can buy any robots. Attempt to buy robot if possible.
            // idea #2: greedily only consider best buyable tier of robot (limits spawn to at most 2 per eval)
            // idea #3 encode a bunch of heuristics I got off the internet:
            //  - don't build a robot of a type if we don't need the resources for
            //  - schedule work when we can build one of each type
            'consider_worker: for (worker_idx, &cost) in self.costs.iter().enumerate() {
                if worker_idx < 3 && state.workers[worker_idx] >= max_cost_per_turn[worker_idx] {
                    continue;
                }
                if state.resources[0] < cost.0
                    || state.resources[1] < cost.1
                    || state.resources[2] < cost.2
                {
                    // schedule work when we can build one of each type
                    let mut turns_needed = 0;
                    let needed_resources = vec![
                        cost.0 - state.resources[0],
                        cost.1 - state.resources[1],
                        cost.2 - state.resources[2],
                    ];
                    for idx in 0..needed_resources.len() {
                        if needed_resources[idx] > 0 {
                            if state.workers[idx] == 0 {
                                break 'consider_worker;
                            }
                            turns_needed = turns_needed.max(
                                (needed_resources[idx] as f32 / state.workers[idx] as f32).ceil()
                                    as u32,
                            );
                        }
                    }
                    // Takes one turn to build a robot
                    assert!(turns_needed != 0);
                    turns_needed += 1;
                    if state.time + turns_needed >= time_limit {
                        continue;
                    }

                    let mut new_resources = state.resources.clone();
                    for idx in 0..state.workers.len() {
                        new_resources[idx] += state.workers[idx] * turns_needed;
                    }

                    new_resources[0] -= cost.0;
                    new_resources[1] -= cost.1;
                    new_resources[2] -= cost.2;
                    let mut workers = state.workers.clone();
                    workers[worker_idx] += 1;

                    let new_state = State {
                        time: state.time + turns_needed,
                        workers,
                        resources: new_resources,
                    };
                    if new_state.resources[3] == 12 {
                        println!(
                            "prev state: {:?} curr state: {:?} with resources {:?}, {}",
                            state, new_state, state.resources, turns_needed
                        );
                        panic!("Shouldn't get here");
                    }
                    queue.add(new_state).expect("should add");
                } else {
                    let mut workers = state.workers.clone();
                    workers[worker_idx] += 1;
                    let mut new_resources = state.resources.clone();
                    new_resources[0] -= cost.0;
                    new_resources[1] -= cost.1;
                    new_resources[2] -= cost.2;

                    for i in 0..state.workers.len() {
                        new_resources[i] += state.workers[i];
                    }
                    queue
                        .add(State {
                            time: state.time + 1,
                            workers,
                            resources: new_resources,
                        })
                        .expect("should add");
                }
            }
        }
        return best_geodes as u32;
    }

    // Idea #2: DFS
    fn evaluate_dfs(&self, robots: Vec<u32>, time_limit: u32) -> u32 {
        fn dfs(bp: &Blueprint, state: State, best_seen: &mut Box<u32>, time_limit: u32) {
            let ore_per_turn = bp.costs.iter().map(|c| c.0).max().expect("Should exist");
            let clay_per_turn = bp.costs.iter().map(|c| c.1).max().expect("Should exist");
            let obsidian_per_turn = bp.costs.iter().map(|c| c.2).max().expect("Should exist");
            let max_cost_per_turn = vec![ore_per_turn, clay_per_turn, obsidian_per_turn];
            // if path.len() > 3 {
            //     return;
            // }
            // Heuristic of best possible future not beating best seen so far.
            let current_geodes = state.resources[3];
            let turns_left = time_limit - state.time;
            let future_geodes = turns_left * (turns_left + 1) / 2 + state.workers[3] * turns_left;
            let future_possible_geodes = future_geodes + current_geodes;
            if future_possible_geodes < **best_seen {
                return;
            }
            // Future geodes if we just wait (important if we only take actions to create new workers)
            let wait_geodes = current_geodes + turns_left * state.workers[3];
            if wait_geodes > **best_seen {
                let b = best_seen.as_mut();
                *b = *b.max(&mut wait_geodes.clone());
                println!("Found potential {:?} {}", state, b);
            }
            'worker_loop: for (worker_idx, &cost) in bp.costs.iter().enumerate().rev() {
                if worker_idx < 3 && state.workers[worker_idx] >= max_cost_per_turn[worker_idx] {
                    continue;
                }
                let mut turns_needed = 0;
                let needed_resources: Vec<i32> = vec![
                    cost.0 as i32 - state.resources[0] as i32,
                    cost.1 as i32 - state.resources[1] as i32,
                    cost.2 as i32 - state.resources[2] as i32,
                ];
                for idx in 0..needed_resources.len() {
                    if needed_resources[idx] > 0 {
                        if state.workers[idx] == 0 {
                            continue 'worker_loop;
                        }
                        turns_needed = turns_needed.max(
                            (needed_resources[idx] as f32 / state.workers[idx] as f32).ceil()
                                as u32,
                        );
                    }
                }
                // time_limit
                turns_needed += 1;
                if state.time + turns_needed > time_limit {
                    continue;
                }

                let mut new_resources = state.resources.clone();
                for idx in 0..state.workers.len() {
                    new_resources[idx] += state.workers[idx] * turns_needed;
                }

                new_resources[0] -= cost.0;
                new_resources[1] -= cost.1;
                new_resources[2] -= cost.2;
                let mut workers = state.workers.clone();
                workers[worker_idx] += 1;

                // if state.time == 0 {
                //     println!(
                //         "time {} cost {:?} resources {:?} -> {:?} workers {:?} -> {:?} turns needed {}",
                //         state.time, cost, state.resources, new_resources, state.workers, workers, turns_needed
                //     );
                // }
                let new_state = State {
                    time: state.time + turns_needed,
                    workers,
                    resources: new_resources,
                };

                if new_state.resources[3] > **best_seen {
                    let b = best_seen.as_mut();
                    *b = *b.max(&mut new_state.resources[3].clone());
                    println!("Found potential {:?} -> {:?}", state, new_state);
                }
                // if state.workers == vec![1, 2, 3, 2] && state.resources == vec![1, 8, 4, 3] {
                //     println!("Found potential {:?} -> {:?}", state, new_state);
                // }
                dfs(bp, new_state, best_seen, time_limit);
            }
        }
        let mut best_seen = Box::new(0);
        dfs(
            self,
            State {
                time: 0,
                workers: robots.clone(),
                resources: vec![0, 0, 0, 0],
            },
            &mut best_seen,
            time_limit,
        );
        return *best_seen;
    }
}

fn parse_input(input: String) -> InputType {
    let mut result = InputType::new();
    let re =
        Regex::new(r#"Blueprint (.*): Each ore robot costs (.*) ore. Each clay robot costs (.*) ore. Each obsidian robot costs (.*) ore and (.*) clay. Each geode robot costs (.*) ore and (.*) obsidian."#).expect("This shouldn't break");

    for line in input.lines() {
        let (
            blueprint_num,
            ore_robot_ore_cost,
            clay_robot_ore_cost,
            obsidian_robot_ore_cost,
            obsidian_robot_clay_cost,
            geode_robot_ore_cost,
            geode_robot_obsidian_cost,
        ) = re
            .captures(line)
            .and_then(|cap| {
                let group = (
                    cap.get(1),
                    cap.get(2),
                    cap.get(3),
                    cap.get(4),
                    cap.get(5),
                    cap.get(6),
                    cap.get(7),
                );
                match group {
                    (
                        Some(blueprint_num),
                        Some(ore_robot_ore_cost),
                        Some(clay_robot_ore_cost),
                        Some(obsidian_robot_ore_cost),
                        Some(obsidian_robot_clay_cost),
                        Some(geode_robot_ore_cost),
                        Some(geode_robot_obsidian_cost),
                    ) => Some((
                        blueprint_num.as_str().parse::<u32>().unwrap(),
                        ore_robot_ore_cost.as_str().parse::<u32>().unwrap(),
                        clay_robot_ore_cost.as_str().parse::<u32>().unwrap(),
                        obsidian_robot_ore_cost.as_str().parse::<u32>().unwrap(),
                        obsidian_robot_clay_cost.as_str().parse::<u32>().unwrap(),
                        geode_robot_ore_cost.as_str().parse::<u32>().unwrap(),
                        geode_robot_obsidian_cost.as_str().parse::<u32>().unwrap(),
                    )),
                    _ => None,
                }
            })
            .expect("Should work");
        let costs: Vec<(u32, u32, u32)> = vec![
            (ore_robot_ore_cost, 0, 0),
            (clay_robot_ore_cost, 0, 0),
            (obsidian_robot_ore_cost, obsidian_robot_clay_cost, 0),
            (geode_robot_ore_cost, 0, geode_robot_obsidian_cost),
        ];
        result.push(Blueprint {
            blueprint_num,
            costs,
        });
    }
    return result;
}

fn part1(input: InputType) -> u32 {
    let mut result = 0;
    let init_robots = vec![1, 0, 0, 0];
    let time_span = 24;
    for b in input {
        let num_geodes = b.evaluate_dfs(init_robots.clone(), time_span);
        let quality_level = num_geodes * b.blueprint_num;
        println!("quality level of {} is {}", b.blueprint_num, quality_level);
        result += quality_level;
    }
    // 1591 is too low
    // Supposed to be 1613
    return result;
}

fn part2(input: InputType) -> u32 {
    let mut result = 1;
    let init_robots = vec![1, 0, 0, 0];
    let time_span = 32;
    for b in &input[..3.min(input.len())] {
        let num_geodes = b.evaluate_dfs(init_robots.clone(), time_span);
        println!("num geodes of {} is {}", b.blueprint_num, num_geodes);
        result *= num_geodes;
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

    println!("Day 19 - Part 1");
    println!("The result for the input is: {}", actual_result_1);
    println!("Day 19 - Part 2");
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
        assert_eq!(sample_result_1, 33);

        let contents_sample =
            fs::read_to_string("sample2.txt").expect("Should have been able to read the file");
        let parsed_input_sample = parse_input(contents_sample);
        let sample_result_1 = part1(parsed_input_sample);
        assert_eq!(sample_result_1, 286);
    }

    #[test]
    fn test_part2() {
        let contents_sample = fs::read_to_string(SAMPLE_INPUT_FILENAME)
            .expect("Should have been able to read the file");
        let parsed_input_sample = parse_input(contents_sample);
        let sample_result_2 = part2(parsed_input_sample);
        assert_eq!(sample_result_2, 62 * 56);
    }
}
