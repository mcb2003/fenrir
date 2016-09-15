#!/bin/python

import evdev
from evdev import InputDevice, UInput
from select import select
import time
from utils import debug

class driver():
    def __init__(self):
        self.iDevices = {}
        self.uDevices = {}
        self.getInputDevices()
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment
    def getInput(self, environment):
        event = None
        r, w, x = select(self.iDevices, [], [], environment['runtime']['settingsManager'].getSettingAsFloat(environment, 'screen', 'screenUpdateDelay'))
        print(len(list(r)))
        if r != []:
            for fd in r:
                event = self.iDevices[fd].read_one()
                return event
        return None

    def writeUInput(self, uDevice, event,environment):
        uDevice.write_event(event)
        uDevice.syn()
  
    def getInputDevices(self):
        self.iDevices = map(evdev.InputDevice, (evdev.list_devices()))
        self.iDevices = {dev.fd: dev for dev in self.iDevices if 1 in dev.capabilities()}

    def grabDevices(self):
        for fd in self.iDevices:
            dev = self.iDevices[fd]
            cap = dev.capabilities()
            del cap[0]
            self.uDevices[fd] = UInput(
              cap,
              dev.name,
              #dev.info.vendor,
              #dev.info.product,
              #dev.version,
              #dev.info.bustype,
              #'/dev/uinput'
              )
            dev.grab()

    def releaseDevices(self):
        for fd in self.iDevices:
            try:
                self.iDevices[fd].ungrab()
            except:
                pass
            try:
                self.iDevices[fd].close()
            except:
                pass
            try:
                self.uDevices[fd].close()
            except:
                pass

        self.iDevices.clear()
        self.uDevices.clear()

        def __del__(self):
            self.releaseDevices()

