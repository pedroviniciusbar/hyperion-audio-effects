# Hyperion audio visualization effect by RanzQ
# ranzq87 [(at)] gmail.com

from devkit import hyperion
import sys
import time
import colorsys
import math

from effects.spectrum_dump import GstSpectrumDump


BLACK = (0, 0, 0)

class Effect(object):

    def __init__(self):


        # Get the parameters
        brightness = float(hyperion.args.get('brightness', 1.0))
        saturation = float(hyperion.args.get('saturation', 1.0))
        self.mag_min = float(hyperion.args.get('magnitude-min', 30.0))
        self.mag_max = float(hyperion.args.get('magnitude-max', 60.0))


        # Check parameters
        brightness = max(0.0, min(brightness, 1.0))
        saturation = max(0.0, min(saturation, 1.0))

        # Initialize the led data
        self.ledsData = bytearray()
        for i in range(hyperion.ledCount/2):
            hue = float(i)/(hyperion.ledCount/2+30)
            rgb = colorsys.hsv_to_rgb(hue, saturation, brightness)
            self.ledsData += bytearray((int(255*rgb[0]), int(255*rgb[1]), int(255*rgb[2])))

        for i in range(hyperion.ledCount/2, 0, -1):
            hue = float(i)/(hyperion.ledCount/2+30)
            rgb = colorsys.hsv_to_rgb(hue, saturation, brightness)
            self.ledsData += bytearray((int(255*rgb[0]), int(255*rgb[1]), int(255*rgb[2])))

        # Temp buffer
        self.ledsDataTemp = bytearray(self.ledsData)

        self.processing = False

        self.bands = hyperion.ledCount / 2


    def receive_magnitudes(self, magnitudes):

        # Don't update when processing
        if self.processing:
            return
        else:
            self.magnitudes = magnitudes
            self.update_leds()


    def normalize_mag(self, magnitude):
        # Normalize magnitude to 0-255

        if magnitude < self.mag_min:
            return 0
        if magnitude > self.mag_max:
            return 255

        return int(((magnitude-self.mag_min) / (self.mag_max - self.mag_min)) * 255)


    def update_leds(self):

        self.processing = True

        # bass = self.normalize_mag(self.magnitudes[0])

        # sys.stdout.write("\033[K")
        # sys.stdout.write('\r' + int(self.magnitudes[0])*'|' )

        # Copy all values
        self.ledsDataTemp[:] = self.ledsData[:]

        self.current_mag = 0.0

        # Scale them
        for i in range(0, self.bands):

            self.mag_min = ((self.bands - i) / float(self.bands)) * 40.0

            self.current_mag = self.normalize_mag(self.magnitudes[i])

            for j in range(0,3):

                self.ledsDataTemp[i*3+j] = (self.ledsDataTemp[i*3+j] * self.current_mag) >> 8

                self.ledsDataTemp[-1-i*3-j] = (self.ledsDataTemp[-1-i*3-j] * self.current_mag) >> 8

        self.processing = False



effect = Effect()

# You can play with the parameters here (quiet=False to print the magnitudes for example)
spectrum = GstSpectrumDump(source='autoaudiosrc', vumeter=False, quiet=True, bands=effect.bands+30, interval=20,callback=effect.receive_magnitudes)
spectrum.start()

while not hyperion.abort():
    hyperion.setColor(effect.ledsDataTemp)
    time.sleep(0.01)


spectrum.stop()
