use std::iter::zip;

fn is_safe(report: &[u32]) -> bool {
    let len = report.len();
    let increasing = report[1] > report[0];
    for (v1, v2) in zip(&report[..len - 1], &report[1..]) {
        if (v2 > v1) != increasing {
            return false;
        }
        let diff = (v1).abs_diff(*v2);
        if diff < 1 || diff > 3 {
            return false;
        }
    }
    true
}

fn is_almost_safe(report: &[u32]) -> bool {
    if is_safe(report) {
        return true;
    }
    let len = report.len();
    for i in 0..len {
        if is_safe(&[&report[..i], &report[(i + 1)..]].concat()) {
            return true;
        }
    }
    false
}

pub fn part1(data: &str) -> usize {
    data.split_terminator('\n')
        .map(|x| {
            x.split(' ')
                .map(|y| y.parse::<u32>().unwrap())
                .collect::<Vec<u32>>()
        })
        .filter(|x| is_safe(x))
        .collect::<Vec<_>>()
        .len()
}

pub fn part2(data: &str) -> usize {
    data.split_terminator('\n')
        .map(|x| {
            x.split(' ')
                .map(|y| y.parse::<u32>().unwrap())
                .collect::<Vec<u32>>()
        })
        .filter(|x| is_almost_safe(x))
        .collect::<Vec<_>>()
        .len()
}

pub fn solve(data: &str) {
    println!("Day 2");
    println!("Part 1: {}", part1(data));
    println!("Part 2: {}", part2(data));
}

#[cfg(test)]
mod tests {
    use crate::puzzles::day02::{is_almost_safe, part1, part2};

    #[test]
    fn test_part1() {
        let input = "7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9";
        assert_eq!(part1(input), 2);
    }

    #[test]
    fn test_part2() {
        let input = "7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9";
        assert_eq!(part2(input), 4);
    }

    #[test]
    fn test_is_almost_safe() {
        let input = vec![6, 7, 9, 8, 12, 15, 18, 19];
        assert_eq!(is_almost_safe(&input), true);
        assert_eq!(is_almost_safe(&vec![4, 3, 2, 2, 2]), false);
    }
}
