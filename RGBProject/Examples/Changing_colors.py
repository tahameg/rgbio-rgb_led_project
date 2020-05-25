from src.Models.rgbio import led
import time

l = led()
l.turn_on()



dr, dg, db = (1, 2, 3)
R, G, B =  (0, 0, 0)
while True:
    l.fire((R, G, B))

    R += dr
    G += dg
    B += db
    time.sleep(0.05)

    if R+dr > 255 or R+dr < 0:
        dr = -1*dr


    if G+dg > 255 or G+dg < 0:
        dg = -1*dg

    if (B+db) > 255 or (B+db) < 0:
        db = -1*db

    print(R, G, B)