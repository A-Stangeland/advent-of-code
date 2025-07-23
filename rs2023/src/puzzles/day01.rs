const DIGITS: &str = "0123456789";
const DIGIT_WORDS: [&str; 10] = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
];

fn first_digit(text: &str) -> char {
    for c in text.chars() {
        if DIGITS.contains(c) {
            return c;
        }
    }
    panic!("No digits found in string: {}", text);
}

fn last_digit(text: &str) -> char {
    for c in text.chars().rev() {
        if DIGITS.contains(c) {
            return c;
        }
    }
    panic!("No digits found in string: {}", text);
}

fn digit_word_to_digit(digit_word: &str) -> char {
    match digit_word {
        "zero" => return '0',
        "one" => return '1',
        "two" => return '2',
        "three" => return '3',
        "four" => return '4',
        "five" => return '5',
        "six" => return '6',
        "seven" => return '7',
        "eight" => return '8',
        "nine" => return '9',
        _ => panic!("Not a valid digit word."),
    }
}

fn first_digit_or_word(text: &str) -> char {
    for (i, c) in text.char_indices() {
        if DIGITS.contains(c) {
            return c;
        }
        for digit_word in DIGIT_WORDS {
            if text[i..].starts_with(digit_word) {
                return digit_word_to_digit(digit_word);
            }
        }
    }
    panic!("Text does not contain any digits or digit words.")
}

fn last_digit_or_word(text: &str) -> char {
    for (i, c) in text.char_indices().rev() {
        if DIGITS.contains(c) {
            return c;
        }
        for digit_word in DIGIT_WORDS {
            if text[..i + 1].ends_with(digit_word) {
                return digit_word_to_digit(digit_word);
            }
        }
    }
    panic!("Text does not contain any digits or digit words.")
}

pub fn part1(data: &str) -> u64 {
    let mut total: u64 = 0;
    for line in data.split('\n') {
        if line.len() == 0 {
            continue;
        }
        let first = first_digit(line);
        let last = last_digit(line);
        total += format!("{}{}", first, last).parse::<u64>().unwrap();
    }
    total
}

pub fn part2(data: &str) -> u64 {
    let mut total: u64 = 0;
    for line in data.split('\n') {
        if line.len() == 0 {
            continue;
        }
        let first = first_digit_or_word(line);
        let last = last_digit_or_word(line);
        total += format!("{}{}", first, last).parse::<u64>().unwrap();
    }
    total
}

pub fn solve(data: &str) {
    println!("Day 1");
    println!("Part 1: {}", part1(data));
    println!("Part 2: {}", part2(data));
}

#[cfg(test)]
mod tests {
    use crate::puzzles::day01::{part1, part2};

    #[test]
    fn test_part1() {
        let input = "1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet";
        assert_eq!(part1(input), 142);
    }

    #[test]
    fn test_part2() {
        let input = "two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen";
        assert_eq!(part2(input), 281);
    }
}
