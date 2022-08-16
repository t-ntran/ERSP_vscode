
import random
def get_sequence():
    sequence = []
    for i in range(25):
        sequence.append(i)
    random.shuffle(sequence)
    return sequence

def make_board():
    #each board is 5x5
    #each spot is a number 0-24
    #no number is repeated on the same board
    rows, cols = (5, 5)
    arr = [[0]*cols]*rows
    board = arr
    sequence = get_sequence()
    for i in range(25):
        board[i//5][i%5] = sequence[i]
    
    return board

def isWinningBoard(board):
    for i in range(5):
        row = True
        for j in range(5):
            if board[i][j] == 100:
                row = True 
            else:
                row = False
                break
        if row == True:
            return True
    
    for i in range(5):
        col = True
        for j in range(5):
            if board[j][i] == 100:
                col = True
            else:
                col = False
                break
        if col == True:
            return True

    return False


def get_score(board, last_number):
    score = 0
    for i in range(5):
        for j in range(5):
            if board[i][j] != 100:
                score += board[i][j]
    return score * last_number

def bingo ():
    board1 = make_board()
    board2 = make_board()
    board3 = make_board()

    sequence = get_sequence()
    last_number = sequence[0]

    print(board1)
    print(board2)
    print(board3)
    print(sequence)
    for i in range(25):
        last_number = sequence[i]
        if isWinningBoard(board1):
            print("Board 1 wins!")
            print(get_score(board1, last_number))
            print("Last number called: " + str(last_number))
            return "Board 1 Wins"
        if isWinningBoard(board2):
            print("Board 2 wins!")
            print(get_score(board2, last_number))
            print("Last number called: " + str(last_number))
            return "Bo"
        if isWinningBoard(board3):
            print("Board 3 wins!")
            print(get_score(board3, last_number))
            print("Last number called: " + str(last_number))
            return
        for j in range(5):
            for k in range(5):
                if board1[j][k] == sequence[i]:
                    board1[j][k] = 100
                if board2[j][k] == sequence[i]:
                    board2[j][k] = 100
                if board3[j][k] == sequence[i]:
                    board3[j][k] = 100

    print("No winner!")


bingo()
