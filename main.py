import RPi.GPIO as GPIO
import time
import w1thermsensor
import sys
from RPLCD import CharLCD
import vlc
from time import sleep

global pulse_counter
global flow
global lcd
global new
music = False
pulse_counter = 0
flow = 0

#wyswietlacz
lcd = CharLCD(cols=16, rows=2, pin_rs=26, pin_e=19, pins_data=[21, 20, 16, 12, 13, 6, 5, 11], numbering_mode = GPIO.BCM)

#czujnik przeplywu
WATER_FLOW_SENSOR = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup(WATER_FLOW_SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)


#zawor
ZAWOR = 2
GPIO.setup(ZAWOR, GPIO.OUT)

#syrena
ALARM = 22
GPIO.setup(ALARM, GPIO.OUT)

#klawiatura
# -
GPIO.setup(3, GPIO.IN,pull_up_down=GPIO.PUD_UP)

# +
GPIO.setup(17, GPIO.IN,pull_up_down=GPIO.PUD_UP)

# OK
GPIO.setup(27, GPIO.IN,pull_up_down=GPIO.PUD_UP)

def set_value(type):
    if type == "temp":
        unit = "'C"
    else:
        unit = "l"
    global new
    new = True
    value = 0
    try:
        while True:
            
            if (GPIO.input(17) == True):
                value += 1
                if type == "temp":
                    if value > 70:
                        lcd.clear()
                        lcd.write_string('Uwaga!')
                        sleep(1)
                        lcd.clear()
                        lcd.write_string('   Temperatura \n\r    maksymalna!')
                        sleep(2)
                        value = 70
                elif type == "vol":
                    if value > 150:
                        lcd.clear()
                        lcd.write_string('Uwaga!')
                        sleep(1)
                        lcd.clear()
                        lcd.write_string('  Wanna zostanie\n\r   zapelniona!')
                        sleep(2)
                        value = 150
                    
                lcd.clear()
                lcd.write_string(f'Aktualna wartosc       {value}{unit}')
                if new:
                    sleep(0.5)
                    new = False

            elif(GPIO.input(3) == True):
                value -= 1
                if value < 0:
                    value = 0
                lcd.clear()
                lcd.write_string(f'Aktualna wartosc       {value}{unit}')
                if new:
                    sleep(0.5)
                    new = False

            elif not new:
                new = True

            if(GPIO.input(27) and value != 0):
                break
                   
            sleep(0.1)
        return value        
    except KeyboardInterrupt:
        GPIO.cleanup()


def count_pulses(channel):
    global pulse_counter
    global flow
    pulse_counter += 1
    flow = pulse_counter/(60)

def get_temperature():
    therm_sensor = w1thermsensor.W1ThermSensor()
    temp = therm_sensor.get_temperature()
    return temp


if __name__ == "__main__":
    
    lcd.clear()
    GPIO.output(ALARM, 1)
    GPIO.output(ZAWOR, 1)
    GPIO.add_event_detect(WATER_FLOW_SENSOR, GPIO.FALLING, callback=count_pulses)
    while True:
        lcd.clear()
        lcd.write_string("  Hej! Tu twoj\n\rasystent kapieli")
        ha = vlc.MediaPlayer('Hej_tu_asystent.m4a')
        ha.play()
        sleep(3)
        lcd.clear()
        lcd.write_string("   Wcisnij OK\n\r  aby rozpoczac")
        wc = vlc.MediaPlayer('wcisnij_ok.m4a')
        wc.play()
        sleep(3)
        finished = False
        started = False
        pulse_counter = 0
        flow = 0
        lcd.cursor_pos=(0,0)
        while True:
            lcd.clear()
            lcd.write_string("  Hej! Tu twoj\n\rasystent kapieli")
            for i in range(30):
                sleep(0.1)
                if GPIO.input(27):
                    started = True
                    break
            if started:
                break
            
            lcd.clear()
            lcd.write_string("   Wcisnij OK\n\r  aby rozpoczac")
            for i in range(30):
                sleep(0.1)
                if GPIO.input(27):
                    started = True
                    break
            if started:
                break
        lcd.clear()
        lcd.write_string("     Podaj \n\rtemperature wody")
        pt = vlc.MediaPlayer('podaj_temperature.m4a')
        pt.play()
        water_temp_set = set_value("temp")
 
        lcd.clear()
        lcd.write_string("     Podaj \n\r   ilosc wody")
        pi = vlc.MediaPlayer('podaj_ilosc.m4a')
        pt.stop()
        pi.play()
        water_vol_set = set_value("vol")


        #wlaczamy zawor
        GPIO.output(ZAWOR, 0)
        
        lcd.clear()
        lcd.cursor_pos=(0,0)
        lcd.write_string(f'Temp. wody: ')
          
        lcd.cursor_pos=(1,0)
        lcd.write_string(f'Ilosc wody: ')
        
        
        while True:
            lcd.cursor_pos=(0,14-len(str(int((get_temperature())))))
            lcd.write_string(str(int(get_temperature()))+'*C')
          
            lcd.cursor_pos=(1,15-len(str(round(float(flow),1))))
            lcd.write_string(str(round(float(flow),1))+'l')
     
            if (flow + 0.5) >= water_vol_set:
                #zamknij zawor
                GPIO.output(ZAWOR, 1)
                #odpal syrene
                GPIO.output(ALARM, 0)
                sleep(5)
                GPIO.output(ALARM, 1)
                break
            if not music and (get_temperature()-4 > water_temp_set):
                p = vlc.MediaPlayer('Norbi.mp3')
                p.play()
                music = True
                
            elif not music and (get_temperature()+4 < water_temp_set):
                p = vlc.MediaPlayer('Ice Ice Baby.mp3')
                p.play()
                music = True
            
            if abs(get_temperature()-water_temp_set) < 4:
                music = False
            sleep(0.1)

        lcd.clear()
         
        lcd.write_string(" Milej kapieli!")
   
        mk = vlc.MediaPlayer('kapiel 2.mp3')
        mk.play()
        sleep(3)
        mk.stop()
        
        lcd.clear()
        lcd.write_string("Daj znac\n\rjak skonczysz :)")
        dz = vlc.MediaPlayer('daj_znac.m4a')
        dz.play()
        sleep(3)
        dz.stop()
        while True:
            lcd.clear()
            lcd.write_string("*** Wcisnij ***\n\r***    OK    ***")
            for i in range(30):
                sleep(0.1)
                if GPIO.input(27):
                    finished = True
                    break
            if finished:
                break
            
            lcd.clear()
            lcd.write_string("Daj znac\n\rjak skonczysz :)")
            for i in range(30):
                sleep(0.1)
                if GPIO.input(27):
                    finished = True
                    break
            if finished:
                break
    
    
        
    
        
        
    
    
    