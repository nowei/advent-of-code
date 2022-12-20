use itertools::Itertools;
use priority_queue::PriorityQueue;
use queues::{IsQueue, Queue};
use regex::Regex;
use std::{
    collections::{HashMap, HashSet},
    fs,
};

static INPUT_FILENAME: &str = "input.txt";

type InputType = (
    HashMap<String, u32>,
    HashMap<String, Vec<String>>,
    HashMap<String, HashMap<String, u32>>,
);

fn parse_input(input: String) -> InputType {
    let re =
        Regex::new(r#"Valve (.*) has flow rate=(.*); tunnel([s]?) lead([s]?) to valve([s]?) (.*)"#)
            .expect("This shouldn't break");

    let mut rate_map: HashMap<String, u32> = HashMap::new();
    let mut path_map: HashMap<String, Vec<String>> = HashMap::new();
    let mut dist_map: HashMap<String, HashMap<String, u32>> = HashMap::new();

    for line in input.lines() {
        let (name, rate, tunnels) = re
            .captures(line)
            .and_then(|cap| {
                let group = (cap.get(1), cap.get(2), cap.get(6));
                let res = match group {
                    (Some(name), Some(rate), Some(tunnels)) => Some((
                        name.as_str().to_string(),
                        rate.as_str().parse::<u32>().unwrap(),
                        tunnels
                            .as_str()
                            .split(", ")
                            .map(|v| v.to_string())
                            .collect::<Vec<String>>(),
                    )),
                    _ => None,
                };
                res
            })
            .expect("Should work");
        rate_map.insert(name.clone(), rate);
        path_map.insert(name, tunnels);
    }
    for from in path_map.keys() {
        let mut curr_dists: HashMap<String, u32> = HashMap::new();
        let mut cands = Queue::new();
        cands.add((from, 0)).expect("Should work");
        while let Ok((curr, cost)) = cands.remove() {
            if curr_dists.contains_key(curr) {
                continue;
            }
            curr_dists.insert(curr.to_string(), cost);
            for neighbor in path_map.get(curr).expect("Should exist") {
                cands.add((neighbor, cost + 1)).expect("Add should work");
            }
        }
        dist_map.insert(from.to_string(), curr_dists);
    }
    return (rate_map, path_map, dist_map);
}

#[derive(Clone, Debug, Hash, PartialEq, Eq)]
struct State {
    time_left: u32,
    curr_pos: String,
    opened_valves: Vec<String>,
    // Estimated pressure at end
    pressure: u32,
}

impl State {
    fn is_terminal(&self, valued_valves: &HashSet<String>) -> bool {
        if self.time_left == 0 {
            return true;
        }
        if valued_valves.is_subset(&self.opened_valves.iter().map(|s| s.clone()).collect()) {
            return true;
        }
        return false;
    }
}

#[derive(Clone, Debug, Hash, PartialEq, Eq)]
struct State2 {
    time_left: u32,
    curr_position: (String, u32),
    curr_position_elephant: (String, u32),
    opened_valves: Vec<String>,
    rate: u32,
    pressure: u32,
}

impl State2 {
    fn is_terminal(&self, valued_valves: &HashSet<String>) -> bool {
        if self.time_left == 0 {
            return true;
        }
        if valued_valves.is_subset(&self.opened_valves.iter().map(|s| s.clone()).collect()) {
            return true;
        }
        return false;
    }
}

// BFS through possible states?
fn part1(input: InputType, starting_time_in_min: u32) -> u32 {
    let mut result = 0;
    let starting_pos = "AA".to_string();
    let rate_map = input.0;
    let path_map = input.1;
    let dist_map = input.2;

    // Initial states
    let mut states: Queue<State> = Queue::new();
    let valued_valves: HashSet<String> = rate_map
        .iter()
        .filter_map(|(k, v)| if *v != 0 { Some((k, v)) } else { None })
        .map(|(k, _)| k.clone())
        .collect();
    let mut seen: HashSet<State> = HashSet::new();
    states
        .add(State {
            time_left: starting_time_in_min,
            curr_pos: starting_pos.clone(),
            opened_valves: vec![],
            pressure: 0,
        })
        .expect("This shouldn't fail");
    let mut i = 0;
    while let Ok(state) = states.remove() {
        // List of possible actions:
        // 1. Stay for the rest of the time (time_remaining)
        // 2. Go somewhere and open a valve (2 minutes)
        // 3. Go somewhere and don't open a valve (1 minutes)

        if i % 10000 == 0 {
            println!("{:?} {}", state, states.size());
        }

        if state.pressure > result {
            println!("{} {}", state.pressure, states.size());
            result = state.pressure;
        }
        if state.is_terminal(&valued_valves) {
            // Staying the course
            continue;
        }
        seen.insert(state.clone());
        for unopened_valve_dest in
            valued_valves.difference(&state.opened_valves.iter().map(|v| v.to_string()).collect())
        {
            let new_rate = rate_map.get(unopened_valve_dest).expect("Should exist");
            let dist_to_valve = dist_map
                .get(&state.curr_pos)
                .expect("Should exist")
                .get(unopened_valve_dest)
                .expect("should exist");
            // Only worthwhile if we get at least some value from opening it
            if *new_rate != 0 && state.time_left > dist_to_valve + 1 {
                let time_left = state.time_left - (dist_to_valve + 1);
                let mut opened_valves = state.opened_valves.clone();
                opened_valves.push(unopened_valve_dest.clone());
                opened_valves.sort();
                let new_state = State {
                    time_left,
                    curr_pos: unopened_valve_dest.clone(),
                    opened_valves,
                    pressure: state.pressure + time_left * new_rate,
                };
                if !seen.contains(&new_state) {
                    // Don't go back unless we were opening something
                    states.add(new_state).expect("Should work");
                }
            }
        }
        i += 1;
    }
    return result;
}

fn concurrently_reached_dest(
    state: State2,
    rate_map: &HashMap<String, u32>,
    dist_map: &HashMap<String, HashMap<String, u32>>,
    unvisited_valves: HashSet<&String>,
) -> Vec<State2> {
    if unvisited_valves.len() == 1 {
        let only_dest = unvisited_valves
            .iter()
            .next()
            .expect("Should exist")
            .clone();
        let dist_worker = dist_map
            .get(&state.curr_position.0)
            .expect("Should be on the map")
            .get(only_dest)
            .expect("should exist");
        let dist_elephant = dist_map
            .get(&state.curr_position_elephant.0)
            .expect("Should be on the map")
            .get(only_dest)
            .expect("should exist");
        let min_dist = dist_worker.min(dist_elephant) + 1;
        if min_dist < state.time_left {
            let new_worker = if min_dist == *dist_worker {
                (only_dest.clone(), 0)
            } else {
                state.curr_position
            };
            let new_elephant = if min_dist == *dist_elephant {
                (only_dest.clone(), 0)
            } else {
                state.curr_position_elephant
            };
            let mut opened_valves = state.opened_valves.clone();
            opened_valves.push(only_dest.to_string());
            opened_valves.sort();
            return vec![State2 {
                time_left: state.time_left - min_dist,
                curr_position: new_worker,
                curr_position_elephant: new_elephant,
                opened_valves,
                rate: state.rate + rate_map.get(only_dest).expect("This should exist"),
                pressure: state.pressure + state.rate * min_dist,
            }];
        } else {
            return vec![];
        }
    } else {
        let cands = unvisited_valves
            .iter()
            .combinations(2)
            .into_iter()
            .filter_map(|pair| {
                let a = pair[0].clone();
                let b = pair[1].clone();
                // Determine whether it's better for worker or elephant to go to each valve;
                let a_dist_worker = dist_map
                    .get(&state.curr_position.0)
                    .expect("Should work")
                    .get(a)
                    .expect("Should exist")
                    + 1;
                let b_dist_worker = dist_map
                    .get(&state.curr_position.0)
                    .expect("Should work")
                    .get(b)
                    .expect("Should exist")
                    + 1;
                let a_dist_elephant = dist_map
                    .get(&state.curr_position_elephant.0)
                    .expect("Should work")
                    .get(a)
                    .expect("Should exist")
                    + 1;
                let b_dist_elephant = dist_map
                    .get(&state.curr_position_elephant.0)
                    .expect("Should work")
                    .get(b)
                    .expect("Should exist")
                    + 1;
                let (min_dist, new_worker, new_elephant) =
                    if a_dist_worker + b_dist_elephant < b_dist_worker + a_dist_elephant {
                        let min_dist = a_dist_worker.min(b_dist_elephant);
                        (
                            min_dist,
                            (a.clone(), a_dist_worker - min_dist),
                            (b.clone(), b_dist_elephant - min_dist),
                        )
                    } else {
                        let min_dist = b_dist_worker.min(a_dist_elephant);
                        (
                            min_dist,
                            (b.clone(), b_dist_worker - min_dist),
                            (a.clone(), a_dist_elephant - min_dist),
                        )
                    };
                if min_dist > state.time_left {
                    return None;
                }
                let mut opened_valves = state.opened_valves.clone();
                let mut new_rate = state.rate;
                if new_worker.1 == 0 {
                    opened_valves.push(new_worker.0.clone());
                    new_rate += rate_map.get(&new_worker.0).expect("Should exist");
                }
                if new_elephant.1 == 0 {
                    opened_valves.push(new_elephant.0.clone());
                    new_rate += rate_map.get(&new_elephant.0).expect("Should exist");
                }
                opened_valves.sort();
                // println!("state: {:?} {}", state, min_dist);
                Some(State2 {
                    time_left: state.time_left - min_dist,
                    curr_position: new_worker,
                    curr_position_elephant: new_elephant,
                    opened_valves: opened_valves,
                    rate: new_rate,
                    pressure: state.pressure + state.rate * min_dist,
                })
            })
            .collect_vec();
        return cands;
    }
}

// Two agent search?
fn part2(input: InputType) -> u32 {
    let mut result = 0;
    let starting_pos = "AA".to_string();
    let starting_time_in_min = 26;
    let rate_map = input.0;
    let dist_map = input.2;

    // Initial states
    let mut states: Queue<State2> = Queue::new();
    let valued_valves: HashSet<String> = rate_map
        .iter()
        .filter_map(|(k, v)| if *v != 0 { Some((k, v)) } else { None })
        .map(|(k, _)| k.clone())
        .collect();
    let mut seen: HashSet<State2> = HashSet::new();
    states
        .add(State2 {
            time_left: starting_time_in_min,
            curr_position: (starting_pos.clone(), 0),
            curr_position_elephant: (starting_pos.clone(), 0),
            opened_valves: vec![],
            rate: 0,
            pressure: 0,
        })
        .expect("This shouldn't fail");
    let mut i = 0;
    while let Ok(state) = states.remove() {
        // List of possible actions:
        // 1. Stay for the rest of the time (time_remaining)
        // 2. Go somewhere and open a valve (2 minutes)
        // 3. Go somewhere and don't open a valve (1 minutes)

        if i % 10000 == 0 {
            println!("{:?} {}", state, states.size());
        }

        // Compute pressure if we just don't do anything
        let new_pressure = state.pressure + state.time_left * state.rate;
        if new_pressure > result {
            println!("{} {} {:?}", new_pressure, states.size(), state);
            result = new_pressure;
        }
        if state.is_terminal(&valued_valves) {
            // Staying the course
            continue;
        }
        seen.insert(state.clone());
        let already_opened: HashSet<String> =
            state.opened_valves.iter().map(|v| v.to_string()).collect();
        let diff: HashSet<&String> = valued_valves.difference(&already_opened).collect();
        if state.curr_position.1 == 0 && state.curr_position_elephant.1 == 0 {
            for new_state in concurrently_reached_dest(state.clone(), &rate_map, &dist_map, diff) {
                if !seen.contains(&new_state) {
                    if state.opened_valves == vec!["BB", "DD", "HH", "JJ"] && state.pressure == 184
                    {
                        println!("where am I state: {:?}", state);
                        println!("next_state: {:?}", new_state);
                    }
                    states.add(new_state);
                }
            }
        } else {
            // Only need to activate one of the two, figure out which of the two needs to be updated
            let update_worker = state.curr_position.1 == 0;
            let worker = state.curr_position.clone();
            let elephant = state.curr_position_elephant.clone();

            let diff_len = diff.len();

            for unopened_valve_dest in diff {
                let dist_to_valve = if update_worker {
                    dist_map
                        .get(&worker.0.clone())
                        .expect("Should exist")
                        .get(unopened_valve_dest)
                        .expect("should exist")
                } else {
                    dist_map
                        .get(&elephant.0)
                        .expect("Should exist")
                        .get(unopened_valve_dest)
                        .expect("should exist")
                };

                // If the other worker is heading there, let don't fight them for it
                let in_progress_dest = if update_worker {
                    elephant.0.clone()
                } else {
                    worker.0.clone()
                };
                // But if it's the only place left, do evaluate it
                if *unopened_valve_dest == in_progress_dest {
                    if diff_len == 1 {
                        let remaining_dist = if update_worker { elephant.1 } else { worker.1 };
                        let mut opened_valves = state.opened_valves.clone();
                        opened_valves.push(in_progress_dest.clone());
                        opened_valves.sort();
                        let rate =
                            state.rate + rate_map.get(&in_progress_dest).expect("Should exist");
                        states.add(State2 {
                            time_left: state.time_left - remaining_dist,
                            curr_position: worker.clone(),
                            curr_position_elephant: elephant.clone(),
                            opened_valves,
                            rate,
                            pressure: state.pressure + state.rate * remaining_dist,
                        });
                    }
                    continue;
                }

                // Only worthwhile if we get at least some value from opening it
                if state.time_left > dist_to_valve + 1 {
                    let mut opened_valves = state.opened_valves.clone();
                    // Determine who's closest to opening the next valve;

                    let dist_to_next_update = if update_worker {
                        (dist_to_valve + 1).min(elephant.1)
                    } else {
                        (dist_to_valve + 1).min(worker.1)
                    };
                    let time_left = state.time_left - dist_to_next_update;

                    let new_worker_pos = if update_worker {
                        (
                            unopened_valve_dest.clone(),
                            dist_to_valve + 1 - dist_to_next_update,
                        )
                    } else {
                        (worker.0.clone(), worker.1 - dist_to_next_update)
                    };
                    let new_elephant_pos = if update_worker {
                        (elephant.0.clone(), elephant.1 - dist_to_next_update)
                    } else {
                        (
                            unopened_valve_dest.clone(),
                            dist_to_valve + 1 - dist_to_next_update,
                        )
                    };
                    let mut new_rate = state.rate;
                    if new_worker_pos.1 == 0 {
                        opened_valves.push(new_worker_pos.0.clone());
                        new_rate += rate_map.get(&new_worker_pos.0).expect("Should exist");
                    }
                    if new_elephant_pos.1 == 0 {
                        opened_valves.push(new_elephant_pos.0.clone());
                        new_rate += rate_map.get(&new_elephant_pos.0).expect("Should exist");
                    }
                    opened_valves.sort();

                    let new_state = State2 {
                        time_left,
                        curr_position: new_worker_pos,
                        curr_position_elephant: new_elephant_pos,
                        opened_valves,
                        pressure: state.pressure + dist_to_next_update * state.rate,
                        rate: new_rate,
                    };
                    if !seen.contains(&new_state) {
                        // if state.opened_valves == vec!["BB", "CC", "DD", "EE", "HH", "JJ"] && state.time_left == 14
                        // if state.opened_valves == vec!["DD"] && state.time_left == 24 {
                        // if state.opened_valves == vec!["DD", "JJ"] && state.time_left == 23 {
                        // if state.pressure == 20 && state.time_left == 23 {
                        //  State2 { time_left: 17, curr_position: ("CC", 0), curr_position_elephant: ("EE", 2), opened_valves: ["BB", "CC", "DD", "HH", "JJ"], rate: 78, pressure: 336 }
                        if state.opened_valves == vec!["BB", "CC", "DD", "HH", "JJ"]
                            && state.pressure == 336
                        {
                            println!("where am I state: {:?}", state);
                            println!("next_state: {:?}", new_state);
                        }
                        // Don't go back unless we were opening something
                        states.add(new_state).expect("Should work");
                    }
                }
            }
        }
        i += 1;
    }
    return result;
}

// Idea 2: Run part 1 on disjoint sets (a set and its complement);
// There are 15 such valves we must pay attention to for our input,
// which may be a little too large.
//
fn part2_rewrite(input: InputType) -> i32 {
    let mut result = 0;
    let starting_pos = "AA".to_string();
    let starting_time_in_min = 26;
    let rate_map = input.0;
    let dist_map = input.2;
    let valued_valves: HashSet<String> = rate_map
        .iter()
        .filter_map(|(k, v)| if *v != 0 { Some((k, v)) } else { None })
        .map(|(k, _)| k.clone())
        .collect();
    let valve_only_dist_map: HashMap<String, HashMap<String, u32>> = dist_map
        .iter()
        .filter_map(|(k, v)| {
            if valued_valves.contains(k) || k == "AA" {
                let new_map: HashMap<String, u32> = v
                    .iter()
                    .filter_map(|(k2, v2)| {
                        if valued_valves.contains(k2) {
                            Some((k2.clone(), v2 + 1)) // Include the cost to activate it
                        } else {
                            None
                        }
                    })
                    .collect();
                Some((k.clone(), new_map))
            } else {
                None
            }
        })
        .collect();
    // Alter the rate map to so that there's only values for two disjoint subsets
    fn bfs(
        dist_map: HashMap<String, HashMap<String, u32>>,
        rate_map: HashMap<String, u32>,
        init_time: u32,
    ) -> HashMap<Vec<String>, u32> {
        // let mut pq: PriorityQueue<(String, Vec<String>, u32, u32, u32), i32> = PriorityQueue::new();
        // pq.push(("AA".to_string(), vec![], init_time, 0, 0), 0);
        let mut queue: Queue<(String, Vec<String>, u32, u32, u32)> = Queue::new();
        queue.add(("AA".to_string(), vec![], init_time, 0, 0));

        // best combinations maps sorted path -> pressure
        let mut all_paths: HashMap<Vec<String>, u32> = HashMap::new();

        let mut i = 0;

        let mut seen: HashSet<String> = HashSet::new();

        // while let Some(((curr, path, time, pressure, rate), _time)) = pq.pop() {
        while let Ok((curr, path, time, pressure, rate)) = queue.remove() {
            let cands = dist_map.get(&curr).expect("This should be fine");

            // If this is the first time we've seen this path, we should save it.
            let path_clone = path.clone();
            let curr_pressure = pressure + rate * time;
            // path_clone.sort();
            if all_paths.contains_key(&path_clone) {
                let prev_pressure = all_paths.get(&path_clone).expect("Should be fine");
                if curr_pressure > *prev_pressure {
                    all_paths.insert(path_clone, curr_pressure);
                }
            } else {
                all_paths.insert(path_clone, curr_pressure);
            }

            for (dest, cost) in cands {
                if path.contains(dest) {
                    continue;
                }
                if *cost < time {
                    let mut new_path = path.clone();
                    new_path.push(dest.clone());
                    let new_rate = rate_map.get(dest).expect("Should exist");
                    let new_pressure = pressure + rate * *cost;
                    let new_time = time - *cost;
                    queue
                        .add((
                            dest.clone(),
                            new_path,
                            new_time,
                            new_pressure,
                            rate + new_rate,
                        ))
                        .expect("should be fine");
                    // pq.push(
                    //     (
                    //         dest.clone(),
                    //         new_path,
                    //         new_time,
                    //         new_pressure,
                    //         rate + new_rate,
                    //     ),
                    //     -(new_time as i32),
                    // );
                }
            }
            i += 1;
            if i % 1000 == 0 {
                println!("{:?}", all_paths.len());
            }
        }
        all_paths
    }

    let all_paths = bfs(valve_only_dist_map, rate_map, 26);
    let mut best_pressure = 0;
    let mut best_paths: HashMap<Vec<String>, u32> = HashMap::new();
    for (k, pressure) in all_paths {
        let mut temp = k.clone();
        temp.sort();
        if best_paths.contains_key(&temp) {
            if pressure > *best_paths.get(&temp).expect("should work") {
                best_paths.insert(temp, pressure);
            }
        } else {
            best_paths.insert(temp, pressure);
        }
    }
    println!("Size of best paths: {}", best_paths.len());
    for (path1, pressure1) in &best_paths {
        for (path2, pressure2) in &best_paths {
            if path1 == path2 {
                continue;
            }
            let unique_a = path1.iter().collect::<HashSet<_>>();
            let unique_b = path2.iter().collect::<HashSet<_>>();
            let c = unique_a.intersection(&unique_b).collect::<Vec<_>>();
            if c.len() == 0 {
                let total_pressure = pressure1 + pressure2;
                if total_pressure > best_pressure {
                    println!("{}", best_pressure);
                    best_pressure = total_pressure;
                }
            }
        }
    }
    return best_pressure as i32;
}

fn main() {
    let contents_actual =
        fs::read_to_string(INPUT_FILENAME).expect("Should have been able to read the file");
    let parsed_input_actual_1 = parse_input(contents_actual.clone());
    let parsed_input_actual_2 = parse_input(contents_actual);

    let actual_result_1 = part1(parsed_input_actual_1, 30);
    let actual_result_2 = part2_rewrite(parsed_input_actual_2);

    println!("Day 16 - Part 1");
    println!("The result for the input is: {}", actual_result_1);
    println!("Day 16 - Part 2");
    println!("The result for the input is: {}", actual_result_2);
}

#[cfg(test)]
mod tests {
    use crate::{parse_input, part1, part2, part2_rewrite};
    use std::fs;

    static SAMPLE_INPUT_FILENAME: &str = "sample.txt";

    #[test]
    fn test_part1() {
        let contents_sample = fs::read_to_string(SAMPLE_INPUT_FILENAME)
            .expect("Should have been able to read the file");
        let parsed_input_sample = parse_input(contents_sample);
        let sample_result_1 = part1(parsed_input_sample, 30);
        assert_eq!(sample_result_1, 1651);
    }

    #[test]
    fn test_part2() {
        let contents_sample = fs::read_to_string(SAMPLE_INPUT_FILENAME)
            .expect("Should have been able to read the file");
        let parsed_input_sample = parse_input(contents_sample.clone());
        let sample_result_2 = part2(parsed_input_sample);
        assert_eq!(sample_result_2, 1707);
        let parsed_input_sample = parse_input(contents_sample);
        assert_eq!(part2_rewrite(parsed_input_sample), 1707);
    }
}
