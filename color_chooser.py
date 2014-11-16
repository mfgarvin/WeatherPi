#This isn't much, but this helps to define color codes for different colors!
import random
#Setting up the Pi...
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
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
complete = 0

print ("Hello! Just follow the prompts.")
print ("If you're looking for a random color, just hit enter throughout the prompts without entering a number.")
try:
    while True:
	r.ChangeDutyCycle(0)
	g.ChangeDutyCycle(0)
	b.ChangeDutyCycle(0)
	if complete == 1:
	    break
        while True:
	    try:
	        red = input("Choose a value for the Red LED between 0 and 100: ")
	        if 0 <= red <= 100:
	            break
	        else:
	            print ("I can't compute that. Try again?")
            except (ValueError, NameError):
                print ("I can't compute that. Try again?")
	    except SyntaxError:
		red = random.randint(0,100)
		break
	while True:
	    try:
	        green = input("Choose a value for the Green LED between 0 and 100: ")
		if 0 <= green <= 100:
		    break
		else:
		   print("I can't compute that. Try again?")
	    except (ValueError, NameError):
		print("I can't compute that. Try again?")
	    except SyntaxError:
		green = random.randint(0,100)
		break
        while True:
	    try:
	        blue = input("Choose a value for the Blue LED between 0 and 100: ")
	    	if 0 <= blue <= 100:
		    break
		else:
		    print("I can't compute that. Try again?")
	    except (ValueError, NameError):
		print("I can't compute that. Try again?")
	    except SyntaxError:
		blue = random.randint(0,100)
		break
	print
        print("Working...")
	r.ChangeDutyCycle(red)
	b.ChangeDutyCycle(blue)
	g.ChangeDutyCycle(green)
        print
        print("Great! Take a look at the LED and if you like what you see, jot down these color values:")
        print(red, green, blue)
        while True:
	    try:
	        answer = input("Press Enter to run this again. Otherwise, type 'quit': ")
                if answer == quit:
		    print ("Bye!")
	            complete = 1
		    break
	    except (ValueError, NameError):
		    continue
	    except SyntaxError:
		break
except KeyboardInterrupt:
    print	
    print("Goodbye!")
