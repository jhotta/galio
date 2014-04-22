#! /usr/bin/env python
# coding: utf-8

import os
from gpio_pins import *

class AnalogPin(_Pins):

  name        = None;
  _initialize = False;

  def __init__(self, number, name, gpioPin, muxPin="00", muxValue="0", mux2Pin="00", mux2Value="0"):
    self.name       = name         #(string)The name of the digital pin ie("A0")
    self._number    = number       #(int)the number of the analog pin
    self._gpioPin   = gpioPin      #(string)The Linux Logical GPIO pin used to access analog pin
    self._muxPin    = muxPin       #(string)The Linux Logical GPIO pin for the first level mux
    self._muxValue  = muxValue     #(string)The drive vaue for the first level mux
    self._mux2Pin   = mux2Pin      #(string)The Linux Logical GPIO pin for the second level mux
    self._mux2Value = mux2Value    #(string)The drive vaue for the first level mux
    self._initialize = False       #(bool)Whether the analog pin has been setup
    self._gpioExport = False       #(bool)Whether Linux Logical GPIO pin has been setup
    self._muxExport  = False       #(bool)Whether Linux Logical GPIO pin for the first level mux has been setup
    self._mux2Export = False       #(bool)Whether Linux Logical GPIO pin for the first second mux has been setup

  def __del__(self):
    #remove the pin
    if(self._gpioExport):
      self._WriteFile("/sys/class/gpio/unexport", self._gpioPin)
    #remove the Mux
    if(self._muxExport):
      self._WriteFile("/sys/class/gpio/unexport", self._muxPin)
    #remove the second mux, if it exists
    if(self._mux2Pin != "00")
      if(self._mux2Export):
        self._WriteFile("/sys/class/gpio/unexport", self._mux2Pin)
    #Close the file handle for the value
    if(self._initialize):
      self._value.close()

  def _SetupMux(self):
    #check to see if the GPIO directory for the mux already exists.
    if(not (os.path.exists("/sys/class/gpio/gpio" + self._muxPin + "/"))):
      #this will create the directory for the GPIO pin
      self._WriteFile("/sys/class/gpio/export", self._muxPin)
    self._muxExport = True
    #There is a bug in the 0.7.5 firmware that requires the drive value to be set to strong
    if(waBug075):
      #Set the drive strength
      self._WriteFile("/sys/class/gpio/gpio" + self._muxPin + "/drive","strong")
    self._WriteFile("/sys/class/gpio/gpio" + self._muxPin + "/direction","out")
    #now drive the Mux pin, the value in MUXDRIVE is the value that needs to be driven.
    self._WriteFile("/sys/class/gpio/gpio" + str(self._muxPin) + "/value",self._muxValue)

  def _Setup2Mux(self):
    if(self._mux2Pin!="00"):
      if(not (os.path.exists("/sys/class/gpio/gpio" + self._mux2Pin + "/"))):
        #this will create the directory for the GPIO pin
        self.self._WriteFile("/sys/class/gpio/export",self._mux2Pin)
        self._mux2Export = True
        #There is a bug in the 0.7.5 firmware that requires the drive value to be set to strong
        if(waBug075):
              #Set the drive strength
          self._WriteFile("/sys/class/gpio/gpio" + self._mux2Pin + "/drive","strong")
          #set the direction for the GPIO pins.
        if(direction == OUTPUT):
          #Set the direction
          self._WriteFile("/sys/class/gpio/gpio" + self._mux2Pin+ "/direction","out")
          return 0
          #now drive the Mux pin, the value in MUXDRIVE is the value that needs to be driven.
        self._WriteFile("/sys/class/gpio/gpio" + str(self._mux2Pin) + "/value",self._mux2Value)

  def _Initialize(self):
    #setup the first level mux if needed. A value of "00" indicates no mux is needed
    if(self._muxPin != "00"):
        self._SetupMux();
    #setup the second level mux if needed. A value of "00" indicates no second level mux is needed
    if(self._mux2Pin != "00"):
      self._Setup2Mux()

    #Open a file handle for the value file.
    self._value = open("/sys/bus/iio/devices/iio:device0/in_voltage" + str(self._number) + "_raw","r")
    #boolean to keep track of whether this function has been called yet.
    self._initialize = True

  def GetValue(self):
    #check to verify if the pin has been initialized.
    if(not (self._initialize)):
      self._Initialize()
    #read the value
    value = self._value.read().strip()
    #set the pointer for the file back to the begining of the file
    self._value.seek(0)
    return int(value)

  def __str__(self):
    return self.name
