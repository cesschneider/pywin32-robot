#
# NFOSS Robot Base Implementation v0.1
# Author: Cesar Schneider <cesschneider@gmail.com>
# Date: Aug 16th, 2014
#

import os, time
from pprint import pprint
import InputEvent

class Robot:

   # Robot states
   STATE_STOP = 0
   STATE_RUN_FOREVER = 1
   STATE_RUN_ONCE = 2
   STATE_SLEEP = 3

   # Config options read from file (can be updated in runtime)
   # debug: Debug flag to display verbose output messages
   # state: robot state flag used to control process execution
   # stepTime: time (in seconds) to wait between each robot move (used for debugging purposes)
   # sleepTime: time (in seconds) before continue to next set of tasks
   config = {}

   def __init__(self):
      print("Initializing robot...")
      self.parseConfig()

   def parseConfig(self):
      file = open("Robot.cfg", "r")
      
      for line in file:
         attr = line.split(" = ")
         key = attr[0]
         value = self.parseStr(attr[1])

         self.config[key] = value

   def parseStr(self, str):
      str = str.replace("\n","")
      try:
         return int(str)
      except ValueError:
         if (str.find(".") > 0):
            return float(str)
         else:
            return str

   def setDebug(self, flag):
      self.config['debug'] = flag

   def setStepTime(self, time):
      self.config['stepTime'] = time

   def setSleepTime(self, time):
      self.config['sleepTime'] = time

   def setState(self, state):
      self.config['state'] = state

   def startProcess(self):
      while (self.config['state'] != Robot.STATE_STOP):

         # Parse config file to reload options
         self.parseConfig()

         print("Processing tasks for robot...")
         time.sleep(self.config['stepTime'])

         self.taskPulse()
         self.taskCSO()
         self.taskSGOS()
         self.taskNSIA()

         if (self.config['state'] == Robot.STATE_SLEEP):
            print("Sleeping for", self.config['sleepTime'], "seconds")
            time.sleep(self.config['sleepTime'])

         if (self.config['state'] == Robot.STATE_STOP or self.config['state'] == Robot.STATE_RUN_ONCE):
            print("Stopping robot")
            break

         # Parse config file to reload options
         self.parseConfig()

   def taskPulse(self):
      print("Connecting to VIVO VPN using Pulse...")

      i = 1
      task = self.config['task_pulse']
      steps = task.split(';')

      if (self.config['debug']): print('Pulse task:', task)

      for step in steps:
         if (self.config['debug']): print('Step', i, step)

         params = step.split(':')
         coords = params[1].split(',')
         
         if (params[0] == 'dc'):
            InputEvent.double_click(int(coords[0]), int(coords[1]))
         else:
            InputEvent.single_click(int(coords[0]), int(coords[1]))
         
         time.sleep(self.config['stepTime'])
         i = i+1


# Create a robot instance and start processing tasks
r0 = Robot()
r0.setDebug(1)
r0.setStepTime(1)
r0.setSleepTime(1)
r0.startProcess()
