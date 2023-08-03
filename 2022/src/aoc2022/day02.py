from aocd.models import Puzzle  # type: ignore

puzzle = Puzzle(year=2022, day=2)

shape_map = {"X": 0, "Y": 1, "Z": 2, "A": 0, "B": 1, "C": 2}


def shape_score(shape):
    return shape_map[shape] + 1


def game_score(you, opponent):
    if shape_map[you] == (shape_map[opponent] - 1) % 3:
        return 0
    if shape_map[you] == shape_map[opponent] % 3:
        return 3
    if shape_map[you] == (shape_map[opponent] + 1) % 3:
        return 6


def game_score_part2(you, opponent):
    if you == "X":
        return (shape_map[opponent] - 1) % 3 + 1 + 0
    if you == "Y":
        return shape_map[opponent] % 3 + 1 + 3
    if you == "Z":
        return (shape_map[opponent] + 1) % 3 + 1 + 6


def part1(data: str) -> str:
    total_score = 0
    for line in data.splitlines():
        opponent = line[0]
        you = line[2]
        total_score += shape_score(you) + game_score(you, opponent)
    return str(total_score)


def part2(data: str) -> str:
    total_score = 0
    for line in data.splitlines():
        opponent = line[0]
        you = line[2]
        total_score += game_score_part2(you, opponent)
    return str(total_score)


if __name__ == "__main__":
    print("--- Part 1 ---")
    print(part1(puzzle.input_data))
    print("--- Part 2 ---")
    print(part2(puzzle.input_data))
