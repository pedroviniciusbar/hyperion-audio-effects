'''
The main module which spawns a gui and a effect thread and opens a socket connection to the specified
host. The effect algorithm is in the effect module. Change this file to develop your effect.
Change the host and port to your needs in this main file and also the values representing your led configuration.

Created on 27.11.2014
Last modified on 28.3.2015

@author: Fabian Hertwig
@author: Juha Rantanen
'''

from threading import Thread

from modules import hyperion

import runpy
import argparse
import time
import json
import commentjson
from sets import Set
import operator

# Change this according to your led configuration.
# horizontal_led_num = 14
# vertical_led_num = 8
# first_led_offset_num = 0
# leds_in_clockwise_direction = True
# has_corner_leds = False

parser = argparse.ArgumentParser()
parser.add_argument("--gui", help="enable GUI", action="store_true")
parser.add_argument("--idx", help="show led indexes in gui", action="store_true")
parser.add_argument("--json", help="enable JSON client", action="store_true")
parser.add_argument("--effect", help="select effect", default="vumeter")
parser.add_argument("--config", help="path to config file", default="./hyperion.config.json")
parser.add_argument("--host", help="JSON host (default localhost)", default="localhost")
parser.add_argument("--port", help="JSON port (default 19444)", type=int, default=19444)
parser.add_argument("--audiosrc", help="Gstreamer audio source string", default="autoaudiosrc")



def run_effect(effect='effect'):
    """
    Runs the module effect. Copy any hyperion effect code in this module or create your own.
    Note that effects that call hyperion.setColor(r, g, b) or hyperion.setImage(img) are not supported.
    """
    runpy.run_module("effects." + effect)

def read_config(file_path):

    """
    Parses hyperion config file.
    """
    with open(file_path) as config_json:
        config = commentjson.load(config_json)

        leds = []

        h_max = 0
        v_max = 0
        h_min = 99999
        v_min = 99999

        xs = []
        ys = []

        for led in config.get('leds', []):
            hscan = led['hscan']
            vscan = led['vscan']
            hmin = hscan['minimum']
            hmax = hscan['maximum']
            vmin = vscan['minimum']
            vmax = vscan['maximum']
            h = round(((hmin + hmax) / 2 ) * 100, 2)
            v = round(((vmin + vmax) / 2 ) * 100, 2)
            xs.append(h)
            ys.append(v)
            leds.append({'x': h, 'y': v})


        xcounts = []
        left = None
        right = None


        for x in Set(xs):
            xcounts.append({'x': x, 'count': xs.count(x)})
            xcounts.sort(key=operator.itemgetter('count'))
            right = xcounts[len(xcounts)-2]
            left = xcounts[len(xcounts)-1]
            if (right['x'] < left['x']):
                left, right = right, left

        ycounts = []
        top = None
        bottom = None

        for y in Set(ys):
            ycounts.append({'y': y, 'count': ys.count(y)})
            ycounts.sort(key=operator.itemgetter('count'))
            bottom = ycounts[len(ycounts)-2]
            top = ycounts[len(ycounts)-1]
            if (bottom['y'] < top['y']):
                top, bottom = bottom, top

        leds_left = []
        leds_right = []
        leds_top = []
        leds_bottom = []

        for i, led in enumerate(leds):
            x = led['x']
            y = led['y']
            if x == left['x']:
                leds_left.append(i)
            elif x == right['x']:
                leds_right.append(i)
            elif y == top['y']:
                leds_top.append(i)
            elif y == bottom['y']:
                leds_bottom.append(i)

        # Sort the lists
        leds_top.sort(key=lambda i: leds[i]['x'], reverse=False)
        leds_right.sort(key=lambda i: leds[i]['y'], reverse=False)
        leds_bottom.sort(key=lambda i: leds[i]['x'], reverse=True)
        leds_left.sort(key=lambda i: leds[i]['y'], reverse=True)

        # Not the lists run like this:

        #  >>>>>>> TOP >>>>>>>
        #  ^                 v
        #  ^                 v
        # LEFT              RIGHT
        #  ^                 v
        #  ^                 v
        #  <<<<< BOTTOM <<<<<<

        # print 'leds_top: {}'.format(leds_top)
        # print 'leds_right: {}'.format(leds_right)
        # print 'leds_bottom: {}'.format(leds_bottom)
        # print 'leds_left: {}'.format(leds_left)

        return (leds, leds_top, leds_right, leds_bottom, leds_left)


def main():

    args = parser.parse_args()

    leds, leds_top, leds_right, leds_bottom, leds_left = read_config(args.config)

    hyperion.init(leds, leds_top, leds_right, leds_bottom, leds_left)

    if args.json:
        from devkit import json_client
        # Open the connection to the json server. Uncomment if you do not want to send data to the server.
        json_client.open_connection(args.host, args.port)

    with open('effects/' + args.effect + '.json') as effect_json:
        effect = json.load(effect_json)
        effect_args = effect.get('args', {})
        effect_args['audiosrc'] = args.audiosrc
        hyperion.set_args(effect_args)

    # create own thread for the effect
    effect_thread = Thread(target=run_effect, kwargs={'effect': args.effect})

    effect_thread.start()

    if args.gui:
        from devkit import gui
        gui.createWindow(args.idx)

        # After the window was closed abort the effect through the fake hyperion module
        hyperion.set_abort(True)
    else:
        print "Exit by typing 'x' or 'exit'"
        cmd = ''
        while cmd != 'x' and cmd != 'exit':
            cmd = raw_input()

        hyperion.set_abort(True)

    # wait for the thread to stop
    effect_thread.join()

    if args.json:
        # close potential connections
        json_client.close_connection()
    print("Exiting")


if __name__ == '__main__':
    main()

