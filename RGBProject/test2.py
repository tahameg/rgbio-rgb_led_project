import RPI.GPIO as GPIO
from time import sleep

while True:
    if GPIO.input(4) == GPIO.HIGH:
        print("motion detected")
        sleep(0.5)
