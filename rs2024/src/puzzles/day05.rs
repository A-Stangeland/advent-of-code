fn parse_input(data: &str) -> (Vec<(u64, u64)>, Vec<Vec<u64>>) {
    let (order_data, updates_data) = data.split_once("\n\n").unwrap();

    let ordering_rules = order_data
        .split_terminator("\n")
        .map(|x| x.split_once("|").unwrap())
        .map(|(x, y)| (x.parse::<u64>().unwrap(), y.parse::<u64>().unwrap()))
        .collect::<Vec<(u64, u64)>>();

    let updates = updates_data
        .split_terminator("\n")
        .map(|s| {
            s.split(",")
                .map(|x| x.parse::<u64>().unwrap())
                .collect::<Vec<u64>>()
        })
        .collect();
    (ordering_rules, updates)
}

fn get_index<T: PartialEq>(list: &[T], item: &T) -> Option<usize> {
    list.iter().position(|x| x == item)
}

fn correctly_ordered(update: &[u64], rules: &[(u64, u64)]) -> bool {
    for (x, y) in rules {
        let x_idx = match get_index(update, x) {
            Some(idx) => idx,
            None => continue,
        };
        let y_idx = match get_index(update, y) {
            Some(idx) => idx,
            None => continue,
        };
        if x_idx > y_idx {
            return false;
        }
    }
    true
}

fn get_middle_element<T: Copy>(list: &[T]) -> T {
    let i = list.len() / 2;
    list[i]
}

fn put_before<T: Clone>(list: &[T], x_idx: usize, y_idx: usize) -> Vec<T> {
    let mut new_list = Vec::<T>::new();
    new_list.extend_from_slice(&list[..y_idx]);
    new_list.push(list[x_idx].clone());
    new_list.extend_from_slice(&list[y_idx..x_idx]);
    if x_idx + 1 < list.len() {
        new_list.extend_from_slice(&list[x_idx + 1..]);
    }
    new_list
}

fn reorder(update: &[u64], rules: &[(u64, u64)]) -> Vec<u64> {
    let mut reordered_update = update.to_vec();
    let mut no_change = false;
    while !no_change {
        no_change = true;
        for (x, y) in rules {
            let x_idx = match get_index(&reordered_update, x) {
                Some(idx) => idx,
                None => continue,
            };
            let y_idx = match get_index(&reordered_update, y) {
                Some(idx) => idx,
                None => continue,
            };
            if x_idx > y_idx {
                reordered_update = put_before(&reordered_update, x_idx, y_idx);
                no_change = false;
            }
        }
    }
    reordered_update
}

pub fn part1(data: &str) -> u64 {
    let (ordering_rules, updates) = parse_input(data);

    let middle_numbers = updates
        .iter()
        .filter(|u| correctly_ordered(u, &ordering_rules))
        .map(|u| get_middle_element(&u))
        .collect::<Vec<u64>>();
    middle_numbers.iter().sum()
}

pub fn part2(data: &str) -> u64 {
    let (ordering_rules, updates) = parse_input(data);

    let middle_numbers = updates
        .iter()
        .filter(|u| !correctly_ordered(u, &ordering_rules))
        .map(|u| reorder(u, &ordering_rules))
        .map(|u| get_middle_element(&u))
        .collect::<Vec<u64>>();
    println!("{:?}", middle_numbers);
    middle_numbers.iter().sum()
}

pub fn solve(data: &str) {
    println!("Day 2");
    println!("Part 1: {}", part1(data));
    println!("Part 2: {}", part2(data));
}

#[cfg(test)]
mod tests {
    use crate::puzzles::day05::{part1, part2};

    #[test]
    fn test_part1() {
        let input = "47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47";
        assert_eq!(part1(input), 143);
    }

    #[test]
    fn test_part2() {
        let input = "47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47";
        assert_eq!(part2(input), 123);
    }
}
