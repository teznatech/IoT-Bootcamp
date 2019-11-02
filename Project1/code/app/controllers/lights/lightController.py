import board
import neopixel
import sys

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18
red = int(sys.argv[1])
green = int(sys.argv[2])
blue = int(sys.argv[3])
brightness = float(sys.argv[4])
# The number of NeoPixels
num_pixels = 8
 
# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGB
 
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=brightness, auto_write=False,
                           pixel_order=ORDER)
pixels.fill((green,red,blue))
pixels.show()