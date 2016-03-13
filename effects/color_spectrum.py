"""Color spectrum effect."""

from modules import hyperion
# import sys
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
        self.mirror = float(hyperion.args.get('mirror', True))
        self.reverse = float(hyperion.args.get('reverse', False))
        self.bw_exp = int(hyperion.args.get('band-width-exp', 5))
        self.start_index = int(hyperion.args.get('start-index', 0))
        self.increment = hyperion.args.get('color-speed', 3)
        self.interval = hyperion.args.get('interval', 100)

        self._magnitudes = None # store incoming messages

        # TODO: Implement possibility to change start index

        # Check parameters
        brightness = max(0.0, min(brightness, 1.0))
        saturation = max(0.0, min(saturation, 1.0))

        # Initialize the led data
        self._leds_data = bytearray()

        color_steps = hyperion.ledCount

        if self.mirror:
            color_steps = color_steps / 2

        colors = []

        for i in range(color_steps):
            hue = float(i)/color_steps
            colors.append(colorsys.hsv_to_rgb(hue, saturation, brightness))

        if self.mirror:
            for i in range(color_steps):
                hue = float(color_steps-i)/color_steps
                colors.append(colorsys.hsv_to_rgb(hue, saturation, brightness))

        if not self.reverse:
            for i in range(color_steps):
                c = colors[i]
                self._leds_data += bytearray((int(255*c[0]), int(255*c[1]), int(255*c[2])))

        if self.mirror or self.reverse:
            for i in range(color_steps, 0, -1):
                c = colors[i-1]
                self._leds_data += bytearray((int(255*c[0]), int(255*c[1]), int(255*c[2])))


        # Temp buffer
        self._leds_data_temp = bytearray(self._leds_data)

        self.processing = False

        # Octaves:
        # 2: 32 - 64 Hz     =   1 * 32
        # 3: 64 - 128 Hz    =   2 * 32
        # 4: 128 - 256 Hz   =   4 * 32
        # 5: 256 - 512 Hz   =   8 * 32
        # 6: 512 - 1024 Hz  =  16 * 32
        # 7: 1024 - 2048 Hz =  32 * 32
        # 8: 2048 - 4096 Hz =  64 * 32
        # 9: 4096 - 8192 Hz = 128 * 32

        # Band index  1         2         4         8        16        32        64        128       256
        # Octave      |   #2    |   #3    |   #4    |   #5    |   #6    |   #7    |   #8    |   #9    |
        # Band count  |    1    |    2    |    4    |    8    |    16   |   32    |   64    |   128   |

        self.band_width = 2**self.bw_exp

        self.bands = int(math.ceil(22050 / self.band_width))

        self.octaves = []

        for i in range(5, 14):
            self.octaves.append(2**(i-self.bw_exp))

        self.cutoff = self.octaves[-1]+1 # Cut rest of the frequencies

        self.octave_count = len(self.octaves)-1


        self.led_count = hyperion.ledCount

        if self.mirror:
            self.led_count = self.led_count / 2

        self.leds_per_octave = int(math.floor(self.led_count / self.octave_count))

        self.leds_per_last_octave = self.leds_per_octave

        if self.leds_per_octave * self.octave_count < self.led_count:
            self.leds_per_octave += 1
            # Make last octave shorter
            self.leds_per_last_octave = self.leds_per_octave - (self.leds_per_octave * self.octave_count - self.led_count)

        self.bins = []

        for octave in self.octaves[:8]:
            octave_divisor = octave/self.leds_per_octave
            for i in range(0, self.leds_per_octave):
                self.bins.append(octave + i*octave_divisor)
        self.bins.append(self.octaves[8])

        # j = 0
        # while j+1 <= self.bins[j]:
        #     self.bins[j] = j+1
        #     j += 1

        # print 'leds_per_octave: {}'.format(self.leds_per_octave)
        # print 'leds_per_last_octave: {}'.format(self.leds_per_last_octave)
        # print 'bins: {}'.format(self.bins)

        # if self.bins[11] < 16:
        #     for i in range(0, 12):
        #         self.bins[i] = i+1

        # print 'bins: {}'.format(self.bins)

        # With 32 Hz bands, we get 9 bins for bass, so lets adjust the bands based on that

        self.mag_min_orig = self.mag_min

        self.half = (hyperion.ledCount/2) * 3

        self._spectrum = GstSpectrumDump(
            source=hyperion.args.get('audiosrc','autoaudiosrc'),
            vumeter=False,
            quiet=True,
            bands=self.bands,
            logamplify=False,
            cutoff=self.cutoff,
            interval=self.interval,
            callback=self.receive_magnitudes
            )
        self._spectrum.start()

        print 'Effect started, waiting for gstreamer messages...'

    def __del__(self):
        self.stop()

    def receive_magnitudes(self, magnitudes):

        # Don't update when processing
        if self.processing:
            return
        elif len(magnitudes) < self.cutoff:
            print 'Invalid len: {}, {}'.format(len(magnitudes), self.cutoff)
        else:
            self._magnitudes = magnitudes
            self.update_leds()

            # TODO: Loop colors if speed > 0
            # Loop colors for both sides
            # ld = effect._leds_data
            # h = effect.half
            # i = effect.increment
            # ld[:h] = ld[h-i:h] + ld[:h-i]
            # ld[h:] = ld[h+i:] + ld[h:h+i]
            hyperion.setColor(self._leds_data_temp)

    def stop(self):
        self._spectrum.stop()

    def normalize_mag(self, magnitude):
        # Normalize magnitude to 0-255

        if magnitude < self.mag_min:
            return 0
        if magnitude > self.mag_max:
            return 255

        return int(((magnitude-self.mag_min) / (self.mag_max - self.mag_min)) * 255)


    def update_leds(self):

        self.processing = True

        # bass = self.normalize_mag(self._magnitudes[0])

        # sys.stdout.write("\033[K")
        # sys.stdout.write('\r' + int(self._magnitudes[0])*'|' )

        # Copy all values
        self._leds_data_temp[:] = self._leds_data[:]

        # self.processing = False
        # return

        # Loop leds
        for i in range(0, self.led_count):

            self.current_mag = 0.0
            self.norm_mag = 0

            if self.bins[i] == self.bins[i+1]:
                self.current_mag = self._magnitudes[self.bins[i]]
            else:
                for k in range(self.bins[i], self.bins[i+1]):
                    self.current_mag += self._magnitudes[k]

            self.norm_mag = self.normalize_mag(self.current_mag)

            for j in range(0,3):

                if not self.reverse:
                    self._leds_data_temp[i*3+j] = (self._leds_data_temp[i*3+j] * self.norm_mag) >> 8

                if self.mirror or self.reverse:
                    self._leds_data_temp[-1-i*3-j] = (self._leds_data_temp[-1-i*3-j] * self.norm_mag) >> 8

        self.processing = False


def run():
    effect = Effect()

    # Keep this thread alive
    while not hyperion.abort():
        time.sleep(1)

    effect.stop()

run()
