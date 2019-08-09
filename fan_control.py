import RPi.GPIO as GPIO
from time import sleep
import os
import sys

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)
pwm = GPIO.PWM(12, 50)
dc=0
temp_range=51
pwm.start(dc)

def getCPUtemp():
    res = os.popen('vcgencmd measure_temp').readline()
    temp = (res.replace("temp=","").replace("'C\n",""))
    return temp
def fanUP(cycle):
    temp_count = cycle
    if cycle<98:
        if cycle < 10:
            pwm.ChangeDutyCycle(100)
            sleep(1)
        pwm.ChangeDutyCycle(cycle + 5)
        temp_count = cycle + 5
    print temp_count
    return temp_count
def fanDown(cycle):
    temp_count = cycle
    if cycle>2:
        pwm.ChangeDutyCycle(cycle - 5)
        temp_count = cycle -5
    print temp_count
    return temp_count
try:
    while True:

        CPU_temp = float(getCPUtemp())
        if CPU_temp > temp_range:
            dc = fanUP(dc)
        elif CPU_temp == temp_range:
            print dc
        else:
            dc = fanDown(dc)
        sleep(1)


except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
