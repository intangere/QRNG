# QRNG
Quantum Random Number Generator using Geiger Counter and time stamps between radioactive decay
<br>
How do you use this?
<hr>
Requirements
<hr>
```
- Python 3
- RPi.GPIO
- Some sort of geiger counter connected to pin 12 that sends pulses every time the geiger counter detects radiation
(I personally used pin 3 to ground my geiger and pin 12 for pulses )
```
How do you run this?
```
python QRNG.py
```
Copyright (C) Intangere 2015
