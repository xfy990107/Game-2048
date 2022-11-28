import tkinter as tk
import Colors as c
import random

class Game2048(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title('2048')

        self.main_grid= tk.Frame(
            self, bg=c.grid_color, bd=3, width=600, height=600
        )
        self.main_grid.grid(pady=(0, 0))
        self.make_GUI()
        self.start_game()

        self.master.bind("<a>", self.left)
        self.master.bind("<A>", self.left)
        self.master.bind("<d>", self.right)
        self.master.bind("<D>", self.right)
        self.master.bind("<w>", self.up)
        self.master.bind("<W>", self.up)
        self.master.bind("<s>", self.down)
        self.master.bind("<S>", self.down)

        self.mainloop()

    def make_GUI(self):
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame= tk.Frame(
                    self.main_grid,
                    bg=c.empty_cell_color,
                    width=150,
                    height=150
                )
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(self.main_grid, bg=c.empty_cell_color)
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)

    def start_game(self):
        self.matrix = [[0] * 4 for _ in range(4)]
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]['frame'].configure(bg=c.cell_colors[2])
        self.cells[row][col]['number'].configure(
            bg=c.cell_colors[2],
            fg=c.cell_number_colors[2],
            font=c.cell_number_fonts[2],
            text='2'
        )
        while self.matrix[row][col] != 0:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]['frame'].configure(bg=c.cell_colors[2])
        self.cells[row][col]['number'].configure(
                bg=c.cell_colors[2],
                fg=c.cell_number_colors[2],
                font=c.cell_number_fonts[2],
                text='2'
        )

    def stack(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = new_matrix

    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0

    def reverse(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3 - j])
        self.matrix = new_matrix

    def transpose(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix

    def add_new_tile(self):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        while self.matrix[row][col] != 0:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = 2

    def update_GUI(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=c.empty_cell_color)
                    self.cells[i][j]["number"].configure(bg=c.empty_cell_color, text="")
                else:
                    self.cells[i][j]["frame"].configure(bg=c.cell_colors[cell_value])
                    self.cells[i][j]["number"].configure(
                        bg=c.cell_colors[cell_value],
                        fg=c.cell_number_colors[cell_value],
                        font=c.cell_number_fonts[cell_value],
                        text=str(cell_value))
        self.update_idletasks()

    def left(self, event):
        self.stack()
        self.combine()
        self.stack()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def right(self, event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def up(self, event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def down(self, event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def horizontal_move_exists(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return True
        return False

    def vertical_move_exists(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True
        return False

    # def again_clicked(self):
    #     self.main_grid.destroy()
    #     Game2048()
    #
    # def end_game(self):
    #     quit()

    def game_over(self):
        if any(2048 in row for row in self.matrix):
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text="You win!",
                bg=c.winner_bg,
                fg=c.game_over_font_color,
                font=c.game_over_font
            ).pack()
            restart_or_end_frame = tk.Frame(self.main_grid, borderwidth=2)
            restart_or_end_frame.place(relx=0.5, rely=0.5, anchor='center')
            tk.Label(
                restart_or_end_frame,
                text="Do you want to play again?",
                bg=c.winner_bg,
                fg=c.game_over_font_color,
                font=c.again_font
            ).pack()
            # again_button = tk.Button(self.main_grid, text='Yes.', command=self.again_clicked()).pack()
            # again_button.grid(relx=0.3, rely=0.7, anchor='center')
            # quit_button = tk.Button(self.main_grid, text='No!', command=self.main_grid.destroy).pack()
            # quit_button.grid(relx=0.7, rely=0.7, anchor='center')
        elif not any(0 in row for row in self.matrix) and not self.horizontal_move_exists() and not self.vertical_move_exists():
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text="Game over!",
                bg=c.loser_bg,
                fg=c.game_over_font_color,
                font=c.game_over_font
            ).pack()
            restart_or_end_frame = tk.Frame(self.main_grid, borderwidth=2)
            restart_or_end_frame.place(relx=0.5, rely=0.5, anchor='center')
            tk.Label(
                restart_or_end_frame,
                text="Do you want to play again?",
                bg=c.winner_bg,
                fg=c.game_over_font_color,
                font=c.again_font
            ).pack()
            # again_button = tk.Button(self.main_grid, text='Yes.', command=self.again_clicked()).pack()
            # again_button.grid(relx=0.3, rely=0.7, anchor='center')
            # quit_button = tk.Button(self.main_grid, text='No!', command=self.main_grid.destroy).pack()
            # quit_button.grid(relx=0.7, rely=0.7, anchor='center')

# def main():
#     Game2048()
#
# if __name__ == "__main__":
#     main()

Game2048()

