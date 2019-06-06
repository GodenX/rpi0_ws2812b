#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     test
   Description :
   Author :       jackie
   date：          2019-05-05 21:09
-------------------------------------------------
   Change Activity:
                   2019-05-05 21:09:
-------------------------------------------------
"""
__author__ = 'jackie'

import logging.handlers
import time
import datetime
import random
from multiprocessing import Process, Queue
import board
import numpy
import neopixel
import app

font5x3 = {
    0x00000020: [0x00, 0x00, 0x00],
    0x00000021: [0x00, 0x17, 0x00],
    0x00000022: [0x03, 0x00, 0x03],
    0x00000023: [0x1f, 0x0a, 0x1f],
    0x00000024: [0x0a, 0x1f, 0x05],
    0x00000025: [0x09, 0x04, 0x12],
    0x00000026: [0x0a, 0x15, 0x1a],
    0x00000027: [0x00, 0x03, 0x00],
    0x00000028: [0x00, 0x0e, 0x11],
    0x00000029: [0x11, 0x0e, 0x00],
    0x0000002a: [0x15, 0x0e, 0x15],
    0x0000002b: [0x04, 0x0e, 0x04],
    0x0000002c: [0x10, 0x08, 0x00],
    0x0000002d: [0x04, 0x04, 0x04],
    0x0000002e: [0x00, 0x18, 0x00],
    0x0000002f: [0x08, 0x04, 0x02],
    0x00000030: [0x1f, 0x11, 0x1f],
    0x00000031: [0x00, 0x1f, 0x00],
    0x00000032: [0x1d, 0x15, 0x17],
    0x00000033: [0x11, 0x15, 0x1f],
    0x00000034: [0x07, 0x04, 0x1f],
    0x00000035: [0x17, 0x15, 0x1d],
    0x00000036: [0x1f, 0x15, 0x1d],
    0x00000037: [0x01, 0x01, 0x1f],
    0x00000038: [0x1f, 0x15, 0x1f],
    0x00000039: [0x17, 0x15, 0x1f],
    0x0000003a: [0x00, 0x0a, 0x00],
    0x0000003b: [0x10, 0x0a, 0x00],
    0x0000003c: [0x04, 0x0a, 0x11],
    0x0000003d: [0x0a, 0x0a, 0x0a],
    0x0000003e: [0x11, 0x0a, 0x04],
    0x0000003f: [0x01, 0x15, 0x03],
    0x00000040: [0x0e, 0x15, 0x16],
    0x00000041: [0x1e, 0x05, 0x1e],
    0x00000042: [0x1f, 0x15, 0x0a],
    0x00000043: [0x0e, 0x11, 0x11],
    0x00000044: [0x1f, 0x11, 0x0e],
    0x00000045: [0x1f, 0x15, 0x15],
    0x00000046: [0x1f, 0x05, 0x05],
    0x00000047: [0x0e, 0x15, 0x1d],
    0x00000048: [0x1f, 0x04, 0x1f],
    0x00000049: [0x11, 0x1f, 0x11],
    0x0000004a: [0x08, 0x10, 0x0f],
    0x0000004b: [0x1f, 0x04, 0x1b],
    0x0000004c: [0x1f, 0x10, 0x10],
    0x0000004d: [0x1f, 0x06, 0x1f],
    0x0000004e: [0x1f, 0x0e, 0x1f],
    0x0000004f: [0x0e, 0x11, 0x0e],
    0x00000050: [0x1f, 0x05, 0x02],
    0x00000051: [0x0e, 0x19, 0x1e],
    0x00000052: [0x1f, 0x0d, 0x16],
    0x00000053: [0x12, 0x15, 0x09],
    0x00000054: [0x01, 0x1f, 0x01],
    0x00000055: [0x0f, 0x10, 0x1f],
    0x00000056: [0x07, 0x18, 0x07],
    0x00000057: [0x1f, 0x0c, 0x1f],
    0x00000058: [0x1b, 0x04, 0x1b],
    0x00000059: [0x03, 0x1c, 0x03],
    0x0000005a: [0x19, 0x15, 0x13],
    0x0000005b: [0x1f, 0x11, 0x11],
    0x0000005c: [0x02, 0x04, 0x08],
    0x0000005d: [0x11, 0x11, 0x1f],
    0x0000005e: [0x02, 0x01, 0x02],
    0x0000005f: [0x10, 0x10, 0x10],
    0x00000060: [0x01, 0x02, 0x00],
    0x00000061: [0x18, 0x14, 0x1c],
    0x00000062: [0x1f, 0x14, 0x08],
    0x00000063: [0x08, 0x14, 0x14],
    0x00000064: [0x08, 0x14, 0x1f],
    0x00000065: [0x0c, 0x1a, 0x16],
    0x00000066: [0x04, 0x1e, 0x05],
    0x00000067: [0x14, 0x16, 0x0e],
    0x00000068: [0x1f, 0x04, 0x18],
    0x00000069: [0x00, 0x1d, 0x00],
    0x0000006a: [0x10, 0x10, 0x0d],
    0x0000006b: [0x1e, 0x08, 0x14],
    0x0000006c: [0x11, 0x1f, 0x10],
    0x0000006d: [0x1c, 0x0c, 0x1c],
    0x0000006e: [0x1c, 0x04, 0x18],
    0x0000006f: [0x08, 0x14, 0x08],
    0x00000070: [0x1c, 0x0a, 0x04],
    0x00000071: [0x04, 0x0a, 0x1c],
    0x00000072: [0x1e, 0x04, 0x04],
    0x00000073: [0x14, 0x1e, 0x0a],
    0x00000074: [0x02, 0x1f, 0x02],
    0x00000075: [0x0c, 0x10, 0x1c],
    0x00000076: [0x0c, 0x18, 0x0c],
    0x00000077: [0x1c, 0x18, 0x1c],
    0x00000078: [0x14, 0x08, 0x14],
    0x00000079: [0x12, 0x14, 0x0e],
    0x0000007a: [0x1a, 0x1e, 0x16],
    0x0000007b: [0x04, 0x1b, 0x11],
    0x0000007c: [0x00, 0x1b, 0x00],
    0x0000007d: [0x11, 0x1b, 0x04],
    0x0000007e: [0x02, 0x03, 0x01],
    0x0000007f: [0x1f, 0x1f, 0x1f],
}

mask = bytearray([1, 2, 4, 8, 16, 32, 64, 128])

#         R    G    B
WHITE = (255, 255, 255)
GRAY = (185, 185, 185)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHTRED = (175, 20, 20)
GREEN = (0, 255, 0)
LIGHTGREEN = (20, 175, 20)
BLUE = (0, 0, 255)
LIGHTBLUE = (20, 20, 175)
YELLOW = (255, 255, 0)
LIGHTYELLOW = (175, 175, 20)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 100, 0)

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS = (BLUE, GREEN, RED, YELLOW, CYAN, MAGENTA, ORANGE)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)

# Zig-Zag resorting array for cylinder matrix
matrix = [4, 5, 14, 15, 24, 25, 34, 35, 44, 45, 54, 55, 64, 65, 74, 75, 84, 85, 94, 95,
          3, 6, 13, 16, 23, 26, 33, 36, 43, 46, 53, 56, 63, 66, 73, 76, 83, 86, 93, 96,
          2, 7, 12, 17, 22, 27, 32, 37, 42, 47, 52, 57, 62, 67, 72, 77, 82, 87, 92, 97,
          1, 8, 11, 18, 21, 28, 31, 38, 41, 48, 51, 58, 61, 68, 71, 78, 81, 88, 91, 98,
          0, 9, 10, 19, 20, 29, 30, 39, 40, 49, 50, 59, 60, 69, 70, 79, 80, 89, 90, 99]
# matrix = [95, 94, 85, 84, 75, 74, 65, 64, 55, 54, 45, 44, 35, 34, 25, 24, 15, 14, 5, 4,
#           96, 93, 86, 83, 76, 73, 66, 63, 56, 53, 46, 43, 36, 33, 26, 23, 16, 13, 6, 3,
#           97, 92, 87, 82, 77, 72, 67, 62, 57, 52, 47, 42, 37, 32, 27, 22, 17, 12, 7, 2,
#           98, 91, 88, 81, 78, 71, 68, 61, 58, 51, 48, 41, 38, 31, 28, 21, 18, 11, 8, 1,
#           99, 90, 89, 80, 79, 70, 69, 60, 59, 50, 49, 40, 39, 30, 29, 20, 19, 10, 9, 0]

brightness_list = [0.000, 0.005, 0.010, 0.015, 0.020, 0.025, 0.030, 0.035, 0.040, 0.05,
                   0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15,
                   0.17, 0.19, 0.21, 0.23, 0.25, 0.27, 0.29, 0.31, 0.33, 0.35,
                   0.38, 0.41, 0.44, 0.47, 0.50, 0.53, 0.56, 0.59, 0.62, 0.65,
                   0.69, 0.73, 0.77, 0.81, 0.85, 0.89, 0.93, 0.97, 1.00]


class LEDDriver(object):
    def __init__(self, queue):
        self.queue = queue

    @staticmethod
    def color_convent(color_r=None, color_g=None, color_b=None, color=None, color_tuple=None):
        try:
            if (color_r is not None) and (color_g is not None) and (color_b is not None):
                return color_g, color_r, color_b
            elif color is not None:
                color_r = (color >> 16) & 0xFF
                color_g = (color >> 8) & 0xFF
                color_b = color & 0xFF
                return color_r, color_g, color_b
            elif color_tuple is not None:
                color_r = color_tuple[0]
                color_g = color_tuple[1]
                color_b = color_tuple[2]
                return color_g, color_r, color_b
            else:
                return None
        except Exception as e:
            logging.error(e)
            return None

    def set_color(self, **color_dict):
        logging.debug("SetColorStart: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        led_sc = {"strip": {}}
        for i in color_dict:
            led_sc["strip"][int(i)] = self.color_convent(color=color_dict[i])
        self.show(**led_sc)
        logging.debug("SetColorEnd:   " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

    def solid_color(self, color):
        led_soc = {"isSolidColor": self.color_convent(color=color)}
        self.show(**led_soc)

    def clear_display(self):
        led_cd = {"isSolidColor": (0, 0, 0)}
        self.show(**led_cd)

    def power_off(self):
        led_cd = {"isSolidColor": (0, 0, 0), "brightness": 0}
        self.show(**led_cd)

    def lightness(self):
        logging.debug("LightnessStart: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        led_swwc = {"brightness": 0}
        self.show(**led_swwc)
        self.solid_color(0xFFFFFF)
        for i in range(0, 49):
            led_swwc = {"brightness": i}
            self.show(**led_swwc)
            time.sleep(0.03)
        logging.debug("LightnessEnd:   " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

    def color_random(self, brightness):
        led_cr = {"brightness": brightness, "strip": {}}
        for i in range(0, 3):
            led_cr["strip"] = {
                random.randrange(0, 100, 1): self.color_convent(color=random.randrange(0, 0xFFFFFF, 2))}
            self.show(**led_cr)
            time.sleep(0.001)

    def color_random_change_brightness(self):
        logging.debug("ColorRandomStart: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        for i in range(0, 49):
            self.color_random(brightness=i)
        for i in range(48, -1, -1):
            self.color_random(brightness=i)
        logging.debug("ColorRandomEnd:   " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

    def scroll_text_display(self, string, color=None, wait_time=0.11):
        logging.debug("ScrollTextStart: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        display = [[(0, 0, 0) for x in range(0, 20)] for y in range(0, 5)]

        def draw_display():
            led_std = {"strip": {}}
            for x in range(0, 20):
                for y in range(0, 5):
                    led_std["strip"][matrix[y * 20 + x]] = display[y][x]
            self.show(**led_std)

        if (color is None) or (color == 0):
            color = self.color_convent(color=random.randrange(0, 0xFFFFFF, 2))
        else:
            color = self.color_convent(color=color)
        logging.debug("scroll_text_display: %s %s" % (string, str(color)))
        for c in range(0, len(string)):
            for i in range(0, 3):
                a = font5x3[ord(string[c])][i]
                for j in range(0, 5):
                    if a & mask[j]:
                        display[j][19] = color
                    else:
                        display[j][19] = (0, 0, 0)
                draw_display()
                display = numpy.roll(display, -1, axis=1)
                time.sleep(wait_time)
            # add zero column after every letter
            for j in range(0, 5):
                display[j][19] = (0, 0, 0)
            draw_display()
            display = numpy.roll(display, -1, axis=1)
            time.sleep(wait_time)
        # shift text out of display (20 pixel)
        for i in range(0, 20):
            for j in range(0, 5):
                display[j][19] = (0, 0, 0)
            draw_display()
            display = numpy.roll(display, -1, axis=1)
            time.sleep(wait_time)
        logging.debug("ScrollTextEnd:   " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

    def color_wipe(self, color=None):
        logging.debug("ColorWipeStart: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        if (color is None) or (color == 0):
            color = self.color_convent(color=random.randrange(0, 0xFFFFFF, 2))
        else:
            color = self.color_convent(color=color)
        for i in range(0, 100):
            led_cw = {"strip": {matrix[i]: color}}
            self.show(**led_cw)
            time.sleep(0.04)
        logging.debug("ColorWipeEnd:   " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

    def show(self, **led):
        self.queue.put(led)


class LEDIOFunc(Process):
    def __init__(self, queue):
        Process.__init__(self)
        self.queue = queue
        self.led = neopixel.NeoPixel(board.D18, 100, brightness=brightness_list[0], auto_write=False,
                                     pixel_order=neopixel.GRB)

    def run(self):
        while True:
            led = self.queue.get()
            try:
                # logging.debug("LEDIOFuncStart: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
                if "brightness" in led:
                    self.led.brightness = brightness_list[led["brightness"]]
                if "isSolidColor" in led:
                    self.led.fill(led["isSolidColor"])
                elif "strip" in led:
                    for i in led["strip"]:
                        self.led[i] = led["strip"][i]
                self.led.show()
                # logging.debug("LEDIOFuncEnd:   " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
                # logging.debug("brightness: " + str(self.led.brightness))
                # logging.debug("strip: " + str(self.led))
            except Exception as e:
                logging.error(e)
