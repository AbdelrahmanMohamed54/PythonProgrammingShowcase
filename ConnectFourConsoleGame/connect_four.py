"""
Name: Abdelrahman Mohamed

Task Description: This Python program implements the classic
two-player game Connect Four, where players take turns dropping
colored discs into a vertical grid. The game board size is set
by quasi-constants in the code, and players win by getting four
of their discs in a row, column, or diagonal. The program allows
for play against another human player or against an AI player
using the Minimax algorithm for optimal play. The code follows
PEP8 style guidelines and includes comments throughout for
readability and understanding.
"""

# Define the board size constants
ROWS = 6
COLS = 7

# Define the player constants
PLAYER1 = 1
PLAYER2 = 2

# Define the player symbols
player1_symbol = ' X '
player2_symbol = ' O '


def display_board(board):
    # Display column numbers above the board
    column_numbers = '  ' + '   '.join(str(i) for i in range(COLS))
    print(column_numbers)
    # Add a horizontal line under the numbers
    print('-' * (COLS * 4 + 1))

    # Display the board contents
    for row in range(ROWS):
        row_string = '|'
        for col in range(COLS):
            row_string += board[row][col] + '|'
        print(row_string)
        # Add a horizontal line between rows
        print('-' * (COLS * 4 + 1))


def choose_game_mode():
    # Initialize the game board
    board = [['   ' for _ in range(COLS)] for _ in range(ROWS)]

    # Display the initial game board and welcome statement
    display_board(board)
    print("Welcome to connect four!!")

    # Ask if the player wants to play against AI or another player
    while True:
        mode = input("Do you want to play against a human (h) or AI (a)? ")
        if mode.lower() == "h":
            play_game()
            return False
        elif mode.lower() == "a":
            return True
        else:
            print("Invalid input. Please enter 'h' to play against a human or 'a' to play against AI.")


def restart_prompt():
    # A function that Prompts the player to ask them if they want to restart or quit.
    restart = input("Do you want to restart (r) or quit (q) the game? : ")
    if restart.lower() == 'r':
        play_game()
        return
    elif restart.lower() == 'q':
        return
    else:
        print("Invalid input. Please enter 'r' to restart or 'q' to quit.")


def play_game():
    # Initialize the game board
    board = [['   ' for _ in range(COLS)] for _ in range(ROWS)]

    # Display the initial game board and welcome statement
    display_board(board)
    print("Welcome to connect four!!")

    # Initialize the player and game status
    player = PLAYER1
    game_over = False

    # Loop until the game is over
    while not game_over:
        # Prompt the player for their move
        move = get_player_move(player, board)

        # Handle restart and quit options
        if move == 'r':
            play_game()
            return
        elif move == 'q':
            return

        # Update the game board with the player's move
        row = ROWS - 1
        while row >= 0:
            if board[row][move] == '   ':
                board[row][move] = player1_symbol if player == PLAYER1 else player2_symbol
                break
            row -= 1

        # Display the updated game board
        display_board(board)

        # Check for a win or tie
        # Check if player 1 won
        if check_win(board, player1_symbol):
            print(f"Player 1 wins!")
            while True:
                restart = input("Do you want to restart (r) or quit (q) the game? : ")
                if restart.lower() == 'r':
                    play_game()
                    return
                elif restart.lower() == 'q':
                    return
                else:
                    print("Invalid input. Please enter 'r' to restart or 'q' to quit.")

        # Check if player 2 won
        elif check_win(board, player2_symbol):
            print(f"Player 2 wins!")
            while True:
                restart = input("Do you want to restart (r) or quit (q) the game? : ")
                if restart.lower() == 'r':
                    play_game()
                    return
                elif restart.lower() == 'q':
                    return
                else:
                    print("Invalid input. Please enter 'r' to restart or 'q' to quit.")

        # Check for tie
        if check_tie(board):
            print("Game is a tie!")
            while True:
                restart = input("Do you want to restart (r) or quit (q) the game? : ")
                if restart.lower() == 'r':
                    play_game()
                    return
                elif restart.lower() == 'q':
                    return
                else:
                    print("Invalid input. Please enter 'r' to restart or 'q' to quit.")

        # Switch to the other player
        player = PLAYER2 if player == PLAYER1 else PLAYER1


# Define a function to get the player's move
def get_player_move(player, board):
    # Use an infinite loop to continuously prompt the player for their move
    while True:
        # Ask the player for their move and give options to restart or quit
        move = input(f"Player {player}, enter a column number (0-{COLS - 1}), or 'r' to restart, 'q' to quit: ")

        # If the player wants to restart or quit, return the input as is
        if move == 'r' or move == 'q':
            return move

        # Try to convert the input to an integer
        try:
            col = int(move)
        # If the input is not an integer, print an error message and continue the loop
        except ValueError:
            print("Invalid input, please enter a valid column number!")
            continue

        # Check if the column number is within the board's boundaries
        if col < 0 or col >= COLS:
            print(f"Column number should be between 0 and {COLS - 1}!")
        # Check if the column is not already full
        elif board[0][col] != '   ':
            print("Column is full, try another column!")
        # If the input is valid, return the column number
        else:
            return col


def check_win(board, symbol):
    # Check rows for win
    for row in range(ROWS):
        for col in range(COLS - 3):
            if board[row][col] == symbol and board[row][col + 1] == symbol \
                    and board[row][col + 2] == symbol and board[row][col + 3] == symbol:
                return True

    # Check columns for win
    for row in range(ROWS - 3):
        for col in range(COLS):
            if board[row][col] == symbol and board[row + 1][col] == symbol \
                    and board[row + 2][col] == symbol and board[row + 3][col] == symbol:
                return True

    # Check diagonal (top-left to bottom-right) for win
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == symbol and board[row + 1][col + 1] == symbol \
                    and board[row + 2][col + 2] == symbol and board[row + 3][col + 3] == symbol:
                return True

    # Check diagonal (bottom-left to top-right) for win
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == symbol and board[row - 1][col + 1] == symbol \
                    and board[row - 2][col + 2] == symbol and board[row - 3][col + 3] == symbol:
                return True

    # No win found
    return False


def check_tie(board):
    # Check if any column is still empty
    for col in range(COLS):
        if board[0][col] == '   ':
            return False

    # All columns are full, so it's a tie
    return True


# Run the Choose game mode function to run the code and start the game.
choose_game_mode()
