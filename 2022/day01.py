a, b, c = 0, 0, 0
running_total = 0
with open('day-01-input') as f:
    for line in f:
        if line != '\n':
            running_total += int(line)
            continue
        
        if running_total < a:
            pass
        elif running_total < b:
            a = running_total
        elif running_total < c:
            a, b = b, running_total
        else:
            a, b, c = b, c, running_total

        running_total = 0

print(a, b, c, sum((a,b,c)))