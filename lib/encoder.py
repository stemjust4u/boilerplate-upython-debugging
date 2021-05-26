from machine import Pin
import utime

class Encoder:
    def __init__(self, dtPin):
        self.dtPin = Pin(dtPin, Pin.IN, Pin.PULL_DOWN)
        self.dtPin.irq(trigger=Pin.IRQ_RISING, handler=self._callback)
        self._t0 = utime.ticks_us()
        self._period = None

    def _callback(self, pin):
        self._period = utime.ticks_diff(utime.ticks_us(), self._t0)
        self._t0 = utime.ticks_us()
        
    def getdata(self):
        return self._period