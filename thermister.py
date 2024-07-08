from pyfirmata import Arduino, util, INPUT,OUTPUT #import pyfirmata module
import math #import math module
import time #import time module

board = Arduino("COM3") #Arduino board port

thermo_pin = 1 #thermister pin
buzzer_pin = 8 #buzzer pin
switch_pin = 4  #switch pin

# analog,digital output & input
board.analog[thermo_pin].mode = INPUT
board.digital[buzzer_pin].mode = OUTPUT
board.digital[switch_pin].mode = INPUT

it  = util.Iterator(board)
it.start()

board.analog[thermo_pin].enable_reporting()

# thermister resistance
R = 1000


while True:
    # analog voltage value
    Vo = board.analog[thermo_pin].read()
    
    # pass the None value
    if Vo == None:
        pass

    else:
        # convert voltage into temperature value equations
        Vt = Vo*5
        Rt = (R * Vt)/(5-Vt)
        T = 1/((math.log(Rt/1000))/35441+(1/298.15))

        # temperature in celsius
        T_c = int(T-273)
        

        # print the temperature value
        print(T_c)

        # dager level temperature detected process         
        if T_c >40:
            board.digital[buzzer_pin].write(1) #buzzer is on
            time.sleep(1.5) #delay the time upto 100 millisecond
            board.digital[buzzer_pin].write(0) # buzzer is off

        else:
            board.digital[buzzer_pin].write(0) # buzzer is off

        # delay time
        time.sleep(0.3)

    
    

