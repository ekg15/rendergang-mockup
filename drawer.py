from utils import Module

class Drawer(Module):
    def __init__(self, screen_width):
        self.cgen = ColumnGen(screen_width)

    def clock(self):
        # connection logic

        # clock
        self.cgen.clock()

    def draw_in(self, valid, height, color, finished):
        pass

    def draw_in_ready(self):
        pass

class ColumnGen(Module):
    def __init__(self, screen_width):
        self.screen_width = screen_width
        self.reg_column = 0

    def clock(self):
        if self.ready:
            new = self.reg_column + 1
            self.reg_column = new if new < self.screen_width else 0

    def column_out(self, ready):
        self.ready = ready
        return self.reg_column

class Screen(Module):
    def __init__(self):
        self.reg_valid = False

    def clock(self):
        if self.valid and self.ready:
            if self.finished:
                self.reg_valid = True
                self.reg_finished = True
            else if self.height < self.zheight:
                self.reg_valid = False
            else:
                self.reg_valid = True
                self.reg_x = self.column
                self.reg_y1 = self.zheight
                self.reg_y2 = self.height
                self.reg_color = self.color
                self.reg_finished = False

    def _in(self, valid, height, color, finished, column, zheight):
        self.valid = valid
        self.height = height
        self.color = color
        self.finished = finished
        self.column = column
        self.zheight = zheight

    def _in_ready(self):
        return self.ready

    def _out(self, ready):
        self.ready = ready or not self.reg_valid
        return (self.reg_valid, self.reg_x, self.reg_y1, self.reg_y2, self.reg_color, self.reg_finished)
