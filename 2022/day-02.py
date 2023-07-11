shape_map = {'X': 0, 'Y': 1, 'Z': 2, 'A': 0, 'B': 1, 'C': 2}

def shape_score(you):
    return shape_map[you] + 1

def game_score(you, opponent):
    if shape_map[you] == (shape_map[opponent] - 1) % 3:
        return 0
    if shape_map[you] == shape_map[opponent] % 3:
        return 3
    if shape_map[you] == (shape_map[opponent] + 1) % 3:
        return 6    

total_score = 0
with open('2022/day-02-input') as f:
    for line in f:
        opponent = line[0]
        you = line[2]
        total_score += shape_score(you) + game_score(you, opponent)

print(total_score)
        