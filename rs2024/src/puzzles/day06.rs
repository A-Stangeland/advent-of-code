use colored::Colorize;
use std::{ops::Index, usize};

#[derive(Clone)]
struct Guard {
    i: usize,
    j: usize,
    direction: u8,
}

impl Guard {
    fn turn(&mut self) {
        self.direction = (self.direction + 1) % 4;
    }

    fn get_next_position(&self, grid: &CharGrid) -> Option<(usize, usize)> {
        let (next_i, next_j) = match self.direction {
            0 => {
                if self.j == grid.width - 1 {
                    return None;
                } else {
                    (self.i, self.j + 1)
                }
            }
            1 => {
                if self.i == grid.height - 1 {
                    return None;
                } else {
                    (self.i + 1, self.j)
                }
            }
            2 => {
                if self.j == 0 {
                    return None;
                } else {
                    (self.i, self.j - 1)
                }
            }
            3 => {
                if self.i == 0 {
                    return None;
                } else {
                    (self.i - 1, self.j)
                }
            }
            _ => panic!("Invalid guard_direction."),
        };
        Some((next_i, next_j))
    }

    fn step(&mut self, grid: &mut CharGrid, check_obstacles: bool) -> bool {
        let (next_i, next_j) = match self.get_next_position(grid) {
            Some(c) => c,
            None => return true,
        };
        if grid[(next_i, next_j)] == '#' {
            self.turn();
            // grid.record_path(self);
        } else {
            self.i = next_i;
            self.j = next_j;
            if check_obstacles {
                self.check_obstacle(grid);
            }
            // grid.record_path(self);
        }
        false
    }

    fn check_obstacle(&mut self, grid: &mut CharGrid) -> bool {
        let (obstacle_i, obstacle_j) = match self.get_next_position(grid) {
            Some(res) => res,
            None => return false,
        };
        let mut phantom_guard = self.clone();
        let mut phantom_grid = grid.clone();
        phantom_guard.turn();
        phantom_grid.add_obstacle(obstacle_i, obstacle_j);

        let mut step_count = 0u32;
        while !phantom_guard.step(&mut phantom_grid, false) {
            if phantom_grid[(phantom_guard.i, phantom_guard.j)]
                == get_direction_char(phantom_guard.direction)
            {
                grid.add_obstacle_position(obstacle_i, obstacle_j);
                // phantom_grid._print();
                return true;
            }
            phantom_grid.record_path(&phantom_guard);
            if step_count == 10000 {
                break;
            }
            step_count = step_count + 1;
        }
        false
    }
}

struct CharGrid {
    height: usize,
    width: usize,
    values: Vec<char>,
    obstacle_positions: Vec<u8>,
}

impl Index<(usize, usize)> for CharGrid {
    type Output = char;

    fn index(&self, index: (usize, usize)) -> &Self::Output {
        let (i, j) = index;
        &self.values[self.width * i + j]
    }
}

impl CharGrid {
    fn clone(&self) -> Self {
        CharGrid {
            height: self.height,
            width: self.width,
            values: self.values.clone(),
            obstacle_positions: self.obstacle_positions.clone(),
        }
    }

    fn record_path(&mut self, guard: &Guard) {
        self.values[guard.i * self.width + guard.j] = get_direction_char(guard.direction)
    }

    fn add_obstacle(&mut self, i: usize, j: usize) {
        self.values[i * self.width + j] = '#';
    }

    fn add_obstacle_position(&mut self, i: usize, j: usize) {
        self.obstacle_positions[i * self.width + j] = 1;
    }

    fn sumx(&self) -> u64 {
        self.values
            .iter()
            .map(|c| {
                if ['^', '<', '>', 'v'].contains(c) {
                    1
                } else {
                    0
                }
            })
            .sum()
    }

    fn sumo(&self) -> u64 {
        self.obstacle_positions.iter().map(|&x| x as u64).sum()
    }

    fn _print(&self) {
        for i in 0..self.height {
            for j in 0..self.width {
                if self.obstacle_positions[self.index(i, j)] == 1 {
                    print!("{}", "o".green());
                } else {
                    if ['^', '<', '>', 'v'].contains(&self[(i, j)]) {
                        print!("{}", self[(i, j)].to_string().red());
                    } else {
                        print!("{}", self[(i, j)]);
                    }
                }
            }
            println!("");
        }
        println!("");
    }

    fn index(&self, i: usize, j: usize) -> usize {
        i * self.width + j
    }
}

fn init_puzzle(data: &str) -> (CharGrid, Guard) {
    let data_split: Vec<&str> = data.split_terminator('\n').collect();
    let height = data_split.len();
    let width = data_split[0].len();
    let grid_values = data_split.join("").chars().collect::<Vec<char>>();
    let internal_index = grid_values.iter().position(|&c| c == '^').unwrap();
    let guard_i = internal_index / width;
    let guard_j = internal_index % width;

    let grid = CharGrid {
        height,
        width,
        obstacle_positions: vec![0; grid_values.len()],
        values: grid_values,
    };

    let guard = Guard {
        i: guard_i,
        j: guard_j,
        direction: 3,
    };
    (grid, guard)
}

fn get_direction_char(direction: u8) -> char {
    match direction {
        0 => '>',
        1 => 'v',
        2 => '<',
        3 => '^',
        _ => panic!("Invalid guard_direction."),
    }
}

pub fn part1(data: &str) -> u64 {
    let (mut grid, mut guard) = init_puzzle(data);
    while !guard.step(&mut grid, false) {
        grid.record_path(&guard);
    }
    grid._print();
    grid.sumx()
}

pub fn part2(data: &str) -> u64 {
    let (mut grid, mut guard) = init_puzzle(data);
    let mut step_count = 0u32;
    while !guard.step(&mut grid, true) {
        grid.record_path(&guard);
        // if step_count % 1000 == 0 {
        //     grid._print();
        // }
        // step_count = step_count + 1;
    }
    grid._print();
    grid.sumo()
}

pub fn solve(data: &str) {
    println!("Day 2");
    println!("Part 1: {}", part1(data));
    println!("Part 2: {}", part2(data));
}

#[cfg(test)]
mod tests {
    use crate::puzzles::day06::{part1, part2};

    #[test]
    fn test_part1() {
        let input = "....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...";
        assert_eq!(part1(input), 41);
    }

    #[test]
    fn test_part2() {
        let input = "....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...";
        assert_eq!(part2(input), 6);
    }
}
