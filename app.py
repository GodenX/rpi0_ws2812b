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
command_list = ("system_control", "mode0", "mode1", "mode2", "wait_command")


class LEDTask(Process):
    def __init__(self, led_brightness, command, wait_s, **value):
        global command_list
        Process.__init__(self)
        self._led_brightness = led_brightness
        if command in command_list:
            self._command = command
        else:
            self._command = "command_error"
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
                self.wait_command()
            elif self._value["cmd"] == "PowerOFF":
                led.power_off()
            elif self._value["cmd"] == "SystemHalt":
                os.popen("halt")
            elif self._value["cmd"] == "SystemReboot":
                os.popen("reboot")
            else:
                self.command_error()
        except Exception as e:
            logging.error(e)
            self.command_error()

    def mode0(self):
        logging.debug("mode0")
        try:
            led = LEDDriver(self._led_brightness)
            led.set_color(**self._value)
        except Exception as e:
            logging.error(e)
            self.command_error()

    def mode1(self):
        logging.debug("mode1")
        try:
            led = LEDDriver(self._led_brightness)
            led.scroll_text_display(self._value["str"])
        except Exception as e:
            logging.error(e)
            self.command_error()

    def mode2(self):
        logging.debug("mode2")
        try:
            led = LEDDriver(self._led_brightness)
            if self._value["effect"] == "effect01":
                while True:
                    led.scroll_text_display("HELLO")
            elif self._value["effect"] == "effect02":
                while True:
                    led.color_random(display_time=1)
            elif self._value["effect"] == "effect03":
                while True:
                    led.color_wipe()
            else:
                self.command_error()
        except Exception as e:
            logging.error(e)
            self.command_error()

    def wait_command(self):
        logging.debug("wait_command")
        try:
            led = LEDDriver(self._led_brightness)
            while True:
                led.color_random(display_time=1)
        except Exception as e:
            logging.error(e)
            self.command_error()

    def command_error(self):
        logging.error("Command error!")


if __name__ == '__main__':
    mq = MyMQTTClient("127.0.0.1", 1883)
    mq.connect()
    mq.run()
