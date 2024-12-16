from m5stack import *
from m5stack_ui import *
from uiflow import *
from m5mqtt import M5mqtt
import time
import unit


screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)
earth_0 = unit.get(unit.EARTH, unit.PORTB)






label0 = M5Label('label0', x=138, y=113, color=0x000, font=FONT_MONT_14, parent=None)

def fun_earth_0_analogValue_(topic_data):
  # global params
  pass


m5mqtt = M5mqtt('dar', 'test.mosquitto.org', 1883, '', '', 300)
m5mqtt.subscribe(str((earth_0.analogValue)), fun_earth_0_analogValue_)
m5mqtt.start()
while True:
  m5mqtt.publish(str('dar_val'), str((earth_0.analogValue)), 0)
  if (earth_0.analogValue) <= 300:
    label0.set_text(str(earth_0.analogValue))
    screen.set_screen_bg_color(0xff0000)
  else:
    label0.set_text(str(earth_0.analogValue))
    screen.set_screen_bg_color(0x33ff33)
    wait(1)
  wait_ms(2)