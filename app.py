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

import logging.handlers
import os
import json
from multiprocessing import Process
import time
from mqtt_client import *
from ws2812b import *


if __name__ == '__main__':
    # task = LEDTask(0.8, "system_control", 5,)
    # task.daemon = True
    # task.start()
    mq = MyMQTTClient("10.141.43.201", 1883)
    mq.connect()
    mq.run()
    # led = MyLED(led_brightness=1)
    #     try:
    #         while True:
    #             for i in range(3, 49, 1):
    #                 led.change_brightness(Brightness[i])
    #                 led.color_random(3)
    #             for i in range(48, 2, -1):
    #                 led.change_brightness(Brightness[i])
    #                 led.color_random(3)
    #
    #     except Exception as e:
    #         print(e)
