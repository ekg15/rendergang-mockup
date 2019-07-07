from myhdl import block, Signal, always_seq, always_comb

@block
def Artist(clock,
        draw_y, draw_color, draw_finished, draw_ready, draw_valid,
        pixel_x, pixel_y, pixel_color, pixel_buffer, pixel_ready, pixel_valid,
        screen_columns):

    prefetch_column = Signal(modbv(0, min=0, max=screen_columns))
    @always_seq(clock)
    def iterate_column():
        if draw_ready and draw_valid:
            prefetch_column += 1

    @always_seq(clock)
    def fetch_y1_from_memory():
        pass

    screen_valid = Signal(0)
    @always_seq(clock)
    def screen():
        pass

    @always_seq(clock)
    def draw_line():
        pass

    return iterate_column, fetch_y1_from_memory, draw_line

@block
def Y1MemoryController(clock,
        x_in, y_in, color_in, finished_in, ready_in, valid_in,
        x_out, y1_out, y2_out, color_out, finished_out, ready_out, valid_out,
        write_enable, read_enable, x_addr, data_out, data_in):
    """
    Memory controller for reading memory containing Y1 data then comparing that data
    against Y2. If necessary, Y1 is updated, otherwise the command is quashed.
    """
    pass
