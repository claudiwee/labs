import tkinter as tk
from tkinter import messagebox
import random

class XO:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Крестики-нолики")
        self.window.configure(bg='#2C3E50')
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.colors = {'bg': '#2C3E50', 'x': '#E74C3C', 'o': '#3498DB', 'btn': '#34495E'}
        self.create_widgets()
    
    def create_widgets(self):
        self.status = tk.Label(self.window, text="Ваш ход (❌)", font=("Arial", 14, "bold"), 
                              fg=self.colors['x'], bg=self.colors['bg'], pady=10)
        self.status.grid(row=0, column=0, columnspan=3)
        
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.window, text="", font=("Arial", 20, "bold"), 
                    width=4, height=2, bg=self.colors['btn'], fg="white", command=lambda r=i, c=j: self.player_move(r, c))
                self.buttons[i][j].grid(row=i+1, column=j, padx=2, pady=2)
        
        tk.Button(self.window, text="🔄 Новая игра", font=("Arial", 12), bg='#1ABC9C', fg='white',
                 command=self.reset_game).grid(row=4, column=0, columnspan=3, pady=10)
    
    def player_move(self, row, col):
        if self.board[row][col] == "" and self.current_player == "X":
            self.make_move(row, col, "X")
            if not self.check_game_over(): 
                self.current_player = "O"
                self.status.config(text="Ход бота...", fg=self.colors['o'])
                self.window.after(300, self.bot_move)
    
    def bot_move(self):
        # 1. Попробовать выиграть
        move = self.find_winning_move("O")
        if not move: 
            # 2. Блокировать выигрыш игрока
            move = self.find_winning_move("X")
        if not move: 
            # 3. Занять центр
            if self.board[1][1] == "": move = (1, 1)
        if not move: 
            # 4. Занять угол
            move = self.get_random_corner()
        if not move: 
            # 5. Случайный ход
            move = self.get_random_move()
        
        if move: 
            self.make_move(move[0], move[1], "O")
            self.current_player = "X"
            self.status.config(text="Ваш ход (❌)", fg=self.colors['x'])
            self.check_game_over()
    
    def find_winning_move(self, player):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = player
                    if self.check_winner() == player:
                        self.board[i][j] = ""
                        return (i, j)
                    self.board[i][j] = ""
        return None
    
    def get_random_corner(self):
        corners = [(0,0), (0,2), (2,0), (2,2)]
        empty_corners = [c for c in corners if self.board[c[0]][c[1]] == ""]
        return random.choice(empty_corners) if empty_corners else None
    
    def get_random_move(self):
        empty_cells = [(i,j) for i in range(3) for j in range(3) if self.board[i][j] == ""]
        return random.choice(empty_cells) if empty_cells else None
    
    def make_move(self, row, col, player):
        self.board[row][col] = player
        symbol = "❌" if player == "X" else "⭕"
        color = self.colors['x'] if player == "X" else self.colors['o']
        self.buttons[row][col].config(text=symbol, state="disabled", fg=color, bg='#2C3E50')
    
    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "": return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "": return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "": return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "": return self.board[0][2]
        if all(cell != "" for row in self.board for cell in row): return "tie"
        return None
    
    def check_game_over(self):
        winner = self.check_winner()
        if winner:
            if winner == "tie": 
                messagebox.showinfo("Игра окончена", "Ничья!")
            else:
                winner_text = "Игрок (❌)" if winner == "X" else "Бот (⭕)"
                messagebox.showinfo("Игра окончена", f"Победил {winner_text}!")
            self.disable_buttons()
            return True
        return False
    
    def disable_buttons(self):
        for row in self.buttons:
            for btn in row: btn.config(state="disabled")
    
    def reset_game(self):
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.status.config(text="Ваш ход (❌)", fg=self.colors['x'])
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state="normal", bg=self.colors['btn'], fg="white")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = XO()
    game.run()