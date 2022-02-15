"""!
@file main.py
This file contains code used to perform the step response of an RC circuit.

@details The main script measures an analog voltage by reading from an ADC object to perform the step response for an RC circuit.
    
@author Nishka Chawla
@author Ronan Shaffer
@date   14-Feb-2022
@copyright (c) Released under GNU Public License
"""

import pyb
import utime
import array
import task_share

import micropython
micropython.alloc_emergency_exception_buf(100)

## The input pin for the Nucleo. 
pc0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)
## The output pin for the Nucleo. 
pc1 = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
## Variable reading from the ADC.
adc = pyb.ADC(pc0)

## Instantiation of Encoder 2 reading shared variable.
queue = task_share.Queue ('h', 1000, thread_protect = False, overwrite = False,
                        name = "adcreading")

## Array storing time data.
time_list = array.array("f", [0] * int(1002))

queue.clear()

## Index to iterate through arrays
runs = 0

## Start time variable.
start_time = utime.ticks_ms()

def interrupts(tim):
    """!
    Interrupt callback function.
    @param tim Timer object used for interrupts
    """
    global runs
    
    if runs <= 1000:
#         adc.read()
        queue.put(adc.read(), in_ISR = True)
        ## Index time variable
        g_time = utime.ticks_ms()
        ## Time data list
        time_list[runs] = utime.ticks_diff(g_time, start_time)
        runs += 1
    else:
        pc1.low()
        tim.callback(None)
        
        
if __name__ == "__main__":
    ## Timer object used for interrupts.
    tim = pyb.Timer(1, freq=500)
    pc1.high()
    tim.callback(interrupts)
    ## Index variable
    idx = 0
    while idx <= 1000:
        ## Voltage data variable
        pos = queue.get()
        print('{:},{:}'.format(time_list[idx], pos))
        idx += 1
    
