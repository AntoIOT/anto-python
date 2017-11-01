import RPi.GPIO as GPIO
import antolib
import time

# LED GPIO
leds = [17, 27, 22]

# Setup LED GPIO
GPIO.setmode(GPIO.BCM)

for led in leds:
    print('Setup {} as GPIO.OUT'.format(led))
    GPIO.setup(led, GPIO.OUT)

# username of anto.io account
user = 'YOUR_USERNAME'

# key of permission, generated on control panel anto.io
key = 'YOUR_KEY'

# your default thing.
thing = 'YOUR_THING'

anto = antolib.Anto(user, key, thing)

def connectedCB():
    anto.sub("led1")
    anto.sub("led2")
    anto.sub("led3")

def dataCB(channel, msg):
    value = int(msg)

    if channel == 'led1':
        GPIO.output(leds[0], value)
    elif channel == 'led2':
        GPIO.output(leds[1], value)
    elif channel == 'led3':
        GPIO.output(leds[2], value)

    if value == 1:
        print('{}: ON'.format(channel))
    else:
        print('{}: OFF'.format(channel))

def setup():
    anto.mqtt.onConnected(connectedCB)
    anto.mqtt.onData(dataCB)
    anto.mqtt.connect()

i = 0

def myLoopFunction():
    global i
    i += 1
    print(i)
    time.sleep(4)
    
setup()
anto.loop(myLoopFunction)
