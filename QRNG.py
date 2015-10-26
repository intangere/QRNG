import RPi.GPIO as GPIO
import time
import re

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

  def xor(self, numbers):
    if not numbers % 2 == 0:
      numbers = ''.join([numbers, '0'])
    for pos, bit in enumerate(numbers):
      next_bit = numbers[pos+1]
      result = int(bit) ^ int(next_bit) 
      numbers = self.insert(numbers, str(result), pos+1)
      numbers = numbers + str(result)
    return numbers + numbers[::-1]

  def insert(self, source, insert, pos):
    return source[:pos]+insert+source[pos:]

  def toBin(self, number):
    return int(bin(number)[2:])

  def hexilify(self, number):
    return ''.join(hex(int(a, 2))[2:] for a in number.split()).replace("L", "")

  def hexToChars(self, numbers):
    if not len(numbers) % 2 == 0:
      numbers = numbers+"0"
    random_string = ""
    segments = re.compile('(..)').findall(numbers)
    for pair in segments:
      char = pair.decode("hex")
      if char.isalnum():
        random_string = random_string + char.lower()
      else:
        char = pair[::-1].decode("hex")
        if char.isalnum():
          random_string = random_string + char.lower()        
    return random_string

  def loop(self):
    while True:
      if self.bit1 != 0 and self.bit2 != 0:
          numbers = self.formalizeNumbers()
          print numbers
          expanded = self.expandNumbers(numbers)
          print expanded
          binnums = self.toBin(int(expanded))
          print binnums
          xorred = self.xor(binnums)
          print xorred
          hexed = self.hexilify(xorred)
          print hexed
          random_string = self.hexToChars(hexed)
          self.log("RESULT", "Random number is %s" % random_string)
          self.bit1, self.bit2 = 0, 0
          self.write(random_string)

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
