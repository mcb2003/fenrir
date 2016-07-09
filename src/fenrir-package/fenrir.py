#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import os, sys, time, signal

if not os.getcwd() in sys.path:
    sys.path.append(os.getcwd())

from threading import Thread
from core import environment 
from core import inputManager
from core import commandManager
from utils import debug

from speech import espeak as es
from speech import speechd as sd
from screen import linux as lx

class fenrir():
    def __init__(self):
        self.threadUpdateScreen = None
        self.threadHandleInput = None
        self.threadHandleCommandQueue = None
        self.environment = environment.environment
        self.environment['runtime']['inputManager'] = inputManager.inputManager()
        self.environment['runtime']['commandManager'] = commandManager.commandManager()
        self.environment = self.environment['runtime']['commandManager'].loadCommands(self.environment)
        self.environment['runtime']['debug'] = debug.debug()
        signal.signal(signal.SIGINT, self.captureSignal)

        # the following hard coded, in future we have a config loader
        self.environment['runtime']['speechDriver'] = sd.speech()
        self.environment['runtime']['screenDriver'] = lx.screenManager()

    def proceed(self):
        self.threadUpdateScreen = Thread(target=self.updateScreen, args=())
        self.threadHandleInput = Thread(target=self.handleInput, args=())
        self.threadCommands = Thread(target=self.handleCommands, args=())
        self.threadUpdateScreen.start()
        self.threadHandleInput.start()
        self.threadCommands.start()
        while(self.environment['generalInformation']['running']):
            time.sleep(0.2)
        self.shutdown()

    def handleInput(self):
        while(self.environment['generalInformation']['running']):
            self.environment = self.environment['runtime']['inputManager'].getKeyPressed(self.environment)
            if self.environment['input']['currShortcutString'] == '':
                self.environment['commandInfo']['currCommand'] = ''

    def updateScreen(self):
        while(self.environment['generalInformation']['running']):
            self.environment = self.environment['runtime']['screenDriver'].analyzeScreen(self.environment)

    def handleCommands(self):
        while(self.environment['generalInformation']['running']):
            self.environment = self.environment['runtime']['commandManager'].getCommandForShortcut(self.environment)
            #self.environment['input']['currShortcut'] = {} 
            if self.environment['commandInfo']['currCommand'] != '':
                self.environment = self.environment['runtime']['commandManager'].executeCommand(self.environment)
                time.sleep(0.5)

    def shutdown(self):
        self.environment['generalInformation']['running'] = False
        if self.environment['runtime']['speechDriver'] != None:
            self.environment['runtime']['speechDriver'].shutdown()
        if self.environment['runtime']['debug'] != None:
            self.environment['runtime']['debug'].closeDebugFile()
        if self.environment['runtime']['soundDriver'] != None:
            self.environment['runtime']['soundDriver'].shutdown()

    def captureSignal(self, siginit, frame):
        self.shutdown()

app = fenrir()
app.proceed()
