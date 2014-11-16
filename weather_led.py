#TODO:
#
#Specify RGB values for all of the situations. I might want to change a couple of the blink rates as well
#Automaticlly set alert to ... after time equals epoch_expire time in the json
#incorporate a dismiss button to set the alert to a solid indicator instead of having it blink continously.
#Build in a quick blue "blip" indicating that the program is running.
#
import json
import urllib2
import time
import RPi.GPIO as GPIO
import sys

#Setting some variables
APIKEY = "0f9045beb1c7e0e7"
CITY = "Cuyahoga_Falls"
STATE = "OH"
last_call = 0
update_interval = 30
last_flip = time.time() + 1
flip_time = 0.3
firstrun = 0
watch = 0
last_indication = 0
indication_time = 60
err = 0
print ("Starting up...")

#Initializing the GPIO pins...
GPIO.setmode(GPIO.BCM)
GPIO.setup(00, GPIO.OUT)
GPIO.setup(01, GPIO.OUT)
GPIO.setup(04, GPIO.OUT)
GPIO.output(00, 1)
GPIO.output(01, 1)
GPIO.output(04, 1)
r = GPIO.PWM(00, 60)
g = GPIO.PWM(01, 60)
b = GPIO.PWM(04, 60)
r.start(0)
g.start(0)
b.start(0)

#This function puts the program to sleep for the smallest value of time between actions (LED cycling, Weather updating, and debug LED cycling)
def sleep():
    time.sleep(min(abs(time.time() - last_flip - flip_time), abs(time.time() - last_call - update_interval), abs(time.time() - last_indication - indication_time)))

#This function pulls weather data from wunderground.com, stores it, and puts it into the correct array. 
def load_weather():
    global err
    try:
        response = urllib2.urlopen('http://api.wunderground.com/api/' + str(APIKEY) + '/alerts/q/' + str(STATE) + '/' + str(CITY) + '.json')
	if response == urllib2.urlopen('http://api.wunderground.com/api/' + str(APIKEY) + '/alerts/q/' + str(STATE) + '/' + str(CITY) + '.json'):
	    err = 0
#        response = urllib2.urlopen('http://127.0.0.1/changeme.json')
	html = response.read()
	report = json.loads(html)
    except (urllib2.HTTPError, urllib2.URLError):
	print (time.strftime("%I:%M:%S, Having trouble connecting to the internet... Ignoring for now."))
	err = "web" 
#	print ("Error Code Changed - Web Exception")
    global a1
    global a2
    global a3
    global a4
    global a5
    global update_interval
    try:
        a1 = report['alerts'][0]['type']
	print (a1)
#	err = 0
	if a1 == 'WIN':
	    update_interval = 300
	else:
	    update_interval = 60
    except (IndexError, UnboundLocalError):
	a1 = "..."
	print (a1)
	update_interval = 300
#	err = "web"
#	print ("Error Code Changed - Web Exception 2")
    try:
        a2 = report['alerts'][1]['type']
	print (a2)
#	err = 0
    except (IndexError, UnboundLocalError):
	a2 = "..."
	print (a2)
    try:
        a3 = report['alerts'][2]['type']
	print (a3)
#	err = 0
    except (IndexError, UnboundLocalError):
	a3 = "..."
	print (a3)
    try:
        a4 = report['alerts'][3]['type']
	print (a4)
#	err = 0
    except (IndexError, UnboundLocalError):
	a4 = "..."
	print (a4)
    try:
        a5 = report['alerts'][4]['type']
	print (a5)
#	err = 0
    except (IndexError, UnboundLocalError):
	a5 = "..."
	print (a5)
    
    global last_flip
    try:
	if last_flip == float("inf") and LED[a1]['T'] != 0:
	    last_flip = time.time() - 1
    except KeyError:
	pass
#The LED Indicator Color Values and Timings
LED = { 'TOR': { 'R': 100, 'G': 0, 'B': 0, 'T': 1 }, 'TOW': { 'R': 100, 'G': 0, 'B': 0, 'T': 0 }, 'WRN': { 'R': 100, 'G':50, 'B': 0, 'T': 1 }, 'SEW': { 'R': 100, 'G': 50, 'B': 0, 'T': 0 }, 'WIN': { 'R': 25, 'G': 25, 'B': 100, 'T': 2.3 }, 'FLO': { 'R': 25, 'G': 100, 'B': 10, 'T': 1 }, 'WAT': { 'R': 25, 'G': 100, 'B': 10, 'T': 0 }, 'WND': { 'R': 60, 'G': 60, 'B': 80, 'T': 2.3 }, 'SVR': { 'R': 100, 'G': 50, 'B': 0, 'T': 2.3 }, 'HEA': { 'R': 0, 'G': 0, 'B': 0, 'T': 2.3 }, 'FOG': { 'R': 0, 'G': 0, 'B': 0, 'T': 2.3 }, 'SPE': { 'R': 0, 'G': 0, 'B': 0, 'T': 2.3 }, 'FIR': { 'R': 0, 'G': 0, 'B': 0, 'T': 2.3 }, 'VOL': { 'R': 0, 'G': 0, 'B': 0, 'T': 2.3 }, 'HWW': { 'R': 0, 'G': 0, 'B': 0, 'T': 1 }, 'HUR': { 'R': 1, 'G': 0, 'B': 0, 'T': 2.3 }, 'REC': { 'R': 0, 'G': 0, 'B': 0, 'T': 2.3 }, 'REP': { 'R': 0, 'G': 0, 'B': 0, 'T': 2.3 }, 'PUB': { 'R': 0, 'G': 0, 'B': 0, 'T': 2.3 }, 'ERR': { 'R': 100, 'G': 0, 'B': 0, 'T': 5 }}

#Warning = .5 seconds, Watch = 0 seconds, Advisory + General Info = 2.3

while True:
    try:
	if time.time() >= last_call + update_interval:
	    load_weather()
	    last_call = time.time()
	    print (time.strftime("%I:%M:%S, Weather was loaded"))
	    print (time.strftime("%I:%M:%S, Sleep was called via weather function"))
	    sleep()
	
	elif time.time() >= last_flip + flip_time:
	    if a1 != "...":
		if GPIO.input(00) == 1 or GPIO.input(01) == 1 or GPIO.input(04) == 1:
		    r.ChangeDutyCycle(0)
	   	    g.ChangeDutyCycle(0)
		    b.ChangeDutyCycle(0)
		    flip_time = LED[a1]['T']
		    print (time.strftime("%I:%M:%S, LED off, last_flip updated, Sleep was called"))
	       	    last_flip = time.time()
		    sleep()
		
		else:
		    r.ChangeDutyCycle(LED[a1]['R'])
		    g.ChangeDutyCycle(LED[a1]['G'])
		    b.ChangeDutyCycle(LED[a1]['B'])
		    flip_time = LED[a1]['T']
		    last_flip = time.time()
		    print (time.strftime("%I:%M:%S, LED color was called, last_flip updated, Sleep was called"))
		    if flip_time == 0:
		        last_flip = float("inf")
		        sleep()
		    else:
	                sleep()
	
	    else:
                r.ChangeDutyCycle(0)
                g.ChangeDutyCycle(0)
                b.ChangeDutyCycle(0)
	        flip_time = 0
	        last_flip = float("inf")
                print (time.strftime("%I:%M:%S, LED off, Sleep was called"))
	        sleep()
	
	if time.time() >= last_indication + indication_time:
	    if err == "web":
		r.ChangeDutyCycle(100)
		time.sleep(1)
		r.ChangeDutyCycle(0)
		indication_time = 5
		last_indication = time.time()
		if a1 != "...":
		    err = 0
		sleep()
	    if err == "sys":
		r.ChangeDutyCycle(50)
		indication_time = 5
		last_indication == time.time()
		sleep()
	    if a1 == "..." and err == 0:
	    	    b.ChangeDutyCycle(100)
	            time.sleep(0.10)
	            b.ChangeDutyCycle(0)
		    indication_time = 60
	            last_indication = time.time()
	            print (time.strftime("%I:%M:%S, LED flickered normally"))
#		    print (err)
#		    print ("^^^ Current Error Code")
#		    print (last_indication)
#		    print (time.time())
	            sleep()
    except:
	print "Error:", sys.exc_info()[0]
	err = "sys"
	raise
