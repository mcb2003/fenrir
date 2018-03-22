#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import time
from fenrirscreenreader.core import debug

class inputManager():
    def __init__(self):
        self.setLedState = True
    def initialize(self, environment):
        self.env = environment
        self.env['runtime']['settingsManager'].loadDriver(\
          self.env['runtime']['settingsManager'].getSetting('keyboard', 'driver'), 'inputDriver')
        self.updateInputDevices()
        # init LEDs with current state
        self.env['input']['newNumLock'] = self.env['runtime']['inputDriver'].getLedState()
        self.env['input']['oldNumLock'] = self.env['input']['newNumLock']
        self.env['input']['newCapsLock'] = self.env['runtime']['inputDriver'].getLedState(1)
        self.env['input']['oldCapsLock'] = self.env['input']['newCapsLock']
        self.env['input']['newScrollLock'] = self.env['runtime']['inputDriver'].getLedState(2)
        self.env['input']['oldScrollLock'] = self.env['input']['newScrollLock']
        self.lastDeepestInput = []
        self.lastInputTime = time.time()
    def shutdown(self):
        self.removeAllDevices()
        self.env['runtime']['settingsManager'].shutdownDriver('inputDriver')
    def  getInputEvent(self):
         return self.env['runtime']['inputDriver'].getInputEvent()
    def handleInputEvent(self, eventData):
        self.env['runtime']['debug'].writeDebugOut('DEBUG INPUT inputMan:'  + str(eventData),debug.debugLevel.INFO)                                               
        if not eventData:
            return
        self.env['input']['prevInput'] = self.env['input']['currInput'].copy()
        if eventData['EventState'] == 0:
            if eventData['EventName'] in self.env['input']['currInput']:
                self.env['input']['currInput'].remove(eventData['EventName'])
                if len(self.env['input']['currInput']) > 1:
                    self.env['input']['currInput'] = sorted(self.env['input']['currInput'])
                elif len(self.env['input']['currInput']) == 0:
                    self.env['input']['shortcutRepeat'] = 1 
                self.setLedState = self.handleLedStates(eventData)                                             
                self.lastInputTime = time.time()                                                   
        elif eventData['EventState'] == 1:
            if not eventData['EventName'] in self.env['input']['currInput']:
                self.env['input']['currInput'].append(eventData['EventName'])
                if len(self.env['input']['currInput']) > 1:
                    self.env['input']['currInput'] = sorted(self.env['input']['currInput'])
                if len(self.lastDeepestInput) < len(self.env['input']['currInput']):
                    self.setLastDeepestInput( self.env['input']['currInput'].copy())
                elif self.lastDeepestInput == self.env['input']['currInput']:
                    if time.time() - self.lastInputTime <= self.env['runtime']['settingsManager'].getSettingAsFloat('keyboard','doubleTapTimeout'):
                        self.env['input']['shortcutRepeat'] += 1
                    else:
                        self.env['input']['shortcutRepeat'] = 1
                self.setLedState = self.handleLedStates(eventData)                                             
                self.lastInputTime = time.time()                                               
        elif eventData['EventState'] == 2:
            self.lastInputTime  = time.time()                                                   

        self.env['input']['oldNumLock'] = self.env['input']['newNumLock']
        self.env['input']['newNumLock'] = self.env['runtime']['inputDriver'].getLedState()
        self.env['input']['oldCapsLock'] = self.env['input']['newCapsLock'] 
        self.env['input']['newCapsLock'] = self.env['runtime']['inputDriver'].getLedState(1)
        self.env['input']['oldScrollLock'] = self.env['input']['newScrollLock'] 
        self.env['input']['newScrollLock'] = self.env['runtime']['inputDriver'].getLedState(2)
        self.env['runtime']['debug'].writeDebugOut("currInput " + str(self.env['input']['currInput'] ) ,debug.debugLevel.INFO)              
        if self.noKeyPressed():
            self.env['input']['prevInput'] = []
            self.setLedState = True

    def handleLedStates(self, mEvent):
        if not self.setLedState:
            return self.setLedState
        if mEvent['EventName'] == 'KEY_NUMLOCK':
            if mEvent['EventState'] == 1 and not self.env['input']['newNumLock'] == 1:
                self.env['runtime']['inputDriver'].toggleLedState() 
                return False
            if mEvent['EventState'] == 0 and not self.env['input']['newNumLock'] == 0:
                self.env['runtime']['inputDriver'].toggleLedState()                                                                        
                return False
        if mEvent['EventName'] == 'KEY_CAPSLOCK':   
            if mEvent['EventState'] == 1 and not self.env['input']['newCapsLock'] == 1:
                self.env['runtime']['inputDriver'].toggleLedState(1)              
                return False
            if mEvent['EventState'] == 0 and not self.env['input']['newCapsLock'] == 0:
                self.env['runtime']['inputDriver'].toggleLedState(1)                                                                         
                return False                                      
        if mEvent['EventName'] == 'KEY_SCROLLLOCK':  
            if mEvent['EventState'] == 1 and not self.env['input']['newScrollLock'] == 1:
                self.env['runtime']['inputDriver'].toggleLedState(2)              
                return False
            if mEvent['EventState'] == 0 and not self.env['input']['newScrollLock'] == 0:
                self.env['runtime']['inputDriver'].toggleLedState(2)                                                                       
                return False
        return self.setLedState

    def grabAllDevices(self):
        if self.env['runtime']['settingsManager'].getSettingAsBool('keyboard', 'grabDevices'):
            self.env['runtime']['inputDriver'].grabAllDevices()
    
    def updateInputDevices(self):
        try:
            self.env['runtime']['inputDriver'].updateInputDevices()  
        except:
            pass
    
    def removeAllDevices(self):
        try:
            self.env['runtime']['inputDriver'].removeAllDevices()
        except:
            pass

    def convertEventName(self, eventName):
        if not eventName:
            return ''
        if eventName == '':
            return ''
        eventName = eventName.upper()
        if eventName == 'KEY_LEFTCTRL':
            eventName = 'KEY_CTRL'         
        elif eventName == 'KEY_RIGHTCTRL':
            eventName = 'KEY_CTRL'
        elif eventName == 'KEY_LEFTSHIFT':
            eventName = 'KEY_SHIFT'
        elif eventName == 'KEY_RIGHTSHIFT':
            eventName = 'KEY_SHIFT'
        elif eventName == 'KEY_LEFTALT':
            eventName = 'KEY_ALT'
        elif eventName == 'KEY_RIGHTALT':
            eventName = 'KEY_ALT'
        elif eventName == 'KEY_LEFTMETA':
            eventName = 'KEY_META'
        elif eventName == 'KEY_RIGHTMETA':
            eventName = 'KEY_META'            
        if self.isFenrirKey(eventName):
            eventName = 'KEY_FENRIR'
        if self.isScriptKey(eventName):
            eventName = 'KEY_SCRIPT'            
        return eventName

    def clearEventBuffer(self):
        self.env['runtime']['inputDriver'].clearEventBuffer()
    def setLastDeepestInput(self, currentDeepestInput):
        self.lastDeepestInput = currentDeepestInput
    def clearLastDeepInput(self):
        self.lastDeepestInput = []  
    def getLastInputTime(self):
        return self.lastInputTime           
    def getLastDeepestInput(self):
        return self.lastDeepestInput 
    def writeEventBuffer(self):
        try:
            if self.env['runtime']['settingsManager'].getSettingAsBool('keyboard', 'grabDevices'):
                self.env['runtime']['inputDriver'].writeEventBuffer()
            self.clearEventBuffer()
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut("Error while writeUInput",debug.debugLevel.ERROR)
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)

    def noKeyPressed(self):
        return self.env['input']['currInput'] == []
    def isKeyPress(self):
        return (self.env['input']['prevInput'] == []) and (self.env['input']['currInput'] != [])
    def getPrevDeepestShortcut(self):
        shortcut = []
        shortcut.append(self.env['input']['shortcutRepeat'])
        shortcut.append(self.getLastDeepestInput())
        return str(shortcut)
        
    def getPrevShortcut(self):
        shortcut = []
        shortcut.append(self.env['input']['shortcutRepeat'])
        shortcut.append(self.env['input']['prevInput'])
        return str(shortcut)

    def getCurrShortcut(self, inputSequence = None):
        shortcut = []
        shortcut.append(self.env['input']['shortcutRepeat'])
        if inputSequence:
            shortcut.append(inputSequence)
        else:        
            shortcut.append(self.env['input']['currInput'])
        if len(self.env['input']['prevInput']) < len(self.env['input']['currInput']):
            if self.env['input']['shortcutRepeat'] > 1  and not self.shortcutExists(str(shortcut)):
                shortcut = []
                self.env['input']['shortcutRepeat'] = 1
                shortcut.append(self.env['input']['shortcutRepeat'])
                shortcut.append(self.env['input']['currInput'])     
        self.env['runtime']['debug'].writeDebugOut("currShortcut " + str(shortcut) ,debug.debugLevel.INFO)                      
        return str(shortcut)
        
    def currKeyIsModifier(self):
        if len(self.getLastDeepestInput()) != 1:
            return False
        return (self.env['input']['currInput'][0] =='KEY_FENRIR') or (self.env['input']['currInput'][0] == 'KEY_SCRIPT')
    
    def isFenrirKey(self, eventName):
        return eventName in self.env['input']['fenrirKey']
    
    def isScriptKey(self, eventName):
        return eventName in self.env['input']['scriptKey']
    
    def getCommandForShortcut(self, shortcut):
        if not self.shortcutExists(shortcut):
            return '' 
        return self.env['bindings'][shortcut]

    def shortcutExists(self, shortcut):
        return(shortcut in self.env['bindings'])