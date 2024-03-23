import tkinter as tk
import random


class TicTacToe:
  def __init__(self):
    self.board = [' ' for _ in range(9)]  # Initialize empty board
    self.game_over = False
    self.window = tk.Tk()
    self.window.title("Tic Tac Toe")
    self.create_board()
    self.play_game()  # Start the game with computer moves

  def create_board(self):
    self.buttons = []
    for i in range(3):
      row = []
      for j in range(3):
        button = tk.Button(self.window, text="", font=("Arial", 40), width=3, height=1, state=tk.DISABLED)
        button.grid(row=i, column=j)
        row.append(button)
      self.buttons.append(row)

  def update_board(self):
    for i in range(3):
      for j in range(3):
        self.buttons[i][j].config(text=self.board[i * 3 + j])

  def check_winner(self):
    # Check rows
    for i in range(3):
      if self.board[i * 3] == self.board[i * 3 + 1] == self.board[i * 3 + 2] != ' ':
        self.game_over = True
        self.display_message(f"{self.board[i * 3]} Wins!")
        return

    # Check columns
    for i in range(3):
      if self.board[i] == self.board[i + 3] == self.board[i + 6] != ' ':
        self.game_over = True
        self.display_message(f"{self.board[i]} Wins!")
        return

    # Check diagonals
    if self.board[0] == self.board[4] == self.board[8] != ' ':
      self.game_over = True
      self.display_message(f"{self.board[0]} Wins!")
      return
    if self.board[2] == self.board[4] == self.board[6] != ' ':
      self.game_over = True
      self.display_message(f"{self.board[2]} Wins!")
      return

    # Check for tie
    if not any(' ' in row for row in self.board):
      self.game_over = True
      self.display_message("It's a Tie!")

  def display_message(self, message):
    label = tk.Label(self.window, text=message, font=("Arial", 30))
    label.grid(row=3, columnspan=3)

  def computer_move(self, player):
    if self.game_over:
      return

    available_moves = [i for i, x in enumerate(self.board) if x == ' ']
    if available_moves:
      move = self.choose_best_move(available_moves, player)  # Implement your AI logic here
      self.board[move] = player
      self.update_board()
      self.check_winner()

  def choose_best_move(self, available_moves, player):
    # Implement your AI logic here (e.g., Minimax algorithm)
    # This example randomly chooses an available space for now
    return random.choice(available_moves)

  def play_game(self):
    while not self.game_over:
      # Alternate player moves (X and O)
      for player in ['X', 'O']:
        self.computer_move(player)

    # Disable buttons after game over
    for row in self.buttons:
      for button in row:
        button.config(state=tk.DISABLED)

  def run(self):
    self.window.mainloop()

# Start the game
game = TicTacToe()
game.run()