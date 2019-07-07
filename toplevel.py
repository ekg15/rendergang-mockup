from myhdl import block, Signal
from artist import Artist

@block
def TopLevel(clock):
    artist = Artist(clock)

    return artist
