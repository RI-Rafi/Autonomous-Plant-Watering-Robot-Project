The Python functions specifically target the robot's individual operations, such as calculating the distance from the pot
using the distance function, which raises a pully using stepper function to pull/lower ultrasonic sensor and get sensor 
reading, then using that to calculate the  water amount. A seperate water2 function calculates remaining water from 
pump_water function's remaining time, which itself is a PID inspired function that integrates water time or water
weight as a function of robot wheel speed, that maneuvers robot slowly when full of water and faster when water 
level is below the spill thresehold. I integrated all the functions by importing them in main.py, which has a 
toggle switch between autonomous mode and website controlled mode that is broadcast with the Raspberry Pi
Pico W and I connect my phone to manually perform robot functions.
