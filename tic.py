from tkinter import Tk, Button


# Define game board and player markers
board = [' ' for _ in range(9)]
player_x = 'X'
player_o = 'O'
current_player = player_x


# Function to display the game board on the GUI
def display_board():
    for i in range(3):
        for j in range(3):
            cell_number = i * 3 + j
            buttons[cell_number].config(text=board[cell_number])


# Function to check if a player has won
def is_winner(player, board):
    win_conditions = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),
                      (0, 4, 8), (2, 4, 6))
    for condition in win_conditions:
        if board[condition[0]] == player and board[condition[1]] == player and board[condition[2]] == player:
            return True
    return False


# Function to check if the board is full
def is_board_full(board):
    return ' ' not in board


# Function to check if a move is valid
def is_valid_move(cell_number):
    return board[cell_number] == ' '


# Function to handle player move and update the board
def player_move(cell_number):
    global current_player
    if is_valid_move(cell_number):
        board[cell_number] = current_player
        buttons[cell_number].config(state='disabled')

        if is_winner(current_player, board):
            display_board()
            print(f"Player {current_player} wins!")
            disable_all_buttons()
        elif is_board_full(board):
            display_board()
            print("It's a tie!")
            disable_all_buttons()

        current_player = player_o if current_player == player_x else player_x
        display_board()
        if current_player == player_o:  # Computer's turn
            computer_move()


# computer moves
def computer_move():
    # Prioritize winning moves for the computer
    for i in range(9):
        if is_valid_move(i):
            board_copy = board.copy()
            board_copy[i] = player_o
            if is_winner(player_o, board_copy):
                player_move(i)
                return

    # Block player's winning moves if possible
    for i in range(9):
        if is_valid_move(i):
            board_copy = board.copy()
            board_copy[i] = player_x
            if is_winner(player_x, board_copy):
                player_move(i)
                return

    # Play the center or a corner if available
    available_moves = [i for i in range(9) if is_valid_move(i)]
    preferred_moves = [4, 0, 2, 6, 8]  # Center, corners
    for move in preferred_moves:
        if move in available_moves:
            player_move(move)
            return

    # Play any random valid move
    if available_moves:
        player_move(available_moves[0])
    else:
    # Handle the case where no valid moves are left (board is full)
        print("The board is full!")
        disable_all_buttons()


# Function to disable all buttons after game ends
def disable_all_buttons():
    for button in buttons:
        button.config(state='disabled')


# Create the main window and buttons
window = Tk()
window.title("Tic Tac Toe")

buttons = []
for i in range(3):
    for j in range(3):
        cell_number = i * 3 + j
        button = Button(window, text=' ', font=("Arial", 20), width=3, height=1, command=lambda c=cell_number: player_move(c))
        button.grid(row=i, column=j)
        buttons.append(button)


# Start the game loop
display_board()
window.mainloop()