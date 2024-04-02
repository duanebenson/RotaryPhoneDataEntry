# RotaryPhoneDataEntry
Code and instructions for converting a rotary phone to a USB numeric data entry
# Rotary phone "Numeric keypad"
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
