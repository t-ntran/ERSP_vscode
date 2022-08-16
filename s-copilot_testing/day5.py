def main():
    with open('C:\Users\sdtnt\ERSP_vscode-5\study\hydrothermal_vent.txt', 'r') as f:
        data = f.readlines()
    data = [line.strip().split('->') for line in data]
    close()
    rows, cols = (10, 10)
    arr = [['.']*cols]*rows
    board = arr
    for line in data:
        x1, y1 = line[0].split(',')
        x2, y2 = line[1].split(',')
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        if x1 == x2:
            for i in range(y1, y2+1):
                if board[x1][i] == '.':
                    board[x1][i] = '1'
                else:
                    board[x1][i] = str(int(board[x1][i]) + 1)
        elif y1 == y2:
            for i in range(x1, x2+1):
                if board[i][y1] == '.':
                    board[i][y1] = '1'
                else:
                    board[i][y1] = str(int(board[i][y1]) + 1)
        else:
            continue
    score = 0
    for i in range(10):
        for j in range(10):
            if board[i][j] != '.':
                if int(board[i][j]) >= 2:
                    score += 1
    print(board)
    print("Score: " + str(score))

main()