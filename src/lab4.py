"""!
@file lab4.py
This file contains code to plot step response of an RC circuit.

@details This file uses the serial module to communicate with the Nucleo to read output voltage to plot the step response.

@author Nishka Chawla
@author Ronan Shaffer
@date   14-Feb-2022
@copyright (c) Released under GNU Public License
"""

import serial
from matplotlib import pyplot
import time
## Stores time values of step response
time_list = []
## Stores position values of encoder during step response
pos_list = []

# Open serial port for communication between PC and Nucleo
with serial.Serial('COM11', 115200) as s_port:
    s_port.flush()
    # data = s_port.readline()
    # if data == b'raw REPL; CTRL-B to exit\r\n':
    s_port.write(b'\x02') #ctrl-B
    s_port.write(b'\x03') #ctrl-C
    s_port.write(b'\x04') #runs main -- ctrl-D
    time.sleep(0.5)
    
    ## Runs counter controls number of iterations of data reading
    runs = 0
    
    while runs <= 1000:
        ## Stores single line of data read from serial port
        raw_data = s_port.readline()
        
        ## Converts data type and removes non-number characters
        # print(raw_data)
        data = str(raw_data)
        data = data[2:-5]
        # data = data[:-7]
        ## Splits string of data into separate time and position values
        l = data.split(',')
        if len(l) == 2:
            print(l)
            try:
                ## Convert time value to float
                time = float(l[0])
                ## Convert position value to float
                pos = float(l[1])
                
            except:
                pass
            
            else:
                # Add current time and position values to list for ploting
                # if time < 2000:
                time_list.append(time)
                pos_list.append(pos)
    #            
            runs += 1
            
    # print(len(time_list))
    ## Color of plot
    pyplot.plot(time_list, pos_list, color = 'b')
    pyplot.xlabel('Time [ms]')
    pyplot.ylabel('Voltage [mV]')
    pyplot.title('Step Response of RC Circuit')
    pyplot.show()


