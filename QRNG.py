import RPi.GPIO as GPIO
import time
class QRNG(object):
  def __init__(self):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12, GPIO.IN)
    self.bit1 = 0
    self.bit2 = 0
    self.log("INFO", "Quantum RNG Started")
 
  def log(self, info, message):
    print("[%s]: %s" % (info ,message))

  def loop(self):
    while True:
      if self.bit1 != 0 and self.bit2 != 0:
          number = (self.bit2 - self.bit1) ** 2
          self.log("RESULT", "Random number is %s" % number)
          self.bit1, self.bit2 = 0, 0

      if GPIO.input(12) == True:
        if self.bit1 == 0:
          self.bit1 = time.time()
          self.log("INFO", "Bit 1 recived %s" % self.bit1)
        elif self.bit2 == 0:
          self.bit2 = time.time()
          self.log("INFO", "Bit 2 recived %s" % self.bit2)
qrng = QRNG()
qrng.loop()
