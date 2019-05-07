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
import json
import paho.mqtt.client
from multiprocessing import Process
from ws2812b import *

logging.getLogger().setLevel(logging.DEBUG)


class MyMQTTClient(object):
    def __init__(self, hostname, port, client_id='', username='', password=''):
        self._hostname = hostname
        self._port = port
        self._username = username
        self._password = password
        self._client = paho.mqtt.client.Client(client_id)
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message

    def _on_connect(self, client, userdata, flags, rc):
        logging.info("MQTT connected with result code " + str(rc))
        self._client.subscribe("/MyLED")

    def _on_message(self, client, userdata, msg):
        var = json.loads(msg.payload.decode("utf-8"))
        logging.debug(var)
        task = LEDTask(var["Brightness"], var["Command"], var["Wait_s"], **var["Value"])
        task.daemon = True
        task.start()

    def connect(self):
        self._client.connect(self._hostname, self._port)
        self._client.username_pw_set(self._username, self._password)

    def run(self):
        self._client.loop_forever()
