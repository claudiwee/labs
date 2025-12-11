import tkinter as tk
from tkinter import messagebox
import random

class SeaBattle:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Морской бой")
        self.root.configure(bg="#2C3E50")
        self.root.geometry("800x600")

        self.size = 10
        self.ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        self.player_board = [[0] * self.size for _ in range(self.size)]
        self.ai_board = [[0] * self.size for _ in range(self.size)]
        self.player_shots = [[0] * self.size for _ in range(self.size)]
        self.ai_shots = [[0] * self.size for _ in range(self.size)]

        self.game_phase = 'placing'
        self.current_ship_idx = 0
        self.orientation = 'horizontal'
        self.my_hits = 0
        self.ai_hits = 0

        self.create_ui()

    def create_ui(self):
        main_frame = tk.Frame(self.root, bg="#2C3E50")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

       
        tk.Label(main_frame, text="МОЁ ПОЛЕ", font=("Segoe UI", 14, "bold"), fg="#3498DB", bg="#2C3E50").grid(row=0, column=0, padx=(0, 30), sticky="w")
        tk.Label(main_frame, text="ПОЛЕ ПРОТИВНИКА", font=("Segoe UI", 14, "bold"), fg="#E74C3C", bg="#2C3E50").grid(row=0, column=1, sticky="w")

        
        player_frame = tk.Frame(main_frame, bg="#34495E")
        ai_frame = tk.Frame(main_frame, bg="#34495E")
        player_frame.grid(row=1, column=0, padx=(0, 30), pady=10)
        ai_frame.grid(row=1, column=1, pady=10)

        
        self.player_buttons = []
        self.ai_buttons = []

        for i in range(self.size):
            player_row = []
            ai_row = []
            for j in range(self.size):
        
                btn_p = tk.Button(player_frame, width=3, height=1, font=("Segoe UI", 10), bg="#ECF0F1", fg="#2C3E50", relief="flat", bd=1)
                btn_p.grid(row=i, column=j, padx=1, pady=1)
                btn_p.config(command=lambda r=i, c=j: self.on_player_click(r, c))
                player_row.append(btn_p)

                btn_a = tk.Button(ai_frame, width=3, height=1, font=("Segoe UI", 10), bg="#BDC3C7", fg="#2C3E50", relief="flat", bd=1, state="disabled")
                btn_a.grid(row=i, column=j, padx=1, pady=1)
                btn_a.config(command=lambda r=i, c=j: self.on_ai_click(r, c))
                ai_row.append(btn_a)

            self.player_buttons.append(player_row)
            self.ai_buttons.append(ai_row)

        
        control_frame = tk.Frame(main_frame, bg="#2C3E50")
        control_frame.grid(row=2, column=0, columnspan=2, pady=20)

        self.rotate_btn = tk.Button(control_frame, text="🔄 Повернуть", command=self.rotate_ship, font=("Segoe UI", 11), bg="#3498DB", fg="white", relief="flat", padx=15, pady=5)
        self.rotate_btn.pack(side="left", padx=5)

        self.start_btn = tk.Button(control_frame, text="▶️ Начать битву", command=self.start_battle, font=("Segoe UI", 11), bg="#2ECC71", fg="white", relief="flat", padx=15, pady=5, state="disabled")
        self.start_btn.pack(side="left", padx=5)

        # Статус
        self.status_var = tk.StringVar()
        self.status_var.set(f"Расставьте {self.ships[self.current_ship_idx]}-палубный корабль ({'Горизонтально'})")
        status_label = tk.Label(main_frame, textvariable=self.status_var, font=("Segoe UI", 11), bg="#2C3E50", fg="white")
        status_label.grid(row=3, column=0, columnspan=2, pady=10)

        self.update_display()

    def get_ship_cells(self, r, c, size, orient):
        cells = []
        if orient == 'horizontal':
            for i in range(size):
                if c + i >= self.size: return []
                cells.append((r, c + i))
        else:
            for i in range(size):
                if r + i >= self.size: return []
                cells.append((r + i, c))
        return cells

    def is_valid_placement(self, board, cells):
        for r, c in cells:
            if board[r][c] != 0: return False
        for r, c in cells:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.size and 0 <= nc < self.size:
                        if board[nr][nc] != 0 and (nr, nc) not in cells:
                            return False
        return True

    def on_player_click(self, r, c):
        if self.game_phase != 'placing': return
        if self.current_ship_idx >= len(self.ships): return  # Защита от лишних кликов
        
        size = self.ships[self.current_ship_idx]
        cells = self.get_ship_cells(r, c, size, self.orientation)
        if not cells or not self.is_valid_placement(self.player_board, cells): return

        for tr, tc in cells:
            self.player_board[tr][tc] = 1

        if self.current_ship_idx < len(self.ships) - 1:
            self.current_ship_idx += 1
            self.status_var.set(f"Расставьте {self.ships[self.current_ship_idx]}-палубный корабль ({'Горизонтально' if self.orientation == 'horizontal' else 'Вертикально'})")
        else:
            self.status_var.set("Все корабли расставлены! Нажмите 'Начать битву'")
            self.start_btn.config(state="normal")
            # ОСНОВНОЕ ИСПРАВЛЕНИЕ: блокируем кнопки после расстановки всех кораблей
            for row in self.player_buttons:
                for btn in row:
                    btn.config(state="disabled")

        self.update_display()

    def rotate_ship(self):
        if self.current_ship_idx >= len(self.ships): return  # Защита от поворота после расстановки
        self.orientation = 'vertical' if self.orientation == 'horizontal' else 'horizontal'
        if self.current_ship_idx < len(self.ships):
            self.status_var.set(f"Расставьте {self.ships[self.current_ship_idx]}-палубный корабль ({'Вертикально' if self.orientation == 'vertical' else 'Горизонтально'})")

    def start_battle(self):
        if self.current_ship_idx < len(self.ships) - 1:
            messagebox.showwarning("Ошибка", "Расставьте все корабли!")
            return

        self.ai_board = self.generate_ai_board()
        if self.ai_board is None: return

        self.game_phase = 'playing'
        self.status_var.set("Ваш ход! Атакуйте вражеское поле.")
        self.rotate_btn.config(state="disabled")
        self.start_btn.config(state="disabled")

        # Разблокируем кнопки ИИ для игры
        for row in self.ai_buttons:
            for btn in row:
                btn.config(state="normal", bg="#ECF0F1")

        self.update_display()

    def generate_ai_board(self):
        board = [[0] * self.size for _ in range(self.size)]
        ships = self.ships[:]
        for size in ships:
            placed = False
            attempts = 0
            while not placed and attempts < 1000:
                orient = random.choice(['horizontal', 'vertical'])
                r = random.randint(0, self.size - 1)
                c = random.randint(0, self.size - 1)
                cells = self.get_ship_cells(r, c, size, orient)
                if cells and self.is_valid_placement(board, cells):
                    for tr, tc in cells:
                        board[tr][tc] = 1
                    placed = True
                attempts += 1
            if not placed:
                messagebox.showerror("Ошибка", "Не удалось расставить корабли ИИ")
                return None
        return board

    def on_ai_click(self, r, c):
        if self.game_phase != 'playing' or self.player_shots[r][c] != 0: return

        hit = (self.ai_board[r][c] == 1)
        self.player_shots[r][c] = 2 if hit else 3

        if hit:
            self.my_hits += 1
            if self.is_ship_destroyed(r, c, self.ai_board, self.player_shots):
                self.mark_destroyed_ship(r, c, self.player_shots, self.ai_buttons)
                if self.my_hits == sum(self.ships):
                    messagebox.showinfo("Победа!", "Вы выиграли!")
                    self.root.destroy()
                    return
                else:
                    self.status_var.set("🚢 Корабль уничтожен! Ваш ход.")
            else:
                self.status_var.set("🎯 Попадание! Ваш ход.")
        else:
            self.status_var.set("💧 Мимо! Ход ИИ...")
            self.root.update()
            self.root.after(500, self.ai_turn)

        self.update_display()

    def ai_turn(self):
        available = [(i, j) for i in range(self.size) for j in range(self.size) if self.ai_shots[i][j] == 0]
        if not available:
            return
        r, c = random.choice(available)

        hit = (self.player_board[r][c] == 1)
        self.ai_shots[r][c] = 2 if hit else 3

        if hit:
            self.ai_hits += 1
            if self.is_ship_destroyed(r, c, self.player_board, self.ai_shots):
                self.mark_destroyed_ship(r, c, self.ai_shots, self.player_buttons)
                if self.ai_hits == sum(self.ships):
                    messagebox.showinfo("Поражение", "ИИ выиграл!")
                    self.root.destroy()
                    return
                else:
                    self.status_var.set("🚢 ИИ уничтожил ваш корабль! Его ход...")
                    self.root.after(1000, self.ai_turn)
                    return
            else:
                self.status_var.set("🎯 ИИ попал! Его ход...")
                self.root.after(1000, self.ai_turn)
                return
        else:
            self.status_var.set("💧 ИИ промахнулся! Ваш ход.")

        self.update_display()

    def is_ship_destroyed(self, r, c, board, shots_board):
        # Находим все клетки корабля
        visited = set()
        stack = [(r, c)]
        ship_cells = []
        
        while stack:
            x, y = stack.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            
            if board[x][y] == 1:
                ship_cells.append((x, y))
                # Проверяем соседние клетки
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dr, y + dc
                    if 0 <= nx < self.size and 0 <= ny < self.size and (nx, ny) not in visited:
                        stack.append((nx, ny))
        
        # Проверяем, все ли клетки корабля подбиты
        return all(shots_board[x][y] == 2 for x, y in ship_cells)

    def mark_destroyed_ship(self, r, c, shots_board, buttons):
        # Находим все клетки корабля
        visited = set()
        stack = [(r, c)]
        ship_cells = []
        
        while stack:
            x, y = stack.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            
            if shots_board[x][y] == 2:  # Только подбитые клетки
                ship_cells.append((x, y))
                # Проверяем соседние клетки
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dr, y + dc
                    if 0 <= nx < self.size and 0 <= ny < self.size and (nx, ny) not in visited:
                        stack.append((nx, ny))
        
        # Отмечаем все клетки вокруг корабля как промахи
        for x, y in ship_cells:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nx, ny = x + dr, y + dc
                    if 0 <= nx < self.size and 0 <= ny < self.size and shots_board[nx][ny] == 0:
                        shots_board[nx][ny] = 3

        self.update_display()

    def update_display(self):
        for i in range(self.size):
            for j in range(self.size):
                btn = self.player_buttons[i][j]
                val = self.player_board[i][j]
                shot = self.ai_shots[i][j]

                if self.game_phase == 'placing':
                    if val == 1:
                        btn.config(text="🚢", bg="#3498DB", fg="white", relief="raised")
                    else:
                        btn.config(text="", bg="#ECF0F1", fg="#2C3E50", relief="raised")
                else:  # playing
                    if shot == 2:
                        btn.config(text="💥", bg="#E74C3C", fg="white", relief="sunken")
                    elif shot == 3:
                        btn.config(text="💧", bg="#BDC3C7", fg="#2C3E50", relief="sunken")
                    elif val == 1:
                        btn.config(text="🚢", bg="#3498DB", fg="white", relief="raised")
                    else:
                        btn.config(text="", bg="#ECF0F1", fg="#2C3E50", relief="raised")

        for i in range(self.size):
            for j in range(self.size):
                btn = self.ai_buttons[i][j]
                shot = self.player_shots[i][j]

                if shot == 2:
                    btn.config(text="💥", bg="#E74C3C", fg="white", relief="sunken")
                elif shot == 3:
                    btn.config(text="💧", bg="#BDC3C7", fg="#2C3E50", relief="sunken")
                else:
                    btn.config(text="", bg="#ECF0F1", fg="#2C3E50", relief="raised")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = SeaBattle()
    game.run()