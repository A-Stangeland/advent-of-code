use std::ops::Index;

struct CharGrid {
    height: usize,
    width: usize,
    values: Vec<char>,
}

impl Index<(usize, usize)> for CharGrid {
    type Output = char;

    fn index(&self, index: (usize, usize)) -> &Self::Output {
        let (i, j) = index;
        &self.values[self.width * i + j]
    }
}

impl CharGrid {
    fn new(data: &str) -> Self {
        let data_split: Vec<&str> = data.split_terminator('\n').collect();
        CharGrid {
            height: data_split.len(),
            width: data_split[0].len(),
            values: data_split.join("").chars().collect::<Vec<char>>(),
        }
    }

    fn get_row(&self, i: usize, j: usize) -> String {
        self.values[self.width * i + j..(self.width * i + j + 4)]
            .iter()
            .collect()
    }

    fn get_col(&self, i: usize, j: usize) -> String {
        let mut col = String::new();
        col.push(self[(i, j)]);
        col.push(self[(i + 1, j)]);
        col.push(self[(i + 2, j)]);
        col.push(self[(i + 3, j)]);
        col
    }

    fn get_diag(&self, i: usize, j: usize, n: usize) -> String {
        let mut diag = String::new();
        for k in 0..n {
            diag.push(self[(i + k, j + k)]);
        }
        diag
    }

    fn get_back_diag(&self, i: usize, j: usize, n: usize) -> String {
        let mut diag = String::new();
        for k in 0..n {
            diag.push(self[(i + k, j - k)]);
        }
        diag
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

fn check_rows(grid: &CharGrid) -> u64 {
    let mut count: u64 = 0;
    for i in 0..grid.height {
        for j in 0..grid.width - 3 {
            let row = grid.get_row(i, j);
            if row == "XMAS" || row == "SAMX" {
                count = count + 1;
            }
        }
    }
    count
}

fn check_cols(grid: &CharGrid) -> u64 {
    let mut count: u64 = 0;
    for i in 0..grid.height - 3 {
        for j in 0..grid.width {
            let row = grid.get_col(i, j);
            if row == "XMAS" || row == "SAMX" {
                count = count + 1;
            }
        }
    }
    count
}

fn check_diag(grid: &CharGrid) -> u64 {
    let mut count: u64 = 0;
    for i in 0..grid.height - 3 {
        for j in 0..grid.width - 3 {
            let row = grid.get_diag(i, j, 4);
            if row == "XMAS" || row == "SAMX" {
                count = count + 1;
            }
        }
    }
    count
}

fn check_back_diag(grid: &CharGrid) -> u64 {
    let mut count: u64 = 0;
    for i in 0..grid.height - 3 {
        for j in 3..grid.width {
            let row = grid.get_back_diag(i, j, 4);
            if row == "XMAS" || row == "SAMX" {
                count = count + 1;
            }
        }
    }
    count
}

fn check_cross(grid: &CharGrid) -> u64 {
    let mut count: u64 = 0;
    for i in 0..grid.height - 2 {
        for j in 0..grid.width - 2 {
            let diag1 = grid.get_diag(i, j, 3);
            if diag1 == "MAS" || diag1 == "SAM" {
                let diag2 = grid.get_back_diag(i, j + 2, 3);
                if diag2 == "MAS" || diag2 == "SAM" {
                    count = count + 1;
                }
            }
        }
    }
    count
}

pub fn part1(data: &str) -> u64 {
    let grid = CharGrid::new(data);
    check_rows(&grid) + check_cols(&grid) + check_diag(&grid) + check_back_diag(&grid)
}

pub fn part2(data: &str) -> u64 {
    let grid = CharGrid::new(data);
    check_cross(&grid)
}

pub fn solve(data: &str) {
    println!("Day 2");
    println!("Part 1: {}", part1(data));
    println!("Part 2: {}", part2(data));
}

#[cfg(test)]
mod tests {
    use crate::puzzles::day04::{part1, part2};

    #[test]
    fn test_part1() {
        let input = "MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX";
        assert_eq!(part1(input), 18);
    }

    #[test]
    fn test_part2() {
        let input = "MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX";
        assert_eq!(part2(input), 9);
    }
}
