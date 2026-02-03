from machine import Pin
import time

#--------------------------------------------------------------------------------
class A4988:
    def __init__(self, DIR=16, STEP=17):
        """This class represents an A4988 stepper motor driver.  It uses two output pins
        for direction and step control signals."""

        self._dir  = Pin(DIR,Pin.OUT)
        self._step = Pin(STEP,Pin.OUT)


    def step(self, forward=True):
        """Emit one step pulse, with an optional direction flag."""
        self._dir.value = forward

        self._step.high()
        #time.sleep(1e-6)
        self._step.low()

    def move_sync(self, steps, speed=1000.0):

        if steps>=0:
            self._dir.high()
        else:
            self._dir.low()

        time_per_step = 1.0 / speed
        for count in range(abs(steps)):
            self._step.high()
            time.sleep(1e-6)
            self._step.low()
            time.sleep(time_per_step)


#--------------------------------------------------------------------------------
class Dual_A4988:
    def __init__(self, DIR1=16, STEP1=17,DIR2=16, STEP2=17):

        self._dir1  = Pin(DIR1,Pin.OUT)
        self._step1 = Pin(STEP1,Pin.OUT)

        self._dir2  = Pin(DIR2,Pin.OUT)
        self._step2 = Pin(STEP2,Pin.OUT)


    def set_direction(self,forward):

        if forward:
            self._dir1.on()
            self._dir2.off()
        else:
            self._dir1.off()
            self._dir2.on()


    def step(self, forward=True):
        """Emit one step pulse, with an optional direction flag."""

        self.set_direction(forward)

        self._step1.high()
        #time.sleep(1e-6)
        self._step1.low()

        self._step2.high()
        #time.sleep(1e-6)
        self._step2.low()

    def move_sync(self, steps, speed=1000.0):

        if steps>=0:
            self.set_direction(True)
        else:
            self.set_direction(False)

        time_per_step = 1.0 / speed
        for count in range(abs(steps)):
            self._step1.high()
            time.sleep(1e-6)
            self._step1.low()
            time.sleep(time_per_step)

            self._step2.high()
            time.sleep(1e-6)
            self._step2.low()
            time.sleep(time_per_step)