def grouped(iterable, n):
    return zip(*[iter(iterable)]*n)


with open('day03-input') as f:
    lines = f.read().splitlines()

alphabet  = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
total = 0
total_part2 = 0
for l1, l2, l3 in grouped(lines, 3):
    badge = (set(l1) & set(l2) & set(l3)).pop()
    total_part2 += alphabet.index(badge) + 1
    for line in (l1, l2, l3):
        n = len(line)
        c1 = line[:n//2]
        c2 = line[n//2:]
        common = (set(c1) & set(c2)).pop()
        total += alphabet.index(common) + 1
print(total)
print(total_part2)