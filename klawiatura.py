import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
SCLPin=17
SDOPin=4

HALF_BIT_TIME=.001
CHARACTER_DELAY=150*HALF_BIT_TIME

NUM_BITS=16

GPIO.setup(SCLPin,GPIO.OUT)
GPIO.setup(SDOPin,GPIO.IN)

GPIO.output(SCLPin,GPIO.HIGH)
time.sleep(HALF_BIT_TIME)
global button_str
button_str = ""

oldKey=18
lets_break = False

try:
    while True:
        if lets_break: 
            print(button_str)
            break
        button=1
        time.sleep(CHARACTER_DELAY)

        while button < 17:
            print_button=button
            if (print_button==17):
                print_button=1

            GPIO.output(SCLPin,GPIO.LOW)
            time.sleep(HALF_BIT_TIME)
            keyval=GPIO.input(SDOPin)
            if not keyval and not pressed:
                pressed=True
                if button == 16:
                    lets_break = True
                    break
                button_str += str(button%10)
            GPIO.output(SCLPin,GPIO.HIGH)
            time.sleep(HALF_BIT_TIME)

            button+=1
        
        pressed=False
except KeyboardInterrupt:
    pass
    GPIO.cleanup()