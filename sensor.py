from math import atan2
from math import degrees
from math import floor
from math import sqrt
from comm import initComm

class sensor:
    """The sensor simulation class"""

    def __init__(self, sampleRate, sampleRateError, rotaionRate, rotationRateError, rangeOfMotion, buff, port):
    	self.sampleRate = sampleRate # sensor sends position data at this rate
    	if sampleRate <= 0:
    		print "Provide positive sample rate for proper sensor instantiation."
    	self.sampleRateError = sampleRateError
    	self.rotaionRate = rotaionRate # Degrees / second
    	self.rotationRateError = rotationRateError
    	self.orientation = 0 # Maximum angle = 45 degrees.
    	self.rangeOfMotion = rangeOfMotion
    	self.buff = buff

    	self.clockwiseRotation = True

        self.lastSample = None
        self.lastLocation = [None, None]

        self.port = port
        self.comm = initComm(port)
        print("\nOpened sensor communication.\n")
        self.sequenceNum = 0

    def incrementSequenceNum(self):
        if self.sequenceNum < 127:
            self.sequenceNum = self.sequenceNum + 1
        else:
            self.sequenceNum = 0

    def getSequenceNum(self):
        currSeqNum = self.sequenceNum
        self.incrementSequenceNum()
        return currSeqNum

    def getPort(self):
        return self.port

    def getComm(self):
        return self.comm

    def getSampleRate(self):
    	return self.sampleRate

    def getLastLocation(self):
        return self.lastLocation

    def getSampleRateError(self):
    	return self.sampleRateError

    def getRotationRate(self):
    	return self.rotaionRate

    def getRotationRateError(self):
    	return self.rotationRateError

    def getRangeOfMotion(self):
    	return self.rangeOfMotion

    def getBuff(self):
    	"""Return the distance from the sensor to the working area."""
    	return self.buff

    def getOrientation(self):
    	return self.orientation

    def orientSensor(self):
    	"""Simulates sensor rotation / servo activation"""

    	timeElapsed = 1/self.sampleRate # The period of sampling is the time elapsed

    	if self.clockwiseRotation == True:
    		self.orientation = self.orientation + timeElapsed*self.rotaionRate
    		if self.orientation > self.rangeOfMotion: # Reached limit of range of motion.
    			self.orientation = self.rangeOfMotion - (self.orientation - self.rangeOfMotion)
    			self.clockwiseRotation = False
    	else: # self.clockwiseRotation == False
    		self.orientation = self.orientation - timeElapsed*self.rotaionRate
    		if self.orientation < 0: # Reached limit of range of motion.
    			self.orientation = 0 + (0 - self.orientation)
    			self.clockwiseRotation = True
        #print ("Sensor orientation", self.getOrientation())

    def sample(self, roverPosition):
    	"""Fire the laser"""
    	# Simulate servo movement

    	self.orientSensor()

        #print ("Sensor orientation", self.getOrientation())

    	roverOrientation = degrees(atan2(roverPosition[1], roverPosition[0])) # Degrees.

    	if abs(self.getOrientation() - roverOrientation) < 1: # The sensor is aimed within a 2 cm margin of the center of the rover. 
            # The sensor is pointing at the rover.
            self.lastSample =  sqrt(roverPosition[0] + roverPosition[1])
            self.lastLocation = roverPosition
            print("")
            print("*Sampled the rover*", self.lastLocation)
            print("")
    	    return True

    	return False

