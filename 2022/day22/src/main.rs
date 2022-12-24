use std::{collections::HashMap, fs};

static INPUT_FILENAME: &str = "input.txt";

type InputType = (HashMap<Point, Position>, Vec<Action>, Point);

#[derive(Debug, Eq, Hash, PartialEq, Clone, Copy)]
enum Facing {
    Right = 0,
    Down = 1,
    Left = 2,
    Up = 3,
}

#[derive(Eq, Hash, PartialEq, Clone, Debug)]
struct Point {
    x: i32,
    y: i32,
}

#[derive(Debug)]
struct Position {
    pos: Point,
    is_wall: bool,
    up: (Point, Facing),
    down: (Point, Facing),
    left: (Point, Facing),
    right: (Point, Facing),
}

enum Action {
    RotateLeft,
    RotateRight,
    Step(i32),
}

#[derive(Debug)]
struct Grid {
    designation: (i32, i32),
    neighbors: HashMap<Facing, (Point, Facing)>,
}

impl Grid {}

fn solve_grids(init_grids: Vec<(i32, i32)>) -> HashMap<(i32, i32), Grid> {
    // Basically we populate our initial idea of the grid with information we can get via input parsing
    // After that, we iteratively fill in information until we know everything
    let mut map = HashMap::new();
    for g in &init_grids {
        map.insert(
            g.clone(),
            Grid {
                designation: g.clone(),
                neighbors: HashMap::new(),
            },
        );
    }

    // Populate initial pops
    for (g, grid) in &mut map {
        let (row, col) = g;
        // up
        if init_grids.contains(&(row - 1, col.clone())) {
            grid.neighbors.insert(
                Facing::Up,
                (
                    Point {
                        x: col.clone(),
                        y: row - 1,
                    },
                    Facing::Up,
                ),
            );
        }
        // bot
        if init_grids.contains(&(row + 1, col.clone())) {
            grid.neighbors.insert(
                Facing::Down,
                (
                    Point {
                        x: col.clone(),
                        y: row + 1,
                    },
                    Facing::Down,
                ),
            );
        }
        // right
        if init_grids.contains(&(row.clone(), col + 1)) {
            grid.neighbors.insert(
                Facing::Right,
                (
                    Point {
                        x: col + 1,
                        y: row.clone(),
                    },
                    Facing::Right,
                ),
            );
        }
        //left
        if init_grids.contains(&(row.clone(), col - 1)) {
            grid.neighbors.insert(
                Facing::Left,
                (
                    Point {
                        x: col - 1,
                        y: row.clone(),
                    },
                    Facing::Left,
                ),
            );
        }
    }

    fn rotate_right(facing: &Facing) -> Facing {
        match facing {
            Facing::Right => Facing::Up,
            Facing::Down => Facing::Right,
            Facing::Left => Facing::Down,
            Facing::Up => Facing::Left,
        }
    }

    fn rotate_left(facing: &Facing) -> Facing {
        match facing {
            Facing::Right => Facing::Down,
            Facing::Down => Facing::Left,
            Facing::Left => Facing::Up,
            Facing::Up => Facing::Right,
        }
    }

    fn get_relative_dir(relative_dir: &Facing, orientation: &Facing, desired: &Facing) -> Facing {
        // relative direction is direction we are looking to
        // orientation is the direction that we go in if we go in a direction
        // desired is the direction we want
        match (relative_dir, desired, orientation) {
            // On our left, we want up
            (Facing::Left, Facing::Up, Facing::Up) => Facing::Right,
            (Facing::Left, Facing::Up, Facing::Right) => Facing::Down,
            (Facing::Left, Facing::Up, Facing::Down) => Facing::Left,
            (Facing::Left, Facing::Up, Facing::Left) => Facing::Up,
            // On our right, we want up
            (Facing::Right, Facing::Up, Facing::Up) => Facing::Left,
            (Facing::Right, Facing::Up, Facing::Right) => Facing::Up,
            (Facing::Right, Facing::Up, Facing::Down) => Facing::Right,
            (Facing::Right, Facing::Up, Facing::Left) => Facing::Down,
            // On our left, we want down
            (Facing::Left, Facing::Down, Facing::Up) => Facing::Left,
            (Facing::Left, Facing::Down, Facing::Right) => Facing::Up,
            (Facing::Left, Facing::Down, Facing::Down) => Facing::Right,
            (Facing::Left, Facing::Down, Facing::Left) => Facing::Down,
            // On our right, we want down
            (Facing::Right, Facing::Down, Facing::Up) => Facing::Right,
            (Facing::Right, Facing::Down, Facing::Right) => Facing::Down,
            (Facing::Right, Facing::Down, Facing::Down) => Facing::Left,
            (Facing::Right, Facing::Down, Facing::Left) => Facing::Up,
            // On our top, we want left
            (Facing::Up, Facing::Left, Facing::Up) => Facing::Left,
            (Facing::Up, Facing::Left, Facing::Right) => Facing::Up,
            (Facing::Up, Facing::Left, Facing::Down) => Facing::Right,
            (Facing::Up, Facing::Left, Facing::Left) => Facing::Down,
            // On our bot, we want left
            (Facing::Down, Facing::Left, Facing::Up) => Facing::Right,
            (Facing::Down, Facing::Left, Facing::Right) => Facing::Down,
            (Facing::Down, Facing::Left, Facing::Down) => Facing::Left,
            (Facing::Down, Facing::Left, Facing::Left) => Facing::Up,
            // On our top, we want right
            (Facing::Up, Facing::Right, Facing::Up) => Facing::Right,
            (Facing::Up, Facing::Right, Facing::Right) => Facing::Down,
            (Facing::Up, Facing::Right, Facing::Down) => Facing::Left,
            (Facing::Up, Facing::Right, Facing::Left) => Facing::Up,
            // On our bot, we want right
            (Facing::Down, Facing::Right, Facing::Up) => Facing::Left,
            (Facing::Down, Facing::Right, Facing::Right) => Facing::Up,
            (Facing::Down, Facing::Right, Facing::Down) => Facing::Right,
            (Facing::Down, Facing::Right, Facing::Left) => Facing::Down,
            _ => panic!("We shouldn't be querying for more than this"),
        }
    }

    loop {
        let mut changed = false;
        for g in &init_grids {
            let mut grid = map.remove(g).expect("should exist");
            // check top
            if !grid.neighbors.contains_key(&Facing::Up) {
                // Check left top
                if let Some(potential) = grid.neighbors.get(&Facing::Left) {
                    let potential_grid_key = (potential.0.y, potential.0.x);
                    let potential_grid = map.get(&potential_grid_key).expect("should exist");
                    let relative_facing =
                        get_relative_dir(&Facing::Left, &potential.1, &Facing::Up);
                    if let Some((new_pt, new_facing)) =
                        potential_grid.neighbors.get(&relative_facing)
                    {
                        let new_facing = rotate_right(&new_facing);
                        grid.neighbors
                            .insert(Facing::Up, (new_pt.clone(), new_facing));
                        changed = true;
                    }
                }
                // Check right top
                if let None = grid.neighbors.get(&Facing::Up) {
                    if let Some(potential) = grid.neighbors.get(&Facing::Right) {
                        let potential_grid_key = (potential.0.y, potential.0.x);
                        let potential_grid = map.get(&potential_grid_key).expect("should exist");
                        let relative_facing =
                            get_relative_dir(&Facing::Right, &potential.1, &Facing::Up);
                        if let Some((new_pt, new_facing)) =
                            potential_grid.neighbors.get(&relative_facing)
                        {
                            let new_facing = rotate_left(&new_facing);
                            grid.neighbors
                                .insert(Facing::Up, (new_pt.clone(), new_facing));
                            changed = true;
                        }
                    }
                }
            }
            // check right
            if !grid.neighbors.contains_key(&Facing::Right) {
                // Check top right
                if let Some(potential) = grid.neighbors.get(&Facing::Up) {
                    let potential_grid_key = (potential.0.y, potential.0.x);
                    let potential_grid = map.get(&potential_grid_key).expect("should exist");
                    let relative_facing =
                        get_relative_dir(&Facing::Up, &potential.1, &Facing::Right);
                    if let Some((new_pt, new_facing)) =
                        potential_grid.neighbors.get(&relative_facing)
                    {
                        let new_facing = rotate_right(&new_facing);
                        grid.neighbors
                            .insert(Facing::Right, (new_pt.clone(), new_facing));
                        changed = true;
                    }
                }
                // Check bot right
                if let None = grid.neighbors.get(&Facing::Right) {
                    if let Some(potential) = grid.neighbors.get(&Facing::Down) {
                        let potential_grid_key = (potential.0.y, potential.0.x);
                        let potential_grid = map.get(&potential_grid_key).expect("should exist");
                        let relative_facing =
                            get_relative_dir(&Facing::Down, &potential.1, &Facing::Right);
                        if let Some((new_pt, new_facing)) =
                            potential_grid.neighbors.get(&relative_facing)
                        {
                            let new_facing = rotate_left(&new_facing);
                            grid.neighbors
                                .insert(Facing::Right, (new_pt.clone(), new_facing));
                            changed = true;
                        }
                    }
                }
            }

            // check bot
            if !grid.neighbors.contains_key(&Facing::Down) {
                // Check left bot
                if let Some(potential) = grid.neighbors.get(&Facing::Left) {
                    let potential_grid_key = (potential.0.y, potential.0.x);
                    let potential_grid = map.get(&potential_grid_key).expect("should exist");
                    let relative_facing =
                        get_relative_dir(&Facing::Left, &potential.1, &Facing::Down);
                    if let Some((new_pt, new_facing)) =
                        potential_grid.neighbors.get(&relative_facing)
                    {
                        let new_facing = rotate_left(&new_facing);
                        grid.neighbors
                            .insert(Facing::Down, (new_pt.clone(), new_facing));
                        changed = true;
                    }
                }
                // Check right bot
                if let None = grid.neighbors.get(&Facing::Down) {
                    if let Some(potential) = grid.neighbors.get(&Facing::Right) {
                        let potential_grid_key = (potential.0.y, potential.0.x);
                        let potential_grid = map.get(&potential_grid_key).expect("should exist");
                        let relative_facing =
                            get_relative_dir(&Facing::Right, &potential.1, &Facing::Down);
                        if let Some((new_pt, new_facing)) =
                            potential_grid.neighbors.get(&relative_facing)
                        {
                            let new_facing = rotate_right(&new_facing);
                            grid.neighbors
                                .insert(Facing::Down, (new_pt.clone(), new_facing));
                            changed = true;
                        }
                    }
                }
            }

            // check left
            if !grid.neighbors.contains_key(&Facing::Left) {
                // Check top left
                if let Some(potential) = grid.neighbors.get(&Facing::Up) {
                    let potential_grid_key = (potential.0.y, potential.0.x);
                    let potential_grid = map.get(&potential_grid_key).expect("should exist");
                    let relative_facing =
                        get_relative_dir(&Facing::Up, &potential.1, &Facing::Left);
                    if let Some((new_pt, new_facing)) =
                        potential_grid.neighbors.get(&relative_facing)
                    {
                        let new_facing = rotate_left(&new_facing);
                        grid.neighbors
                            .insert(Facing::Left, (new_pt.clone(), new_facing));
                        changed = true;
                    }
                }
                // Check bot left
                if let None = grid.neighbors.get(&Facing::Left) {
                    if let Some(potential) = grid.neighbors.get(&Facing::Down) {
                        let potential_grid_key = (potential.0.y, potential.0.x);
                        let potential_grid = map.get(&potential_grid_key).expect("should exist");
                        let relative_facing =
                            get_relative_dir(&Facing::Down, &potential.1, &Facing::Left);
                        if let Some((new_pt, new_facing)) =
                            potential_grid.neighbors.get(&relative_facing)
                        {
                            let new_facing = rotate_right(&new_facing);
                            grid.neighbors
                                .insert(Facing::Left, (new_pt.clone(), new_facing));
                            changed = true;
                        }
                    }
                }
            }

            map.insert(grid.designation.clone(), grid);
        }

        if !changed {
            break;
        }
    }

    return map;
}

fn parse_input(input: String) -> InputType {
    let mut line_iter = input.lines().into_iter();
    // Parse map
    let mut row_num = 1;
    let mut col_num = 1;
    let mut rows = row_num;
    let mut cols = col_num;

    let mut positions: HashMap<Point, Position> = HashMap::new();
    let mut init_point = Point { x: 0, y: 0 };
    while let Some(line) = line_iter.next() {
        if line == "" {
            break;
        }
        let mut row = vec![];
        col_num = 1;
        for c in line.chars() {
            row.push(c);
            if c != ' ' {
                let curr_point = Point {
                    x: col_num,
                    y: row_num,
                };

                // Mark the starting position
                if positions.is_empty() {
                    init_point = curr_point.clone();
                }
                positions.insert(
                    curr_point.clone(),
                    Position {
                        pos: curr_point,
                        is_wall: c == '#',
                        up: (Point { x: 0, y: 0 }, Facing::Right),
                        down: (Point { x: 0, y: 0 }, Facing::Right),
                        left: (Point { x: 0, y: 0 }, Facing::Right),
                        right: (Point { x: 0, y: 0 }, Facing::Right),
                    },
                );
            }
            col_num += 1;
            if col_num > cols {
                cols = col_num;
            }
        }
        row_num += 1;
        if row_num > rows {
            rows = row_num;
        }
    }

    // parse instructions
    let instruction_str = line_iter.next().expect("should exist");
    let mut curr_num = "".to_string();

    let mut instructions = Vec::new();

    for c in instruction_str.chars() {
        match c {
            'R' => {
                if !curr_num.is_empty() {
                    instructions.push(Action::Step(curr_num.parse().expect("should work")));
                    curr_num = "".to_string();
                }
                instructions.push(Action::RotateRight);
            }
            'L' => {
                if !curr_num.is_empty() {
                    instructions.push(Action::Step(curr_num.parse().expect("should work")));
                    curr_num = "".to_string();
                }
                instructions.push(Action::RotateLeft);
            }
            num => {
                curr_num.push(num);
            }
        }
    }
    if !curr_num.is_empty() {
        instructions.push(Action::Step(curr_num.parse().expect("should work")));
    }

    // For each row, track the first and last and tie up left-right relationships
    for row in 1..rows {
        let mut left_most = Point { x: 1, y: row };
        let mut right_most = Point {
            x: cols - 1,
            y: row,
        };
        for col in 1..cols {
            let p = Point { x: col, y: row };
            if positions.contains_key(&p) {
                // check left and right. If no left, record left-most. If no right, record right-most;
                let left = Point { x: col - 1, ..p };
                let right = Point { x: col + 1, ..p };
                if !positions.contains_key(&left) {
                    left_most = p.clone();
                } else {
                    let mut pos = positions.get_mut(&p).expect("should exist");
                    pos.left = (left.clone(), Facing::Left);
                }
                if !positions.contains_key(&right) {
                    right_most = p.clone();
                } else {
                    let mut pos = positions.get_mut(&p).expect("should exist");
                    pos.right = (right.clone(), Facing::Right);
                }
            }
        }
        let left_border = positions.get_mut(&left_most).expect("should exist");
        left_border.left = (right_most.clone(), Facing::Left);
        let right_border = positions.get_mut(&right_most).expect("should exist");
        right_border.right = (left_most.clone(), Facing::Right);
    }
    // For each col, track the first and last and tie up up-down relationships
    for col in 1..cols {
        let mut top_most = Point { x: col, y: 1 };
        let mut bot_most = Point {
            x: col,
            y: rows - 1,
        };
        for row in 1..rows {
            let p = Point { x: col, y: row };
            if positions.contains_key(&p) {
                let top = Point { y: row - 1, ..p };
                let bot = Point { y: row + 1, ..p };

                if !positions.contains_key(&top) {
                    top_most = p.clone();
                } else {
                    let mut pos = positions.get_mut(&p).expect("should exist");
                    pos.up = (top.clone(), Facing::Up);
                }
                if !positions.contains_key(&bot) {
                    bot_most = p.clone();
                } else {
                    let mut pos = positions.get_mut(&p).expect("should exist");
                    pos.down = (bot.clone(), Facing::Down);
                }
            }
        }
        let top_border = positions.get_mut(&top_most).expect("should exist");
        top_border.up = (bot_most.clone(), Facing::Up);
        let bot_border = positions.get_mut(&bot_most).expect("should exist");
        bot_border.down = (top_most.clone(), Facing::Down);
    }

    return (positions, instructions, init_point);
}

fn parse_input_cube(input: String) -> InputType {
    let mut line_iter = input.lines().into_iter();
    // Parse map
    let mut row_num = 1;
    let mut col_num = 1;
    let mut rows = row_num;
    let mut cols = col_num;

    let mut positions: HashMap<Point, Position> = HashMap::new();
    let mut init_point = Point { x: 0, y: 0 };
    let mut cube_width = i32::MAX;
    while let Some(line) = line_iter.next() {
        if line == "" {
            break;
        }
        let mut row = vec![];
        col_num = 1;
        let mut cube_start = 0;
        let mut cube_end = 0;
        for c in line.chars() {
            row.push(c);
            if c != ' ' {
                if cube_start == 0 {
                    cube_start = col_num;
                }
                cube_end = col_num;
                let curr_point = Point {
                    x: col_num,
                    y: row_num,
                };

                // Mark the starting position
                if positions.is_empty() {
                    init_point = curr_point.clone();
                }
                positions.insert(
                    curr_point.clone(),
                    Position {
                        pos: curr_point,
                        is_wall: c == '#',
                        up: (Point { x: 0, y: 0 }, Facing::Up),
                        down: (Point { x: 0, y: 0 }, Facing::Up),
                        left: (Point { x: 0, y: 0 }, Facing::Up),
                        right: (Point { x: 0, y: 0 }, Facing::Up),
                    },
                );
            }
            col_num += 1;
            if col_num > cols {
                cols = col_num;
            }
        }
        row_num += 1;
        if row_num > rows {
            rows = row_num;
        }
        let cube_width_curr = cube_end - cube_start;
        if cube_width_curr < cube_width {
            cube_width = cube_width_curr + 1;
        }
    }

    println!("cube width: {}", cube_width);
    let mut grids: Vec<(i32, i32)> = positions
        .keys()
        .into_iter()
        .map(|k| ((k.y - 1) / cube_width, (k.x - 1) / cube_width))
        .collect();
    grids.sort();
    grids.dedup();
    println!("grids: {:?}", grids);
    // We can collect the sides of each grid, in which case for each side we can give it an idea of top, right, bot, and left.
    // Then the only problem left is stitching together the cube.
    // Let us say that up and down on the level of individual grids are always the same, in which case it is only the edges that need special casing
    // Also note that at least 1 side is connected, so we have a sense of at least some sense of shared direction on each grid?.
    // e.g.
    //     1
    // 2 3 4
    //     5 6
    // 1: up is down for 2, right is left for 6, down is down for 4, left is down for 3
    // 2: up is down for 1, right is right for 3, down is up for 5, left is up for 6
    // 3: up is right for 1, right is right for 4, down is right for 5, left is left for 2
    // 4: up is up for 1, right is down for 6, down is down for 5, left is left for 3
    // 5: up is up for 4, right is right for 6, down is up for 2, left is up for 3
    // 6: up is left for 4, right is left for 1, down is right for 2, left is left for 5

    // e.g.
    //    1 2
    //    3
    //  4 5
    //  6
    // Things to figure out:
    // up, left for 1
    // up, right, down for 2
    // left, right for 3
    // up, left for 4
    // down, right for 5
    // left, down, right for 6

    // 1 away is always adjacent side, adjacent corners are also adjacent (corners -> rotate 90 degrees?)
    // 2 away vertically (possibly asymmetric) are always opposite sides, so we know that the other 4 are what we need to pay attention to
    // algo proposal:
    // for each face (consider it as facing you)
    //     For every edge, determine what it is adjacent to and which direction we're mapping across [facing dir is opposing edge dir we came from, if we are facing left, we came from right edge?]
    // Essentially we want to find a mapping from an edge to another edge. (if we go down twice, then we're facing the same direction as up on the opposite side)
    // There's two ways to fold the box, (inside vs. outside), we opt to view it as folding the box such that the center is pointing towards us (rather than away).
    //
    // Maybe we can fold more informative ones first and force constraints? Like if we fold 3 -> 4, we know that 4 up is 3 left. Then if we fold 3 -> 2, we know that 3 right is 2 up and necessarily makes 5 neighboring 2?

    // For each time we go off the edge, determine where it would land, i.e. if we want down, but down doesn't exist, check left down or right down or right right down? up up up?
    // Must do it per-grid rather than per-pos in edge because we want unity among ideas?

    // Paste grid onto existing cube and force constraints around pasting?
    // 3d traversals?

    // Alternative idea is to map this out into a cubic globe with x, y, and z and keeping track of directions?

    // Determine Grid directions
    // This gives us which grid borders which grid and the direction it will go in if we cross the grid?
    let mut grid_solved = solve_grids(grids.clone());

    // For each grid, get all edges
    let mut known_edges: HashMap<(i32, i32), (Vec<Point>, Vec<Point>, Vec<Point>, Vec<Point>)> =
        HashMap::new();
    for (grid_row, grid_col) in grid_solved.keys() {
        let start_row = cube_width * grid_row + 1;
        let end_row = cube_width * (grid_row + 1) + 1;
        let start_col = cube_width * grid_col + 1;
        let end_col = cube_width * (grid_col + 1) + 1;
        // clockwise obtain edges
        let top: Vec<Point> = (start_col..end_col)
            .into_iter()
            .map(|col| Point {
                x: col,
                y: start_row,
            })
            .collect();
        let right: Vec<Point> = (start_row..end_row)
            .into_iter()
            .map(|row| Point {
                x: end_col - 1,
                y: row,
            })
            .collect();
        let bot: Vec<Point> = (start_col..end_col)
            .into_iter()
            .rev()
            .map(|col| Point {
                x: col,
                y: end_row - 1,
            })
            .collect();
        let left: Vec<Point> = (start_row..end_row)
            .into_iter()
            .rev()
            .map(|row| Point {
                x: start_col,
                y: row,
            })
            .collect();
        known_edges.insert((*grid_row, *grid_col), (top, right, bot, left));
    }

    // parse instructions
    let instruction_str = line_iter.next().expect("should exist");
    let mut curr_num = "".to_string();

    let mut instructions = Vec::new();

    for c in instruction_str.chars() {
        match c {
            'R' => {
                if !curr_num.is_empty() {
                    instructions.push(Action::Step(curr_num.parse().expect("should work")));
                    curr_num = "".to_string();
                }
                instructions.push(Action::RotateRight);
            }
            'L' => {
                if !curr_num.is_empty() {
                    instructions.push(Action::Step(curr_num.parse().expect("should work")));
                    curr_num = "".to_string();
                }
                instructions.push(Action::RotateLeft);
            }
            num => {
                curr_num.push(num);
            }
        }
    }
    if !curr_num.is_empty() {
        instructions.push(Action::Step(curr_num.parse().expect("should work")));
    }

    // For each row, connect everything except for the edges
    for row in 1..rows {
        for col in 1..cols {
            let p = Point { x: col, y: row };
            if positions.contains_key(&p) {
                // check left and right. If no left, record left-most. If no right, record right-most;
                let left = Point { x: col - 1, ..p };
                let right = Point { x: col + 1, ..p };
                if positions.contains_key(&left) {
                    let mut pos = positions.get_mut(&p).expect("should exist");
                    pos.left = (left.clone(), Facing::Left);
                }
                if positions.contains_key(&right) {
                    let mut pos = positions.get_mut(&p).expect("should exist");
                    pos.right = (right.clone(), Facing::Right);
                }
            }
        }
    }
    // For each col, connect everything except for the edges
    for col in 1..cols {
        for row in 1..rows {
            let p = Point { x: col, y: row };
            if positions.contains_key(&p) {
                let top = Point { y: row - 1, ..p };
                let bot = Point { y: row + 1, ..p };

                if positions.contains_key(&top) {
                    let mut pos = positions.get_mut(&p).expect("should exist");
                    pos.up = (top.clone(), Facing::Up);
                }
                if positions.contains_key(&bot) {
                    let mut pos = positions.get_mut(&p).expect("should exist");
                    pos.down = (bot.clone(), Facing::Down);
                }
            }
        }
    }

    // Tie up edges by iterating through the list and getting relative directions from
    for g in &grids {
        let grid = grid_solved.remove(&g).expect("should exist");
        let (top, right, bot, left) = known_edges.remove(&g).expect("edges should exist");
        // check top
        let (grid_top, top_facing) = grid.neighbors.get(&Facing::Up).expect("should exist");
        let relative_facing = known_edges
            .get(&(grid_top.y, grid_top.x))
            .expect("should be fine");
        // Note that this is the direction this is going, which means that we want the points on the opposite edge since those are the touching points
        let relative_edges = match top_facing {
            Facing::Up => &relative_facing.2,
            Facing::Right => &relative_facing.3,
            Facing::Down => &relative_facing.0,
            Facing::Left => &relative_facing.1,
        };
        // Since we recorded everything in clock-wise order, we can just connect each thing together as long as we reverse one array
        for (p1, p2) in top.iter().zip(relative_edges.iter().rev()) {
            // We don't actually need to overwrite existing ones, but it should still be correct if we do
            let pos1 = positions.get_mut(p1).expect("should exist");
            pos1.up = (p2.clone(), *top_facing);
        }

        // check bot
        let (grid_bot, bot_facing) = grid.neighbors.get(&Facing::Down).expect("Should exist");
        let relative_facing = known_edges
            .get(&(grid_bot.y, grid_bot.x))
            .expect("should be fine");
        let relative_edges = match bot_facing {
            Facing::Up => &relative_facing.2,
            Facing::Right => &relative_facing.3,
            Facing::Down => &relative_facing.0,
            Facing::Left => &relative_facing.1,
        };
        for (p1, p2) in bot.iter().zip(relative_edges.iter().rev()) {
            let pos1 = positions.get_mut(p1).expect("should exist");
            pos1.down = (p2.clone(), *bot_facing);
        }

        // right
        let (grid_right, right_facing) = grid.neighbors.get(&Facing::Right).expect("Should exist");
        let relative_facing = known_edges
            .get(&(grid_right.y, grid_right.x))
            .expect("should be fine");
        let relative_edges = match right_facing {
            Facing::Up => &relative_facing.2,
            Facing::Right => &relative_facing.3,
            Facing::Down => &relative_facing.0,
            Facing::Left => &relative_facing.1,
        };
        for (p1, p2) in right.iter().zip(relative_edges.iter().rev()) {
            let pos1 = positions.get_mut(p1).expect("should exist");
            pos1.right = (p2.clone(), *right_facing);
        }

        // left
        let (grid_left, left_facing) = grid.neighbors.get(&Facing::Left).expect("Should exist");
        let relative_facing = known_edges
            .get(&(grid_left.y, grid_left.x))
            .expect("should be fine");
        let relative_edges = match left_facing {
            Facing::Up => &relative_facing.2,
            Facing::Right => &relative_facing.3,
            Facing::Down => &relative_facing.0,
            Facing::Left => &relative_facing.1,
        };
        for (p1, p2) in left.iter().zip(relative_edges.iter().rev()) {
            let pos1 = positions.get_mut(p1).expect("should exist");
            pos1.left = (p2.clone(), *left_facing);
        }

        grid_solved.insert(g.clone(), grid);
        known_edges.insert(g.clone(), (top, right, bot, left));
    }

    return (positions, instructions, init_point);
}

fn part1(input: InputType) -> i32 {
    let mut result = 0;

    let map = input.0;
    let instructions = input.1;
    let mut pos = input.2;
    let mut facing = Facing::Right;

    for instruction in instructions {
        match instruction {
            Action::RotateLeft => {
                facing = match facing {
                    Facing::Right => Facing::Up,
                    Facing::Down => Facing::Right,
                    Facing::Left => Facing::Down,
                    Facing::Up => Facing::Left,
                }
            }
            Action::RotateRight => {
                facing = match facing {
                    Facing::Right => Facing::Down,
                    Facing::Down => Facing::Left,
                    Facing::Left => Facing::Up,
                    Facing::Up => Facing::Right,
                }
            }
            Action::Step(num_steps) => {
                for i in 0..num_steps {
                    let curr_pos = map.get(&pos).expect("should exist");
                    let next_step = match facing {
                        Facing::Right => &curr_pos.right,
                        Facing::Down => &curr_pos.down,
                        Facing::Left => &curr_pos.left,
                        Facing::Up => &curr_pos.up,
                    };
                    let next_pos = map.get(&next_step.0).expect("should exist");
                    if next_pos.is_wall {
                        break;
                    } else {
                        pos = next_step.0.clone();
                    }
                }
            }
        }
    }

    let row = pos.y;
    let col = pos.x;
    println!("{} {} {:?}", row, col, facing);

    result = 1000 * row + 4 * col + facing as i32;
    return result;
}

fn part2(input: InputType) -> i32 {
    let mut result = 0;

    let map = input.0;
    let instructions = input.1;
    let mut pos = input.2;
    let mut facing = Facing::Right;

    for instruction in instructions {
        match instruction {
            Action::RotateLeft => {
                facing = match facing {
                    Facing::Right => Facing::Up,
                    Facing::Down => Facing::Right,
                    Facing::Left => Facing::Down,
                    Facing::Up => Facing::Left,
                }
            }
            Action::RotateRight => {
                facing = match facing {
                    Facing::Right => Facing::Down,
                    Facing::Down => Facing::Left,
                    Facing::Left => Facing::Up,
                    Facing::Up => Facing::Right,
                }
            }
            Action::Step(num_steps) => {
                for i in 0..num_steps {
                    let curr_pos = map.get(&pos).expect("should exist");
                    let next_step = match facing {
                        Facing::Right => &curr_pos.right,
                        Facing::Down => &curr_pos.down,
                        Facing::Left => &curr_pos.left,
                        Facing::Up => &curr_pos.up,
                    };
                    let next_pos = map.get(&next_step.0).expect("should exist");
                    if next_pos.is_wall {
                        break;
                    } else {
                        facing = next_step.1;
                        pos = next_step.0.clone();
                    }
                }
            }
        }
    }

    let row = pos.y;
    let col = pos.x;
    println!("{} {} {:?}", row, col, facing);

    result = 1000 * row + 4 * col + facing as i32;
    return result;
}

fn main() {
    let contents_actual =
        fs::read_to_string(INPUT_FILENAME).expect("Should have been able to read the file");
    let parsed_input_actual_1 = parse_input(contents_actual.clone());
    let parsed_input_actual_2 = parse_input_cube(contents_actual);

    let actual_result_1 = part1(parsed_input_actual_1);
    let actual_result_2 = part2(parsed_input_actual_2);

    println!("Day 22 - Part 1");
    println!("The result for the input is: {}", actual_result_1);
    println!("Day 22 - Part 2");
    println!("The result for the input is: {}", actual_result_2);
}

#[cfg(test)]
mod tests {
    use crate::{parse_input, parse_input_cube, part1, part2};
    use std::fs;

    static SAMPLE_INPUT_FILENAME: &str = "sample.txt";

    #[test]
    fn test_part1() {
        let contents_sample = fs::read_to_string(SAMPLE_INPUT_FILENAME)
            .expect("Should have been able to read the file");
        let parsed_input_sample = parse_input(contents_sample);
        let sample_result_1 = part1(parsed_input_sample);
        assert_eq!(sample_result_1, 6032);
    }

    #[test]
    fn test_part2() {
        let contents_sample = fs::read_to_string(SAMPLE_INPUT_FILENAME)
            .expect("Should have been able to read the file");
        let parsed_input_sample = parse_input_cube(contents_sample);
        let sample_result_2 = part2(parsed_input_sample);
        assert_eq!(sample_result_2, 5031);
    }
}
