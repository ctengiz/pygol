from tkinter import *
import random


class Gol:
    def __init__(self, cols, rows, size):
        self.root = Tk()
        self.cols = cols
        self.rows = rows
        self.size = size

        self.canvas = Canvas(self.root, width=rows*size, height=cols*size)

        self.alive_cell = "#00FF00"
        self.dead_cell = "#808080"
        self.blank_cell = "#FFFFFF"

        self.grid = [[0 for x in range(cols)] for y in range(rows)]

        self.init_grid()

        self.canvas.pack(fill=BOTH, expand=1)

        self.root.after(0, self.tick)
        self.root.mainloop()

    def random_color(self):
        rc = [random.randint(0, 255) for i in range(0, 3)]
        return '#%02x%02x%02x' % tuple(rc)

    def init_grid(self):
        for cl in range(self.cols):
            for rw in range(self.rows):

                is_alive = random.randint(0, 1)
                if is_alive == 1:
                    self.grid[cl][rw] = is_alive
                else:
                    self.grid[cl][rw] = -1 #empty cell

                if is_alive:
                    color = self.alive_cell

                    x1 = cl * self.size
                    y1 = rw * self.size
                    x2 = x1 + self.size
                    y2 = y1 + self.size

                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

    def tick(self):
        for cl in range(self.cols):
            for rw in range(self.rows):
                n_alive = 0

                for x in range(-1, 2):
                    for y in range(-1, 2):
                        nx = cl + x
                        ny = rw + y
                        if (nx >= 0) \
                                and (ny >= 0) \
                                and (nx < self.rows) \
                                and (ny < self.cols) \
                                and ((nx != cl) or (ny != rw)):
                            if self.grid[nx][ny] == 1:
                                n_alive += 1

                if self.grid[cl][rw] == 1:
                    #if cell is alive !
                    if n_alive < 2:
                        self.grid[cl][rw] = 0
                    if n_alive > 3:
                        self.grid[cl][rw] = 0

                if self.grid[cl][rw] == 0:
                #else:
                    if n_alive == 3:
                        self.grid[cl][rw] = 1

                if self.grid[cl][rw] == 1:
                    color = self.alive_cell

                if self.grid[cl][rw] == 0:
                    color = self.dead_cell

                if self.grid[cl][rw] == -1:
                    color = self.blank_cell

                x1 = cl * self.size
                y1 = rw * self.size
                x2 = x1 + self.size
                y2 = y1 + self.size

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

        self.root.after(25, self.tick)



Gol(50, 50, 10)

