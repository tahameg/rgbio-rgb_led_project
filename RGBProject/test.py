from src.Models.rgbio import frame, led
import time
f = frame(frame.TURN_ON, data=[13, 17, 124])
ser = led()
data = f.as_bytes()
print(data)

while True:
    ser.handle.write(data)
    if ser.handle.in_waiting > 0:
        print(ser.handle.readline())

