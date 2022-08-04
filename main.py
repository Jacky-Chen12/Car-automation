from machine import Pin, PWM, ADC
from myservo import Servo
import time
import _thread

servo1=Servo(13) #Servo for left wheel
servo2=Servo(2) #Servo for right wheel
servo3=Servo(0) #Servo for mounted sensor
Trig = Pin(14, Pin.OUT, 0) #Trigger Pin
Echo = Pin(15, Pin.IN, 0) #Echo Pin
distance = 0
adc=ADC(26) #Analog to digital converter

#Reads the distance from the mounted ultrasonic sensor using the trigger and echo pins
def getDistance():
    Trig.value(1)
    time.sleep_us(10)
    Trig.value(0)
    while not Echo.value():
        pass
    pingStart = time.ticks_us()
    while Echo.value():
        pass
    pingStop = time.ticks_us()
    Duration = time.ticks_diff(pingStop, pingStart)
    distance = round((Duration/2) /29.1)
    return distance
time.sleep(2)

#Spins the wheels in an angle to move forwards
def moveForward():
    servo1.ServoAngle(180)
    servo2.ServoAngle(65)

#Spins the wheels in an angle to move backwards
def moveBack():
    servo1.ServoAngle(0)
    servo2.ServoAngle(180)
#     time.sleep_ms(800)

#Spins the wheels in an angle to turn right
def moveRight():
    servo1.ServoAngle(180)
    servo2.ServoAngle(180)
    
#Spins the wheels in an angle to turn left
def moveLeft():
    servo1.ServoAngle(0)
    servo2.ServoAngle(0)

#Stops the wheels from spinning
def applyBreak():
    servo1.ServoAngle(88)
    servo2.ServoAngle(85)
    
try:
    #Begins a new thread which will run on one of the cores of the Raspberry Pi Pico
    def second_thread() :
        while True:
            
            #Turns the sweeping servo 180 degrees from right to left
            for i in range(0, 180, 1):
                servo3.ServoAngle(i)
                time.sleep_ms(3)
                
            #Turns the sweeping servo 180 degrees from left to right
            for i in range(180, 00 , -1):
                servo3.ServoAngle(i)
                time.sleep_ms(3)

    #ends current thread and begins a new one
    _thread.start_new_thread(second_thread, ())

    while True:
        #Wait 5 milli seconds before starting to spin the wheels
        time.sleep_ms(5)
        distance = getDistance()
        
        #Apply break and then turn right when detecting an object that is less than 30 centi meters
        #Print a reading of how far the object is from the from of the car
        if (distance <= 30):
            adcValue = adc.read_u16()
            print("Object is ", distance, "cm away.")
            applyBreak()
            time.sleep_ms(300)
            moveBack()
            time.sleep_ms(800)
            moveLeft()
            time.sleep_ms(500)
            moveForward()
            
        #Spin wheels to go forward if there's no object detected
        else :
            adcValue = adc.read_u16()
            moveForward()
            print("No object in path.")
            time.sleep_ms(150)
except:
        servo1.deinit()
        servo2.deinit()
        servo3.deinit()