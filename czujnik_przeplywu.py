import RPi.GPIO as GPIO
import time, sys

WATER_FLOW_SENSOR = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(WATER_FLOW_SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)

global pulse_counter
pulse_counter = 0

def count_pulses(channel):
    global pulse_counter
    pulse_counter += 1
    print(pulse_counter)
    flow = pulse_counter/(60*11.42)
    print(flow)
    
GPIO.add_event_detect(WATER_FLOW_SENSOR, GPIO.FALLING, callback=count_pulses)

while True:
    try:
        time.sleep(0.5)
        
    except KeyboardInterrupt:
        print('do widzenia')
        GPIO.cleanup()
        sys.exit()
