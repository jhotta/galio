# coding: utf-8

import os
from pin_map import *

class Pins:

  #GPIO virtual files path
  _GPIO_PATH = "/sys/class/gpio/"
  _PWM_PATH = "/sys/class/pwm/pwmchip0"
  _GPIO_GPIO = os.path.join(_GPIO_PATH, "gpio")
  _GPIO_EXPORT = os.path.join(_GPIO_PATH, "export")
  _GPIO_UNEXPORT = os.path.join(_GPIO_PATH, "unexport")
  _PWM_EXPORT = os.path.join(_PWM_PATH, "export")
  _PWM_UNEXPORT = os.path.join(_PWM_PATH, "unexport")

  def __init__(self):
    pass

  def __del__(self):
    pass

  def __str__(self):
    return self.name;

  def readFile(self, filename):
    file = open(filename, "r")
    value = file.read().strip()
    file.close()
    return value

  def writeFile(self, filename, value):
    file = open(filename, "w")
    file.write(value)
    file.close()


  def GetValue(self):
      #check to verify if the pin has been initialized.
      if(not (self._initialize)):
          self._Initialize()
      if(DEBUG): print "Reading a value on pin: %s" % str(self.name)
      #read the value
      value = self._value.read().strip()
      #set the pointer for the file back to the begining of the file
      self._value.seek(0)
      if(DEBUG): print "Value: [ %s ]" % value
      return int(value)
