use std::collections::HashMap;
use std::ops::Index;
use std::vec::Vec;

const DIGITS: &str = "0123456789";
type GearMap = HashMap<(usize, usize), Vec<u64>>;

struct CharGrid {
    height: usize,
    width: usize,
    values: Vec<char>,
}

impl CharGrid {
    fn new(data: &str) -> Self {
        let mut data_split: Vec<&str> = data.split('\n').collect();
        if data_split.last().unwrap().len() == 0 {
            data_split.remove(data_split.len() - 1);
        }
        CharGrid {
            height: data_split.len(),
            width: data_split[0].len(),
            values: data_split.join("").chars().collect::<Vec<char>>(),
        }
    }

    fn valid_coord(&self, i: usize, j: usize) -> bool {
        if i >= self.height {
            return false;
        }
        if j >= self.width {
            return false;
        }
        true
    }

    fn is_symbol(&self, i: usize, j: usize) -> bool {
        if self.valid_coord(i, j) && is_symbol(self[(i, j)]) {
            return true;
        }
        false
    }

    fn is_gear(&self, i: usize, j: usize) -> bool {
        if self.valid_coord(i, j) && self[(i, j)] == '*' {
            return true;
        }
        false
    }

    fn _print(&self) {
        for i in 0..self.height {
            for j in 0..self.width {
                print!("{}", self[(i, j)]);
            }
            println!("");
        }
    }
}

impl Index<(usize, usize)> for CharGrid {
    type Output = char;

    fn index(&self, index: (usize, usize)) -> &Self::Output {
        let (i, j) = index;
        &self.values[self.width * i + j]
    }
}

// struct GridParser {
//     grid: &CharGrid,
//     buffer: String,
// }

fn is_symbol(c: char) -> bool {
    c != '.' && !DIGITS.contains(c)
}

fn is_part_number(grid: &CharGrid, i: usize, j: usize, w: usize) -> bool {
    for k in 0..(w + 2) {
        if j + k < w {
            continue;
        }
        if grid.is_symbol(i + 1, j + k - w) {
            return true;
        }
        if i > 0 && grid.is_symbol(i - 1, j + k - w) {
            return true;
        }
    }
    if j >= w && grid.is_symbol(i, j - w) {
        return true;
    }
    if grid.is_symbol(i, j + 1) {
        return true;
    }
    false
}

fn flush_buffer(buffer: &mut String, grid: &CharGrid, i: usize, j: usize) -> u64 {
    let w: usize = buffer.len();
    let mut buffer_value: u64 = 0;
    if w > 0 {
        if j > 0 && is_part_number(&grid, i, j - 1, w) {
            buffer_value = buffer.parse::<u64>().unwrap();
        }
    }
    buffer.clear();
    buffer_value
}

fn push_if_is_gear(grid: &CharGrid, gear_map: &mut GearMap, i: usize, j: usize, n: u64) {
    if grid.is_gear(i, j) {
        if gear_map.get(&(i, j)).is_none() {
            gear_map.insert((i, j), vec![n]);
        } else {
            gear_map.get_mut(&(i, j)).unwrap().push(n);
        }
    }
}

fn check_adjacent_gear(
    grid: &CharGrid,
    gear_map: &mut GearMap,
    i: usize,
    j: usize,
    w: usize,
    n: u64,
) {
    for k in 0..(w + 2) {
        if j + k < w {
            continue;
        }
        push_if_is_gear(grid, gear_map, i + 1, j + k - w, n);
        if i > 0 {
            push_if_is_gear(grid, gear_map, i - 1, j + k - w, n);
        }
    }
    if j > w {
        push_if_is_gear(grid, gear_map, i, j - w, n);
    }
    push_if_is_gear(grid, gear_map, i, j + 1, n);
}

fn flush_buffer_to_gear_map(
    buffer: &mut String,
    gear_map: &mut GearMap,
    grid: &CharGrid,
    i: usize,
    j: usize,
) {
    let w: usize = buffer.len();
    if w > 0 {
        let n = buffer.parse::<u64>().unwrap();
        check_adjacent_gear(grid, gear_map, i, j, w, n);
        buffer.clear();
    }
}

pub fn part1(data: &str) -> u64 {
    let grid = CharGrid::new(data);
    let mut total: u64 = 0;
    let mut buffer = String::from("");
    for i in 0..grid.height {
        for j in 0..grid.width {
            let c = grid[(i, j)];
            if DIGITS.contains(c) {
                buffer.push(c);
            } else {
                total += flush_buffer(&mut buffer, &grid, i, j);
            }
        }
        total += flush_buffer(&mut buffer, &grid, i, grid.width);
    }
    total
}

pub fn part2(data: &str) -> u64 {
    let grid = CharGrid::new(data);
    let mut buffer = String::from("");
    let mut gear_map = GearMap::new();
    for i in 0..grid.height {
        for j in 0..grid.width {
            let c = grid[(i, j)];
            if DIGITS.contains(c) {
                buffer.push(c);
            } else {
                if j > 0 {
                    flush_buffer_to_gear_map(&mut buffer, &mut gear_map, &grid, i, j - 1);
                }
            }
        }
        flush_buffer_to_gear_map(&mut buffer, &mut gear_map, &grid, i, grid.width - 1);
    }
    let mut total: u64 = 0;
    for (_coord, nums) in gear_map {
        if nums.len() == 2 {
            total += nums[0] * nums[1];
        }
    }
    total
}

pub fn solve(data: &str) {
    println!("Day 3");
    println!("Part 1: {}", part1(data));
    println!("Part 2: {}", part2(data));
}

#[cfg(test)]
mod tests {
    use crate::puzzles::day03::{part1, part2};

    #[test]
    fn test_part1() {
        let input = "467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..";
        assert_eq!(part1(input), 4361);
    }

    #[test]
    fn test_part2() {
        let input = "467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..";
        assert_eq!(part2(input), 467835);
    }
}
