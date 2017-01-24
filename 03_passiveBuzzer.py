#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

BZRPin = 12

GPIO.setmode(GPIO.BOARD)       # Numbers pins by physical location
GPIO.setup(BZRPin, GPIO.OUT)   # Set pin mode as output
GPIO.output(BZRPin, GPIO.LOW)

p = GPIO.PWM(BZRPin, 50) # init frequency: 50HZ
p.start(50)  # Duty cycle: 50%

try:
	while True:
		for f in range(10, 200, 10):
			p.ChangeFrequency(f)
			time.sleep(0.2)
		for f in range(200, 10, -10):
			p.ChangeFrequency(f)
			time.sleep(0.2)
except KeyboardInterrupt:
	p.stop()
	GPIO.cleanup()
