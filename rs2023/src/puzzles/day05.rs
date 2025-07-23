use std::cmp::{max, min};

#[derive(Copy, Clone)]
struct InputRange {
    start: u64,
    length: u64,
}

impl InputRange {
    fn end(&self) -> u64 {
        self.start + self.length
    }
}

struct Range {
    destination_start: u64,
    source_start: u64,
    length: u64,
}

impl Range {
    fn source_end(&self) -> u64 {
        self.source_start + self.length
    }
}

struct CategoryMap {
    _name: String,
    ranges: Vec<Range>,
}

impl CategoryMap {
    fn new(map_definition: &str) -> Self {
        let mut ranges = Vec::new();
        let (name, ranges_definitions) = map_definition.split_once('\n').unwrap();
        for range_str in ranges_definitions.split_terminator('\n') {
            let range: Vec<u64> = range_str
                .split(' ')
                .map(|x| x.parse::<u64>().unwrap())
                .collect();
            if range.len() != 3 {
                panic!("Invalid input: {}", range_str);
            }
            ranges.push(Range {
                destination_start: range[0],
                source_start: range[1],
                length: range[2],
            });
        }
        ranges.sort_unstable_by_key(|x| x.source_start);
        CategoryMap {
            _name: String::from(name),
            ranges,
        }
    }

    fn map(&self, x: u64) -> u64 {
        for range in &self.ranges {
            if x >= range.source_start && x < range.source_start + range.length {
                return x - range.source_start + range.destination_start;
            }
        }
        x
    }

    fn map_vec(&self, input: &Vec<u64>) -> Vec<u64> {
        input.iter().map(|&x| self.map(x)).collect()
    }

    fn map_range(&self, input_range: &InputRange) -> Vec<InputRange> {
        let mut output_ranges = Vec::new();
        let input_start = input_range.start;
        let input_end = input_range.end();

        let map_start = self.ranges.first().unwrap().source_start;
        let map_end = self.ranges.last().unwrap().source_end();

        if input_start < map_start {
            let end = min(input_end, map_start);
            let length = end - input_start;
            output_ranges.push(InputRange {
                start: input_start,
                length,
            });
        }
        if input_end > map_end {
            let start = max(input_start, map_end);
            let length = input_end - start;
            output_ranges.push(InputRange { start, length });
        }

        for range in &self.ranges {
            if range.source_start >= input_end {
                break;
            }
            let range_end = range.source_start + range.length;
            if range_end < input_start {
                continue;
            }
            let start = max(input_start, range.source_start);
            let end = min(input_end, range_end);
            let length = end - start;
            output_ranges.push(InputRange {
                start: start - range.source_start + range.destination_start,
                length,
            });
        }

        output_ranges
    }

    fn map_range_vec(&self, input: &Vec<InputRange>) -> Vec<InputRange> {
        input
            .iter()
            .map(|x| self.map_range(x))
            .reduce(|x, y| x.into_iter().chain(y.into_iter()).collect())
            .unwrap()
    }
}

fn parse_seed_numbers(data: &str) -> Vec<u64> {
    let (_, numbers) = data.split_once(' ').unwrap();
    numbers.split(' ').map(|x| x.parse().unwrap()).collect()
}

fn seed_numbers_to_ranges(seed_numbers: &[u64]) -> Vec<InputRange> {
    let mut ranges = Vec::new();
    for chunk in seed_numbers.chunks(2) {
        ranges.push(InputRange {
            start: chunk[0],
            length: chunk[1],
        });
    }
    ranges
}

pub fn part1(data: &str) -> u64 {
    let mut blocks = data.split("\n\n");
    let seed_numbers = parse_seed_numbers(blocks.next().unwrap());
    let mut category_numbers = seed_numbers.clone();
    for category_map in blocks.map(|x| CategoryMap::new(x)) {
        category_numbers = category_map.map_vec(&category_numbers);
    }
    *category_numbers.iter().min().unwrap()
}

pub fn part2(data: &str) -> u64 {
    let mut blocks = data.split("\n\n");
    let seed_numbers = parse_seed_numbers(blocks.next().unwrap());
    let mut ranges = seed_numbers_to_ranges(&seed_numbers);
    for category_map in blocks.map(|x| CategoryMap::new(x)) {
        ranges = category_map.map_range_vec(&ranges);
    }
    ranges.iter().map(|x| x.start).min().unwrap()
}

pub fn solve(data: &str) {
    println!("Day 5");
    println!("Part 1: {}", part1(data));
    println!("Part 2: {}", part2(data));
}

#[cfg(test)]
mod tests {
    use crate::puzzles::day05::{part1, part2};

    #[test]
    fn test_part1() {
        let input = "seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
";
        assert_eq!(part1(input), 35);
    }

    #[test]
    fn test_part2() {
        let input = "seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
";
        assert_eq!(part2(input), 46);
    }
}
