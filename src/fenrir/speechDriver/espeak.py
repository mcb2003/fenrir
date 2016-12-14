#!/usr/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.
# Espeak driver

from core import debug

class driver():
    def __init__(self):
        self._es = None
        self._isInitialized = False

    def initialize(self, environment):
        self.env = environment          
        try:
            from espeak import espeak 
            self._es = espeak
            self._isInitialized = True
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)         
            self._initialized = False
                    
    def shutdown(self):
        pass

    def speak(self,text, interrupt=True):
        if not self._isInitialized:
            return False
        if not interrupt:
            self.cancel()
        self._es.synth(text)
        return True

    def cancel(self):
        if not self._isInitialized:
            return False
        self._es.cancel()
        return True

    def setCallback(self, callback):
        pass

    def clear_buffer(self):
        if not self._isInitialized:
            return False
        return True

    def setVoice(self, voice):
        if not self._isInitialized:
            return False
        if voice =='':
            return False            
        return self._es.set_voice(voice)

    def setPitch(self, pitch):
        if not self._isInitialized:
            return False
        return self._es.set_parameter(self._es.Parameter().Pitch, int(pitch * 99)) 
        
    def setRate(self, rate):
        if not self._isInitialized:
            return False
        return self._es.set_parameter(self._es.Parameter().Rate, int(rate * 500 + 100))

    def setModule(self, module):
        if not self._isInitialized:
            return False

    def setLanguage(self, language):
        if not self._isInitialized:
            return False
        if language =='':
            return False
        return self._es.set_voice(language)

    def setVolume(self, volume):
        if not self._isInitialized:
            return False    
        return self._es.set_parameter(self._es.Parameter().Volume, int(volume * 200))
