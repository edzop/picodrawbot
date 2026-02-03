from machine import Pin

class myButton:
    
    def __init__(self,pin):
        self.Pin  = Pin(pin,Pin.IN)

    def is_pressed(self):
        val = self.Pin.value()

        if val:
            return False
        else:
            return True

        #return val

        #if val:
        #    return True
        #else:
        #    return False