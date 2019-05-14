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
import os
import paho.mqtt.client
from multiprocessing import Queue
from ws2812b import *
from app import *

logging.getLogger().setLevel(logging.INFO)


class MyMQTTClient(object):
    def __init__(self, hostname, port, client_id='', username='', password=''):
        self._hostname = hostname
        self._port = port
        self._username = username
        self._password = password
        self._client = paho.mqtt.client.Client(client_id)
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._task = LEDTask("wait_command", 0, **{"Brightness": 43})
        self._task.daemon = True
        self._task.start()

    def _on_connect(self, client, userdata, flags, rc):
        logging.info("MQTT connected with result code " + str(rc))
        self._client.subscribe(mqtt_topic_rx)

    def _on_message(self, client, userdata, msg):
        try:
            var = json.loads(msg.payload.decode("utf-8"))
            logging.debug(var)
            self._task.terminate()
            self._task.join()
            self._task = LEDTask(var["Command"], var["Wait_s"], **var["Value"])
            self._task.daemon = True
            self._task.start()
        except Exception as e:
            logging.error(e)
            self._client.publish(mqtt_topic_tx, payload=e, qos=0, retain=False)

    def connect(self):
        self._client.connect(self._hostname, self._port)
        self._client.username_pw_set(self._username, self._password)

    def pub(self, topic, msg):
        self._client.publish(topic, payload=msg, qos=0, retain=False)

    def run(self):
        self._client.loop_forever()
