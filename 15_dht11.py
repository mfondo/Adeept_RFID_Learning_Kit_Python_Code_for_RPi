#!/usr/bin/python

import RPi.GPIO as GPIO
import time

def pulseDuration(lastVal, minSameValSeconds):
        startSeconds = time.time()
        newVal = None
        startSecondsOppositeVal = None
        now = None
        measureCnt = 0
        while True:
                newVal = GPIO.input(channel)
                measureCnt = measureCnt + 1
                if newVal is not lastVal:
                        print "different val " + str(newVal)
                        now = time.time()
                        if startSecondsOppositeVal is None:
                                startSecondsOppositeVal = now
                        if now - startSecondsOppositeVal > minSameValSeconds:
                                return (startSecondsOppositeVal - startSeconds, measureCnt)
                else:
                        startSecondsOppositeVal = None
                

channel = 18
data = []
j = 0

GPIO.setmode(GPIO.BCM)

time.sleep(1)

GPIO.setup(channel, GPIO.OUT)

GPIO.output(channel, GPIO.LOW)
time.sleep(0.02)
GPIO.output(channel, GPIO.HIGH)

GPIO.setup(channel, GPIO.IN, GPIO.PUD_UP)

quitTime = time.time() + 1
dataList = []
lastVal = GPIO.input(channel)
while time.time() < quitTime:
        print str(lastVal) + " " + str(time.time()) + " " + str(quitTime)
        #dataList.append(pulseDuration(lastVal, 0.000001))
        dataList.append(pulseDuration(lastVal, -1))
        if lastVal is GPIO.HIGH:
                lastVal = GPIO.LOW
        else:
                lastVal = GPIO.HIGH

print "results"
for data in dataList:
        print data
GPIO.cleanup()
exit(0)

#while GPIO.input(channel) == GPIO.LOW:
#        continue

print "pulse duration " + str(pulseDuration(GPIO.LOW, 0.000001) * 1000000)
#while GPIO.input(channel) == GPIO.HIGH:
#        continue

startMeasureTime = time.time()
bitReadTime = 0
while j < 40:
        bitReadTime = time.time()
        k = 0
        while GPIO.input(channel) == GPIO.LOW:
                print "read low"
                continue

        while GPIO.input(channel) == GPIO.HIGH:
                k += 1
                if k > 100:
                        break        
        #print "k " + str(time.time() - bitReadTime)
        if k < 8:
                data.append(0)
        else:
                data.append(1)

        j += 1
print "read data in " + str(time.time() - startMeasureTime)        

print "sensor is working."
print data

humidity_bit = data[0:8]
humidity_point_bit = data[8:16]
temperature_bit = data[16:24]
temperature_point_bit = data[24:32]
check_bit = data[32:40]

humidity = 0
humidity_point = 0
temperature = 0
temperature_point = 0
check = 0

for i in range(8):
        humidity += humidity_bit[i] * 2 ** (7 - i)
        humidity_point += humidity_point_bit[i] * 2 ** (7 - i)
        temperature += temperature_bit[i] * 2 ** (7 - i)
        temperature_point += temperature_point_bit[i] * 2 ** (7 - i)
        check += check_bit[i] * 2 ** (7 - i)

tmp = humidity + humidity_point + temperature + temperature_point

if check == tmp:
        print "temperature : ", temperature, ", humidity : " , humidity
else:
        print "wrong"
        print "temperature : ", temperature, ", humidity : " , humidity, " check : ", check, " tmp : ", tmp

GPIO.cleanup()
