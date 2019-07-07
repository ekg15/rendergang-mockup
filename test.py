import unittest
from myhdl import Simulation, Signal, delay, intbv, bin,\
        ResetSignal
from fifo import ConstFIFO
import random

MAX_DELAY = 10
WIDTH = 10
random.seed(0)

class TestConstFIFO(unittest.TestCase):
    def testFIFOInvalid(self):
        """ Test no change in FIFO when never ready """
        def test(clock, reset,
                in_data, in_ready, in_valid,
                out_data, out_ready, out_valid, length):
            out_ready = False
            yield delay(10)
            for i in range(2*length):
                clock.next = 1
                yield delay(10)
                clock.next = 0
                yield delay(10)
                self.assertEqual(in_ready, False)

        self.runTests(test)

    def testFIFORandom(self):
        """ Test FIFO under random operation """
        def test(clock, reset,
                in_data, in_ready, in_valid,
                out_data, out_ready, out_valid, length):
            data = [0] * length
            valid = [False] * length

            out_ready.next = True
            in_valid.next = True

            for i in range(3*length):
                clock.next = 0
                yield delay(10)

                new = random.randrange(2**WIDTH)
                new_valid = random.choice([True, False])

                in_data.next = new
                in_valid.next = new_valid
                data = data[1:] + [new]
                valid = valid[1:] + [new_valid]

                clock.next = 1
                yield delay(10)

                self.assertEqual(bool(in_ready), True)
                self.assertEqual(bool(out_valid), valid[0])
                if bool(out_valid):
                    self.assertEqual(int(out_data), data[0])

        self.runTests(test)

    def runTests(self, test):
        for length in range(1, MAX_DELAY):
            clock = Signal(0)
            reset = ResetSignal(1, active=0, isasync=True)

            in_data = Signal(intbv(0)[WIDTH:])
            out_data = Signal(intbv(0)[WIDTH:])
            in_valid = Signal(0)
            out_valid = Signal(0)
            in_ready = Signal(0)
            out_ready = Signal(0)

            dut = ConstFIFO(clock, reset,
                    in_data, in_ready, in_valid,
                    out_data, out_ready, out_valid, length)
            check = test(clock, reset,
                    in_data, in_ready, in_valid,
                    out_data, out_ready, out_valid, length)

            sim = Simulation(dut, check)
            sim.run(quiet = 1)

if __name__ == '__main__':
    unittest.main(verbosity=2)
