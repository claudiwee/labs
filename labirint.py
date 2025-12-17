import tkinter as tk
from tkinter import messagebox
import random

class Labirint:
    def __init__(self, root, cols=21, rows=15, cell=30, time=40):
        self.root = root
        self.root.title("Паук в лабиринте")
        self.root.configure(bg="#e0e0e0")  
        
        self.cols = cols if cols % 2 == 1 else cols + 1
        self.rows = rows if rows % 2 == 1 else rows + 1
        self.cell = cell
        self.time = time

        self.canvas = tk.Canvas(root, width=self.cols * self.cell,
                                height=self.rows * self.cell, bg="#f5f5f5",
                                highlightthickness=1, highlightbackground="#888")
        self.canvas.pack(pady=10)

        btn_frame = tk.Frame(root, bg="#e0e0e0")
        btn_frame.pack()
        
        tk.Button(btn_frame, text="Новая игра", command=self.reset,
                  bg="#4CAF50", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(btn_frame, text="Запустить", command=self.start,
                  bg="#2196F3", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5, pady=5)

        self.time_label = tk.Label(root, text="Время: -- с", 
                                   font=("Arial", 12, "bold"), fg="#D32F2F", bg="#e0e0e0")
        self.time_label.pack()

        self.moving = False
        self.game_over = False
        self.player_id = None
        self.reset()

    def reset(self):
        if self.moving:
            return
        
        self.game_over = False
        self.moving = False
        self.time_left = self.time
        self.time_label.config(text="Время: -- с")
        self.create()
        self.draw()
        self.draw_player()
        self.canvas.delete("trail")

    def create(self):
        self.grid = [[True for _ in range(self.cols)] for _ in range(self.rows)]

        def dfs(x, y):
            self.grid[y][x] = False
            dirs = [(0, -2), (0, 2), (-2, 0), (2, 0)]
            random.shuffle(dirs)
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 < nx < self.cols - 1 and 0 < ny < self.rows - 1 and self.grid[ny][nx]:
                    self.grid[y + dy // 2][x + dx // 2] = False
                    dfs(nx, ny)

        dfs(1, 1)

        ways = []
        for y in range(1, self.rows - 1):
            for x in range(1, self.cols - 1):
                if not self.grid[y][x]:
                    ways.append((x, y))

        self.player = random.choice(ways)
        self.exits = [(1, 5), (9, 5), (5, 7)]

    def draw(self):
        self.canvas.delete("all")
        for y in range(self.rows):
            for x in range(self.cols):
                cx, cy = x * self.cell, y * self.cell
                if self.grid[y][x]:
                    self.canvas.create_rectangle(
                        cx, cy, cx + self.cell, cy + self.cell,
                        fill="#78909C", outline="#546E7A"
                    )
        
        for (ex, ey) in self.exits:
            cx = ex * self.cell + self.cell // 2
            cy = ey * self.cell + self.cell // 2
            self.canvas.create_text(cx, cy, text="EXIT", font=("Arial", 10), fill="red")
            self.canvas.create_rectangle(
                cx - self.cell//3, cy - self.cell//3,
                cx + self.cell//3, cy + self.cell//3,
                outline="#FF5252", width=2
            )

    def draw_player(self):
        if self.player_id:
            self.canvas.delete(self.player_id)
        
        x, y = self.player
        cx = x * self.cell + self.cell // 2
        cy = y * self.cell + self.cell // 2
        r = self.cell * 0.35
        self.player_id = self.canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            fill="#303F9F", outline="white", width=2
        )

    def update_time(self):
        if not self.game_over:
            self.time_left = max(0, self.time_left - 1)
            self.time_label.config(text=f"Время: {self.time_left:02d} с")
            if self.time_left == 0:
                self.end_game(win=False)
        if not self.game_over:
            self.root.after(1000, self.update_time)

    def end_game(self, win):
        self.game_over = True
        self.moving = False
        msg = "Ура, паучок выбрался через один из выходов!" if win else "Паучок проиграл(("
        messagebox.showinfo("Победа!" if win else "Проигрыш", msg)

    def start(self):
        if self.moving or self.game_over:
            return
        self.moving = True
        self.update_time()
        self.stack = [self.player]
        self.visited = {self.player}
        self.dfs_step()

    def dfs_step(self):
        if self.game_over or not self.moving:
            return
        if not self.stack:
            return

        curr = self.stack[-1]
        self.player = curr
        self.draw_player()

        x, y = curr
        cx = x * self.cell + self.cell // 2
        cy = y * self.cell + self.cell // 2
        r = self.cell * 0.12
        self.canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            fill="#BDBDBD", outline="", tags="trail"
        )
       
        if curr in self.exits:
            self.end_game(win=True)
            return

        sosedi = []
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.cols and 0 <= ny < self.rows:
                if not self.grid[ny][nx] and (nx, ny) not in self.visited:
                    sosedi.append((nx, ny))

        if sosedi:
            next_cell = random.choice(sosedi)
            self.visited.add(next_cell)
            self.stack.append(next_cell)
        else:
            self.stack.pop()

        self.root.after(200, self.dfs_step)

if __name__ == "__main__":
    root = tk.Tk()
    game = Labirint(root, cols=21, rows=15, cell=30, time=40)
    root.mainloop()
