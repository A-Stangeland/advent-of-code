use std::collections::HashMap;
use std::iter::zip;
use std::ops::Not;

fn get_sorted_vectors(data: &str) -> (Vec<u64>, Vec<u64>) {
    let (mut v1, mut v2): (Vec<u64>, Vec<u64>) = data
        .split('\n')
        .filter(|s| s.len() > 0)
        .map(|x| x.split_once("   ").unwrap())
        .map(|x| (x.0.parse::<u64>().unwrap(), x.1.parse::<u64>().unwrap()))
        .unzip();
    v1.sort();
    v2.sort();
    (v1, v2)
}

fn count_occurences<T: PartialEq>(list: &[T], element: &T) -> u64 {
    let mut count: u64 = 0;
    for item in list {
        if item == element {
            count = count + 1;
        }
    }
    count
}

pub fn part1(data: &str) -> i64 {
    let (v1, v2) = get_sorted_vectors(data);
    zip(v1, v2).map(|(x, y)| (x as i64 - y as i64).abs()).sum()
}

pub fn part2(data: &str) -> u64 {
    let (v1, v2) = get_sorted_vectors(data);
    let mut counts = HashMap::new();
    let mut total: u64 = 0;
    for x in v1 {
        if counts.contains_key(&x).not() {
            let count = count_occurences(&v2, &x);
            counts.insert(x, count);
        }
        total = total + x * counts.get(&x).unwrap();
    }
    total
}

pub fn solve(data: &str) {
    println!("Day 1");
    println!("Part 1: {}", part1(data));
    println!("Part 2: {}", part2(data));
}
