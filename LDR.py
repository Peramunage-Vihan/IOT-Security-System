from pyfirmata import Arduino, util, INPUT,OUTPUT #import pyfirmata module
import time #import time module


board = Arduino("COM3") #Arduino port
ldr_pin = 0 #ldr pin
led_pin_g = 2 #green light led pin
led_pin_r = 7 #red light led pin

# anlog,digital output & input 
board.analog[ldr_pin].mode = INPUT
board.digital[led_pin_g].mode = OUTPUT
board.digital[led_pin_r].mode = OUTPUT


it = util.Iterator(board)
it.start()

board.analog[ldr_pin].enable_reporting()

# initial times
dot_space_start_time = 0
dash_space_start_time=0
space_end_time = 0
start_time = 0
end_time = 0

# morse code list
code = []

# encoded morse code list
decode_morse = []

# previous ldr value
previous_ldr_val = 0.9

# morse code dictionary
morse_code_dict = {".____":"1",
                    "..___":"2",
                    "...__":"3",
                    "...._":"4",
                    ".....":"5",
                    "_....":"6",
                    "__...":"7",
                    "___..":"8",
                    "____.":"9",
                    "_____":"0",
                    "._" : "A",
                    "_...":"B",
                    "_._.":"C",
                    "_..":"D",
                    ".":"E",
                    ".._.":"F",
                    "__.":"G",
                    "....":"H",
                    "..":"I",
                    ".___":"J",
                    "_._":"K",
                    "._..":"L",
                    "__":"M",
                    "_.":"N",
                    "___":"O",
                    ".__.":"P",
                    "__._":"Q",
                    "._.":"R",
                    "...":"S",
                    "_":"T",
                    ".._":"U",
                    "..._":"V",
                    ".__":"W",
                    "_.._":"X",
                    "_.__":"Y",
                    "__..":"Z"}


while True:
    # red led light on
    board.digital[led_pin_r].write(1)

    # ldr value
    ldr_val = board.analog[ldr_pin].read()
    print(ldr_val)

    # pass the None value
    if ldr_val == None:
        pass

    else:
        # time claculation process
        if ldr_val < 0.9 and previous_ldr_val > 0.9:
            start_time = time.time()
            dot_space_start_time = time.time()

        elif ldr_val > 0.9 and previous_ldr_val < 0.9:
            dash_space_start_time = time.time()
            end_time = time.time()
            space_end_time = 0

        elif ldr_val > 0.9 and previous_ldr_val>0.9:
            space_end_time = time.time()
            end_time=0
            start_time=0
        
        # time duration between letter space or word space after dash
        dash_space_duration =space_end_time - dash_space_start_time

        # time duration between letter space or word space after dot
        dot_space_duration = space_end_time - dot_space_start_time

        # time duration between dot or dash
        duration = end_time - start_time 

        # find the dot
        if duration > 0.3 and duration < 0.61:
            code += ["."]
        
        # find the dash
        elif (duration >0.85 and duration < 1.3):
            code += ["_"]

        # space between letters or numbers after the dot
        if dot_space_duration > 0.89 and dot_space_duration< 0.95:
            code += [" "]

        # space between letter or number after the dash
        if len(code)>0:
            if (dash_space_duration > 0.6 and dash_space_duration< 0.65) and code[-1] == "_":
                code += [" "]

        # space between words
        if dot_space_duration> 1.8 and dot_space_duration < 1.9:
            code += ["-"]
            code += [" "]

        # letter, word or sentence encoding process
        if dot_space_duration >3 and dot_space_duration <3.2:
            
            # mosh code string with dot and dash
            code_str = "".join(code)
            
            # split list that split from single spacing
            code_str_split = code_str.split(" ")

            # morse code encoding processing
            for morse in code_str_split:
                if morse == "-":
                    decode_morse += [" "]
                for key,value in morse_code_dict.items():
                    if morse == key:
                        decode_morse += [value]

            # morse code list clear        
            code.clear()

            # remove the unnesasery last element of the decode_morse list 
            if len(decode_morse)>0:
                decode_morse.pop(-1)

            # convert decode_morse list to the string
            decode_morse_str = "".join(decode_morse)

            # check whether the password is correct or incorrect
            if decode_morse_str == "67AB":
                board.digital[led_pin_r].write(0) #if password is correct red led is off
                board.digital[led_pin_g].write(1) # green light is on
                time.sleep(2.5) # delay time                
                board.digital[led_pin_g].write(0) # after 2.5 sec green light is off 
                board.digital[led_pin_r].write(1) # red light is on again

                # decode_morse list clear
                decode_morse.clear()
            
            # if password is incorrect decode_morse list is cleared
            else:
                decode_morse.clear()

        

        # assign the previous ldr value to previous_ldr_val variable
        previous_ldr_val = ldr_val
        
        # delay time
        time.sleep(0.3)