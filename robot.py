import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
print('Wait untill device gets connected....')
leds = [26,19,13,6]
for i in leds:GPIO.setup(i,GPIO.OUT)



p1 = GPIO.PWM(26,50)
p2 = GPIO.PWM(19,50)
p3 = GPIO.PWM(13,50)
p4 = GPIO.PWM(6,50)

p1.start(0)
p2.start(0)
p3.start(0)
p4.start(0)


def stop():
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(0)
    p4.ChangeDutyCycle(0)


def Left(D):
    print("Turning left")
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(D)
    p3.ChangeDutyCycle(D)
    p4.ChangeDutyCycle(0)
##    GPIO.output(leds[0],False)
##    GPIO.output(leds[1],True)
##    GPIO.output(leds[2],True)
##    GPIO.output(leds[3],False)

def Right(D):
    print("Turning Right")
    p1.ChangeDutyCycle(D)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(0)
    p4.ChangeDutyCycle(D)
##    GPIO.output(leds[0],True)
##    GPIO.output(leds[1],False)
##    GPIO.output(leds[2],False)
##    GPIO.output(leds[3],True)


def Forward(D):
    print("Moving Forward")
    p1.ChangeDutyCycle(D)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(D)
    p4.ChangeDutyCycle(0)
##    GPIO.output(leds[0],True)
##    GPIO.output(leds[1],False)
##    GPIO.output(leds[2],True)
##    GPIO.output(leds[3],False)


def Down(D):
    print("Moving Backward")
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(D)
    p3.ChangeDutyCycle(0)
    p4.ChangeDutyCycle(D)
##    GPIO.output(leds[0],False)
##    GPIO.output(leds[1],True)
##    GPIO.output(leds[2],False)
##    GPIO.output(leds[3],True)


