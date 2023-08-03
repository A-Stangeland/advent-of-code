from aoc2022 import day01, day18


def test_day01():
    for example in day01.puzzle.examples:
        assert day01.part1(example.input_data) == example.answer_a
        assert day01.part2(example.input_data) == example.answer_b


def test_day02():
    for example in day01.puzzle.examples:
        assert day01.part1(example.input_data) == example.answer_a
        assert day01.part2(example.input_data) == example.answer_b


def test_day18():
    for example in day18.puzzle.examples:
        assert day18.part1(example.input_data) == example.answer_a
        assert day18.part2(example.input_data) == example.answer_b
