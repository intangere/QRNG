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

  def formalizeNumbers(self):
    num1 = str(self.bit2).replace('.', '')
    num2 = str(self.bit1).replace('.', '')
    res = "%s%s" % (num1, num2)
    return res

  def expandNumbers(self, number):
    res += res[::-1]
    return res
  
  def loop(self):
    while True:
      if self.bit1 != 0 and self.bit2 != 0:
          number = self.formalizeNumbers()

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
