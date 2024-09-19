import math
import time

# Constants for the game
PLAYER = 'O'  # Human player
AI = 'X'  # Computer player
EMPTY = ' '

# Initialize the Tic-Tac-Toe board
def create_board():
    return [[EMPTY for _ in range(3)] for _ in range(3)]

# Check for a winner
def check_winner(board):
    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]

    return None

# Check if the board is full (tie condition)
def is_board_full(board):
    return all(cell != EMPTY for row in board for cell in row)

# Display the board
def print_board(board):
    for row in board:
        print('|'.join(row))
        print("-" * 5)

# Minimax algorithm with alpha-beta pruning
def minimax(board, depth, is_maximizing, alpha, beta):
    winner = check_winner(board)
    if winner == AI:
        return 1
    elif winner == PLAYER:
        return -1
    elif is_board_full(board):
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = AI
                    eval = minimax(board, depth + 1, False, alpha, beta)
                    board[i][j] = EMPTY
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER
                    eval = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = EMPTY
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

# Find the best move for the AI
def best_move(board):
    start = time.time()
    best_val = -math.inf
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = AI
                move_val = minimax(board, 0, False, -math.inf, math.inf)
                board[i][j] = EMPTY
                if move_val > best_val:
                    best_val = move_val
                    move = (i, j)
    end = time.time()  # End time
    print('AI evaluation time: {}s'.format(round(end - start, 7)))
    return move, (end - start)

# Check if the game is over
def is_game_over(board):
    return check_winner(board) or is_board_full(board)

# Main game loop
def play_game():
    board = create_board()
    current_player = AI  # AI moves first
    total_ai_time = 0  # Initialize total time for AI
    total_player_time = 0  # Initialize total time for the player

    while not is_game_over(board):
        print_board(board)
        if current_player == PLAYER:
            # Player move
            print("Your turn!")
            start = time.time()  # Start time for player input
            row = int(input("Enter row (0-2): "))
            col = int(input("Enter column (0-2): "))
            end = time.time()  # End time for player input
            player_time = end - start
            print('Player input time: {}s'.format(round(player_time, 7)))
            total_player_time += player_time  # Add player input time to total

            if board[row][col] == EMPTY:
                board[row][col] = PLAYER
                current_player = AI
            else:
                print("Invalid move, try again!")
        else:
            # AI move
            print("AI's turn...")
            move, ai_time = best_move(board)
            board[move[0]][move[1]] = AI
            print(f"AI move time: {round(ai_time, 7)}s")
            total_ai_time += ai_time  # Add AI time to total
            current_player = PLAYER

    print_board(board)
    winner = check_winner(board)
    if winner:
        print(f"{winner} wins!")
    else:
        print("It's a tie!")

    # Print the total time for both separately
    print(f"Total AI time: {round(total_ai_time, 7)}s")
    print(f"Total player time: {round(total_player_time, 7)}s")

# Run the game
if __name__ == "__main__":
    play_game()
