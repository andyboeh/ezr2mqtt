#!/usr/bin/env python

class HeatCtrl():
    def __init__(self, xml, id): 
        self.xml = xml
        self.id = id
        self.savePending = False
        
    def getNumber(self):
        return self.xml.attrib['nr']
        
    def getHeatArea(self):
        return self.xml.find('HEATAREA_NR').text
        
    def getActor(self):
        return self.xml.find('ACTOR').text
        
    def getInUse(self):
        return self.xml.find('INUSE').text
        
    def getState(self):
        return self.xml.find('HEATCTRL_STATE').text
        
