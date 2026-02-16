def print_board(board):
#prints out the Gomoku board
    s = "*"
    for i in range(len(board[0]) - 1):
        s += str(i % 10) + "|"
    s += str((len(board[0]) - 1) % 10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i % 10)
        for j in range(len(board[0]) - 1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0]) - 1])

        s += "*\n"
    s += (len(board[0]) * 2 + 1) * "*"

    print(s)


def score(board):
#computes and returns the score for the position of the board, assuming black has just moved
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)

    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4]) +
            500 * open_b[4] +
            50 * semi_open_b[4] +
            -100 * open_w[3] +
            -30 * semi_open_w[3] +
            50 * open_b[3] +
            10 * semi_open_b[3] +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

def play_gomoku(board_size):
#allows user to play against a computer on a square board of size board_size by board_size
#interacts with the AI engine by calling the function searchMax() -> have to write
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

def put_seq_on_board(board, y, x, d_y, d_x, length, col):
#helper function that faciltates the testing of the AI engine
#adds the sequence of stones of colour col of length length to the board, starting at (y, x) and moving in the direction (d_y, d_x)
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x

def analysis(board):
#analyses the position of the board by computing the number of open and semi open sequences of both colours
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))

def is_empty(board): #is called on by prewritten functions
    rows = len(board)
    columns = len(board[0])
    for i in range(rows):
        for j in range (columns):
            if board[i][j] == "w":
                return False
            elif board[i][j] == "b":
                return False
    return True

def is_bounded(board, y_end, x_end, length, d_y, d_x):
    colour = board[y_end][x_end]
    boardLength = len(board)
    xCoorEndBarrier = x_end + d_x
    yCoorEndBarrier = y_end + d_y

    xCoorStartBarrier = x_end
    yCoorStartBarrier = y_end
    xCoorStartBarrier = x_end - (length * d_x)
    yCoorStartBarrier = y_end - (length * d_y)

    if xCoorEndBarrier < 0 or xCoorEndBarrier >= boardLength:
        endStatus = "CLOSED"
    elif yCoorEndBarrier < 0 or yCoorEndBarrier >= boardLength:
        endStatus = "CLOSED"
    elif board[yCoorEndBarrier][xCoorEndBarrier] == " ":
        endStatus = "OPEN"
    else:
        endStatus = "CLOSED"

    if xCoorStartBarrier < 0 or xCoorStartBarrier >= boardLength:
        startStatus = "CLOSED"
    elif yCoorStartBarrier < 0 or yCoorStartBarrier >= boardLength:
        startStatus = "CLOSED"
    elif board[yCoorStartBarrier][xCoorStartBarrier] == " ":
        startStatus = "OPEN"
    else:
        startStatus = "CLOSED"

    if startStatus == "OPEN" and endStatus == "OPEN":
        return "OPEN"
    if startStatus == "CLOSED" and endStatus == "CLOSED":
        return "CLOSED"
    return "SEMIOPEN" ##pas

def detect_row(board, col, y_start, x_start, length, d_y, d_x): 
    result = [0, 0] #open, semi open
    boardLength = len(board)
    if length > 5:
        return (0, 0)

    if length > boardLength:
        return (0, 0)

    y = y_start
    x = x_start
    while 0 <= y < boardLength and 0 <= x < boardLength:
        target_y = y + (length - 1) * d_y
        target_x = x + (length - 1) * d_x
        if 0 <= target_y < boardLength and 0 <= target_x < boardLength:
            found = True
            for i in range(length):
                if board[y + i * d_y][x + i * d_x] != col:
                    found = False
                    break
            if found:
                # Check if not part of a longer sequence
                if (y - d_y < 0 or x - d_x < 0 or board[y - d_y][x - d_x] != col) and \
                   (target_y + d_y >= boardLength or target_x + d_x >= boardLength or board[target_y + d_y][target_x + d_x] != col):
                    ans = is_bounded(board, target_y, target_x, length, d_y, d_x)
                    if ans == "OPEN":
                        result[0] += 1
                    elif ans == "SEMIOPEN":
                        result[1] += 1
        y += d_y
        x += d_x
    return tuple(result)



def detect_rows(board, col, length):
    boardLength = len(board)
    open_seq_count, semi_open_seq_count = 0, 0

    # Vertical (direction: down)
    for x in range(boardLength):
        res = detect_row(board, col, 0, x, length, 1, 0)
        open_seq_count += res[0]
        semi_open_seq_count += res[1]

    # Horizontal (direction: right)
    for y in range(boardLength):
        res = detect_row(board, col, y, 0, length, 0, 1)
        open_seq_count += res[0]
        semi_open_seq_count += res[1]

    # Diagonal (direction: down-right)
    # Start from first column for all rows
    for y in range(boardLength):
        res = detect_row(board, col, y, 0, length, 1, 1)
        open_seq_count += res[0]
        semi_open_seq_count += res[1]
    # Start from first row for all columns except first column (already counted)
    for x in range(1, boardLength):
        res = detect_row(board, col, 0, x, length, 1, 1)
        open_seq_count += res[0]
        semi_open_seq_count += res[1]

    # Anti-diagonal (direction: down-left)
    # Start from first row for all columns
    for x in range(boardLength):
        res = detect_row(board, col, 0, x, length, 1, -1)
        open_seq_count += res[0]
        semi_open_seq_count += res[1]
    # Start from rows 1 to bottom (except first row which is counted) for last column
    for y in range(1, boardLength):
        res = detect_row(board, col, y, boardLength - 1, length, 1, -1)
        open_seq_count += res[0]
        semi_open_seq_count += res[1]

    return open_seq_count, semi_open_seq_count


def search_max(board): #is called on by prewritten functions
    if is_win(board) == "Draw":
        return None, None
    boardLength = len(board)
    move_y = 0
    move_x = 0
    bestScore = -10000000000000000000000000000000000000
    for i in range(boardLength):
        for j in range(boardLength):
            if board[j][i] == " ":
                board[j][i] = "b"
                tempScore = score(board)
                if tempScore > bestScore:
                    bestScore = tempScore
                    move_y = j
                    move_x = i
                board[j][i] = " "
    return move_y, move_x

def is_win(board): # is called on by prewritten functions
    blackRes = detect_rows(board, "b", 5)
    whiteRes = detect_rows(board, "w", 5)
    if blackRes[0] or blackRes[1]> 0:
        return "Black won"
    if whiteRes[0] or whiteRes [1]> 0:
        return "White won"

    boardLength = len(board)
    for i in range (boardLength):
        for j in range (boardLength):
            if board[j][i] == " ":
                return "Continue playing"
    return "Draw"

#TESTER FUNCTIONS
def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "] * sz)
    return board


def test_is_empty():
    board = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")


def test_is_bounded():
    board = make_empty_board(8)
    x = 5;
    y = 1;
    d_x = 0;
    d_y = 1;
    length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")

def test_detect_row():
    board = make_empty_board(8)
    x = 5;
    y = 1;
    d_x = 0;
    d_y = 1;
    length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0, x, length, d_y, d_x) == (1, 0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")
        print(detect_row(board, "w", 0, x, length, d_y, d_x))

def test_detect_rows(): #fail
    board = make_empty_board(8)
    x = 5;
    y = 1;
    d_x = 0;
    d_y = 1;
    length = 3;
    col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col, length) == (1, 0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max(): #fail
    board = make_empty_board(8)
    x = 5;
    y = 0;
    d_x = 0;
    d_y = 1;
    length = 4;
    col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6;
    y = 0;
    d_x = 0;
    d_y = 1;
    length = 4;
    col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4, 6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5;
    x = 2;
    d_x = 0;
    d_y = 1;
    length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0 #got 1
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3;
    x = 5;
    d_x = -1;
    d_y = 1;
    length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1 #got 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0 #got 1
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5;
    x = 3;
    d_x = -1;
    d_y = 1;
    length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1 #got 0
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0 #got 1
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
#MAIN CODE
if __name__ == '__main__':
    some_tests()


