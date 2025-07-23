use std::cmp;

fn split_game_line(game_line: &str) -> (u64, &str) {
    let game_split: Vec<&str> = game_line
        .strip_prefix("Game ")
        .unwrap()
        .split(": ")
        .collect();
    if game_split.len() != 2 {
        panic!("Invalid game line.")
    }
    let game_id: u64 = game_split[0].parse().unwrap();
    let game_record = game_split[1];
    (game_id, game_record)
}

fn game_is_possible(game_record: &str, red: u64, green: u64, blue: u64) -> bool {
    for round in game_record.split("; ") {
        for color_count in round.split(", ") {
            let mut iter = color_count.split(' ');
            let count: u64 = iter.next().unwrap().parse().unwrap();
            let color = iter.next().unwrap();
            match color {
                "red" => {
                    if count > red {
                        return false;
                    }
                }
                "green" => {
                    if count > green {
                        return false;
                    }
                }
                "blue" => {
                    if count > blue {
                        return false;
                    }
                }
                _ => panic!("Invalid game record."),
            }
        }
    }
    true
}

fn power(game_record: &str) -> u64 {
    let mut red: u64 = 0;
    let mut green: u64 = 0;
    let mut blue: u64 = 0;
    for round in game_record.split("; ") {
        for color_count in round.split(", ") {
            let mut iter = color_count.split(' ');
            let count: u64 = iter.next().unwrap().parse().unwrap();
            let color = iter.next().unwrap();
            match color {
                "red" => red = cmp::max(red, count),
                "green" => green = cmp::max(green, count),
                "blue" => blue = cmp::max(blue, count),
                _ => panic!("Invalid game record."),
            }
        }
    }
    red * green * blue
}

pub fn part1(data: &str) -> u64 {
    let mut total: u64 = 0;
    for line in data.split('\n') {
        if line.len() == 0 {
            continue;
        }
        let (game_id, game_record) = split_game_line(line);
        if game_is_possible(game_record, 12, 13, 14) {
            total += game_id;
        }
    }
    total
}

pub fn part2(data: &str) -> u64 {
    let mut total: u64 = 0;
    for line in data.split('\n') {
        if line.len() == 0 {
            continue;
        }
        let (_, game_record) = split_game_line(line);
        total += power(game_record);
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
    use crate::puzzles::day02::{part1, part2};

    #[test]
    fn test_part1() {
        let input = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green";
        assert_eq!(part1(input), 8);
    }

    #[test]
    fn test_part2() {
        let input = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green";
        assert_eq!(part2(input), 2286);
    }
}
