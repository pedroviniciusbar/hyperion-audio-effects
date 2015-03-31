"""
This module is used to display the leds in a gui

Created on 27.11.2014

@author: Fabian Hertwig
"""
from Tkinter import *
import tkFont
import hyperion

_led_height = 16
_led_width = 16

master = Tk()


def rgb_to_string(r, g, b):
    # As defined by tkinter documentation
    return "#%02x%02x%02x" % (r, g, b)


def createWindow(show_idx):
    # the empty window
    # window_width = (hyperion.horizontal + 4) * _led_width
    # window_height = (hyperion.vertical + 2) * _led_height

    window_width = 1920/2-100
    window_height = 1080/2-100

    canvas = Canvas(master, width=window_width, height=window_height)
    canvas.pack()

    # list for the led representing rectangles
    # leds_without_offset = []

    # list for the led representing rectangles
    gui_leds = []

    # calculate positions of the rectangles
    # x_increase = _led_width
    # y_increase = _led_height
    # x_pos = _led_width
    # y_pos = 0

    # leave a space for the first corner led if necessary
    # if not hyperion.corner_leds:
    #     x_pos += x_increase

    gui_font = tkFont.Font(family='Helvetica',size=8)

    for i, led in enumerate(hyperion.leds):

        x = round((led['x'] / 100.0) * (window_width-30))
        y = round((led['y'] / 100.0) * (window_height-30))

        # if i >= 17 and i <= 27:
        #     print 'Led {}: {} {}'.format(i, x, y)

        rect = canvas.create_rectangle(x, y, x + _led_width, y + _led_height, fill="black", outline="white")
        if show_idx:
            canvas.create_text(x + _led_width/2, y + _led_height/2, font=gui_font, fill="white", text=str(i))

        # leds_without_offset.append(rect)
        gui_leds.append(rect)

        # # Update the x and y pos so the result is a rectangle of single rectangles
        # if i < hyperion.horizontal:
        #     # go one step to the right
        #     x_pos += x_increase
        # elif i < hyperion.horizontal + hyperion.vertical:
        #     # go one step down
        #     y_pos += y_increase
        # elif i < (2 * hyperion.horizontal) + hyperion.vertical:
        #     # go one step to the left
        #     x_pos -= x_increase
        # elif i < (2 * hyperion.horizontal) + (2 * hyperion.vertical):
        #     # go one step up
        #     y_pos -= y_increase

        # # Handle the corner leds
        # if not hyperion.corner_leds:
        #     if i == hyperion.horizontal - 1:
        #         # At the top right corner, leave the space for the corner led empty
        #         y_pos += y_increase
        #     elif i == hyperion.horizontal + hyperion.vertical - 1:
        #         # At the bottom right corner, leave the space for the corner led empty
        #         x_pos -= x_increase
        #     elif i == 2 * hyperion.horizontal + hyperion.vertical - 1:
        #         # At the bottom left corner, leave the space for the corner led empty
        #         y_pos -= y_increase

    # Handle offset and counterclockwise led arrangement
    # leds_with_direction = leds_without_offset[:]
    # if not hyperion.clockwise_direction:
    #     # Reverse list but keep first entry (this is how hypercon does it)
    #     leds_with_direction = leds_without_offset[len(leds_without_offset):0:-1]
    #     leds_with_direction.insert(0, leds_without_offset[0])

    # offset = hyperion.first_led_offset % hyperion.ledCount

    # leds_with_offset = leds_with_direction[offset:]
    # leds_with_offset.extend(leds_with_direction[:offset])

    # Call master which recalls itself to update the gui in the mainloop
    master.after(33, update_leds, canvas, gui_leds)
    mainloop()


def update_leds(canvas, gui_leds):
    for i, led in enumerate(gui_leds):
        change_color(canvas, led, i)

    master.after(33, update_leds, canvas, gui_leds)


def change_color(canvas, rect, led_number):
    led_data_copy = hyperion.get_led_data()
    if len(led_data_copy) >= 3 * led_number + 2:
        r = hyperion.get_led_data()[3 * led_number + 0]
        g = hyperion.get_led_data()[3 * led_number + 1]
        b = hyperion.get_led_data()[3 * led_number + 2]

        canvas.itemconfigure(rect, fill=rgb_to_string(r, g, b))