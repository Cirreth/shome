import serial
import os


class RGB:

  def __init__(self):
    for dev in os.listdir('/dev'):
      if 'ttyACM' in dev:
        self.s = serial.Serial('//dev//'+dev, 300)
        self.init_pwm()
        return
    raise Exception('There is no device ttyACM* in /dev')

  def write(self, com):
    self.s.write((com+' = ').encode())
    self.s.readline()

  def init_pwm(self):
    self.write('FF DDRB') #all ports B as outputs
    self.write('00 PORTB') #set all ports B to 0
    self.write('61 45') #init PWM on OC2  - value in 0x43
    self.write('A1 4F') #init PWM on OC1A - value in 0x4A
    self.write('01 4E') #init PWM on OC1B - value in 0x48

  def setColor(self, color_hex):
    """
                    bgr   <- channels
        ||||||||||||||
      [)   atmega8   ]
       ||||||||||||||
    """
    self.write((color_hex[1:3]+' 4A'))
    self.write((color_hex[3:5]+' 48'))
    self.write((color_hex[5:]+' 43'))


