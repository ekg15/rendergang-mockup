from utils import *

class Chip(Module):
    def __init__(self, swidth, sheight, scans):
        raise NotImplementedError()

    def clock(self):
        raise NotImplementedError()

if __name__ == '__main__':
    pass
