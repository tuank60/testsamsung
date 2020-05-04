import os
from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'
application = get_wsgi_application()

from ble import models
import paho.mqtt.client as mqtt
import json
from datetime import datetime


TOPIC = "/test"

# username_pw_set(username="hieu", password="12345678")
def on_connect(client, userdata, flags, rc):
    client.subscribe(TOPIC, 0)
    print("Result code " + str(rc))
    if(rc == 0):
        print("Result code " + str(rc) + ": good connection")
    else:
        print("Result code " + str(rc) + ": authentication error")
# def on_subcribe(client, obj, mid, granted_qos):
#     print("Subscribed: " + str(mid) + " " + str(granted_qos))
def on_log(client, obj, level, string):
    print(string)
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(payload)
    print(msg.topic)
    if msg.topic == '/gateway':
        raw_data = json.loads(payload)
        # try:
        #     devices = models.DevicesGateway.objects.filter(device_name=raw_data["uuid"])[0]
        # except Exception as e:
        #     print("1")
        #     devices = models.DevicesGateway(device_name=raw_data["uuid"],device_description=raw_data["type"])
        #     devices.save()
        #     print(e)
        numberdevices = models.DevicesGateway.objects.filter(device_name=raw_data["uuid"]).count()
        try:
            if numberdevices ==0:
                devices = models.DevicesGateway(device_name=raw_data["uuid"], device_description=raw_data["type"])
                devices.save()
            else:
                devices = models.DevicesGateway.objects.filter(device_name=raw_data["uuid"])[0]
            cnt = models.DataGateway.objects.filter(device_id=devices.device_id).count()
            if cnt==0:
                print(1)
                data = models.DataGateway(device_id_id=devices.device_id, rssi=raw_data["rssi"], deltaA=0,
                                          rssitb=raw_data["rssi"], timestamp=datetime.now())
                data.save()
            else:
                rssi = models.DataGateway.objects.filter(device_id=devices.device_id)[0].rssitb
                print(rssi)
                rssi = (int(raw_data["rssi"])+rssi*cnt)/(cnt+1)
                print("a")
                deltaA = int(raw_data["rssi"]) - rssi
                print("b")
                print("Now RSSI: " + str(rssi))
                data = models.DataGateway(device_id_id=devices.device_id, rssi=raw_data["rssi"],deltaA= deltaA, rssitb=rssi, timestamp=datetime.now())
                data.save()

            # mosquitto_mqtt_pub(rssi)
        except Exception as e:
            print(e)

    if msg.topic == '/user':
        print("aaaa")

def mosquitto_mqtt_pub(rssi):
    data = {"rssi": rssi}
    CLOUD_URL = '107.113.169.14'
    TOPIC = '/test1'
    PORT = 1883
    client = mqtt.Client()
    client.connect(CLOUD_URL, PORT)
    client.publish(TOPIC, json.dumps(data))

# CLOUD_URL = '192.168.43.94'
#
# PORT = 1883
# client = mqtt.Client()
# client.connect(CLOUD_URL,PORT)
#
# client.on_connect = on_connect
# client.on_log = on_log
# client.on_message = on_message
# client.subscribe(TOPIC, 0)
#
# while True:
#     client.loop()


# {"rssi":"-80","uuid":"00000000-0000-0000-0000-000000000003","type":"Real Beacon"}
# {"rssi":"-95","uuid":"00000000-0000-0000-0000-000000000008","type":"Simulated Beacon"}

    # mosquitto_pub.exe - t / test - m “TAPIT”
# "{\"rssi\":\"-80\",\"uuid\":\"00000000-0000-0000-0000-000000000003\",\"type\":\"Real Beacon\"}"