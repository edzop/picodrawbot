from machine import Pin
import utime

# Define pin numbers
step_pin = Pin(17, Pin.OUT)
dir_pin = Pin(16, Pin.OUT)


# Set motor direction
dir_pin.high()


def loop():
    while True:
        # Read potentiometer value and map it to desired range

        custom_delay_mapped = 400

        # Pulse the stepper motor
        step_pin.high()
        utime.sleep_us(int(custom_delay_mapped))
        step_pin.low()
        utime.sleep_us(int(custom_delay_mapped))

# Start the loop
loop()