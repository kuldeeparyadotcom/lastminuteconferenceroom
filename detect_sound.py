#!/usr/bin/python3

"""
Purpose - To demonstrate how sound sensor can be used to detect if room is occupied or not
Logic - 
If no sound detected for last 10 minutes, mark the room available (configurable)
"""

import RPi.GPIO as GPIO
import time

#Integration with Google Calendar
import GoogleCalendarDemo

channel = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

#Logic to detect if someone is really in meeting room
from datetime import datetime

tracker = {} #Empty dict for tracking
tracker["last_time_sound_detected"] = datetime.now() #Originally to start
def callback(channel):
    print("Sound detected")
    tracker["last_time_sound_detected"] = datetime.now() #Capture current timestamp
    

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300) #Detect when pin goes high or low
GPIO.add_event_callback(channel, callback) #Assign function to GPIO Pin, Run function on change

#Infinite Loop
while True:
    #poll every 10 seconds - It is configurable
    diff = datetime.now() - tracker["last_time_sound_detected"]
    silence_duration = diff.seconds
    print("Room is found silent for", silence_duration)

    if silence_duration >= 10:
        print("Meeting from conference room calendar will be auto removed")
        GoogleCalendarDemo.main()
        print("Meeting removed from calendar")
    time.sleep(10)
