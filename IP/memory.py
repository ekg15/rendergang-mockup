from myhdl import block, Signal, always_seq
from fifo import ConstFIFO

@block
def SChMemory(clock, reset, data_in, data_out, address, write, enable,
        d, width, size, init_data=None):
    high = Signal(1)
    
    data = Signal(0)
    addr = Signal(0)
    w = Signal(0)
    valid = Signal(0)

    dfifo = ConstFIFO(clock, reset,
            data_in, Signal(0), enable,
            data, high, Signal(0), d)
    afifo = ConstFIFO(clock, reset,
            address, Signal(0), enable,
            addr, high, Signal(0), d)
    wfifo = ConstFIFO(clock, reset,
            write, Signal(0), enable,
            w, high, valid, d)

    mem = [0]*size if init_data is None else init_data

    @always_seq(clock.posedge, reset)
    def seq_logic():
        if valid:
            if w:
                mem[int(addr)] = int(data)
            else:
                data_out.next = mem[int(addr)]

    return seq_logic, wfifo, afifo, dfifo
