#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return _('get current quick menu value')
    def run(self):
        value = self.env['runtime']['quickMenuManager'].getCurrentValue()
        self.env['runtime']['outputManager'].presentText(value, interrupt=True)
    def setCallback(self, callback):
        pass
