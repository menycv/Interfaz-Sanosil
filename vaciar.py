import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)
GPIO.output(20, 0)
user = input()
if user == 1:
    GPIO.output(20, 1)

GPIO.cleanup()
