import time														# time module
import RPi.GPIO as gpio													# GPIO ports module
import os														# OS module						
gpio.setmode(gpio.BCM)													# define pinout schema
gpio.setwarnings(False)													# disable GPIO warnings

arm_pin = 27														# define pin for arming
pir_pin = 22														# define pin for pir sensor
irl_pin = 23														# define pin for infra leds relay

gpio.setup(arm_pin, gpio.IN, pull_up_down=gpio.PUD_UP)									# activate arm_pin as input with pull up 
gpio.setup(pir_pin, gpio.IN)	        										# activate pir_pin as input
gpio.setup(irl_pin, gpio.OUT)												# acitvate irl_pin as output

while True:														
	if gpio.input(pir_pin) and gpio.input(arm_pin):									# do if pir_pin and arm_pin is high
		print("PIR ALARM!")											# print PIR ALARM!
		gpio.output(irl_pin, 1)											# switch infra leds on
		os.system("raspistill -t 0 -w 640 -h 480 -o /home/pi/alarm/alarm.jpg")					# make photo
		os.system("mailx -s ALARM -a /home/pi/alarm/alarm.jpg email@email.com < /home/pi/alarm/alarm.txt")	# send photo in email	    		
		os.system("raspivid -t 60000 -o /home/pi/alarm/alarm.h264")						# make 1 min video
		time.sleep(0.5)												# wait 0.5 sec
		gpio.output(irl_pin, 0)											# switch infra leds off
