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
    expanded = int(number) ** 10
    expanded = '{0:f}'.format(expanded * time.time()).replace('.', '')[:-6]
    return expanded

  def loop(self):
    while True:
      if self.bit1 != 0 and self.bit2 != 0:
          numbers = self.formalizeNumbers()
          numbers = self.expandNumbers(numbers)
          self.log("RESULT", "Random number is %s" % numbers)
          self.bit1, self.bit2 = 0, 0
          self.write(numbers)

      if GPIO.input(12) == True:
        if self.bit1 == 0:
          self.bit1 = time.time()
          self.log("INFO", "Bit 1 recived %s" % self.bit1)
        elif self.bit2 == 0:
          self.bit2 = time.time()
          self.log("INFO", "Bit 2 recived %s" % self.bit2)

  def write(self, numbers):
    f = open('bits.txt', 'a+')
    f.write(numbers)
    f.close()


qrng = QRNG()
qrng.loop()
