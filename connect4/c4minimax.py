#code for minimax  vs basic ai
import tkinter as tk
from tkinter import messagebox
import numpy as np
import random
import csv
import time
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
        self.total_time = 0
        self.move_count = 0
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
            start_time = time.time()  # Measure start time
            column = self.minimax(self.connect4.board, depth=3, maximizing_player=True)[0]
            end_time = time.time()  # Measure end time
            self.total_time += end_time - start_time  # Add to total time
            self.move_count += 1  # Increment move count
        else:
            column = self.basic_ai()
        self.make_move(column)

    def minimax(self, board, depth, maximizing_player):
        if depth == 0 or self.connect4.check_winner(self.connect4.player1) or self.connect4.check_winner(self.connect4.player2) or self.connect4.is_board_full():
            return None, self.evaluate_board(board)

        if maximizing_player:
            max_eval = float('-inf')
            best_column = None
            for col in range(self.connect4.columns):
                if self.is_valid_move(board, col):
                    new_board = self.make_temp_move(board, col, self.connect4.player1)
                    _, eval_score = self.minimax(new_board, depth - 1, False)
                    if eval_score > max_eval:
                        max_eval = eval_score
                        best_column = col
            return best_column, max_eval
        else:
            min_eval = float('inf')
            best_column = None
            for col in range(self.connect4.columns):
                if self.is_valid_move(board, col):
                    new_board = self.make_temp_move(board, col, self.connect4.player2)
                    _, eval_score = self.minimax(new_board, depth - 1, True)
                    if eval_score < min_eval:
                        min_eval = eval_score
                        best_column = col
            return best_column, min_eval

    def evaluate_board(self, board):
        score = 0

        # Check rows for player 1
        score += self.evaluate_line(board, self.connect4.player1)

        # Check columns for player 1
        score += self.evaluate_line(np.transpose(board), self.connect4.player1)

        # Check diagonals for player 1
        for i in range(-2, 4):
            score += self.evaluate_line(np.diagonal(board, offset=i), self.connect4.player1)

        # Check rows for player 2
        score -= self.evaluate_line(board, self.connect4.player2)

        # Check columns for player 2
        score -= self.evaluate_line(np.transpose(board), self.connect4.player2)

        # Check diagonals for player 2
        for i in range(-2, 4):
            score -= self.evaluate_line(np.diagonal(board, offset=i), self.connect4.player2)

        return score

    def evaluate_line(self, line, player):
        score = 0
        empty = 0
        opp_player = self.connect4.player1 if player == self.connect4.player2 else self.connect4.player2

        for i in range(len(line)):
            if np.all(line[i] == player):
                score += 1
            elif np.all(line[i] == 0):
                empty += 1
            else:
                empty = 0
                break

        if score == 4:
            return 1000000
        elif score == 3 and empty == 1:
            return 100
        elif score == 2 and empty == 2:
            return 10
        elif score == 1 and empty == 3:
            return 1
        else:
            return 0

    def is_valid_move(self, board, column):
        return board[0][column] == 0

    def make_temp_move(self, board, column, player):
        new_board = np.copy(board)
        for row in range(self.connect4.rows - 1, -1, -1):
            if new_board[row][column] == 0:
                new_board[row][column] = player
                break
        return new_board

    def basic_ai(self):
        for col in range(self.connect4.columns):
            if self.is_winning_move(col, self.connect4.player2):
                return col

        for col in range(self.connect4.columns):
            if self.is_winning_move(col, self.connect4.player1):
                return col

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

def main():
    wins_player1 = 0
    wins_player2 = 0

    for _ in range(1):   #update to increase no. of games
        root = tk.Tk()
        gui = Connect4GUI(root)
        root.mainloop()

        if gui.connect4.check_winner(gui.connect4.player1):
            wins_player1 += 1
        elif gui.connect4.check_winner(gui.connect4.player2):
            wins_player2 += 1

    # Write results to CSV file
    with open('results.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Player 1 Wins', 'Player 2 Wins'])
        writer.writerow([wins_player1, wins_player2])
    average_time = gui.total_time / gui.move_count
    print(f"Average minimax move runtime: {average_time:.6f} seconds")

if __name__ == "__main__":
    main()
