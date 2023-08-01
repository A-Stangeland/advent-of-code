import os
import glob

year = os.getcwd().split("/")[-1]
max_day = max(
    int(day.removeprefix("day").removesuffix(".py")) for day in glob.glob("day*.py")
)
file_template = f"""from aocd.models import Puzzle # type: ignore

puzzle = Puzzle(year={year}, day={max_day+1})


def part1(data: str) -> str:
\tpass

def part2(data: str) -> str:
\tpass

if __name__==\"__main__\":
\tpass
"""

with open(f"day{max_day+1}.py", "w") as f:
    f.write(file_template)
