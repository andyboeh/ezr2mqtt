#!/usr/bin/env python

import requests
from xml.etree import ElementTree
from pyezr import HeatArea
from pyezr import IoDevice
from pyezr import HeatCtrl

class pyezr():
    def __init__(self, hostname):
        self.hostname = hostname
        self.objects = {}
        self.objects['heatareas'] = []
        self.objects['heatctrls'] = []
        self.objects['iodevices'] = []
        self.id = ""
        self.coolingMode = False
        
    def refresh(self):
        self.connect()

    def save(self):
        for item in ['heatareas', 'heatctrls', 'iodevices']:
            for obj in self.objects[item]:
                if obj.savePending:
                    self.sendRequest(obj.getSaveXml())
                    obj.sent()
                    
    def sendRequest(self, xml):
        url = 'http://' + self.hostname + '/data/changes.xml'
        print(xml)
        response = requests.post(url, data = xml, headers={'Connection':'close'})
        print(response.content)
        return True

    def map(self):
        for heatarea in self.objects['heatareas']:
            heatarea.clearIoDevices()
            heatarea.clearHeatCtrls()

        for heatctrl in self.objects['heatctrls']:
            number = heatctrl.getHeatArea()
            heatarea = self.getHeatAreaByNumber(number)
            if heatarea:
                heatarea.addHeatCtrl(heatctrl)
                
        for iodevice in self.objects['iodevices']:
            number = iodevice.getHeatArea()
            heatarea = self.getHeatAreaByNumber(number)
            if heatarea:
                heatarea.addIoDevice(iodevice)

    def connect(self):
        url = 'http://' + self.hostname + '/data/static.xml'
        response = requests.get(url, headers={'Connection':'close'})
        tree = ElementTree.fromstring(response.content)
        device = tree.find('Device')
        if not device:
            return False
        
        self.id = device.find('ID').text
        name = device.find('NAME').text
        
        self.parseCoolingMode(device)
        
        self.objects['heatareas'].clear()
        heatareas = device.findall('HEATAREA')
        for heatarea in heatareas:
            self.objects['heatareas'].append(HeatArea.HeatArea(heatarea, self.id))
        
        self.objects['iodevices'].clear()
        iodevices = device.findall('IODEVICE')
        for iodevice in iodevices:
            self.objects['iodevices'].append(IoDevice.IoDevice(iodevice, self.id))
        
        self.objects['heatctrls'].clear()
        heatctrls = device.findall('HEATCTRL')
        for heatctrl in heatctrls:
            self.objects['heatctrls'].append(HeatCtrl.HeatCtrl(heatctrl, self.id))
            
        self.map()
        
        return True
        
    def parseCoolingMode(self, xml):
        if xml.find('COOLING').text == '1':
            self.coolingMode = True
        else:
            self.coolingMode = False
        
    def getCoolingMode(self):
        return self.coolingMode
        
    def createVirtualRoom(self, zone):
        devices = ElementTree.Element('Devices')
        device = ElementTree.SubElement(devices, 'Device')
        
        cmd = ElementTree.SubElement(device, 'COMMAND')
        cmd.text = 'CMD_CREATE_XMLDEVICE:' + str(zone)
        xml = '<?xml version="1.0" encoding="UTF-8"?>' + ElementTree.tostring(devices).decode()
        return self.sendRequest(xml)
        
    def addZoneToVirtualRoom(self, devid, zone):
        devices = ElementTree.Element('Devices')
        device = ElementTree.SubElement(devices, 'Device')
        
        cmd = ElementTree.SubElement(device, 'COMMAND')
        cmd.text = 'CMD_CONNECT_XMLDEVICE:' + str(devid) + ',' + str(zone)
        xml = '<?xml version="1.0" encoding="UTF-8"?>' + ElementTree.tostring(devices).decode()
        return self.sendRequest(xml) 
        
    def deleteVirtualRoom(self, devid):
        devices = ElementTree.Element('Devices')
        device = ElementTree.SubElement(devices, 'Device')
        
        cmd = ElementTree.SubElement(device, 'COMMAND')
        cmd.text = 'CMD_DELETE_XMLDEVICE:' + str(devid)
        xml = '<?xml version="1.0" encoding="UTF-8"?>' + ElementTree.tostring(devices).decode()
        return self.sendRequest(xml) 
        
    def getHeatAreas(self):
        return self.objects['heatareas']
        
    def getIoDevices(self):
        return self.objects['iodevices']
        
    def getHeatCtrls(self):
        return self.objects['heatctrls']
        
    def getHeatAreaByNumber(self, number):
        for heatarea in self.objects['heatareas']:
            if heatarea.getNumber() == number:
                return heatarea

        return None
        
    def getPrograms(self):
        pass
        
