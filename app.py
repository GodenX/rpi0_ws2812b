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
import paho.mqtt.client as mqtt

# from ws2812b import *

logging.getLogger().setLevel(logging.DEBUG)


class MyMQTTClient(object):
    def __init__(self, hostname, port, client_id='', username='', password=''):
        self._hostname = hostname
        self._port = port
        self._username = username
        self._password = password
        self._client = mqtt.Client(client_id)
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message

    def _on_connect(self, client, userdata, flags, rc):
        logging.info("MQTT connected with result code " + str(rc))
        self._client.subscribe("/MyLED")

    def _on_message(self, client, userdata, msg):
        var = json.loads(msg.payload.decode("utf-8"))
        logging.debug(var["Lightness"])

    def connect(self):
        self._client.connect(self._hostname, self._port)
        self._client.username_pw_set(self._username, self._password)

    def run(self):
        self._client.loop_forever()


if __name__ == '__main__':
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
