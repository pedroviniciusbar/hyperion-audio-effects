# Hyperion audio visualization effect by RanzQ
# ranzq87 [(at)] gmail.com

from devkit import hyperion
import time
import colorsys

from effects.spectrum_dump import GstSpectrumDump


BLACK = (0, 0, 0)

class Effect(object):

    def __init__(self):


        # Get the parameters
        # rotationTime = float(hyperion.args.get('rotation-time', 3.0))
        # brightness = float(hyperion.args.get('brightness', 1.0))
        # saturation = float(hyperion.args.get('saturation', 1.0))
        # reverse = bool(hyperion.args.get('reverse', False))
        rotationTime = 3.0
        brightness = 1.0
        saturation = 1.0
        reverse = False

        # Check parameters
        rotationTime = max(0.1, rotationTime)
        brightness = max(0.0, min(brightness, 1.0))
        saturation = max(0.0, min(saturation, 1.0))

        # Initialize the led data
        self.ledsData = bytearray()
        for i in range(hyperion.ledCount):
            hue = float(i)/hyperion.ledCount
            rgb = colorsys.hsv_to_rgb(hue, saturation, brightness)
            self.ledsData += bytearray((int(255*rgb[0]), int(255*rgb[1]), int(255*rgb[2])))

        # Temp buffer
        self.ledsDataTemp = bytearray(self.ledsData)

        # Calculate the sleep time and rotation increment
        self.increment = 3
        self.sleepTime = rotationTime / hyperion.ledCount

        if reverse:
            self.increment = -self.increment


        self.processing = False

        # Minimum magnitude level
        self.mag_min = 50.0

        # Maximum magnitude level
        self.mag_max = 70.0


    def receive_magnitudes(self, magnitudes):

        # Don't update when processing
        if self.processing:
            return
        else:
            self.magnitudes = magnitudes
            self.update_leds()


    def normalize_mag(self, magnitude):
        # Normalize magnitude to 0.0-1.0

        if magnitude < self.mag_min:
            return 0.0
        if magnitude > self.mag_max:
            return 1.0

        return (magnitude-self.mag_min) / (self.mag_max - self.mag_min)


    # def update_led(self, i, color):
    #     self.ledsData[3*i:3*i+3] = color


    # def get_led_color(self, i):
    #     # Gradient from green to red
    #     return (int(255*(i/self.height_float)), int(255*((self.height_float-i)/self.height_float)), 0)


    def update_leds(self):

        self.processing = True

        bass = self.normalize_mag(self.magnitudes[0])

        # print bass

        self.ledsDataTemp = map(lambda x: int(x * bass), self.ledsData)

        # print self.ledsData
        # print self.ledsDataTemp

        self.processing = False



effect = Effect()

# You can play with the parameters here (quiet=False to print the magnitudes for example)
spectrum = GstSpectrumDump(source='autoaudiosrc', vumeter=False, quiet=True, bands=4, callback=effect.receive_magnitudes)
spectrum.start()

while not hyperion.abort():

    hyperion.setColor(effect.ledsDataTemp)
    effect.ledsData = effect.ledsData[-effect.increment:] + effect.ledsData[:-effect.increment]
    time.sleep(0.05)


spectrum.stop()




# import hyperion
# import time
# import colorsys

# # Get the parameters
# rotationTime = float(hyperion.args.get('rotation-time', 3.0))
# brightness = float(hyperion.args.get('brightness', 1.0))
# saturation = float(hyperion.args.get('saturation', 1.0))
# reverse = bool(hyperion.args.get('reverse', False))

# # Check parameters
# rotationTime = max(0.1, rotationTime)
# brightness = max(0.0, min(brightness, 1.0))
# saturation = max(0.0, min(saturation, 1.0))

# # Initialize the led data
# ledData = bytearray()
# for i in range(hyperion.ledCount):
#     hue = float(i)/hyperion.ledCount
#     rgb = colorsys.hsv_to_rgb(hue, saturation, brightness)
#     ledData += bytearray((int(255*rgb[0]), int(255*rgb[1]), int(255*rgb[2])))

# # Calculate the sleep time and rotation increment
# increment = 3
# sleepTime = rotationTime / hyperion.ledCount
# while sleepTime < 0.05:
#     increment *= 2
#     sleepTime *= 2
# increment %= hyperion.ledCount

# # Switch direction if needed
# if reverse:
#     increment = -increment

# # Start the write data loop
# while not hyperion.abort():
#     hyperion.setColor(ledData)
#     ledData = ledData[-increment:] + ledData[:-increment]
#     time.sleep(sleepTime)
