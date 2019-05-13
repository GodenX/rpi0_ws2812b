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
import os, re
from multiprocessing import Process
from mqtt_client import *
from ws2812b import *

mqtt_topic_tx = "/LED0/Tx"
mqtt_topic_rx = "/LED0/Rx"
command_list = ("system_control", "mode0", "mode1", "mode2", "wait_command")
led_brightness_default = 0.8


class LEDTask(Process):
    def __init__(self, command, wait_s, led_object, **value):
        global command_list
        Process.__init__(self)
        if command in command_list:
            self._command = command
        else:
            self._command = "command_error"
        self._wait_s = wait_s
        self._value = value
        self._led = led_object

    def run(self):
        logging.debug("Wait %d seconds" % self._wait_s)
        time.sleep(self._wait_s)
        return getattr(self, self._command, self.run)()

    def system_control(self):
        logging.info("system_control")
        try:
            if self._value["cmd"] == "PowerON":
                self.wait_command()
            elif self._value["cmd"] == "PowerOFF":
                self._led.power_off()
            elif "Brightness:" in self._value["cmd"]:
                var = re.search(r"\d{1,2}", self._value["cmd"])
                brightness = int(var.group())
                self._led.change_brightness(brightness)
            elif self._value["cmd"] == "SystemHalt":
                os.popen("halt")
            elif self._value["cmd"] == "SystemReboot":
                os.popen("reboot")
            else:
                self.command_error()
        except Exception as e:
            self.command_error(str(e))

    def mode0(self):
        logging.info("mode0")
        try:
            self._led.set_color(**self._value)
        except Exception as e:
            self.command_error(str(e))

    def mode1(self):
        logging.info("mode1")
        try:
            self._led.scroll_text_display(self._value["str"])
        except Exception as e:
            self.command_error(str(e))

    def mode2(self):
        logging.info("mode2")
        try:
            if self._value["effect"] == "effect01":
                while True:
                    self._led.scroll_text_display("HELLO")
            elif self._value["effect"] == "effect02":
                while True:
                    for i in range(0, 49):
                        self._led.change_brightness(i)
                        self._led.color_random(display_time=0.003)
                    for i in range(48, -1, -1):
                        self._led.change_brightness(i)
                        self._led.color_random(display_time=0.003)
            elif self._value["effect"] == "effect03":
                while True:
                    self._led.color_wipe()
            else:
                self.command_error()
        except Exception as e:
            self.command_error(str(e))

    def wait_command(self):
        logging.info("wait_command")
        try:
            while True:
                self._led.color_random(display_time=1)
        except Exception as e:
            self.command_error(str(e))

    def command_error(self, e="command not in list!"):
        logging.error("Command error: %s" % e)


if __name__ == '__main__':
    led = LEDDriver(led_brightness_default)
    mq = MyMQTTClient("127.0.0.1", 1883, led)
    mq.connect()
    mq.run()
