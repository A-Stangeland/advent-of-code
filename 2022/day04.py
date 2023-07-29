with open("day04-input") as f:
    lines = f.read().splitlines()


def contains_fully(a, b):
    start_a, stop_a = a
    start_b, stop_b = b
    return (start_a <= start_b) & (stop_b <= stop_a)


def contains(a, b):
    start_a, stop_a = a
    start_b, stop_b = b
    return (start_a <= start_b <= stop_a) or (start_a <= stop_b <= stop_a)


def overlaps(a, b):
    start_a, stop_a = a
    start_b, stop_b = b
    print(" " * (start_a - 1), end="")
    print("-" * (stop_a - start_a + 1))
    print(" " * (start_b - 1), end="")
    print("-" * (stop_b - start_b + 1))
    return contains(a, b) or contains(b, a)


total_contains = 0
total_overlaps = 0
for line in lines:
    x1, x2 = line.split(",")
    i1 = [int(n) for n in x1.split("-")]
    i2 = [int(n) for n in x2.split("-")]
    if contains_fully(i1, i2) or contains_fully(i2, i1):
        total_contains += 1
    if overlaps(i1, i2):
        total_overlaps += 1
print(total_contains)
print(total_overlaps)
