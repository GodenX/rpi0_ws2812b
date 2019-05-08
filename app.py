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
from multiprocessing import Process
from mqtt_client import *
from ws2812b import *

mqtt_topic_tx = "/LED0/Tx"
mqtt_topic_rx = "/LED0/Rx"


class LEDTask(Process):
    def __init__(self, led_brightness, command, wait_s, **value):
        Process.__init__(self)
        self._led_brightness = led_brightness
        self._command = command
        self._wait_s = wait_s
        self._value = value

    def run(self):
        logging.debug("Wait %d seconds" % self._wait_s)
        time.sleep(self._wait_s)
        return getattr(self, self._command, self.run)()

    def system_control(self):
        logging.debug("system_control")
        try:
            led = LEDDriver(self._led_brightness)
            if self._value["cmd"] == "PowerON":
                led.scroll_text_display("hello", random.randrange(0, 0xFFFFFF, 1), 0.2)
            elif self._value["cmd"] == "PowerOFF":
                led.power_off()
            elif self._value["cmd"] == "":
                led.change_brightness(self._led_brightness)
            else:
                logging.debug("Command error")
        except Exception as e:
            logging.error(e)

    def mode0(self):
        try:
            logging.debug("mode0")
            led = LEDDriver(self._led_brightness)
            led.set_color(**self._value)
        except Exception as e:
            logging.error(e)

    def mode1(self):
        try:
            logging.debug("mode1")
            led = LEDDriver(self._led_brightness)
            led.scroll_text_display(self._value["str"])
        except Exception as e:
            logging.error(e)

    def mode2(self):
        try:
            logging.debug("mode2")
            led = LEDDriver(self._led_brightness)
            if self._value["effect"] == "effect01":
                led.scroll_text_display("hello")
            elif self._value["effect"] == "effect02":
                led.color_random(display_time=1)
            elif self._value["effect"] == "effect03":
                led.color_wipe()
            else:
                logging.debug("Command error")
        except Exception as e:
            logging.error(e)


if __name__ == '__main__':
    mq = MyMQTTClient("192.168.1.111", 1883)
    mq.connect()
    mq.run()
