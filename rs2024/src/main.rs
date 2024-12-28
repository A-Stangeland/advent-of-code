mod puzzles;

use puzzles::*;

use std::fs;

fn main() {
    let args = std::env::args().collect::<Vec<String>>();
    if args.len() < 2 {
        panic!("Not enough arguments")
    }
    let day: u8 = args[1].parse().unwrap();
    let data = fs::read_to_string(format!("data/d{:02}.txt", day))
        .expect(&format!("File: data/d{:02}.txt not fount", day));
    let solver = get_day_solver(day);
    solver(&data);
}

fn get_day_solver(day: u8) -> fn(&str) {
    match day {
        1 => day01::solve,
        2 => day02::solve,
        3 => day03::solve,
        // 4 => day04::solve,
        // 5 => day05::solve,
        // 6 => day06::solve,
        // 7 => day07::solve,
        // 8 => day08::solve,
        // 9 => day09::solve,
        // 10 => day10::solve,
        // 11 => day11::solve,
        // 12 => day12::solve,
        // 13 => day13::solve,
        // 14 => day14::solve,
        // 15 => day15::solve,
        // 16 => day16::solve,
        // 17 => day17::solve,
        // 18 => day18::solve,
        // 19 => day19::solve,
        // 20 => day20::solve,
        // 21 => day21::solve,
        // 22 => day22::solve,
        // 23 => day23::solve,
        // 24 => day24::solve,
        // 25 => day25::solve,
        _ => unimplemented!(),
    }
}
