#!/usr/bin/env python

class IoDevice():
    def __init__(self, xml, id): 
        self.xml = xml
        self.id = id
        self.savePending = False
        
    def getNumber(self):
        return self.xml.attrib['nr']
        
    def getName(self):
        return self.xml.find('HEATAREA_NAME').text
        
    def getHeatArea(self):
        return self.xml.find('HEATAREA_NR').text

    def getIoDeviceType(self):
        return self.xml.find('IODEVICE_TYPE').text
        
    def getIoDeviceId(self):
        return self.xml.find('IODEVICE_ID').text
        
    def getState(self):
        return self.xml.find('IODEVICE_STATE').text
        
    def getIsOn(self):
        return self.xml.find('ISON').text
