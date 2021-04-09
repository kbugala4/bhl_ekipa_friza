import RPi.GPIO as GPIO
import time
import w1thermsensor
import sys
from RPLCD import CharLCD
import vlc
from time import sleep

global pulse_counter
global flow
pulse_counter = 0

lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[40, 38, 36, 32, 33, 31, 29, 23], numbering_mode = GPIO.BOARD)

#czujnik przeplywu
WATER_FLOW_SENSOR = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(WATER_FLOW_SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)

global pulse_counter
global flow
pulse_counter = 0
#czujnik przeplywu

def keyboard_input(lcd):
    #klawiatura
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
    #klawiatura
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
                lcd.clear()
                lcd.write_string(button_str)
            GPIO.output(SCLPin,GPIO.HIGH)
            time.sleep(HALF_BIT_TIME)

            button+=1
        
        pressed=False
except KeyboardInterrupt:
    pass
    GPIO.cleanup()
    

def count_pulses(channel):
    global pulse_counter
    global flow
    pulse_counter += 1
    flow = pulse_counter/(60)
    #return flow

def get_temperature():
    therm_sensor = w1thermsensor.W1ThermSensor()
    temp = therm_sensor.get_temperature()
    return temp

# def lcd_display_temperature(lcd):
#     water_temp = int(get_temperature())
#     lcd.cursor_pos=(0,13)
#     lcd.write_string(str(water_temp)+"*C")    
# 
# def lcd_display_level(lcd, level):
#     water_vol = int(level)
#     lcd.cursor_pos=(0,12)
#     lcd.write_string(str(water_vol))

if __name__ == "__main__":
    while True:
        lcd.cursor_pos=(0,0)
        lcd.write_string("  Hej! Tu twoj\n\rasystent kapieli")
        sleep(5)
        lcd.clear()
        lcd.write_string("     Podaj \n\rtemperature wody")
        keyboard_input()
        water_temp_set = button_str
        lcd.clear()
        lcd.write_string("     Podaj \n\r   ilosc wody")
        keyboard_input()
        water_vol_set = button_str
        GPIO.add_event_detect(WATER_FLOW_SENSOR, GPIO.FALLING, callback=count_pulses)
        
        #wlaczamy zawor
        
        while True:
            lcd.clear()
            lcd.cursor_pos=(0,0)
            lcd.write_string(f'Temp. wody: {int(get_temperature())} *C')
            
            lcd.cursor_pos=(1,0)
            lcd.write_string(f'Ilosc wody: {int(flow)} l')
            
            if flow >= water_vol_set:
                #zamknij zawor
                #odpal syrene, time sleep
                break
            if not music and (get_temperature()-4 > water_temp_set):
                p = vlc.MediaPlayer('Ice Ice Baby.mp3')
                p.play()
                music = True
                
            elif not music and (get_temperature()+4 < water_temp_set):
                p = vlc.MediaPlayer('Norbi.mp3')
                p.play()
                music = True
            
            elif music:
                music = False
        lcd.write_string(" Milej kapieli!")
    
    
    
        
    
        
        
    
    
    