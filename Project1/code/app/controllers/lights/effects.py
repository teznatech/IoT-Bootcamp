import board
import neopixel
import time, sys
import datetime
import math
import random

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18
 
# The number of NeoPixels
num_pixels = 8
 
# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGB
 
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=float(sys.argv[1]), auto_write=False,
                           pixel_order=ORDER)


#Define functions which animate LEDs in various ways.
def SetAll(strip, color):
    """Wipe color across display a pixel at a time."""
    for i in range(num_pixels):
        strip[i] = color

def FadeRGB(strip):
    for i in range(0, 3):
        #Fade In.
        for j in range (0, 256):
            if i == 0:
                SetAll(strip, (j, 0, 0))
            elif i == 1:
                SetAll(strip, (0, j, 0))
            elif i == 2:
                SetAll(strip, (0, 0, j))
            strip.show()
        #Fade Out.
        for j in range (256, 0):
            if i == 0:
                SetAll(strip, (j, 0, 0))
            elif i == 1:
                SetAll(strip, (0, j, 0))
            elif i == 2:
                SetAll(strip, (0, 0, j))
            strip.show()


delay = 3 #seconds
t_end = time.time() + delay
while time.time() < t_end:
	FadeRGB(pixels)