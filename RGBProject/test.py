from src.Models.rgbio import frame, led
import time
ser = led()
count = 0
print(frame(frame.FIRE, [123, 123, 123]).as_bytes())
while True:
    ser.fire_with_color("red")
    count = 0

    if ser.handle.in_waiting > 0:
        print(ser.handle.readline())



#----
from src.Models.rgbio import frame, led
import time
f = frame(frame.TURN_ON, data=[123, 123, 123])
