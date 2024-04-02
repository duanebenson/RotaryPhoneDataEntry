##########################################################
#
# Rotary phone "Numberic keypad"
# by Duane Benson, September, February 2024
#
# This configuration uses: 
#   Unexpected Maker TinyS3, ESP32 based microcontroller board, CircuitPython V 8.X
#   1950's vintage Bell System model F1 rotary desk phone
#
#   Written in CircuitPython
#   Read more in the accompanying article in Design News, by Duane Benson
#
#   Rotary phone dials (yes, this is where the term “dial” a phone comes from) transmit numbers as a series of 
#   electric pulses. When you pick up the handset, a current loop is created between the phone and the local 
#   phone exchange. If I recall correctly, the two active conductors, labled tip and ring carried 48 volts at 
#   low current when off hook (the phone handset was picked up). Each number in the dial would have a momentary 
#   switch to break the loop and the dial is spring loaded. The break is approximately 40 milliseconds long with 
#   a 60 ms pause between breaks. The timing is regulated by the mechanical clock spring that spins the dial 
#   back to its home position.
#
#   If you turn it to the number 3, for example, it will spin back to its home position and break the current 
#   loop three times, once for each number it passes. Zero (0) is in the last spot and gets ten pulses. That 
#   means that in an analog rotary phone system, numbers one through ten are represented, but the MSB for ten 
#   is essentially stripped off to turn it into a zero.
#
# Note that my naming convention uses a leading capital for hardware pins and a leading lower case for constants and variables
# While Python doesn't really have a constant, I use a leading lower case "c" to indicate that it is supposed to be a constant
#
# Diagnostic "print" functions will only show if you connect a terminal application in your PC to
# the USB/Com port from the TinyS3.
#
##########################################################


#############################
# External libraries
#############################
import time, gc, os
import board
import digitalio
import tinys3
from digitalio import DigitalInOut, Direction, Pull

# USB HID libraries
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

#############################
# Hardware pin declarations
#############################
pDialActive = board.IO4         # Indicates that dial is being used (0 when not being used. 1 when being used)
pDigitPulse = board.IO5         # CPulses as digit spots are passed. Pulse is a 1->0->1
pOffHook = board.IO3            # State of handset (0 when on hook. 1 when off hook)
LedPin1 = board.IO6             # Status LED

UARTrx = board.RX               # UART RX is pin 44 on the TinyS3
UARTtx = board.TX               # UART TX is pin 43 on the TinyS3


#############################
# Constants and variable declarations
#
# Variables do not need to be pre-defined in Python. However, they will be given a global or local
# state depending on whena and where they are first used. Anything that will be global but may also be
# used within a function should be defined outside the function first to ensure that it is treated as 
# global. In most languages, it's best practice to pre-define variables anyway, even if not required.
#############################
cUARTbaud = 115200               # For communicating through the UART

dialActive = 0                   # Indicates that dial is being used or not (0 when not being used. 1 when being used)
digitPulse = 0
offHook    = 0                   # Indicates the handset is on hook                            
digitCount = 0                   # The variable that holds the count of pulses, meaning the digit value
numberToReturn = 0

#############################
# Creating object instances
#############################

# "DialState" input digital input object
oDialActive = digitalio.DigitalInOut(pDialActive)           # Connect the dial active input pin
oDialActive.direction = Direction.INPUT       # Set to digital input
oDialActive.pull = Pull.DOWN                  # Apply internal pull-down resistor

# "DigitPulse" input digital input object
oDigitPulse = digitalio.DigitalInOut(pDigitPulse)           # Connect the dial active input pin
oDigitPulse.direction = Direction.INPUT       # Set to digital input
oDigitPulse.pull = Pull.DOWN                  # Apply internal pull-down resistor

# "OffHook" input digital input object
oOffHook = digitalio.DigitalInOut(pOffHook)           # Connect the dial active input pin
oOffHook.direction = Direction.INPUT       # Set to digital input
oOffHook.pull = Pull.DOWN                  # Apply internal pull-down resistor

# LED status indicator digital output object
oStatusLed = digitalio.DigitalInOut(LedPin1)         # Connect the LED status pin
oStatusLed.direction = Direction.OUTPUT    # Set to digital output

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

#############################
# Helper functions
#############################

# Read hook state with debounce delay
def hookState():
    LoffHook = oOffHook.value
    time.sleep(0.005)
    oStatusLed.value = LoffHook 
    return LoffHook


#############################
# Main code
#############################

while True:

    offHook = hookState()
    oStatusLed.value = offHook 
    print("Sleeping")
    while (not offHook):
        offHook = hookState()
    
    print("Waiting to dial")
    digitCount = 0
    dialActive = oDialActive.value          # Check to see if dialing
    while (not dialActive):                 # Wait if not dialing
        dialActive = oDialActive.value      # Check to see if dialing
        time.sleep(0.005)
        offHook = hookState()
        if not offHook: break

    print("Dial is active")
    while (dialActive):                     # Stay in loop as long as dial is active
        digitPulse = oDigitPulse.value
        time.sleep(0.005)
        if (not digitPulse):                # Increment counter and wait if digit pulse is detected
            digitCount += 1
            while (not digitPulse):
                digitPulse = oDigitPulse.value

        dialActive = oDialActive.value      # Check to see if still dialing
        if (not dialActive):
            numberToReturn = digitCount
            #if (numberToReturn == 10): numberToReturn = 0  # Needed if I were sending ASCII or binary. The HID keyboard codes don't need this
            print ("\n\nFinal Number dialed =", end = " ")
            print(numberToReturn)
            kbd.send(numberToReturn + 0x1d) # Add 0x1d to match numbers with HID keyboard codes. Note that "0" is the tenth value in digit sequence in HID codes
            kbd.release_all()
            
        offHook = hookState()
        if not offHook: break

