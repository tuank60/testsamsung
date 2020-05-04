#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import threading
import paho.mqtt.client as mqtt
import mqttSub
import time
import json
from ble import models

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def mosquitto_mqtt_sub():
    print("1")
    #CLOUD_URL = '192.168.43.94'
    # CLOUD_URL = '107.113.169.14'
    CLOUD_URL = '192.168.1.15'
    TOPIC = '/gateway'
    PORT = 1883
    client = mqtt.Client()
    client.connect(CLOUD_URL, PORT)
    #client.username_pw_set(username="stp", password="anhtuan1997")
    client.on_connect = mqttSub.on_connect
    client.on_message = mqttSub.on_message
    client.subscribe(TOPIC, 0)
    rc = 0
    while rc == 0:
        rc = client.loop()
    print('Result code: ' + str(rc))

def mosquitto_mqtt_sub_user():
    print("1")
    # CLOUD_URL = '192.168.43.94'
    # CLOUD_URL = '107.113.169.14'
    CLOUD_URL = '192.168.1.15'
    TOPIC = '/user'
    PORT = 1883
    client = mqtt.Client()
    client.connect(CLOUD_URL, PORT)
    #client.username_pw_set(username="stp", password="anhtuan1997")
    client.on_connect = mqttSub.on_connect
    client.on_message = mqttSub.on_message
    client.subscribe(TOPIC, 0)
    rc = 0
    while rc == 0:
        rc = client.loop()
    print('Result code: ' + str(rc))

def mosquitto_mqtt_pub():
    data = {"rssi": 1}
    CLOUD_URL = '107.113.169.14'
    TOPIC = '/test'
    PORT = 1883
    client = mqtt.Client()
    client.connect(CLOUD_URL, PORT)
    client.publish(TOPIC, json.dumps(data))

def Test():
    a = models.DevicesGateway.object.filter(device_name = "aaa")
    print(a.device_name)

if __name__ == '__main__':
    # mqttSubThread = threading.Thread(target=mosquitto_mqtt_sub)
    # mqttSubThreaduser = threading.Thread(target=mosquitto_mqtt_sub_user)
    # mainThread = threading.Thread(target=main)
    # mqttSubThread.start()
    # mqttSubThreaduser.start()
    # mainThread.start()
    # mqttSubThread.join()
    # mqttSubThreaduser.join()
    # mainThread.join()
    # mosquitto_mqtt_sub()
    #mosquitto_mqtt_pub()
    main()
    #Test()

# python manage.py runserver --noreload