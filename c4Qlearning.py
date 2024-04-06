import tkinter as tk
from tkinter import messagebox
import numpy as np
import random

class Connect4:
    def __init__(self):
        self.rows = 6
        self.columns = 7
        self.board = np.zeros((self.rows, self.columns))
        self.player1 = 1
        self.player2 = 2
        self.current_player = self.player1
        self.game_over = False
        self.moves = []

    def check_winner(self, player):
        # Check horizontal
        for r in range(self.rows):
            for c in range(self.columns - 3):
                if np.all(self.board[r, c:c+4] == player):
                    return True

        # Check vertical
        for c in range(self.columns):
            for r in range(self.rows - 3):
                if np.all(self.board[r:r+4, c] == player):
                    return True

        # Check diagonal (positive slope)
        for r in range(self.rows - 3):
            for c in range(self.columns - 3):
                if np.all([self.board[r+i, c+i] == player for i in range(4)]):
                    return True

        # Check diagonal (negative slope)
        for r in range(3, self.rows):
            for c in range(self.columns - 3):
                if np.all([self.board[r-i, c+i] == player for i in range(4)]):
                    return True

        return False

    def is_board_full(self):
        return 0 not in self.board

    def make_move(self, column):
        if self.game_over:
            return False
        
        if column < 0 or column >= self.columns or self.board[0][column] != 0:
            return False
        
        row = self.rows - 1
        while row >= 0:
            if self.board[row][column] == 0:
                self.board[row][column] = self.current_player
                self.moves.append(column)
                return True
            row -= 1
        
        return False

    def switch_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

class Connect4GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Connect4")
        self.connect4 = Connect4()
        self.buttons = []
        self.q_table = {}  # Q-table for Q-learning
        self.alpha = 0.1  # Learning rate
        self.gamma = 0.9  # Discount factor
        self.epsilon = 0.1  # Epsilon for exploration
        self.create_board()
        self.play()

    def create_board(self):
        for row in range(self.connect4.rows):
            button_row = []
            for col in range(self.connect4.columns):
                button = tk.Button(self.master, text=" ", width=5, height=2,
                                   command=lambda column=col: self.make_move(column))
                button.grid(row=row, column=col)
                button_row.append(button)
            self.buttons.append(button_row)

    def update_board(self):
        for row in range(self.connect4.rows):
            for col in range(self.connect4.columns):
                player = self.connect4.board[row][col]
                if player == 1:
                    self.buttons[row][col].config(text="X", state="disabled")
                elif player == 2:
                    self.buttons[row][col].config(text="O", state="disabled")

    def make_move(self, column):
        if self.connect4.make_move(column):
            self.update_board()
            if self.connect4.check_winner(self.connect4.current_player):
                messagebox.showinfo("Winner", f"Player {self.connect4.current_player} wins!")
                self.master.quit()
            elif self.connect4.is_board_full():
                messagebox.showinfo("Draw", "It's a draw!")
                self.master.quit()
            else:
                self.connect4.switch_player()
                self.play()

    def play(self):
        current_player = self.connect4.current_player
        if current_player == 1:
            # Player 1 uses Q-learning for making moves
            column = self.q_learning()
        else:
            # Player 2 uses a basic AI for making moves
            column = self.basic_ai()
        self.make_move(column)

    def q_learning(self):
        state = tuple(map(tuple, self.connect4.board))
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.connect4.columns)

        if random.random() < self.epsilon:
            # Exploration: Choose a random action
            return random.choice([col for col in range(self.connect4.columns) if self.is_valid_move(self.connect4.board, col)])
        else:
            # Exploitation: Choose the action with the highest Q-value
            return np.argmax(self.q_table[state])

    def basic_ai(self):
        # Check for winning moves
        for col in range(self.connect4.columns):
            if self.is_winning_move(col, self.connect4.player2):
                return col

        # Block opponent's winning moves
        for col in range(self.connect4.columns):
            if self.is_winning_move(col, self.connect4.player1):
                return col

        # Otherwise, select a random valid move
        return random.choice([col for col in range(self.connect4.columns) if self.is_valid_move(self.connect4.board, col)])

    def is_winning_move(self, column, player):
        temp_board = np.copy(self.connect4.board)
        for row in range(self.connect4.rows - 1, -1, -1):
            if temp_board[row][column] == 0:
                temp_board[row][column] = player
                if self.connect4.check_winner(player):
                    return True
                else:
                    return False

    def is_valid_move(self, board, column):
        return board[0][column] == 0

def main():
    root = tk.Tk()
    gui = Connect4GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
