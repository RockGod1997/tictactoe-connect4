import tkinter as tk
import tkinter.messagebox
import random
import pickle
import csv

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.board = [' ']*9
        self.current_player = 'X'
        self.game_over = False
        self.x_wins = 0
        self.o_wins = 0
        self.q_table = self.load_q_table()  # Load Q-table from file
        self.create_board_gui()
        self.play_games(1)  # update for number of games

    def load_q_table(self):
        try:
            with open('q_table.pickle', 'rb') as f:
                print("pickle file loaded")
                return pickle.load(f)
        except FileNotFoundError:
            return {}

    def save_q_table(self):
        with open('q_table.pickle', 'wb') as f:
            pickle.dump(self.q_table, f)

    def create_board_gui(self):
        self.labels = []
        for i in range(3):
            row_labels = []
            for j in range(3):
                label = tk.Label(self.master, text=' ', font=('Arial', 20), width=5, height=2, relief='raised')
                label.grid(row=i, column=j, padx=5, pady=5)
                row_labels.append(label)
            self.labels.append(row_labels)

    def play_games(self, num_games):
        for _ in range(num_games):
            self.play_game()
            self.reset_game()

        # Save the results to CSV
        with open('qlearn.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Player X Wins', 'Player O Wins'])
            writer.writerow([self.x_wins, self.o_wins])

    def play_game(self):
        self.update_board_gui()  # Initial update
        self.play_next_move()  # Start the game loop

    def reset_game(self):
        self.board = [' ']*9
        self.game_over = False
        self.current_player = 'X'

    def play_next_move(self):
        if self.game_over:
            return

        if self.current_player == 'X':
            self.q_learning_move()
        else:
            self.select_move_for_O()

        self.update_board_gui()

        if self.check_winner():
            self.game_over = True
            if self.current_player == 'X':
                self.x_wins += 1
            else:
                self.o_wins += 1
        elif ' ' not in self.board:
            self.game_over = True

        self.current_player = 'O' if self.current_player == 'X' else 'X'  # Alternate players
        self.play_next_move()  # Schedule the next move

    def update_board_gui(self):
        for i in range(3):
            for j in range(3):
                self.labels[i][j].config(text=self.board[i*3 + j])

    def check_winner(self):
        lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        for line in lines:
            if self.board[line[0]] == self.board[line[1]] == self.board[line[2]] != ' ':
                return True
        return False

    def available_moves(self):
        return [i for i, mark in enumerate(self.board) if mark == ' ']

    def q_learning_move(self):
        state = ''.join(self.board)
        if state not in self.q_table:
            self.q_table[state] = [0] * 9  # Initialize Q-values for new state

        # Explore or exploit
        if random.random() < 0.1:  # Explore with 10% probability
            move = random.choice(self.available_moves())
        else:  # Exploit (select action with max Q-value)
            max_q_value = max(self.q_table[state])
            best_moves = [i for i, q_value in enumerate(self.q_table[state]) if q_value == max_q_value]
            move = random.choice(best_moves)

        # Update Q-value
        reward = self.reward(state)
        next_state = self.result(state, move)
        if next_state not in self.q_table:
            self.q_table[next_state] = [0] * 9
        self.q_table[state][move] += 0.1 * (reward + 0.9 * max(self.q_table[next_state]) - self.q_table[state][move])

        # Save Q-table after every move
        self.save_q_table()

        # Check if the selected move is available
        if move in self.available_moves():
            # Update game board with player X's move
            self.board = list(next_state)
        else:
            # If the selected move is not available, choose another move randomly
            self.q_learning_move()

    def result(self, state, move):
        new_state = list(state)
        new_state[move] = 'X'
        return ''.join(new_state)

    def reward(self, state):
        if self.check_winner() and self.current_player == 'X':
            return 1  # Win
        elif self.check_winner() and self.current_player == 'O':
            return -1  # Lose
        elif ' ' not in state:
            return 0  # Draw
        else:
            return 0.5  # Intermediate state

    def select_move_for_O(self):
        # Check for winning move
        for move in self.available_moves():
            self.board[move] = 'O'
            if self.check_winner():
                return
            self.board[move] = ' '

        # Check for blocking move
        for move in self.available_moves():
            self.board[move] = 'X'
            if self.check_winner():
                self.board[move] = 'O'
                return
            self.board[move] = ' '

        # If no winning or blocking move, make a random move
        move = random.choice(self.available_moves())
        self.board[move] = 'O'

def main():
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

if __name__ == "__main__":
    main()
