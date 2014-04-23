#! /usr/bin/env python
# coding: utf-8

# import os
from Pins import *

def main():
  a = Pins()
  print a._GPIO_UNEXPORT
  print a._PWM_PATH

if __name__ == '__main__':
  main()