#!/usr/bin/env python

from xml.etree import ElementTree

class HeatArea():
    def __init__(self, xml, id): 
        self.id = id
        self.xml = xml
        self.iodevices = []
        self.heatctrls = []
        self.savePending = False
        self.tagsToSave = {}
        
    def getNumber(self):
        return self.xml.attrib['nr']
        
    def getName(self):
        return self.xml.find('HEATAREA_NAME').text
        
    def getActualTemperature(self):
        if 'T_ACTUAL' in self.tagsToSave:
            return self.tagsToSave['T_ACTUAL']
        return self.xml.find('T_ACTUAL').text
        
    def setActualTemperature(self, val):
        self.savePending = True
        self.tagsToSave['T_ACTUAL'] = str(val)
        
    def setTargetTemperature(self, val):
        self.savePending = True
        self.tagsToSave['T_TARGET'] = str(val)

    def getSaveXml(self):
        devices = ElementTree.Element('Devices')
        device = ElementTree.SubElement(devices, 'Device')
        id = ElementTree.SubElement(device, 'ID')
        id.text = self.id
        ha = ElementTree.SubElement(device, 'HEATAREA', nr = self.getNumber())
        for tag in self.tagsToSave:
            node = ElementTree.SubElement(ha, tag)
            node.text = self.tagsToSave[tag]
        return '<?xml version="1.0" encoding="UTF-8"?>' + ElementTree.tostring(devices).decode()

    def sent(self):
        self.tagsToSave = {}
        self.savePending = False

    def setMode(self, mode):
        self.savePending = True
        self.tagsToSave['HEATAREA_MODE'] = str(mode)

    def getMode(self):
        if 'HEATAREA_MODE' in self.tagsToSave:
            return self.tagsToSave['HEATAREA_MODE']
        return self.xml.find('HEATAREA_MODE').text

    def getTargetTemperature(self):
        if 'T_TARGET' in self.tagsToSave:
            return self.tagsToSave['T_TARGET']
        return self.xml.find('T_TARGET').text
        
    def getMinTemperature(self):
        return self.xml.find('T_TARGET_MIN').text
        
    def getMaxTemperature(self):
        return self.xml.find('T_TARGET_MAX').text
        
    def getState(self):
        return self.xml.find('HEATAREA_STATE').text
        
    def getIoDevices(self):
        return self.iodevices
        
    def getHeatCtrls(self):
        return self.heatctrls
        
    def clearHeatCtrls(self):
        self.heatctrls.clear()
        
    def clearIoDevices(self):
        self.iodevices.clear()
        
    def addIoDevice(self, device):
        self.iodevices.append(device)
        
    def addHeatCtrl(self, heatctrl):
        self.heatctrls.append(heatctrl)
