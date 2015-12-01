import sys
from time import sleep
from time import time
from rover import rover
from control import control
from sensor import sensor
import string
from theMap import theMap
import comm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import pi
import random

def buildMap(mapFileName):
	return theMap(mapFileName)

def instantiateRover(params, messagePeriod):
	"""Instantiate the rover."""
	
	# Parse out the rover attributes.
	for param in params:
		words = param.split('=', 1)
		if words[0] == "system":
			continue
		elif words[0] == "rotationSpeed":
			rotationSpeed = float(words[1])
		elif words[0] == "forwardSpeed":
			forwardSpeed = float(words[1])
		elif words[0] == "rotationSpeedError":
			rotationSpeedError = float(words[1])
		elif words[0] == "forwardSpeedError":
			forwardSpeedError = float(words[1])
		elif words[0] == "x":
			x = float(words[1])
		elif words[0] == "y":
			y = float(words[1])
		elif words[0] == "orientation":
			orientation = float(words[1])
		elif words[0] == "port":
			port = words[1]
		else:
			print "Rover instantiation received undefined attribute"

	# Instantiate the rover and return its handle.
	return rover(rotationSpeed, forwardSpeed, rotationSpeedError, forwardSpeedError, x, y, orientation, port, messagePeriod)


def instantiateSensor(params):
	"""Instantiate the sensor."""

	# Parse out the rover attributes.
	for param in params:
		words = param.split('=', 1)
		if words[0] == "system":
			continue
		elif words[0] == "sampleRate":
			sampleRate = float(words[1])
		elif words[0] == "sampleRateError":
			sampleRateError = float(words[1])
		elif words[0] == "rotationRate":
			rotationRate = float(words[1])
		elif words[0] == "rotationRateError":
			rotationRateError = float(words[1])
		elif words[0] == "rangeOfMotion":
			rangeOfMotion = int(words[1])
		elif words[0] == "buff":
			buff = float(words[1])
		elif words[0] == "port":
			port = words[1]
		else:
			print ("Sensor instantiation received undefined attribut: ", words[0])

	# Instantiate the sensor and return its handle.
	return sensor(sampleRate, sampleRateError, rotationRate, rotationRateError, rangeOfMotion, buff, port)

def instantiateControl(params):
	"""Instantiate the control."""

	# Parse out the rover attributes.
	for param in params:
		words = param.split('=', 1)
		if words[0] == "system":
			continue
		# elif words[0] == "rate":
		# 	rate = float(words[1])
		# elif words[0] == "rateError":
		# 	rateError = float(words[1])
		else:
			print "Control instantiation received undefined attribute"

	# Instantiate the sensor and return its handle.
	return control()

def instantiateSystems(configFileName, messagePeriod):
	"""Instantiate the control, rover and sensor systems."""

	# Parse the configuration file by line.
	configFile = open(configFileName, 'r')
	for system in configFile: # Each line represents a system
		params = system.split() # Each paramater is of the form attribute=value.
		if "rover" in params[0]:
			r = instantiateRover(params, messagePeriod)
		elif "sensor" in params[0]:
			s = instantiateSensor(params)
		elif "control" in params[0]:
			c = instantiateControl(params)
		else:
			print ("Undefined system configuration: ", params[0])

	# Check for a problem instantiating a system.
	if r == None:
		print "Did not instantiate the rover."
	if s == None:
		print "Did not instantiate the sensor."
	if c == None:
		print "Did not instantiate the control."

	if r.getPosition()[0] < 0 or r.getPosition()[0] > 150:
		print "Rover not initialized within X bounds"

	if r.getPosition()[1] < s.getBuff() or r.getPosition()[1] > 75:
		print "Rover not initialized within Y bounds"

	r.setBuff(s.getBuff())

	return (r, s, c)
	
def config(configFileName, mapFileName, messagePeriod):
	"""Configure the system."""

	m = buildMap(mapFileName)
	systs = instantiateSystems(configFileName, messagePeriod)
	# Set the rover's initial position
	#systs[0].setPosition(0, systs[1].getBuff())
	return m, systs

def main(argv): 

    # Create rover and sensor threads.
    #time = float(0)
    frequency = 1000*float(argv[3]) # Ten times faster than the message rate.
    period = 1/frequency
    loopCount = 0
    messagePeriod = 1/float(argv[3])
    # command = None # Could be left, right move

    # Configure the system for simulation.
    m, systs = config(argv[1], argv[2], messagePeriod) # systs[0] = rover, systs[1] = sensor, systs[2] = control

    r = systs[0]
    roverCommandFreq = float(argv[3])
    roverCommandPeriod = 1/roverCommandFreq

    lastSampleTime = 0

    movementDurration = 0
    movementStart = 0
    executingMovement = 0

    print ("Loop period", period)
    print("")
    startTime = time()

    sampleFreq = systs[1].getSampleRate()
    samplePeriod = 1/sampleFreq
    print("sample period", samplePeriod)

    sampleLoopFrequency = frequency/sampleFreq

    while(1):

        sleep(period) # Inverse of frequency = period
        elapsedTime = loopCount*period
        print ("loop count", loopCount)
        print("elapsedTime", elapsedTime)

        if (loopCount % sampleLoopFrequency == 0):
         	#elapsedTime = time - lastSampleTime
         	systs[1].sample(systs[0].getPosition()) # The sensor needs the "physical location of the rover"
         	#lastSampleTime = time
         	print("sample")

        #if loopCount % 1000 == 0: # Rover receives instruction from control
        # elif loopCount == 2000:
        #  	r.move(5, roverCommandPeriod)
        # elif loopCount == 3000:
        # 	break;

       	# Sensor messages most recent sensor sample to controller.
       	# Control messages rover. 
       	# Rover Messages control. 
        if loopCount % 1000 == 0 and loopCount > 0:

            comm.sendMessage(systs[1].getSequenceNum(), systs[1].getLastLocation()[0], systs[1].getLastLocation()[1], systs[1].getComm())
            print("Sensor messaged sampled rover location to control", systs[1].getLastLocation()[0], systs[1].getLastLocation()[1])
            receivedMessage = comm.receiveMessage(systs[0].getComm())
            print ("Control messaged rover.", receivedMessage[0], receivedMessage[1])
            print("radius", receivedMessage[1])
            print("sign", receivedMessage[0])
            if receivedMessage[0] == 3:
                r.move(0-(receivedMessage[1]), roverCommandPeriod)
                print("radius is", 0-receivedMessage[1])
            elif receivedMessage[0] == 2:
                r.move(receivedMessage[1], roverCommandPeriod)
            elif receivedMessage[0] == 1: # going straight
            	if receivedMessage[1] == 0:
            		r.stop()
            	else:
            		r.move(10000, roverCommandPeriod)


        if loopCount == 100000:
        	break;

        # if ((time - movementStart) < movementDurration) and executingCommand == True:
        # 	systs[0].move(period)
        # else:
        # 	executingCommand = False
        	#comm.sendMessage(systs[0].getSequenceNum(), 0, 0, systs[0].getComm())


        loopCount = loopCount + 1
 
    pass

    print("times", r.getMovementTimes())
    plt.plot([0, 50], [25, 25])
    plt.plot([50, 50], [25, 50])
    plt.plot([50, 100], [50,50])
    plt.plot(r.getXHist(), r.getYHist(), 'ro')
    plt.ylabel('Rover Position')
    plt.axis([0, 150, 0, 75])
    plt.show()

    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.plot(xs = r.getMovementTimes(), ys = r.getXHist(), zs = r.getYHist())
    # plt.show()

if __name__ == "__main__": 
    main(sys.argv)

