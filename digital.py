#! /usr/bin/env python
# coding: utf-8

import os
from gpio_pins import *

class digPins(gpio_pins.Pins):

  name = None;
  GPIO_PATH = "/sys/class/gpio/"
  PWM_PATH = "/sys/class/pwm/pwmchip0"
  GPIO_EXPORT = os.path.join(GPOI_PATH, "export")
  GPIO_GPIO = os.path.join(GPOI_PATH, "gpio")
  GPIO_UNEXPORT = os.path.jpin(GPOI_PATH, "unexport")
  PWM_EXPORT = os.path.join(PWN_PATH, "export")
  PWM_UNEXPORT = os.path.join(PWM_PATH, "unexport")

  digitalPins = []

  def __init__(self,name,gpioPin,muxPin,muxValue,pwmPin="00",pwmMuxPin="00",pwmMuxValue="00",mux2Pin="00",mux2Value="00",pwmMux2Pin="00",pwmMux2Value="00"):
    self._gpioPin      = gpioPin
    self._muxPin       = muxPin
    self._muxValue     = muxValue
    self._mux2Pin      = mux2Pin
    self._mux2Value    = mux2Value
    #file handles for controlling digital pin
    self._drive        = None
    self._direction    = None
    self._value        = None
    #PWM pin information.
    self._pwmPin       = pwmPin
    self._pwmMuxPin    = pwmMuxPin
    self._pwmMuxValue  = pwmMuxValue
    self._pwmMux2Pin   = pwmMux2Pin
    self._pwmMux2Value = pwmMux2Value
    #file handles for PWM pins.
    self._pwmPeriod    = None
    self._pwmDuty      = None
    #used to keep track if a file handles are open
    self._initialize   = False
    #used to keep track if we have exported a GPIO pin
    self._gpioExport   = False
    self._muxExport    = False
    self._mux2Export   = False
    self._pwmExport    = False
    self._setStrong    = False

  def __str__(self):
    return str(self.name)

  def __del__(self):
  if(self._initialize):
    self._value.close()
    if(self._pwmPin != "00")
      self._pwmPeriod.close()
      self._pwmDuty.close()
  #remove the pin
  if(self._gpioExport):
    self._WriteFile(UNEXPORT, self._gpioPin)
  #remove the Mux
  if(self._muxExport):
    self._WriteFile(UNEXPORT, self._muxPin)
  #remove the second mux, if it exists
  if(self._mux2Pin != "00"):
    if(self._mux2Export):
      self._WriteFile(UNEXPORT, self._mux2Pin)
  if(self._pwmPin != "00"):
    if(self._pwmExport):
      self._WriteFile(PWM_UNEXPORT, self._pwmPin)


  def SetupMode(self, direction):
    #this setup the level one mux, if needed. GPIO number "00" indicates no mux is used.
    if(self._muxPin != "00"):
      self._SetupMux()
    #this setup the level two mux, if needed. GPIO number "00" indicates no mux is used.
    #if(self._mux2Pin != "00"):
    #    self._Setup2Mux();
    #this setup the PWM, if this is a PWM pin. PWM number "00" indicates this is not a PWM pin.
    if(self._pwmPin != "00"):
      self._SetupPWM()
    #this sets up the GPIO pin for controlling the digital pin
    self._SetupPin(direction)
    #This is a file handle that we will use to drive the value for the digital pin.
    self._value = open("/sys/class/gpio/gpio" + self._gpioPin + "/value", "r+")
    #this keeps track of whether the file handle is open or not
    self._initialize = True

  def _SetupMux(self):
      #Check if the MUX GPIO directory already exists
      if(not (os.path.exists("/sys/class/gpio/gpio" + self._muxPin + "/"))):
          #This should create the Setting value on MUX forGPIO drirectory for the mux
          self._WriteFile("/sys/class/gpio/export", self._muxPin);
          self._muxExport = True

      #Set the drive strength
      #this only needs to be done for firmware version 0.7.5
      if(waBug075):
          self._WriteFile("/sys/class/gpio/gpio" + self._muxPin + "/drive", "strong")
      #Make sure the Mux pin is setup as an output
      self._WriteFile("/sys/class/gpio/gpio" + self._muxPin + "/direction","out")
      #now drive the Mux pin, the value in MUXDRIVE is the value that needs to be driven.
      self._WriteFile("/sys/class/gpio/gpio" + self._muxPin + "/value", self._muxValue)

  def _Setup2Mux(self):
      #Check if the MUX GPIO directory already exists
      if(not (os.path.exists("/sys/class/gpio/gpio" + self._mux2Pin + "/"))):
          #This should create the Setting value on MUX forGPIO drirectory for the mux
          self._WriteFile("/sys/class/gpio/export", self._mux2Pin)
          self._mux2Export = True

      #Set the drive strength
      #this only needs to be done for firmware version 0.7.5
      if(waBug075):
          self._WriteFile("/sys/class/gpio/gpio" + self._mux2Pin + "/drive", "strong")

      #Make sure the Mux pin is setup as an output
      self._WriteFile("/sys/class/gpio/gpio" + self._mux2Pin + "/direction","out")
      #now drive the Mux pin, the value in MUXDRIVE is the value that needs to be driven.
      self._WriteFile("/sys/class/gpio/gpio" + self._mux2Pin + "/value", self._mux2Value)

  def _SetupPin(self,direction):
      #Enable the output
      #check to see if the GPIO directory for the pin already exists.
      if(not (os.path.exists("/sys/class/gpio/gpio" + self._gpioPin + "/"))):
          #this will create the directory for the GPIO pin
          self._WriteFile("/sys/class/gpio/export", self._gpioPin)
          self._gpioExport = True
      #set the direction for the GPIO pins.
      if(direction == OUTPUT):
          #Set the direction
          self._WriteFile("/sys/class/gpio/gpio" + self._gpioPin + "/direction","out")
      elif(direction == INPUT):
          #set the direction
          self._WriteFile("/sys/class/gpio/gpio" + self._gpioPin + "/direction","in")
          self._WriteFile("/sys/class/gpio/gpio" + self._gpioPin + "/drive","hiz")
          return 0
      else:
          print("Unrecongnized direction: " + direction)
          return -1

  def _SetupPWM(self):
    #If it is an output, and it is one of the PWM pins then we need to Enable PWM.
    if(not (os.path.exists("/sys/class/pwm/pwmchip0/pwm" + self._pwmPin + "/enable"))):
      self._WriteFile("/sys/class/pwm/pwmchip0/export", self._pwmPin)
      self._pwmExport = True;
    self._WriteFile("/sys/class/pwm/pwmchip0/pwm" + self._pwmPin + "/enable","1")
    self._pwmPeriod = open("/sys/class/pwm/pwmchip0/pwm" + self._pwmPin + "/period", "r+")
    self._pwmDuty   = open("/sys/class/pwm/pwmchip0/pwm" + self._pwmPin + "/duty_cycle", "r+")
    return 0

  def GetValue(self):
    value = self._value.read().strip()
    self._value.seek(0)
    if(value == "1"):
      retVal = "HIGH"
    elif(value == "0"):
      retVal = "LOW"
    else:
      print("Error: Read for digital pin returned a value of :" + value)
      return -1
    return retVal

  def SetValue(self,value):
    #Check Inputs
    if(value == HIGH):
      setValue = "1"
    elif(value == LOW):
      setValue = "0"
    else:
      print("Valid values are only HIGH and LOW\n")
      return -1

    #write the value to the file
    self._value.write(setValue)
    #set the pointer for the file back to the begining of the file
    self._value.seek(0)


  def SetPWMValue(self,value):
    PERIOD = 1000000
    if(((value < 0) or (value > 255))):
      print("Valid values are between 0 and 255.\n")
      return -1
    dutyCycle = int(round(((PERIOD*value)/255),0))

    #we need to turn off the digital driver for this pin so the PWM drive will work
    self._value.write("0")
    #self._value.close()

    #Set the Period of the Pulse
    self._pwmPeriod.write(str(PERIOD))
    self._pwmPeriod.seek(0)

    #Set the Duty Cycle for the pulse
    self._pwmDuty.write(str(dutyCycle))
    self._pwmDuty.seek(0)