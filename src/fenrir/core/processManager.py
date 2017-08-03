#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
from core.eventData import fenrirEventType
import time 
from threading import Thread
from multiprocessing import Process, Queue
from multiprocessing.sharedctypes import Value
from ctypes import c_bool

class processManager():
    def __init__(self):
        self._Processes = []
        self._Threads = []       
    def initialize(self, environment):
        self.env = environment 
        self.running = self.env['runtime']['eventManager'].getMainLoopRunning()
        self.addSimpleEventThread(fenrirEventType.HeartBeat, self.heartBeatTimer, multiprocess=False)        
    def shutdown(self):
        self.terminateAllProcesses()
    def heartBeatTimer(self, active):
        try:
            time.sleep(0.5)
        except:
            pass
        return time.time()        
    def terminateAllProcesses(self):
        time.sleep(1)
        for proc in self._Processes:
            try:
                proc.terminate()
            except Exception as e:
                print(e)            
                          
    def addCustomEventThread(self, function, pargs = None, multiprocess = False, runOnce = False):      
        eventQueue = self.env['runtime']['eventManager'].getEventQueue()
        if multiprocess:        
            t = Process(target=self.customEventWorkerThread, args=(eventQueue, function, pargs, runOnce))
            self._Processes.append(t)                        
        else:# thread not implemented yet
            t = Thread(target=self.customEventWorkerThread, args=(eventQueue, function, pargs, runOnce))        
            self._Threads.append(t)                                
        t.start()

    def addSimpleEventThread(self, event, function, pargs = None, multiprocess = False, runOnce = False):
        if multiprocess:
            t = Process(target=self.simpleEventWorkerThread, args=(event, function, pargs, runOnce))
            self._Processes.append(t)            
        else:# thread not implemented yet
            t = Thread(target=self.simpleEventWorkerThread, args=(event, function, pargs, runOnce))                    
            self._Threads.append(t)                        
        t.start()

    def customEventWorkerThread(self, eventQueue, function, pargs = None, runOnce = False):      
        #if not isinstance(eventQueue, Queue):
        #    return
        if not callable(function):
            return
        while self.running.value:
            try:
                if pargs:
                    function(self.running, eventQueue, pargs)
                else:
                    function(self.running, eventQueue)
            except Exception as e:
                print(e)
            if runOnce:
                break

    def simpleEventWorkerThread(self, event, function, pargs = None, runOnce = False):            
        if not isinstance(event, fenrirEventType):
            return
        if not callable(function):
            return
        while self.running.value:
            Data = None
            try:
                if pargs:
                    Data = function(self.running, pargs)                
                else:
                    Data = function(self.running)
            except Exception as e:
                self.env['runtime']['debug'].writeDebugOut('processManager:simpleEventWorkerThread:function():' + str(e),debug.debugLevel.ERROR) 
            self.env['runtime']['eventManager'].putToEventQueue(event, Data)
            if runOnce:
                break
