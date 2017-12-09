# lastminuteconferenceroom

Problem - Have you ever faced the situation when you need conference room and calendar shows no room available. 
But actually you know if you walk around the building, you will find booked and vacant rooms?
This program may be useful for you.

How does it work ?
A sound sensor is connected to Raspberry Pi. Python program runs on Pi to detect silence (for configured time). 
Once it detects that room is vacant for configured time, it checks if room is booked on calendar (Google Calendar) in this case,
and delete the event from conference room's calendar. Now room will be available for the ones who need it.
