from machine import Pin, ADC
import utime

POTMIN=400  #experimentally determined
POTMAX=65535
SCALEDMIN=0
SCALEDMAX=100

POTGPIO=26
GREENGPIO=10
YELLOWGPIO=11
REDGPIO=12
GREENRANGE=(0,80) # 79 is green
YELLOWRANGE=(80,95)  #94 yellow
REDRANGE=(95,101)  #95 is red
CRITICALVALUES = (79,80,94,95)  #check range extremes are  correct 

pot=ADC(POTGPIO)  #potentiometer gpio 26
greenLED, yellowLED, redLED=( Pin(GREENGPIO, Pin.OUT), Pin(YELLOWGPIO, Pin.OUT), Pin(REDGPIO, Pin.OUT) )

# (320, 0), (65535,100)
# m=(100/(65535-320))
# y-0=m*(x-320)
# y=m*(x-320)

def calcScaledValue(potValue):
    m=(SCALEDMAX-SCALEDMIN)/(POTMAX-POTMIN)
    scaled = m*(potValue-POTMIN) + SCALEDMIN
    return int(scaled)

def setLeds(data,red,yellow,green):
    if data in range(GREENRANGE[0],GREENRANGE[1]):
        green.value(1)
        yellow.value(0)
        red.value(0)
        print(f'data: {data}, green=ON, yellow=OFF, red=OFF')
    elif data in range(YELLOWRANGE[0],YELLOWRANGE[1]):
        green.value(0)
        yellow.value(1)
        red.value(0)
        print(f'data: {data}, green=OFF, yellow=ON, red=OFF')
    elif data in range(REDRANGE[0],REDRANGE[1]):
        green.value(0)
        yellow.value(0)
        red.value(1)
        print(f'data: {data}, green=OFF, yellow=OFF, red=ON')
    else:
        print(f'ERROR, data={data}')
        
def checkBorderValues(criticalValues):
    for criticalValue in criticalValues:
        setLeds(criticalValue,red,yellow,green)
        utime.sleep(1)

        


checkBorderValues(CRITICALVALUES)
_ =input("Press <ENTER> to continue ")

while True:
    data = calcScaledValue(pot.read_u16())
    setLeds(data, redLED, yellowLED, greenLED)
    utime.sleep(1 )

