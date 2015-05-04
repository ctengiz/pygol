from tkinter import *
import random

class Gol:
    def __init__(self, cols=30, rows=30, size=10, tick_delay=10):
        self.is_active = False
        self.in_tick = False
        self.grid = []
        self.tick_count = 0
        self.dead = 0
        self.alive = 0
        self.tick_delay = tick_delay #in ms

        self.root = Tk()
        self.cols = cols
        self.rows = rows
        self.size = size

        self.canvas = Canvas(self.root)
        self.canvas.grid(row=0, columnspan=15)

        _crr = 1
        self.lbl_edt_rows = Label(self.root, text="Rows", anchor=W)
        self.lbl_edt_rows.grid(row=_crr, column=0)
        self.edt_rows = Entry(self.root, width=4)
        self.edt_rows.insert(0, str(self.rows))
        self.edt_rows.grid(row=_crr, column=1)

        self.lbl_edt_cols = Label(self.root, text="Cols", anchor=W)
        self.lbl_edt_cols.grid(row=_crr, column=2)
        self.edt_cols = Entry(self.root, width=4)
        self.edt_cols.insert(0, str(self.cols))
        self.edt_cols.grid(row=_crr, column=3)

        self.btn_seed = Button(self.root, text="Seed", command=self.init_grid)
        self.btn_seed.grid(row=_crr, column=4)

        self.btn_clear = Button(self.root, text="Clear", command=self.clear_grid)
        self.btn_clear.grid(row=_crr, column=5)

        _crr += 1
        self.btn_start_stop = Button(self.root, text="Start", command=self.start_stop)
        self.btn_start_stop.grid(row=_crr, column=1)

        self.btn_tick = Button(self.root, text=">>", command=self.tick)
        self.btn_tick.grid(row=_crr, column=2)


        _crr += 1
        self.lbl_tickno = Label(self.root, text="Round:0")
        self.lbl_tickno.grid(row=_crr)

        _crr += 1
        self.lbl_alive = Label(self.root, text="Alive:0")
        self.lbl_alive.grid(row=_crr)

        _crr += 1
        self.lbl_dead = Label(self.root, text="Dead:0")
        self.lbl_dead.grid(row=_crr)


        self.alive_cell_color = "#00FF00"
        self.dead_cell_color = "#FFFFFF" #"#e5e5e5"
        self.blank_cell_color = "#FFFFFF"
        self.grid_color = "#808080"

        self.clear_grid()

        self.root.mainloop()

    def put_rect(self, cl, rw, color):
        x1 = cl * self.size
        y1 = rw * self.size
        x2 = x1 + self.size
        y2 = y1 + self.size

        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=self.grid_color)

    def clear_grid(self):
        self.cols = int(self.edt_cols.get())
        self.rows = int(self.edt_rows.get())

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
                self.grid[rw][cl] = 0
                self.put_rect(cl, rw, self.dead_cell_color)


    def init_grid(self):
        self.clear_grid()

        for rw in range(self.rows):
            for cl in range(self.cols):

                is_alive = random.randint(0, 1)
                if is_alive == 1:
                    self.grid[rw][cl] = is_alive
                else:
                    self.grid[rw][cl] = 0 #empty cell

                if is_alive:
                    color = self.alive_cell_color
                else:
                    color = self.dead_cell_color

                self.put_rect(cl, rw, color)

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
            self.is_active = True
            self.root.after(self.tick_delay, self.tick)
            self.btn_start_stop.config(text='Stop')

            self.btn_tick.config(state=DISABLED)
            self.btn_seed.config(state=DISABLED)
            self.btn_clear.config(state=DISABLED)

    def update_labels(self):
        self.lbl_tickno.config(text="Round:%d" %(self.tick_count))
        self.lbl_alive.config(text="Alive:%d" %(self.alive))
        self.lbl_dead.config(text="Dead:%d" %(self.dead))

    def tick(self):
        if self.in_tick:
            return

        self.in_tick = True

        self.alive = 0
        self.dead = 0

        self.canvas.delete("all")

        old_grid = self.grid[:]

        for rw in range(self.rows):
            for cl in range(self.cols):
                n_alive = 0

                for y in range(-1, 2):
                    for x in range(-1, 2):
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

                if self.grid[rw][cl] <= 0:
                #else:
                    if n_alive == 3:
                        self.grid[rw][cl] = 1

                if self.grid[rw][cl]:
                    color = self.alive_cell_color
                    self.alive += 1
                else:
                    color = self.dead_cell_color
                    self.dead += 1

                self.put_rect(cl, rw, color)

        self.in_tick = False

        self.tick_count += 1
        self.update_labels()

        if self.is_active:
            self.root.after(self.tick_delay, self.tick)


Gol(30, 30, 10, 100)

