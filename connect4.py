import random
from tkinter import Button, Canvas, Tk, messagebox

# Define game constants
ROWS = 6
COLS = 7
PLAYER_ONE = 1
PLAYER_TWO = 2

def create_board():
  """Creates a new empty Connect 4 board"""
  board = []
  for _ in range(ROWS):
    board.append([0] * COLS)
  return board

def is_valid_location(board, col):
  """Checks if a piece can be placed in the given column"""
  return board[0][col] == 0

def drop_piece(board, col, player):
  """Drops a piece into the given column for the specified player"""
  for row in reversed(range(ROWS)):
    if board[row][col] == 0:
      board[row][col] = player
      return row
  return None

def is_winning_move(board, row, col, player):
  """Checks if the last move resulted in a win for the player"""
  # Check horizontal
  count = 0
  for c in range(col, min(col + 4, COLS)):
    if board[row][c] == player:
      count += 1
    else:
      count = 0
    if count == 4:
      return True

  # Check vertical
  count = 0
  for r in range(row, min(row + 4, ROWS)):
    if board[r][col] == player:
      count += 1
    else:
      count = 0
    if count == 4:
      return True

  # Check positive diagonal
  count = 0
  for i in range(min(row, col), min(row + 4, ROWS), 1):
    j = col + i - row
    if 0 <= j < COLS and board[i][j] == player:
      count += 1
    else:
      count = 0
    if count == 4:
      return True

  # Check negative diagonal
  count = 0
  for i in range(max(row - 3, 0), max(row, ROWS - 4), -1):
    j = col + i - row
    if 0 <= j < COLS and board[i][j] == player:
      count += 1
    else:
      count = 0
    if count == 4:
      return True

  return False

def is_board_full(board):
  """Checks if the board is completely filled"""
  for col in range(COLS):
    if is_valid_location(board, col):
      return False
  return True

def get_computer_move(board, player):
  """Chooses a random valid move for the computer player"""
  valid_locations = [col for col in range(COLS) if is_valid_location(board, col)]
  return random.choice(valid_locations)

def draw_board(board, canvas):
  """Draws the Connect 4 board on the Tkinter canvas"""
  canvas.delete("all")
  for row in range(ROWS):
    for col in range(COLS):
      x = 75 + col * 100
      y = 60 + row * 100
      radius = 40
      color = "white"
      if board[row][col] == PLAYER_ONE:
        color = "red"
      elif board[row][col] == PLAYER_TWO:
        color = "yellow"
      canvas.create_circle(x, y, radius, fill=color)

def main():
  window = Tk()
  window.title("Connect 4")

  canvas = Canvas(window, width=700, height=600)
  canvas.pack()

  board = create_board()
  current_player = random.choice([PLAYER_ONE, PLAYER_TWO])

  def handle_click(col):
    if not is_valid_location(board, col):
      return
    row = drop_piece(board, col, current_player)
    if is_winning_move(board, row, col, current_player):
      draw_board(board, canvas)
      message = f"Player {current_player} wins!"
      window.after(1000, lambda: messagebox.showinfo("Game Over", message))
      return

    if is_board_full(board):
      draw_board(board, canvas)
      message = "It's a tie!"
      window.after(1000, lambda: messagebox.showinfo("Game Over", message))
      return

    # Computer's turn
    computer_col = get_computer_move(board, PLAYER_TWO)
    row = drop_piece(board, computer_col, PLAYER_TWO)
    draw_board(board, canvas)

    # Switch turns
    current_player = PLAYER_ONE if current_player == PLAYER_TWO else PLAYER_TWO

  # Create buttons for each column
  for col in range(COLS):
    button = Button(window, text=f"{col+1}", width=2, command=lambda c=col: handle_click(c))
    button.grid(row=0, column=col)

  draw_board(board, canvas)

  window.mainloop()

if __name__ == "__main__":
  main()
