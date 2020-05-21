from src.Models.rgbio import frame, connection
import time
f = frame(12, 245, 123)
ser = connection()
data = f.as_bytes()
st_ = time.time_ns()


while True:
    ser.handle.write(data)
    if ser.handle.in_waiting > 0:
        print("")

