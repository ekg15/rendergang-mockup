import unittest
from myhdl import Simulation, Signal, delay, intbv, bin,\
        ResetSignal
from fifo import ConstFIFO
from memory import SChMemory
import random
from math import log2, ceil

random.seed(0)

class TestSingleChannelMemory(unittest.TestCase):
    def testInitialize(self):
        """ Tests setting memory to a default value """  
        def test(clock, reset, data_in, data_out, address, write, enable,
                init_data, width, size):
            enable.next = False

            for loc in range(size):
                clock.next = 0
                yield delay(10)

                address.next = loc
                enable.next = True

                clock.next = 1
                yield delay(10)

                self.assertEqual(int(data_out), init_data[loc])
                 
        self.runTests(test, 1)

    def testSingleReadWrite(self):
        """ Tests a single read write operation on the memory """
        def test(clock, reset, data_in, data_out, address, write, enable,
                init_data, width, size):
            number = random.randrange(2**WIDTH)
            
            enable.next = True
            write.next = True
            address.next = 0
            data_in.next = number

            clock.next = 1
            yield delay(10)

            clock.next = 0
            yield delay(10)

            write.next = False

            clock.next = 1
            yield delay(10)

            self.assertEqual(int(data_out), number)

        self.runTests(test, 1)

    def testManyReadWrite(self):
        """ Tests many reads and writes """
        def test(clock, reset, data_in, data_out, address, write, enable,
                init_data, width, size):
            for loc in [random.randrange(0, size) for i in range(size)]:
                clock.next = 0
                yield delay(10)
                
                number = random.randrange(2**WIDTH)
            
                enable.next = True
                write.next = True
                address.next = loc
                data_in.next = number

                clock.next = 1
                yield delay(10)

                clock.next = 0
                yield delay(10)

                write.next = False

                clock.next = 1
                yield delay(10)

                self.assertEqual(int(data_out), number)

        self.runTests(test, 1)

    def testDelay(self):
        """ Test that memory has appropriate latency and size """
        d = 3

        def test(clock, reset, data_in, data_out, address, write, enable,
                init_data, width, size):
            locs = [random.randrange(size) for i in range(5)]
            pred_locs = [None]*d

            for loc, ploc in zip(locs, pred_locs):
                enable.next = True
                address.next = loc

                if ploc is not None:
                    pval = init_data[ploc]
                    self.assertEqual(int(data_in), pval)

                clock.next = 1
                yield delay(10)

                clock.next = 0
                yield delay(10)

        self.runTests(test, d)
        

    def runTests(self, test, d):
        """ Helper function for memory tests """
        for size in [4, 23, 1024, 10000]:
            init_data = [random.randrange(2**WIDTH) for i in range(size)]

            clock = Signal(0)
            reset = ResetSignal(1, active=0, isasync=True)

            data_in = Signal(intbv()[WIDTH:])
            data_out = Signal(intbv()[WIDTH:])

            address = Signal(intbv()[ceil(log2(size)):])
            write = Signal(False)
            enable = Signal(False)

            test = test(clock, reset, data_in, data_out, address, write, enable,
                    init_data, WIDTH, size)
            dut = SChMemory(clock, reset, data_in, data_out, address, write, enable,
                    d, WIDTH, size, init_data)

            sim = Simulation(dut, test)
            sim.run(quiet = 1)


class TestY1MemoryController(unittest.TestCase):
    def testBlocking(self):
        """ Verify that blocking works correctly """
        raise NotImplementedError()

    def testReset(self):
        """ Test y1mc controller """
        raise NotImplementedError()

    def testRandomYs(self):
        """ Test controller quashing with random Y values """
        raise NotImplementedError()
    
    def runTests(self, test):
        """ Helper function to run tests """
        raise NotImplementedError()

MAX_DELAY = 10
WIDTH = 10
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
