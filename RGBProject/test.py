from src.lib.ssstuff import dominant_color
from src.Models.rgbio import led
dominant_color.resolution = (50,50)
led.port ="COM5"
l = led()
l.turn_on()
while True:
    if l.handle.in_waiting > 0:
        a =  l.handle.readline()
        print(a)
        if a == b'ups!\r\n':
            l.turn_on()
    try:
        dom_color = dominant_color.get_dominant_color_from_monitor(monitor=0, img_show=False, breaks=True)
        l.fire(dom_color)
        print(dom_color)
    except Exception as i:
        print(i.args)
        break
