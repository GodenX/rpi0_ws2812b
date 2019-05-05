#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     app
   Description :
   Author :       jackie
   date：          2019-05-05 22:44
-------------------------------------------------
   Change Activity:
                   2019-05-05 22:44:
-------------------------------------------------
"""
__author__ = 'jackie'

from ws2812b import *


# Main program logic follows:
def main():
    led = MyLED(led_brightness=1)
    try:
        while True:
            for i in range(3, 49, 1):
                led.change_brightness(Brightness[i])
                led.color_random(3)
            for i in range(48, 2, -1):
                led.change_brightness(Brightness[i])
                led.color_random(3)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
