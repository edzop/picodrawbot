from machine import Pin

class myLED:

    def __init__(self,pin):
        self.LEDPin  = Pin(pin,Pin.OUT)
        self.LED_State=False

    def toggle(self):
        if self.LED_State:
            self.LED_State=False
            self.LEDPin.low()
        else:
            self.LED_State=True
            self.LEDPin.high()

