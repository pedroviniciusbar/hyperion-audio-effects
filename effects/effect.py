# Hyperion audio visualization effect by RanzQ
# ranzq87 [(at)] gmail.com

from devkit import hyperion
import time

from effects.spectrum_dump import GstSpectrumDump


BLACK = (0, 0, 0)

class Effect(object):

    def __init__(self):
        self.processing = False
        self.ledsData = bytearray(hyperion.ledCount * (0, 0, 0))

        # TODO: Read options from json

        # Adjust these according to hyperion config
        # For now hardcoded for setups which start from bottom
        # since dev kit doesn't support the setImage()
        self.width = 48
        self.height = 30
        self.corners = True
        self.bottom_padding = 4

        if self.corners:
            self.height += 2

        # Helpers for updating the led array
        self.pad_left = (self.width - self.bottom_padding) / 2 + 1 # + 1 but why?
        self.pad_right = self.pad_left + 2*self.height + self.width - 4 # - 4 but why?

        # Minimum bar level
        self.bar_min = 90

        # Maximum bar level
        self.bar_max = 100


        # Helper for color function
        self.height_float = float(self.height)

        self.color_map = []
        for i in range(0, self.height):
            self.color_map.append(self.get_led_color(i))




    def receive_magnitudes(self, magnitudes):

        # Don't update when processing
        if self.processing:
            return
        else:
            self.magnitudes = magnitudes
            self.update_leds()


    def mag_to_idx(self, magnitude):
        # Magnitude is 0-100, get index according to min and max
        return int(((magnitude-self.bar_min) / (self.bar_max - self.bar_min)) * self.height )


    def update_led(self, i, color):
        self.ledsData[3*i:3*i+3] = color


    def get_led_color(self, i):
        # Gradient from green to red
        return (int(255*(i/self.height_float)), int(255*((self.height_float-i)/self.height_float)), 0)


    def update_leds(self):

        self.processing = True

        # We get 4 magnitudes from gst (not sure about R/L order)
        # [0] Left, [1] left peak, [2] right, [3] right peak

        # If vumeter=False, magnitudes hold the spectrum data,
        # do something else with them...

        # Length of magnitudes array equals number of bands

        left = self.mag_to_idx(self.magnitudes[0])
        left_peak = self.mag_to_idx(self.magnitudes[1])
        right = self.mag_to_idx(self.magnitudes[2])
        right_peak = self.mag_to_idx(self.magnitudes[3])

        for i in range(0, self.height):

            left_i = self.pad_left + i
            right_i = self.pad_right - i # right goes to negative direction

            color_i = self.color_map[i]

            if i <= left or i == left_peak:
                self.update_led(left_i, color_i)
            else:
                self.update_led(left_i, BLACK)

            if i <= right or i == right_peak:
                self.update_led(right_i, color_i)
            else:
                self.update_led(right_i, BLACK)

        self.processing = False



effect = Effect()

# You can play with the parameters here (quiet=False to print the magnitudes for example)
spectrum = GstSpectrumDump(source='alsasrc', vumeter=True, quiet=True, bands=4, callback=effect.receive_magnitudes)
spectrum.start()

while not hyperion.abort():
    # spectrum.iterate()
    hyperion.setColor(effect.ledsData)
    time.sleep(0.05)

spectrum.stop()
