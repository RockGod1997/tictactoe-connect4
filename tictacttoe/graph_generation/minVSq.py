#minimax w alpha beta vs q learning code
import tkinter as tk
import tkinter.messagebox
import random
import csv
import pickle
class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.board = [' ']*9
        self.current_player = 'X'
        self.game_over = False
        self.x_wins = 0
        self.o_wins = 0
        self.games_played = 0
        self.q_table = self.load_q_table()  # Q-table for Q-learning
        self.create_board_gui()
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

    def play_game(self):
        while not self.game_over:
            if self.current_player == 'X':
                self.minimax_move()
            else:
                self.q_learning_move()  # Use Q-learning for player 'O'

            if self.check_winner():
                self.game_over = True
                if self.current_player == 'X':
                    self.x_wins += 1
                else:
                    self.o_wins += 1
            elif ' ' not in self.board:
                self.game_over = True
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'

        self.games_played += 1
        self.reset_board()

    def reset_board(self):
        self.board = [' ']*9
        self.current_player = 'X'
        self.game_over = False
        self.update_board_gui()

        if self.games_played == 100: # update value for increasing no of games
            self.write_results_to_csv()
        else:
            self.play_game()

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

    def minimax_move(self):
        best_score = -float('inf')
        best_move = None
        for move in self.available_moves():
            self.board[move] = 'X'
            score = self.minimax_alpha(self.board, False)
            self.board[move] = ' '
            if score > best_score:
                best_score = score
                best_move = move
        self.board[best_move] = 'X'

    def minimax_alpha(self, board, is_maximizing, alpha=-float('inf'), beta=float('inf')):
        if self.check_winner() and not is_maximizing:
            return -1
        elif self.check_winner() and is_maximizing:
            return 1
        elif ' ' not in board:
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for move in self.available_moves():
                board[move] = 'X'
                score = self.minimax_alpha(board, False, alpha, beta)
                board[move] = ' '
                best_score = max(score, best_score)
                alpha = max(alpha, score)
                if alpha >= beta:
                    break
            return best_score
        else:
            best_score = float('inf')
            for move in self.available_moves():
                board[move] = 'O'
                score = self.minimax_alpha(board, True, alpha, beta)
                board[move] = ' '
                best_score = min(score, best_score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return best_score

    def q_learning_move(self):
        state = self.board_to_str(self.board)
        if state not in self.q_table:
            self.q_table[state] = [0] * 9  # Initialize Q-values for the state if not already present

        if random.random() < epsilon:  # Exploration
            move = random.choice(self.available_moves())
        else:  # Exploitation
            move = self.choose_best_move(state)

        self.board[move] = 'O'

    def choose_best_move(self, state):
        # Choose the best move based on Q-values
        max_q_value = max(self.q_table[state])
        best_moves = [i for i, q_value in enumerate(self.q_table[state]) if q_value == max_q_value]
        return random.choice(best_moves)

    def update_q_values(self, state, action, reward, next_state):
        # Update Q-values using the Q-learning update rule
        old_q_value = self.q_table[state][action]
        next_max_q_value = max(self.q_table[next_state]) if next_state in self.q_table else 0
        new_q_value = old_q_value + alpha * (reward + gamma * next_max_q_value - old_q_value)
        self.q_table[state][action] = new_q_value

    def write_results_to_csv(self):
        with open('tic_tac_toe_results.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Player X Wins', 'Player O Wins'])
            writer.writerow([self.x_wins, self.o_wins])

    def board_to_str(self, board):
        # Convert the board state to a string representation for Q-learning
        return ''.join(board)

def main():
    root = tk.Tk()
    game = TicTacToe(root)
    game.play_game()
    root.mainloop()

if __name__ == "__main__":
    epsilon = 0.1  # Exploration rate
    alpha = 0.1  # Learning rate
    gamma = 0.9  # Discount factor
    main()
