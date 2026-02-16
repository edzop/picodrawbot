import _thread
import time
from edlib import myled, mybutton, stepper

def core1_task(counter):
    delay=0.5

    for i in range(counter):
        systemLED.toggle()
        time.sleep(delay)
        systemLED.toggle()
        time.sleep(delay)

systemLED = myled.myLED("LED")
sz = stepper.Dual_A4988(DIR1=18,STEP1=17,DIR2=21,STEP2=20)

debug=False

delay = 0.1

    
#    stepper2.move_sync(steps, speed)


iSpeed = 20
iStep = 4
direction = 1


def handle_command(command):

    global delay
    global iSpeed
    global direction

    if debug:
        print("handle")
    response="-"

    print(command)

    command_name=command[0]
    parm=int(command[1])

    if debug:
        print("Command: ")
        print(command_name)
        print("Parm: ")
        print(parm)

    if command_name=="LT":
        iStep = parm
        adjusted_iStep = iStep * direction
        sz.move_left(adjusted_iStep, iSpeed)
        #move_stepper(sz,adjusted_iStep,iSpeed)
        response = "stepL: " + str(adjusted_iStep)

    if command_name=="RT":
        iStep = parm
        adjusted_iStep = iStep * direction
        sz.move_right(adjusted_iStep, iSpeed)
        #move_stepper(sz,adjusted_iStep,iSpeed)
        response = "stepR: " + str(adjusted_iStep)

    if command_name=="ST":
        iStep = parm
        adjusted_iStep = iStep * direction
        sz.move_sync(adjusted_iStep, iSpeed)
        #move_stepper(sz,adjusted_iStep,iSpeed)
        response = "stepS: " + str(adjusted_iStep)

    if command_name=="SP":
        iSpeed = parm
        response = "speed: " + str(iSpeed)

    if command_name=="DR":
        if parm==0:
            direction = -1 
        else:
            direction = 1
        response = "direction: " + str(direction)

    if command_name=="DL":
        delay = parm / 10
        response="delay: " + str(delay)

    if command_name=="BL":
        #_thread.start_new_thread(core1_task, (parm,))

        response="blink"

        for i in range(parm):
            systemLED.toggle()
            time.sleep(delay)
            systemLED.toggle()
            time.sleep(delay)

    response = "%s(%s %d)"%(response,command_name,parm)

    return response


if __name__ == '__main__':
    import command_processor
    c = command_processor.CommandProcessor()
    c.load_test_file("command_test.txt")
    commands = c.get_commands()

    for command in commands:
        print(handle_command(command))
