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
import time
from multiprocessing import Process, Queue
import mqtt_client
import ws2812b

logging.getLogger().setLevel(logging.DEBUG)
command_list = ("system_control", "mode0", "mode1", "mode2")


class LEDTask(Process):
    def __init__(self, queue, command, wait_s, brightness, **value):
        Process.__init__(self)
        self.queue = queue
        if command in command_list:
            self.command = command
        else:
            self.command = "command_error"
        self.wait_s = wait_s
        if (brightness >= 0) and (brightness <= 48):
            self.brightness = brightness
        else:
            self.brightness = 48
        self.value = value

    def run(self):
        logging.debug("Wait %d seconds" % self.wait_s)
        time.sleep(self.wait_s)
        return getattr(self, self.command, self.run)()

    def system_control(self):
        logging.debug("system_control")
        try:
            if self.value["cmd"] == "PowerON":
                display_obj = ws2812b.LEDDriver(self.queue)
                display_obj.start_with_white_color(self.brightness)
            elif self.value["cmd"] == "PowerOFF":
                display_obj = ws2812b.LEDDriver(self.queue)
                display_obj.clear_display()
            elif self.value["cmd"] == "SystemHalt":
                os.popen("halt")
            elif self.value["cmd"] == "SystemReboot":
                os.popen("reboot")
            else:
                self.command_error()
        except Exception as e:
            self.command_error(str(e))

    def mode0(self):
        logging.debug("mode0")
        try:
            display_obj = ws2812b.LEDDriver(self.queue)
            display_obj.clear_display()
            display_obj.set_color(self.brightness, **self.value)
        except Exception as e:
            self.command_error(str(e))

    def mode1(self):
        logging.debug("mode1")
        try:
            display_obj = ws2812b.LEDDriver(self.queue)
            display_obj.clear_display()
            while True:
                if "color" in self.value:
                    if (self.value["color"] >= 0) and (self.value["color"] <= 0xFFFFFF):
                        display_obj.scroll_text_display(self.value["str"], self.brightness, self.value["color"])
                    else:
                        display_obj.scroll_text_display(self.value["str"], self.brightness)
                else:
                    display_obj.scroll_text_display(self.value["str"], self.brightness)
        except Exception as e:
            self.command_error(str(e))

    def mode2(self):
        logging.debug("mode2")
        try:
            display_obj = ws2812b.LEDDriver(self.queue)
            display_obj.clear_display()
            if self.value["effect"] == "effect01":
                while True:
                    display_obj.scroll_text_display("HELLO WORLD", self.brightness)
            elif self.value["effect"] == "effect02":
                while True:
                    display_obj.color_random_change_brightness()
            elif self.value["effect"] == "effect03":
                while True:
                    display_obj.color_wipe(self.brightness)
            else:
                self.command_error()
        except Exception as e:
            self.command_error(str(e))

    @staticmethod
    def command_error(e="command not in list!"):
        logging.error("Command error: %s" % e)


if __name__ == '__main__':
    queue = Queue()
    led_process = ws2812b.LEDIOFunc(queue)
    led_process.daemon = True
    led_process.start()
    mq = mqtt_client.MyMQTTClient("127.0.0.1", 1883, queue)
    mq.connect()
    mq.run()
