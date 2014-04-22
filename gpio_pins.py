#! /usr/bin/env python
# coding: utf-8

#Digital Pins and Muxes
VALIDPINS  = [  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13]
PIN2GPIO   = ["50","51","32","18","28","17","24","27","26","19","16","25","38","39"]
MUXGPIO    = ["40","41","31","30","00","00","00","00","00","00","42","43","54","55"]
MUXDRIVE   = [ "1", "1", "1", "1","00","00","00","00","00","00", "1", "1", "1", "1"]
MUX2GPIO   = ["00","00", "1", "0","00","00","00","00","00","00","00","00","00","00"]
MUX2DRIVE  = ["00","00", "0", "0","00","00","00","00","00","00","00","00","00","00"]

#PWM Pins (muxes are same as digital)
VALIDPWM   = [3,5,6,9,10,11]
PWMDICT    = {'3':"3",'5':"5",'6':"6",'9':"1",'10':"7",'11':"4"}

#Analog Pins and Muxes
ANALOGPINS = ["A0","A1","A2","A3","A4","A5"]
ANALGPIO   = ["44","45","46","47","48","49"]
ANALOGNUM  = {'A0': '0','A1': '1','A2': '2','A3': '3','A4': '4','A5': '5'}
ANAMUXPINS = ["37","36","23","22","21","20"]
ANAMUXVAL  = [ '0', '0', '0', '0', '0', '0']
ANAMUX2P   = ["00","00","00","00","29","29"]
ANAMUX2V   = ["00","00","00","00", "1", "1"]


class Pins:
  def readFile(self, filename):
    file = open(filename, "r")
    value = file.read().strip()
    file.close()
    return value

  def writeFile(self, filename, value):
    file = open(fullFilename, "w")
    file.write(value)
    file.close()