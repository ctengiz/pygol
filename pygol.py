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
                color = self.random_color()

                x1 = cl * self.size
                y1 = rw * self.size
                x2 = x1 + self.size
                y2 = y1 + self.size

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

    def tick(self):

        x1 = 10
        y1 = 10
        x2 = x1 + self.size
        y2 = y1 + self.size

        color = self.random_color()
        print(color)

        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

        self.root.after(25, self.tick)

Gol(50, 50, 10)

