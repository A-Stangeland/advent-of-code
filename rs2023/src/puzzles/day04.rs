use std::cmp::min;
use std::collections::HashSet;

fn str_to_hashset(s: &str) -> HashSet<u32> {
    let mut set = HashSet::new();
    for i in 0..(s.len() / 3) {
        set.insert(s[(3 * i + 1)..(3 * i + 3)].trim().parse::<u32>().unwrap());
    }
    set
}

fn num_winning_cards(line: &str) -> usize {
    let (_, card_set_data) = line.split_once(':').unwrap();
    let (winning_numbers, owned_numbers) = card_set_data.split_once('|').unwrap();
    let winning_set = str_to_hashset(winning_numbers);
    let owned_set = str_to_hashset(owned_numbers);
    let inter: Vec<_> = winning_set.intersection(&owned_set).collect();
    inter.len()
}

pub fn part1(data: &str) -> u32 {
    let mut total: u32 = 0;
    for line in data.split_terminator('\n') {
        let n: u32 = num_winning_cards(line).try_into().unwrap();
        if n > 0 {
            total += 2u32.pow(n - 1);
        }
    }
    total
}

pub fn part2(data: &str) -> u32 {
    let num_cards = data.split_terminator('\n').collect::<Vec<_>>().len();
    let mut card_counts = vec![1u32; num_cards];
    for (card_idx, line) in data.split_terminator('\n').enumerate() {
        let n = num_winning_cards(line);
        if n > 0 {
            for i in (card_idx + 1)..min(card_idx + n + 1, num_cards) {
                card_counts[i] += card_counts[card_idx];
            }
        }
    }
    card_counts.iter().sum()
}

pub fn solve(data: &str) {
    println!("Day 4");
    println!("Part 1: {}", part1(data));
    println!("Part 2: {}", part2(data));
}

#[cfg(test)]
mod tests {
    use crate::puzzles::day04::{part1, part2};

    #[test]
    fn test_part1() {
        let input = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
";
        assert_eq!(part1(input), 13);
    }

    #[test]
    fn test_part2() {
        let input = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
";
        assert_eq!(part2(input), 30);
    }
}
