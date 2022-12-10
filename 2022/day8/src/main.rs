use std::cmp;
use std::fmt::Debug;
use std::fs;
static SAMPLE_INPUT_FILENAME: &str = "sample.txt";
static INPUT_FILENAME: &str = "input.txt";

type ContentType = Vec<Vec<u8>>;

fn parse_input(contents: String) -> ContentType {
    let (mut width, mut height) = (0, 0);
    for line in contents.lines() {
        width = line.len();
        height += 1;
    }

    let mut array = vec![vec![0u8; width]; height];

    let mut i;
    let mut j = 0;
    for line in contents.lines() {
        i = 0;
        for c in line.chars() {
            array[j][i] = c.to_digit(10).expect("parsing should work") as u8;
            i += 1;
        }
        j += 1
    }
    return array;
}

fn puzzle1(contents: &ContentType) -> i32 {
    let mut result = 0;
    let height = contents.len();
    let width = contents.get(0).expect("This should exist").len();

    // Compute top, left, right, and bot covers by taking the max of the top, left, right, and bot blocks.
    // This gives us the max seen so far for a given row/col in a direction.
    let mut left_cover = vec![vec![0u8; width]; height];
    let mut top_cover = vec![vec![0u8; width]; height];
    for row in 0..height {
        for col in 0..width {
            if row != 0 {
                top_cover[row][col] = cmp::max(top_cover[row - 1][col], contents[row - 1][col]);
            }
            if col != 0 {
                left_cover[row][col] = cmp::max(left_cover[row][col - 1], contents[row][col - 1])
            }
        }
    }
    let mut right_cover = vec![vec![0u8; width]; height];
    let mut bot_cover = vec![vec![0u8; width]; height];
    for row in (0..height).rev() {
        for col in (0..width).rev() {
            if row != height - 1 {
                bot_cover[row][col] = cmp::max(bot_cover[row + 1][col], contents[row + 1][col]);
            }
            if col != width - 1 {
                right_cover[row][col] = cmp::max(right_cover[row][col + 1], contents[row][col + 1])
            }
        }
    }
    for row in 1..height - 1 {
        for col in 1..width - 1 {
            if contents[row][col] > left_cover[row][col]
                || contents[row][col] > top_cover[row][col]
                || contents[row][col] > bot_cover[row][col]
                || contents[row][col] > right_cover[row][col]
            {
                result += 1;
            }
        }
    }

    // Add 2 * width + 2 * height - 4 to get the sides minus overlapping corners
    return result + (height * 2 + width * 2 - 4) as i32;
}

fn puzzle2(contents: &ContentType) -> u32 {
    let height = contents.len();
    let width = contents.get(0).expect("This should exist").len();

    // Suppose going from left to right, if left tree is at least as tall as right tree,
    // we reset the count. If the left tree is larger than
    // 7 6 5 4 6 7 7 8 2 4 9
    // [7] 0 -> [7, 6] 1 -> [7, 6, 5] 1 -> [7, 6, 5, 4] 1 -> [7, 6] 3 -> [7] 5 -> [7] 1 -> [8] 6 -> [8, 2] 1 -> [9] 9
    //
    // 8 7 5 3 2 1 2 3 1 4 6 9
    // [8] 0 -> [8, 7] 1 -> [8, 7, 5] 1 -> [8, 7, 5, 3] 1 -> [8, 7, 5, 3, 2] 1 -> [8, 7, 5, 3, 2, 1] 1 ->
    // [8, 7, 5, 3, 2] 2 -> [8, 7, 5, 3] 4 -> [8, 7, 5, 3, 1] 1 -> [8, 7, 5, 4] 7 -> [8, 7, 6] 9 -> [9] 11
    // Rules:
    // First col is 0
    // If lower, always view of 1
    // If greater than or equal to, we collapse a view (keep popping until less than or equal) and count
    // If greatest we've seen so far, then we go all the way to the beginning
    // ================= Roll-up algorithm =================
    // if lower, add new array dominated by itself, e.g. (9, 1) -> (9, 1) (8, 0)
    // if higher, keep rolling up until we know how many things we can see, init is 1 because we must
    //     see at least 1 tree unless we're an edge, e.g. (4, 0) (2, 1) (1, 1) (3, 0) -> (4, 0) (3, 2) => (4, 0) (3, 2) (5, 0) -> (5, 4)
    fn roll_up(stack: &mut Vec<(u8, u8)>, height: u8) -> u32 {
        let mut curr_amount = 0;

        while let Some((prev_height, amount)) = stack.last() {
            if *prev_height < height {
                curr_amount += *amount + 1;
                stack.pop();
            } else if *prev_height == height {
                // Stay here
                break;
            } else {
                break;
            }
        }
        stack.push((height, curr_amount));
        if stack.len() > 1 {
            curr_amount += 1;
        }
        return (curr_amount) as u32;
    }

    let mut left_cover = vec![vec![0u32; width]; height];
    for row in 0..height {
        let mut left_stack: Vec<(u8, u8)> = Vec::new();
        for col in 0..width {
            let curr_height = contents[row][col];
            if col == 0 {
                left_stack.push((curr_height, 0));
            } else {
                left_cover[row][col] = roll_up(&mut left_stack, curr_height);
            }
        }
    }

    let mut top_cover = vec![vec![0u32; width]; height];
    for col in 0..width {
        let mut top_stack: Vec<(u8, u8)> = Vec::new();
        for row in 0..height {
            let curr_height = contents[row][col];
            if row == 0 {
                top_stack.push((curr_height, 0));
            } else {
                top_cover[row][col] = roll_up(&mut top_stack, curr_height);
            }
        }
    }

    let mut right_cover = vec![vec![0u32; width]; height];
    for row in (0..width).rev() {
        let mut right_stack: Vec<(u8, u8)> = Vec::new();
        for col in (0..height).rev() {
            let curr_height = contents[row][col];
            if col == width - 1 {
                right_stack.push((curr_height, 0));
            } else {
                right_cover[row][col] = roll_up(&mut right_stack, curr_height);
            }
        }
    }

    let mut bot_cover = vec![vec![0u32; width]; height];
    for col in (0..height).rev() {
        let mut bot_stack: Vec<(u8, u8)> = Vec::new();
        for row in (0..width).rev() {
            let curr_height = contents[row][col];
            if row == height - 1 {
                bot_stack.push((curr_height, 0))
            } else {
                bot_cover[row][col] = roll_up(&mut bot_stack, curr_height);
            }
        }
    }

    let mut array = vec![vec![0u32; width]; height];
    let mut result = 0;
    for col in 0..width {
        for row in 0..height {
            array[row][col] = bot_cover[row][col]
                * top_cover[row][col]
                * left_cover[row][col]
                * right_cover[row][col];
            if array[row][col] > result {
                result = array[row][col]
            }
        }
    }

    return result;
}

fn _print_array<T: Debug>(array: &Vec<Vec<T>>) {
    for v in array {
        println!("{:?}", v);
    }
    println!();
}

fn main() {
    let contents_sample =
        fs::read_to_string(SAMPLE_INPUT_FILENAME).expect("Should have been able to read the file");
    let parsed_input_sample = parse_input(contents_sample);
    let contents_actual =
        fs::read_to_string(INPUT_FILENAME).expect("Should have been able to read the file");
    let parsed_input_actual = parse_input(contents_actual);

    let sample_result_1 = puzzle1(&parsed_input_sample);
    assert_eq!(sample_result_1, 21);
    let actual_result_1 = puzzle1(&parsed_input_actual);
    println!("Day 8 - Puzzle 1");
    println!("The sample result is: {}", sample_result_1);
    println!("The result for the input is: {}", actual_result_1);

    let sample_result_2 = puzzle2(&parsed_input_sample);
    assert_eq!(sample_result_2, 8);
    let actual_result_2 = puzzle2(&parsed_input_actual);
    println!("Day 8 - Puzzle 2");
    println!("The sample result is: {}", sample_result_2);
    println!("The result for the input is: {}", actual_result_2);
}
