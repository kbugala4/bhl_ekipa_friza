from RPLCD import CharLCD
import RPi.GPIO as GPIO
from time import sleep
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[40, 38, 36, 32, 33, 31, 29, 23], numbering_mode = GPIO.BOARD)

lcd.clear()
lcd.cursor_pos=(0,0)
lcd.write_string("  Hej! Tu twoj\n\rasystent kapieli")
sleep(5)
lcd.clear()
lcd.write_string("     Podaj \n\rtemperature wody")
   