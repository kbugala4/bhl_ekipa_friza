import w1thermsensor

therm_sensor = w1thermsensor.W1ThermSensor()
try:
    while True:
        temp = therm_sensor.get_temperature()
        print(temp)
except KeyboardInterrupt:
    print("dowidzenia")
