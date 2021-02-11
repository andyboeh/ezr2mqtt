#!/usr/bin/env python
# (c) 2021 Andreas Böhler
# License: Apache 2.0

import paho.mqtt.client as mqtt
import json
import yaml
import os
import sys
import requests
import time
from pyezr import pyezr
from threading import Thread

if not os.path.exists('config.yaml'):
    print('Configuration file "config.yaml" not found, exiting.')
    sys.exit(1)

fp = open('config.yaml', 'r')
config = yaml.safe_load(fp)
print(config)

commandlist = []

class EzrSetTemperatureCommand:
    def __init__(self, ezr, heatarea, target):
        self.ezr = ezr
        self.heatarea = heatarea
        self.target = target
        
class EzrSetHoldStateCommand:
    def __init__(self, ezr, heatarea, state):
        self.ezr = ezr
        self.heatarea = heatarea
        self.state = state

# Define MQTT event callbacks
def on_connect(client, userdata, flags, rc):
    connect_statuses = {
        0: "Connected",
        1: "incorrect protocol version",
        2: "invalid client ID",
        3: "server unavailable",
        4: "bad username or password",
        5: "not authorised"
    }
    print("MQTT: " + connect_statuses.get(rc, "Unknown error"))

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection")
    else:
        print("Disconnected")

def on_message(client, obj, msg):
    print("Msg: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    topic = msg.topic.replace(config['mqtt']['topic'] + '/', '')
    name, command = topic.split('/')
    prefix, heatarea = name.split('_')
    if command == 'set_temperature':
        print('set_temperature')
        commandlist.append(EzrSetTemperatureCommand(prefix, heatarea, msg.payload.decode('ascii')))
        mqttc.publish(config['mqtt']['topic'] + "/" + name + "/target_temperature", payload=msg.payload, retain=True)
    elif command == 'set_hold':
        print('set_hold')
        mode = msg.payload.decode('ascii')
        hmode = '0'
        if mode == 'auto':
            hmode = '0'
        elif mode == 'day':
            hmode = '1'
        elif mode == 'night':
            hmode = '2'
        commandlist.append(EzrSetHoldStateCommand(prefix, heatarea, hmode))

        mqttc.publish(config['mqtt']['topic'] + "/" + name + "/hold_state", payload='\"' + mode + '\"', retain=True)

def on_publish(client, obj, mid):
    print("Pub: " + str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, obj, level, string):
    print(string)

def get_ezr_data():
    ezrs = config['ezr']

    result = {}

    for ii in range(0, len(ezrs)):
        dev = config['ezr'][ii]['host']
        ezr = pyezr.pyezr(config['ezr'][ii]['host'])
        if not dev in result:
            result[dev] = {}
        result[dev]['name'] = config['ezr'][ii]['name']
        result[dev]['id'] = config['ezr'][ii]['prefix']
        try:
            if ezr.connect():
                result[dev]['status'] = 'ok'
            else:
                result[dev]['status'] = 'error'
                continue
        except:
            result[dev]['status'] = 'error'
            continue

        heatareas = ezr.getHeatAreas()

        ha_names = []
        for ha in heatareas:
            ha_name = ha.getName()
            result[dev][ha_name] = {}
            result[dev][ha_name]['number'] = ha.getNumber()
            result[dev][ha_name]['min_temperature'] = ha.getMinTemperature()
            result[dev][ha_name]['max_temperature'] = ha.getMaxTemperature()
            result[dev][ha_name]['actual_temperature'] = ha.getActualTemperature()
            result[dev][ha_name]['target_temperature'] = ha.getTargetTemperature()
            result[dev][ha_name]['mode'] = ha.getMode()
            ha_names.append(ha_name)
        result[dev]['heatareas'] = ha_names

        for command in commandlist:
            if command.ezr == config['ezr'][ii]['prefix']:
                for ha in heatareas:
                    save = False
                    if ha.getNumber() == command.heatarea:
                        if isinstance(command, EzrSetTemperatureCommand):
                            if command.target != ha.getTargetTemperature():
                                ha.setTargetTemperature(command.target)
                                result[dev][ha.getName()]['target_temperature'] = command.target
                                save = True
                        elif isinstance(command, EzrSetHoldStateCommand):
                            if command.state != ha.getMode():
                                ha.setMode(command.state)
                                result[dev][ha.getName()]['mode'] = command.state
                                save = True
                        
                        if save:
                            try:
                                ezr.save()
                            except:
                                print('Error saving to EZR')
                            save = False
                        commandlist.remove(command)
    return result

# Setup MQTT connection
mqttc = mqtt.Client()

mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_disconnect = on_disconnect
mqttc.on_message = on_message

if config['mqtt']['debug']:
    print("Debugging messages enabled")
    mqttc.on_log = on_log    
    mqttc.on_publish = on_publish

mqttc.connect(config['mqtt']['host'], config['mqtt']['port'], 60)
mqttc.loop_start()


# Set up discovery structure

firsttime = True

while True:
    if config['mqtt']['debug']:
        print('Poll...')
    data = get_ezr_data()
    if config['mqtt']['debug']:
        print(data)

    for dev in data:
        if data[dev]['status'] == 'ok':
            heatareas = data[dev]['heatareas']
            for heatarea in heatareas:
                identifier = data[dev]['id'] + '_' + data[dev][heatarea]['number']
                dtopic = config['mqtt']['discovery_prefix'] + '/climate/' + \
                         identifier + '/config'
                topic = config['mqtt']['topic'] + '/' + identifier
                name = heatarea
                mqttc.publish(topic + "/current_temperature", payload=data[dev][heatarea]['actual_temperature'], retain=True)
                mqttc.publish(topic + "/target_temperature", payload=data[dev][heatarea]['target_temperature'], retain=True)
                mode = data[dev][heatarea]['mode']
                # 1 is actually day, 2 is actually night, but this is not
                # supported by Home Assistant
                pmode = '\"off\"'
                hmode = '\"auto\"'
                if mode == '0':
                    hmode = '\"auto\"'
                    pmode = '\"auto\"'
                elif mode == '1':
                    hmode = '\"day\"'
                    pmode = '\"auto\"'
                elif mode == '2':
                    hmode = '\"night\"'
                    pmode = '\"auto\"'
                elif mode == '3':
                    hmode = '\"auto\"'
                    pmode = '\"off\"'
                mqttc.publish(topic + "/mode", payload=pmode, retain=True)
                mqttc.publish(topic + "/hold_state", payload=hmode, retain=True)
                
                
                if firsttime:
                    payload = {
                        "current_temperature_topic" : topic + "/current_temperature",
                        "name" : name,
                        "temperature_command_topic" : topic + "/set_temperature",
                        "temperature_state_topic" : topic + "/target_temperature",
                        "temperature_unit" : "C",
                        "temp_step" : 0.1,
                        "max_temp" : data[dev][heatarea]['max_temperature'],
                        "min_temp" : data[dev][heatarea]['min_temperature'],
                        "modes" : [
                            "auto",
                            "off",
                        ],
                        "mode_state_topic" : topic + "/mode",
                        "mode_state_template" : "{{ value_json }}",
                        "hold_command_topic" : topic + "/set_hold",
                        "hold_state_topic" : topic + "/hold_state",
                        "hold_state_template" : "{{ value_json }}",
                        "hold_modes" : [
                            "auto",
                            "day",
                            "night",
                        ],
                        "unique_id" : identifier,
                        "precision" : 0.1,
                        "value_template" : "{{ value_json }}",
                        "device" : {
                            "identifiers" : data[dev]['id'],
                            "manufacturer" : "Möhlenhoff",
                            "model" : "Alpha 2",
                            "name" : data[dev]['name'],
                        },
                    }
                    payload = json.dumps(payload)
                    mqttc.subscribe(topic + "/set_temperature")
                    mqttc.subscribe(topic + "/set_hold")
                    mqttc.publish(dtopic, payload=payload, retain=True)

    firsttime = False
    if config['mqtt']['debug']:
        print('Done.')
    time.sleep(config['general']['interval'])

