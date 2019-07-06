import  numpy as np
import io
from PIL import Image

#include ready and valid signals for func to run

def parseMaps(colorFileName, heightFileName):
    myColorMap = Image.open(colorFileName, 'r')
    myHeightMap = Image.open(heightFileName, 'r')

    imgByteArr = io.BytesIO()
    myColorMap.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()

    print(imgByteArr)

    CMPA = list(myColorMap.getdata())
    print("Pixel: ")
    print(myColorMap.getpixel((0,0)))
    print(CMPA[2])
    print(myHeightMap)

parseMaps('./maps/C13.png','./maps/D13.png')