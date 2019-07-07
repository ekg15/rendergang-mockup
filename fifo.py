from myhdl import block, Signal, always_seq, always_comb, intbv

@block
def ConstFIFO(clock, reset,
        in_data, in_ready, in_valid,
        out_data, out_ready, out_valid, delay=1):
    
    _reg = [Signal(intbv()[len(in_data):]) for i in range(delay)]
    _reg_valid = [Signal(0) for i in range(delay)]
    
    @always_comb
    def comb_logic():
        in_ready.next = out_ready

        out_data.next = _reg[-1]
        out_valid.next = _reg_valid[-1]
    
    @always_seq(clock.posedge, reset)
    def seq_logic():
        if out_ready:
            _reg[0].next = in_data
            _reg_valid[0].next = in_valid
    
            for i in range(delay-1):
                _reg[i+1].next = _reg[i]
                _reg_valid[i+1].next = _reg_valid[i]

    return comb_logic, seq_logic
