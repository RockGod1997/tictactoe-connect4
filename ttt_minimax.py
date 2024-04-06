import tkinter as tk
import tkinter.messagebox
import random

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.board = [' ']*9
        self.current_player = 'X'
        self.game_over = False
        self.create_board_gui()
        self.play_game()

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
                self.select_move_for_O()

            self.update_board_gui()

            if self.check_winner():
                self.game_over = True
                if self.current_player == 'X':
                    tkinter.messagebox.showinfo("Tic Tac Toe", "Player X wins!")
                else:
                    tkinter.messagebox.showinfo("Tic Tac Toe", "Player O wins!")
            elif ' ' not in self.board:
                self.game_over = True
                tkinter.messagebox.showinfo("Tic Tac Toe", "It's a tie!")
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'

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
            score = self.minimax(self.board, False)
            self.board[move] = ' '
            if score > best_score:
                best_score = score
                best_move = move
        self.board[best_move] = 'X'

    def minimax(self, board, is_maximizing):
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
                score = self.minimax(board, False)
                board[move] = ' '
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for move in self.available_moves():
                board[move] = 'O'
                score = self.minimax(board, True)
                board[move] = ' '
                best_score = min(score, best_score)
            return best_score

    def select_move_for_O(self):
        # Check for winning move
        for move in self.available_moves():
            self.board[move] = 'O'
            if self.check_winner():
                self.board[move] = 'O'
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
        self.random_move()

    def random_move(self):
        move = random.choice(self.available_moves())
        self.board[move] = 'O'

def main():
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()


if __name__ == "__main__":
    main()
