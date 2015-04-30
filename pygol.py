from tkinter import *
import random

class Gol:
    def __init__(self, cols, rows, size):
        self.is_active = False
        self.in_tick = False

        self.root = Tk()
        self.cols = cols
        self.rows = rows
        self.size = size

        self.canvas = Canvas(self.root, width=rows*size, height=cols*size)
        self.btn_start = Button(self.root, text="Start", command=self.start)
        self.btn_stop = Button(self.root, text="Stop", command=self.stop)
        self.btn_tick = Button(self.root, text=">>", command=self.tick)
        self.btn_reset = Button(self.root, text="Reset", command=self.init_grid)

        self.lbl_tickno = Label(self.root, text="Round:0")
        self.lbl_alive = Label(self.root, text="Alive:0")
        self.lbl_dead = Label(self.root, text="Dead:0")
        self.lbl_empty = Label(self.root, text="Empty:0")

        self.alive_cell_color = "#00FF00"
        self.dead_cell_color = "#e5e5e5"
        self.blank_cell_color = "#FFFFFF"
        self.grid_color = "#808080"

        self.init_grid()

        self.canvas.pack(fill=BOTH, expand=1)
        self.btn_start.pack(side=LEFT)
        self.btn_stop.pack(side=LEFT)
        self.btn_tick.pack(side=LEFT)
        self.btn_reset.pack(side=RIGHT)

        self.lbl_tickno.pack()
        self.lbl_dead.pack()
        self.lbl_alive.pack()
        self.lbl_empty.pack()


        self.root.mainloop()

    def random_color(self):
        rc = [random.randint(0, 255) for i in range(0, 3)]
        return '#%02x%02x%02x' % tuple(rc)

    def init_grid(self):
        self.grid = [[0 for x in range(self.cols)] for y in range(self.rows)]
        self.tick_count = 0
        self.dead = 0
        self.alive = 0
        self.blank = 0

        for cl in range(self.cols):
            for rw in range(self.rows):

                is_alive = random.randint(0, 1)
                if is_alive == 1:
                    self.grid[cl][rw] = is_alive
                else:
                    self.grid[cl][rw] = -1 #empty cell

                if is_alive:
                    color = self.alive_cell_color

                    x1 = cl * self.size
                    y1 = rw * self.size
                    x2 = x1 + self.size
                    y2 = y1 + self.size

                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=self.grid_color)
                else:
                    color = self.blank_cell_color

                    x1 = cl * self.size
                    y1 = rw * self.size
                    x2 = x1 + self.size
                    y2 = y1 + self.size
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=self.grid_color)

        self.update_labels()

    def start(self):
        self.is_active = True
        self.btn_tick.config(state=DISABLED)
        self.root.after(0, self.tick)

    def stop(self):
        self.is_active = False
        self.btn_tick.config(state=NORMAL)

    def update_labels(self):
        self.lbl_tickno.config(text="Round:%d" %(self.tick_count))
        self.lbl_empty.config(text="Empty:%d" %(self.blank))

    def tick(self):
        if self.in_tick:
            return

        self.in_tick = True

        for cl in range(self.cols):
            for rw in range(self.rows):
                n_alive = 0

                for x in range(-1, 2):
                    for y in range(-1, 2):
                        nx = cl + x
                        ny = rw + y
                        if (nx >= 0) and (ny >= 0) and (nx < self.rows) and (ny < self.cols) and ((x != 0) or (y != 0)):
                            if self.grid[nx][ny] == 1:
                                n_alive += 1

                if self.grid[cl][rw] == 1:
                    #if cell is alive !
                    if n_alive < 2:
                        self.grid[cl][rw] = 0
                    if n_alive > 3:
                        self.grid[cl][rw] = 0

                if self.grid[cl][rw] <= 0:
                #else:
                    if n_alive == 3:
                        self.grid[cl][rw] = 1

                if self.grid[cl][rw] == 1:
                    color = self.alive_cell_color

                if self.grid[cl][rw] == 0:
                    color = self.dead_cell_color

                if self.grid[cl][rw] == -1:
                    color = self.blank_cell_color

                x1 = cl * self.size
                y1 = rw * self.size
                x2 = x1 + self.size
                y2 = y1 + self.size

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=self.grid_color)

        self.in_tick = False

        self.tick_count += 1
        self.lbl_tickno.config(text="Round:%d" %(self.tick_count))

        if self.is_active:
            self.root.after(10, self.tick)



Gol(30, 30, 10)

