import tkinter as tk
from tkinter import messagebox
import numpy as np
import random
import csv
import pickle
import sys
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
                self.moves.append((column, time.time()))  # Record move and timestamp
                return True
            row -= 1
        
        return False

    def switch_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

class Connect4GUI:
    def __init__(self, master, q_table=None):
        self.master = master
        self.master.title("Connect4")
        self.connect4 = Connect4()
        self.buttons = []
        self.q_table = q_table if q_table else {}
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.1  # Exploration rate
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
                self.update_q_values(reward=1)
                print(f"Player {self.connect4.current_player} wins!")
                self.master.quit()
            elif self.connect4.is_board_full():
                self.update_q_values(reward=0)
                print("It's a draw!")
                self.master.quit()
            else:
                self.connect4.switch_player()
                self.play()

    def play(self):
        current_player = self.connect4.current_player

        if current_player == 1:
            start_time = time.time()  # Measure start time
            column = self.choose_action()
            end_time = time.time()  # Measure end time
            self.total_time += end_time - start_time  # Add to total time
            self.move_count += 1  # Increment move count
        else:
            column = self.basic_ai()

        self.make_move(column)

    def choose_action(self):
        if random.random() < self.epsilon:
            # Randomly select action for exploration
            return random.choice([col for col in range(self.connect4.columns) if self.is_valid_move(self.connect4.board, col)])
        else:
            # Choose action with highest Q-value
            state = self.get_state_key(self.connect4.board)
            q_values = self.q_table.get(state, np.zeros(self.connect4.columns))
            return np.argmax(q_values)

    def get_state_key(self, board):
        return str(board.flatten())

    def update_q_values(self, reward):
        states = [self.get_state_key(self.connect4.board)]
        actions = [self.connect4.moves[-1][0]]  # Latest action

        # Update Q-values backwards
        for i in range(len(self.connect4.moves) - 2, -1, -1):
            state = self.get_state_key(self.connect4.board)
            states.append(state)
            actions.append(self.connect4.moves[i][0])
            if self.connect4.check_winner(self.connect4.current_player):
                # Reward for winning
                reward = 1
            elif self.connect4.is_board_full():
                # Reward for draw
                reward = 0
            else:
                # Reward for intermediate steps (no reward)
                reward = 0
            # Q-value update
            next_state = self.get_state_key(self.connect4.board)
            q_values = self.q_table.get(state, np.zeros(self.connect4.columns))
            next_q_values = self.q_table.get(next_state, np.zeros(self.connect4.columns))
            q_values[actions[-1]] += self.learning_rate * (reward + self.discount_factor * np.max(next_q_values) - q_values[actions[-1]])
            self.q_table[state] = q_values

    def is_valid_move(self, board, column):
        return board[0][column] == 0

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

def save_q_table(q_table, filename):
    with open(filename, 'wb') as f:
        pickle.dump(q_table, f)

def load_q_table(filename):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        print("File not found. Returning empty Q-table.")
        return {}

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "load":
        q_table = load_q_table('q_table.pickle')
    else:
        q_table = None

    wins_player1 = 0
    wins_player2 = 0

    for _ in range(1):   # Update to increase the number of games
        root = tk.Tk()
        gui = Connect4GUI(root, q_table)
        root.mainloop()

        if gui.connect4.check_winner(gui.connect4.player1):
            wins_player1 += 1
        elif gui.connect4.check_winner(gui.connect4.player2):
            wins_player2 += 1
    
    # Write results to CSV file
    with open('results.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Player 1 Wins', 'Player 2 Wins', 'Average Q-learning Move Runtime'])
        writer.writerow([wins_player1, wins_player2])
    average_time = gui.total_time / gui.move_count
    print(f"Average qlearning move runtime: {average_time:.6f} seconds")

    save_q_table(gui.q_table, 'q_table.pickle')

if __name__ == "__main__":
    main()
