# Motion-Detection
Using opencv, checks for any amount of sustained movement and sends a notifcation to my phone with a picture if found.

This is my first project / attempt at doing anything with the opencv library, and i've come to realize that its a very in-depth and expansive library at that.
There are likely ways to do what I have done but better, and i'll be fixing/improving the program if I figure that out. But for now this is a very early version of a motion detection system

# Notifications
To actually send notifications I used the pushbullet API and wrote the currect frame into a jpg, 
so I could attach that to the message I would send thus reciving both a notification and a picture to fully know what set off the camera

# Examples
SMS notification + image:
![smsnotif](https://user-images.githubusercontent.com/99112665/163859390-cae02397-b819-425b-8346-08241bdc1f77.jpg)
