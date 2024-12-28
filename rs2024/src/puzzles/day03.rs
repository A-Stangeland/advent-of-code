use regex::Regex;
use std::cmp::min;

fn parse_mul_statement(statement: &str) -> u64 {
    let len = statement.len();
    let (x, y) = statement[4..len - 1].split_once(",").unwrap();
    return x.parse::<u64>().unwrap() * y.parse::<u64>().unwrap();
}

fn parse_memory(data: &str) -> u64 {
    let mut total = 0;
    let pattern = r"mul\(\d+,\d+\)";
    let re = Regex::new(pattern).unwrap();
    for cap in re.find_iter(data) {
        // println!("{}", cap.as_str());
        total = total + parse_mul_statement(cap.as_str());
    }
    total
}

pub fn part1(data: &str) -> u64 {
    parse_memory(data)
}

pub fn part2(data: &str) -> u64 {
    let len = data.len();
    let mut total = 0;
    let mut instructions_enabled = true;
    let mut buffer_start = 0;
    let mut buffer_end = 0;
    for i in 0..len {
        if instructions_enabled {
            if &data[i..min(i + 7, len)] == "don't()" {
                instructions_enabled = false;
                let buffer_value = &data[buffer_start..buffer_end];
                total = total + parse_memory(buffer_value);
            } else {
                buffer_end = i + 1;
            }
        } else {
            if &data[i..min(i + 4, len)] == "do()" {
                instructions_enabled = true;
                buffer_start = i;
            }
        }
    }
    if instructions_enabled {
        let buffer_value = &data[buffer_start..];
        total = total + parse_memory(buffer_value);
    }
    total
}

pub fn solve(data: &str) {
    println!("Day 2");
    println!("Part 1: {}", part1(data));
    println!("Part 2: {}", part2(data));
}

#[cfg(test)]
mod tests {
    use crate::puzzles::day03::{part1, part2};

    #[test]
    fn test_part1() {
        let input = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))";
        assert_eq!(part1(input), 161);
    }

    #[test]
    fn test_part2() {
        let input = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))";
        assert_eq!(part2(input), 48);
    }
}
