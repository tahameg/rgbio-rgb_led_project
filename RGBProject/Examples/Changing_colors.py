from src.Models.rgbio import led
import time

led = led()
time.sleep(1)
led.turn_on()
led.turn_on()
led.turn_on()
led.turn_on()
led.turn_on()
led.turn_on()
led.turn_on()
led.turn_on()
led.turn_on()

dr, dg, db = (0, 0, 0)

while True:
    led.fire_with_color((dr, dg, db))
    time.sleep(0.1)
    dr = (dr + 1) % 255
    dg = (dg + 2) % 255
    db = (db + 3) % 255

