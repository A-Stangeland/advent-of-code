with open('day06-input') as f:
    message = f.read()

marker_len = 14
for i in range(len(message)):
    sub = message[i:i+marker_len]
    # print(sub)
    if len(set(sub)) == marker_len:
        print(sub, i+marker_len)
        break