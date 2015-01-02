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

        color_steps = hyperion.ledCount/2

        colors = []

        for i in range(color_steps):
            hue = float(i)/color_steps
            colors.append(colorsys.hsv_to_rgb(hue, saturation, brightness))

        for i in range(color_steps):
            hue = float(color_steps-i)/color_steps
            colors.append(colorsys.hsv_to_rgb(hue, saturation, brightness))

        for i in range(color_steps):
            c = colors[i]
            self.ledsData += bytearray((int(255*c[0]), int(255*c[1]), int(255*c[2])))

        for i in range(color_steps, 0, -1):
            c = colors[i-1]
            self.ledsData += bytearray((int(255*c[0]), int(255*c[1]), int(255*c[2])))


        # Temp buffer
        self.ledsDataTemp = bytearray(self.ledsData)

        self.processing = False

        self.bands = hyperion.ledCount / 2

        self.mag_min_orig = self.mag_min

        self.half = (hyperion.ledCount/2) * 3
        self.increment = 3


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

        # self.processing = False
        # return

        self.current_mag = 0.0

        # Scale them
        for i in range(0, self.bands):

            # Lower minimum for upper bands
            self.mag_min = ((self.bands - i) / float(self.bands)) * self.mag_min_orig/2 + self.mag_min_orig/2

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

    # Loop colors for both sides
    ld = effect.ledsData
    h = effect.half
    i = effect.increment
    ld[:h] = ld[h-i:h] + ld[:h-i]
    ld[h:] = ld[h+i:] + ld[h:h+i]

    time.sleep(0.05)


spectrum.stop()
