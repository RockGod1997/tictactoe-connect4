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
  def choose_best_move(self, available_moves, player):
  
   best_score = float('-inf')  # Initialize best score for maximizing player (computer)
   best_move = None

   for move in available_moves:
    # Simulate the move by placing the computer's mark ('O') on the board
    self.board[move] = player
    score = self.minimax(False)  # Call minimax for minimizing player (human)
    self.board[move] = ' '  # Undo the simulated move

    # Update best move if current score is better for the computer
    if score > best_score:
      best_score = score
      best_move = move

   return best_move
  def minimax(self, is_minimizing):
  
  
   if self.check_winner():
     # Return score based on winner (10 for computer win, -10 for human win, 0 for tie)
     winner = self.board[0]  # Assuming winner is placed in the first cell for efficiency
     if winner == 'O':
      return 10
     elif winner == 'X':
      return -10
     else:
      return 0

  # Check for tie (no available moves)
   if not any(' ' in row for row in self.board):
    return 0

   if is_minimizing:
    # Minimizing player (human) wants to minimize the score for the computer
    best_score = float('inf')
    for move in [i for i, x in enumerate(self.board) if x == ' ']:
      self.board[move] = 'X'  # Simulate human's move
      score = self.minimax(True)  # Recursively call minimax for maximizing player
      self.board[move] = ' '  # Undo the simulated move
      best_score = min(best_score, score)  # Minimize score for human
   else:
    # Maximizing player (computer) wants to maximize the score
    best_score = float('-inf')
    for move in [i for i, x in enumerate(self.board) if x == ' ']:
      self.board[move] = 'O'  # Simulate computer's move
      score = self.minimax(False)  # Recursively call minimax for minimizing player
      self.board[move] = ' '  # Undo the simulated move
      best_score = max(best_score, score)  # Maximize score for computer

   return best_score

# Start the game
game = TicTacToe()
game.run()

