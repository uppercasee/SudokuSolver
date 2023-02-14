import tkinter as tk
from random import randint
from tkinter import messagebox
from isvalid import is_valid_sudoku
from generator import _gen
import time

class SudokuSolver:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku Solver")
        self.grid = [[None for _ in range(9)] for _ in range(9)]
        self._create_grid()
        self._create_menu()
        self._buttons()
        self._bindings()

    def _create_grid(self):
        # Create the grid
        self.grid = []
        for i in range(9):
            row = []
            for j in range(9):
                entry = tk.Entry(
                    width=3,
                    font=("Helvetica", 30),
                    justify="center",
                    bd=1,
                    relief=tk.RIDGE,
                )
                entry.grid(row=i, column=j, padx=1, pady=1)
                row.append(entry)
                entry.config(bg="#bbdefd")
                entry.config(fg="#000000")
                entry.bind(
                    "<KeyRelease>", lambda event: event.widget.config(
                        bg="white")
                )
                entry.bind(
                    "<FocusOut>",
                    lambda event: event.widget.config(bg="#bbdefd")
                    if event.widget.get() == ""
                    else event.widget.config(bg="white"),
                )
            self.grid.append(row)

    def _create_menu(self):
        # Create a menu
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        # Create a file menu
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Exit(E)", command=self.master.destroy)

        # Create a puzzle menu
        self.puzzle_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Puzzle", menu=self.puzzle_menu)
        self.puzzle_menu.add_command(label="Solve(S)", command=self.solve)
        self.puzzle_menu.add_command(label="Generate(G)", command=lambda: self.generate("Easy"))
        self.puzzle_menu.add_command(label="Clear(C)", command=self.clear)

        # Create a help menu
        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self._about)

    def _about(self):
        messagebox.showinfo(
            "About",
            "Sudoku Solver\n"
        )
        

    def _buttons(self):
        # Create "Solve" button
        self.solve_button = tk.Button(
            self.master, text="Solve", command=self.solve, bg="#4CAF50", fg="white", width=13
        )
        self.solve_button.grid(row=9, column=0, columnspan=2)

        # create generate button
        self.generate_button = tk.Button(
            self.master,
            text="Generate",
            command=lambda: self.generate("Easy"),
            bg="#E91E63",
            fg="white",
            width=13
        )
        self.generate_button.grid(row=9, column=2, columnspan=2)

        # create dofficulty button with background color light green
        self.difficulty_button = tk.Menubutton(
            self.master, text="Difficulty", relief=tk.RAISED, bg="#8BC34A", fg="white", width=15
        )
        self.difficulty_button.grid(row=9, column=5, columnspan=2)
        self.difficulty_menu = tk.Menu(self.difficulty_button, tearoff=0)
        self.difficulty_menu.add_command(
            label="Easy", command=lambda: self.generate("Easy")
        )
        self.difficulty_menu.add_command(
            label="Medium", command=lambda: self.generate("Medium")
        )
        self.difficulty_menu.add_command(
            label="Hard", command=lambda: self.generate("Hard")
        )
        self.difficulty_button["menu"] = self.difficulty_menu

        # create clear button with background color RED
        self.clear_button = tk.Button(
            self.master, text="Clear", command=self.clear, bg="#F44336", fg="white", width=12
        )
        self.clear_button.grid(row=9, column=7, columnspan=2)

    def _bindings(self):
        # type to change difficulty level
        self.master.bind("1", lambda event: self.generate("Easy"))
        self.master.bind("2", lambda event: self.generate("Medium"))
        self.master.bind("3", lambda event: self.generate("Hard"))

        # Type S to solve the puzzle
        self.master.bind("s", lambda event: self.solve())
        self.master.bind("S", lambda event: self.solve())

        # Type G to generate a puzzle
        self.master.bind("g", lambda event: self.generate("Easy"))
        self.master.bind("G", lambda event: self.generate("Easy"))

        # Type C to clear the puzzle
        self.master.bind("c", lambda event: self.clear())
        self.master.bind("C", lambda event: self.clear())

        # Type E to exit the program
        self.master.bind("e", lambda event: self.master.destroy())
        self.master.bind("E", lambda event: self.master.destroy())

    def solve(self):
        puzzle = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                try:
                    puzzle[i][j] = int(self.grid[i][j].get())
                except ValueError:
                    pass
        # print(puzzle)
        if is_valid_sudoku(puzzle):
            if self.backtrack(puzzle):
                for i in range(9):
                    for j in range(9):
                        self.grid[i][j].delete(0, tk.END)
                        self.grid[i][j].insert(0, puzzle[i][j])
                        # sleep for 0.05 seconds
                        time.sleep(randint(1, 10) / 100)
                        self.master.update()
            else:
                messagebox.showerror("Error", "No solution exists")
        else:
            messagebox.showerror("Error", "Invalid Sudoku")

    def backtrack(self, puzzle):
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] == 0:
                    for num in range(1, 10):
                        if is_valid_sudoku(puzzle):
                            # if self.is_valid(puzzle, i, j, num):
                            puzzle[i][j] = num
                            if self.backtrack(puzzle):
                                return True
                            puzzle[i][j] = 0
                    return False
        return True

    def generate(self, difficulty):
        board = _gen()
        for i in range(9):
            for j in range(9):
                self.grid[i][j].delete(0, tk.END)
                self.grid[i][j].insert(0, board[i][j])
                self.grid[i][j].config(bg="white")
        if difficulty == "Easy":
            for i in range(9):
                for j in range(9):
                    if randint(0, 1) == 1:
                        self.grid[i][j].delete(0, tk.END)
                        self.grid[i][j].config(bg="#bbdefd")
        elif difficulty == "Medium":
            for i in range(9):
                for j in range(9):
                    if randint(0, 2) == 1:
                        self.grid[i][j].delete(0, tk.END)
                        self.grid[i][j].config(bg="#bbdefd")
        elif difficulty == "Hard":
            for i in range(9):
                for j in range(9):
                    if randint(0, 3) == 1:
                        self.grid[i][j].delete(0, tk.END)
                        self.grid[i][j].config(bg="#bbdefd")

    def clear(self):
        for i in range(9):
            for j in range(9):
                self.grid[i][j].delete(0, tk.END)
                self.grid[i][j].config(bg="#bbdefb")


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolver(root)
    root.mainloop()
