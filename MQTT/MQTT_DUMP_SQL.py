# -*- coding: utf-8 -*-
"""
Created on Mon May 10 16:26:19 2021

@author: Jan Nielsen
"""
import paho.mqtt.client as mqtt
import sqlite3
import sys
import time
import json
import os
from datetime import datetime
from queue import Queue


# the following function "on_*" are callback for the MQTT loop.
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True
        print("Connected OK")
             
    else:
        print("Bad connection, Returned code: "+str(rc))
        client.bad_connection_flag=True
        
def on_disconnect(client, userdata, flags, rc=0):
    print("disconnecting reason  "  +str(rc))
    client.connected_flag=False
    client.disconnect_flag=True

def on_log(client, userdata, level, buf):
    if buf != 'PINGREQ' or buf != 'PINGRESP':
        print("Log: ", buf)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribe, mID value: "+ str(mid))
    for t in topics_ack:
        if t[1]==mid:
            t[2]=1
            print("Subscription acknowledged "+ t[0])
    
def on_unsubscribe(client, userdata, mid):
    print("Unsubscribed, mID value: ", str(mid))

def on_message(client, userdata, msg):
    print("Message received:")
    q.put(msg)
    
#Checking for MQTT subscriptions
def subscribe_topics(client, topics):
    for t in topics:
        try:
            r=client.subscribe(t)
            if r[0]!=0:
                print("Error on subscribing "+str(t[0]))
                return -1
            print("Subscribe "+ str(t) +". Return Code "+str(r))
        except Exception as e:
            print("Error Code: "+str(e))
            return -1
        topics_ack.append([t[0],r[1],0])
    print("All subscriptions complete.")
    return 0

def check_subs():
    for t in topics_ack:
        if t[2]==0:
            print("Subscription to "+t[0]+" not acknowledged.")
            return False
    return True

def wait_for(client, msgType, period=0.25):
    if msgType == "CHECKSUBS":
        if check_subs:
            print("Waiting for subsriptions approval")
            lcount = 0
            client.loop()
            while not check_subs():                
                print("Waiting for subscriptions approval")
                time.sleep(period)
                if lcount > 20:
                    return False
        return True



##################################################################################
#Varibles for the program

q = Queue()   
now = datetime.now() 

mqtt.Client.connected_flag=False
mqtt.Client.bad_connection_flag=False
mqtt.Client.disconnect_flag=False

#For Windows
MQTT_BROKER = os.environ.get('MQTT_BROKER')
MQTT_USER = os.environ.get('MQTT_USER')
MQTT_PASS = os.environ.get('MQTT_PASS')

port = 8883


client = mqtt.Client("ioTrace_test")
client.username_pw_set(username=MQTT_USER, password=MQTT_PASS)

#For debuging
#client.on_log = on_log

client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscribe
client.on_disconnect = on_disconnect
client.on_message = on_message

topics=[]
topics_ack=[]

path = "C:/Users/Jwalkern/Desktop/MQTT_MSG2.txt"
database = "D:/Git_projects/iotrace/webapplikation/iotrace/site.db"


##################################################################################
#The program
#Connectin to broker
print("#######################################################################")
try:
    print("Connecting to broker: ", MQTT_BROKER)
    client.connect(MQTT_BROKER, 8883)
       
except Exception:
    print("Failed to connect")
    sys.exit(1)
    
#Check if connection is OK
client.loop_start()    
while not client.connected_flag and not client.bad_connection_flag:
    print("In wait loop")
    time.sleep(1)
    
    if client.bad_connection_flag:
        client.loop_stop()
        sys.exit(1)

print("#######################################################################")
#Get subscriptions, add to topics list
con = sqlite3.connect(database)
cur = con.cursor()
for row in cur.execute('SELECT * FROM xtel'):
    topics.append(("uts/"+row[1], 0))
con.close()

#Subscribe to topics
if client.connected_flag:
    print("Subscribing to " + str(topics))
    if subscribe_topics(client, topics) == -1:
        print("Can't subscribe, quitting")
        client.bad_connection_flag=True
        loopFlag=False
    else:
        time.sleep(1)
        ret=wait_for(client, "CHECKSUBS")
        if not ret:
            print("All subscriptions not complete, quitting")
            client.loop_stop()
            sys.exit(1)
        print("All subscriptions OK")

    
print("#######################################################################")    

print("Press 'ctrl+C' to exit the program.")

try:
    loopFlag=True
    while loopFlag:
        while not q.empty():
            message = q.get()
            if message is None:
                continue
            print(now.strftime("%d/%m/%Y %H:%M:%S"))
            print("Received message from queue: ")
            
            device_mac = message.topic.replace("uts/", "")
            json_obj = json.loads(message.payload.decode("utf-8"))
            
            print("--------- Message to MySQL START---------")
            con = sqlite3.connect(database)
            cur = con.cursor()
            
            for item in json_obj:
                if item == 'ts':
                    timestamp = datetime.strptime(json_obj.get(item).translate({ord(i): '' for i in 'TZ'}), '%Y-%m-%d%H:%M:%S.%f').strftime(('%Y-%m-%d %H:%M:%S'))
                    
                if item == 'data':
                    try:
                        volt = json_obj["data"]["volt"]
                        alarm_1 = json_obj["data"]["alarm_1"]
                        alarm_2 = json_obj["data"]["alarm_2"]
                        lte_rssi = json_obj["data"]["lte_rssi"]
                        print(device_mac)
                        print(timestamp, volt, alarm_1, alarm_2, lte_rssi)
                        cur.execute("INSERT INTO device_data (device_mac, timestamp, volt, alarm_1, alarm_2, lte_rssi) VALUES (?, ?, ?, ?, ?, ?)", (device_mac, timestamp, volt, alarm_1, alarm_2, lte_rssi))
                        
                    except:
                        volt = json_obj["data"]["volt"]
                        temp = json_obj["data"]["temp"]
                        hpa = json_obj["data"]["hpa"]
                        lte_rssi = json_obj["data"]["lte_rssi"]
                        humid = json_obj["data"]["humid"]
                        geo = json_obj["data"]["geo"]
                        print(device_mac)
                        print(timestamp, volt, temp, hpa, lte_rssi, humid, geo)
                        cur.execute("INSERT INTO device_data (device_mac, timestamp, volt, temp, hpa, humid, geo, lte_rssi) VALUES (?, ?, ?, ?, ?, ?, ? ,?)", (device_mac, timestamp, volt, temp, hpa, humid, geo, lte_rssi))
            con.commit()
            con.close()
            print("--------- Message to MySQL END--------")

                
        time.sleep(1)
        

except KeyboardInterrupt:
    print("shutdown sent")
    
except Exception as e:
    print(e)
    
finally:
    print("Unsubscribing: " +str(topics))
    for t in topics:
        client.unsubscribe(t[0])
    time.sleep(5)       
    client.loop_stop()
    print("Shutdown")
    sys.exit()
