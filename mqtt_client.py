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
import app
import ws2812b

mqtt_topic_tx = "/LED/Tx"
mqtt_topic_rx = "/LED/Rx"


class MyMQTTClient(object):
    def __init__(self, hostname, port, queue, client_id='', username='', password=''):
        self._hostname = hostname
        self._port = port
        self.queue = queue
        self._username = username
        self._password = password
        self._client = paho.mqtt.client.Client(client_id)
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message

        self._task = app.LEDTask(task_queue=self.queue, command="system_control", wait_s=0, **{"cmd": "PowerON"})
        self._task.daemon = True
        self._task.start()

    def _on_connect(self, client, userdata, flags, rc):
        logging.info("MQTT connected with result code " + str(rc))
        self._client.subscribe(mqtt_topic_rx)

    def _on_message(self, client, userdata, msg):
        try:
            var = json.loads(msg.payload.decode("utf-8"))
            logging.debug(var)
            led_cb = {"brightness": var["Brightness"]}
            self.queue.put(led_cb)
            if "change_brightness" in var["Command"]:
                pass
            else:
                self._task.terminate()
                self._task.join()
                self._task = app.LEDTask(task_queue=self.queue, command=var["Command"], wait_s=var["Wait_s"],
                                         **var["Value"])
                self._task.daemon = True
                self._task.start()
        except Exception as e:
            logging.error(e)
            self._client.publish(mqtt_topic_tx, payload=str(e), qos=0, retain=False)

    def connect(self):
        self._client.connect(self._hostname, self._port)
        self._client.username_pw_set(self._username, self._password)

    def pub(self, topic, msg):
        self._client.publish(topic, payload=msg, qos=0, retain=False)

    def run(self):
        self._client.loop_forever()
