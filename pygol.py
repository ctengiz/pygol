from tkinter import *
import random
from copy import deepcopy


class Gol:
    def __init__(self, rows=30, cols=60, size=10, tick_delay=100, seed_ratio=30):
        self.is_active = False
        self.in_tick = False
        self.grid = []
        self.tick_count = 0
        self.dead = 0
        self.alive = 0
        self.tick_delay = tick_delay #in ms
        self.seed_ratio = seed_ratio

        self.root = Tk()
        self.cols = cols
        self.rows = rows
        self.size = size

        self.canvas = Canvas(self.root)
        self.canvas.grid(row=0, columnspan=15)
        self.canvas.bind("<Button-1>", self.canvas_click)

        _rw = 1
        _cl = 0
        self.lbl_edt_rows = Label(self.root, text="Rows")
        self.lbl_edt_rows.grid(row=_rw, column=_cl, sticky=E)
        _cl += 1
        self.edt_rows = Entry(self.root, width=4)
        self.edt_rows.insert(0, str(self.rows))
        self.edt_rows.grid(row=_rw, column=_cl, sticky=W)
        _cl += 1
        self.lbl_edt_size = Label(self.root, text="Size")
        self.lbl_edt_size.grid(row=_rw, column=_cl, sticky=E)
        _cl += 1
        self.edt_size = Entry(self.root, width=4)
        self.edt_size.insert(0, str(self.size))
        self.edt_size.grid(row=_rw, column=_cl, sticky=W)
        _cl += 1
        self.lbl_edt_seed_ratio = Label(self.root, text="Seed Ratio")
        self.lbl_edt_seed_ratio.grid(row=_rw, column=_cl, sticky=E)
        _cl += 1
        self.edt_seed_ratio = Entry(self.root, width=4)
        self.edt_seed_ratio.insert(0, str(self.seed_ratio))
        self.edt_seed_ratio.grid(row=_rw, column=_cl, sticky=W)
        _cl += 1
        self.btn_seed = Button(self.root, text="Seed", command=self.init_grid)
        self.btn_seed.grid(row=_rw, column=_cl)
        _cl += 1
        self.btn_clear = Button(self.root, text="Clear", command=self.clear_grid)
        self.btn_clear.grid(row=_rw, column=_cl)

        _rw += 1
        _cl = 0
        self.lbl_edt_cols = Label(self.root, text="Cols")
        self.lbl_edt_cols.grid(row=_rw, column=_cl, sticky=E)
        _cl += 1
        self.edt_cols = Entry(self.root, width=4)
        self.edt_cols.insert(0, str(self.cols))
        self.edt_cols.grid(row=_rw, column=_cl, sticky=W)
        _cl += 1
        self.lbl_edt_delay = Label(self.root, text="Delay")
        self.lbl_edt_delay.grid(row=_rw, column=_cl, sticky=E)
        _cl += 1
        self.edt_delay = Entry(self.root, width=4)
        self.edt_delay.insert(0, str(self.tick_delay))
        self.edt_delay.grid(row=_rw, column=_cl, sticky=W)
        _cl += 3
        self.btn_start_stop = Button(self.root, text="Start", command=self.start_stop)
        self.btn_start_stop.grid(row=_rw, column=_cl)
        _cl += 1
        self.btn_tick = Button(self.root, text=">>", command=self.tick)
        self.btn_tick.grid(row=_rw, column=_cl)

        _rw += 1
        _cl = 0
        self.lbl_tickno = Label(self.root, text="Round:0")
        self.lbl_tickno.grid(row=_rw, column=_cl)
        _cl += 1
        self.lbl_alive = Label(self.root, text="Alive:0")
        self.lbl_alive.grid(row=_rw, column=_cl)
        _cl += 1
        self.lbl_dead = Label(self.root, text="Dead:0")
        self.lbl_dead.grid(row=_rw, column=_cl)

        self.alive_cell_color = "#00FF00"
        self.dead_cell_color = "#FFFFFF" #"#e5e5e5"
        self.blank_cell_color = "#FFFFFF"
        self.grid_color = "#808080"

        #self.init_grid()
        self.clear_grid()

        self.root.mainloop()

    def canvas_click(self, e):
        cl = int(e.x / self.size) + (e.x % self.size > 0) - 1
        rw = int(e.y / self.size) + (e.y % self.size > 0) - 1
        if self.is_active is False:
            if self.grid[rw][cl]:
                self.grid[rw][cl] = 0
                color = self.dead_cell_color
                self.alive -= 1
                self.dead += 1
            else:
                self.grid[rw][cl] = 1
                color = self.alive_cell_color
                self.alive += 1
                self.dead -= 1

            self.put_rect(rw, cl, color)
            self.update_labels()

            if self.alive:
                self.btn_start_stop.config(state=NORMAL)
                self.btn_tick.config(state=NORMAL)
            else:
                self.btn_start_stop.config(state=DISABLED)
                self.btn_tick.config(state=DISABLED)

    def put_rect(self, rw, cl, color):
        x1 = cl * self.size
        y1 = rw * self.size
        x2 = x1 + self.size
        y2 = y1 + self.size

        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=self.grid_color, tags="cell")

    def clear_grid(self):
        self.cols = int(self.edt_cols.get())
        self.rows = int(self.edt_rows.get())
        self.size = int(self.edt_size.get())

        self.canvas.config(width=self.cols*self.size, height=self.rows*self.size)

        self.btn_start_stop.config(state=DISABLED)
        self.btn_tick.config(state=DISABLED)

        self.grid = [[0 for x in range(self.cols)] for y in range(self.rows)]
        self.tick_count = 0
        self.dead = 0
        self.alive = 0

        self.canvas.delete("all")

        for rw in range(self.rows):
            for cl in range(self.cols):
                """
                if rw == 1 and (cl == 1 or cl == 2 or cl == 3):
                    self.grid[rw][cl] = 1
                    self.put_rect(rw, cl, self.alive_cell_color)
                    self.dead += 1
                    self.btn_start_stop.config(state=NORMAL)
                    self.btn_tick.config(state=NORMAL)
                else:
                """
                self.grid[rw][cl] = 0
                self.put_rect(rw, cl, self.dead_cell_color)
                self.dead += 1

        self.update_labels()

    def init_grid(self):
        self.clear_grid()

        for rw in range(self.rows):
            for cl in range(self.cols):

                is_alive = random.randint(0, 1)
                if is_alive == 1:
                    self.grid[rw][cl] = is_alive
                    self.alive += 1
                    self.dead -= 1
                    color = self.alive_cell_color
                else:
                    self.grid[rw][cl] = 0 #empty cell
                    color = self.dead_cell_color

                self.put_rect(rw, cl, color)

        self.update_labels()

        self.btn_start_stop.config(state=NORMAL)
        self.btn_tick.config(state=NORMAL)

    def start_stop(self):
        if self.is_active:
            self.is_active = False
            self.btn_start_stop.config(text='Start')

            self.btn_tick.config(state=NORMAL)
            self.btn_seed.config(state=NORMAL)
            self.btn_clear.config(state=NORMAL)
        else:
            self.tick_delay = int(self.edt_delay.get())
            self.is_active = True
            self.root.after(self.tick_delay, self.tick)
            self.btn_start_stop.config(text='Stop')

            self.btn_tick.config(state=DISABLED)
            self.btn_seed.config(state=DISABLED)
            self.btn_clear.config(state=DISABLED)

    def update_labels(self):
        self.lbl_tickno.config(text="Round: %d" %(self.tick_count))
        self.lbl_alive.config(text="Alive: %d" %(self.alive))
        self.lbl_dead.config(text="Dead: %d" %(self.dead))

    def tick(self):
        if self.in_tick:
            return

        self.in_tick = True

        self.alive = 0
        self.dead = 0

        self.canvas.delete("all")

        #because slicing does not copy if a list is contained in a list !
        old_grid = deepcopy(self.grid)

        for rw in range(self.rows):
            for cl in range(self.cols):
                n_alive = 0

                for x in range(-1, 2):
                    for y in range(-1, 2):
                        nx = cl + x
                        ny = rw + y

                        if (nx >= 0) and (ny >= 0) and (nx < self.cols) and (ny < self.rows) and ((x != 0) or (y != 0)):
                            if old_grid[ny][nx] == 1:
                                n_alive += 1

                if self.grid[rw][cl] == 1:
                    #if cell is alive !
                    if n_alive < 2:
                        self.grid[rw][cl] = 0
                    if n_alive > 3:
                        self.grid[rw][cl] = 0

                if self.grid[rw][cl] == 0:
                    if n_alive == 3:
                        self.grid[rw][cl] = 1

                if self.grid[rw][cl]:
                    color = self.alive_cell_color
                    self.alive += 1
                else:
                    color = self.dead_cell_color
                    self.dead += 1

                self.put_rect(rw, cl, color)

        self.in_tick = False

        self.tick_count += 1
        self.update_labels()

        if self.is_active:
            self.root.after(self.tick_delay, self.tick)

Gol()