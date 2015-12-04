from math import radians
from math import degrees
from math import cos
from math import sin
from math import pi
from math import atan
from math import atan2
from comm import initComm
from math import ceil
import time
import random

class rover:
    """The rover simulator class"""

    def __init__(self, rotationSpeed, forwardSpeed, rotationSpeedError, forwardSpeedError, x, y, orientation, port, messagePeriod):
    	self.rotationSpeed = rotationSpeed # Degrees per second.
    	self.forwardSpeed = forwardSpeed
    	self.rotationSpeedError = rotationSpeedError
    	self.forwardSpeedError = forwardSpeedError
    	self.length = 5 # length = 5 cm
    	self.width = 3 # width = 3 cm
        #self.position = [None] * 10
        self.position = []
    	self.position.append((x, y))
        self.orientation = []
    	self.orientation.append(orientation)
    	self.buff = 0
    	self.movement = None
        self.messagePeriod = messagePeriod

        self.times = []
        self.times.append(0) # T0 = rover instantiation

    	self.initTime = time.time()

    	self.comm = initComm(port)
    	print("\nOpened rover location.\n")
    	self.sequenceNum = 0

    def getComm(self):
    	return self.comm

    def incrementSequenceNum(self):
    	if self.sequenceNum < 127:
    		self.sequenceNum = self.sequenceNum + 1
    	else:
    		self.sequenceNum = 0

    def getSequenceNum(self):
    	return self.sequenceNum

    def getRotationSpeed(self):
    	return self.rotationSpeed

    def getRotationSpeedErrorpeed(self):
    	return self.rotationSpeed

    def getForwardSpeed(self):
    	return self.forwardSpeed

    def getRotationSpeedError(self):
    	return self.rotationSpeedError

    def getForwardSpeedError(self):
    	return self.forwardSpeedError

    def getPosition(self):
    	return self.position[-1] # Gets the first-to-last element, i.e. the last element

    def setPosition(self, x, y):
    	self.position.append((x, y))

    def getOrientation(self):
    	return self.orientation[-1] # Gets the first-to-last element, i.e. the last element

    def setOrientation(self, orientation):
    	self.orientation.append(orientation)

    def setBuff(self, buff):
    	self.buff = buff

    def getOrientationHistory(self):
        return self.orientation

    def getPositionHistory(self):
        return self.position

    def getYHist(self):
        yCoords = []
        for position in self.position:
            yCoords.append(position[1])
        return yCoords

    def getXHist(self):
        xCoords = []
        for position in self.position:
            xCoords.append(position[0])
        return xCoords

    def setTime(self, theTime):
        self.times.append(theTime)

    def getTime(self):
        return self.times[-1]

    def getInitTime(self):
        return self.initTime

    def getMovementTimes(self):
        return self.times

    def stop(self):
        print "stopped!!!"
        pass # do

    def getMessagePeriod(self):
        return self.messagePeriod


    def move(self, r, durration):
    	"""The rover's movement method"""
    	# Positive radius: rightward turn.
    	# Negative radius: leftward turn.
    	# Infinity: straight.
    	# Negative infinity: straight.

        self.setTime(self.getTime() + self.getMessagePeriod())

        if self.getOrientation() < -(3*pi)/2:
                self.setOrientation(self.getOrientation() + 2*pi)
        elif self.getOrientation() > (3*pi)/2:
            self.setOrientation(self.getOrientation() - 2*pi)

        print("Rover orientation", self.getOrientation())
    	print ("moving from", self.getPosition()[0], self.getPosition()[1])

    	dist = self.getForwardSpeed() * durration
        print ("distance to go", dist)

    	if (r < 1) and (r > -1): # Turn radius is too small; turn is too sharp * Make thresholds configurable
    		print("turn radius too small")
    		return False

    	elif (r < -100) or (r > 100): # Go straight. * Make threshold configurable
            x = dist * cos(self.getOrientation())
            print("forward x", x)
            y = dist * sin(self.getOrientation())
            print("forward y", y)
            self.setPosition((self.getPosition()[0] + x), (self.getPosition()[1] + y))
            print ("going straight")
            # + forward speed error -> veers right
            self.setOrientation(self.getOrientation()) # random error and bias.

    	elif (r < 0):

            print "turning left"

            # convert to positive radians

            r = abs(r)

            circum = 2*pi*r

            angleToPoint =  (dist/circum) * 2*pi # In radians.
            print ("angle from rover to destination", angleToPoint)

            # Find the origin of the circle.
            directionToOrigin = self.getOrientation() + pi/2

            delta_theta = dist/r
            x = 0
            y = -1*r
            x_local = x * cos(delta_theta) - y * sin(delta_theta) + 0
            y_local = x * sin(delta_theta) + y * cos(delta_theta) + r

            delta_x_t = x_local * cos(self.getOrientation()) - y_local * sin(self.getOrientation())
            delta_y_t = x_local * sin(self.getOrientation()) + y_local * cos(self.getOrientation())

            x_t = self.getPosition()[0] + delta_x_t
            y_t = self.getPosition()[1] + delta_y_t
            self.setPosition(x_t, y_t)

            self.setOrientation(self.getOrientation() + delta_theta)

            if abs(self.getOrientation() / 6.78) >= 1:
                print 'reset theta'
                if self.getOrientation() > 0:
                    setOrientation(self.getOrientation() - 6.28)

    	elif (r > 0): # Turn right.

            print("turning right")


            print "turning left"

            # convert to positive radians

            r = abs(r)

            circum = 2*pi*r

            angleToPoint =  (dist/circum) * 2*pi # In radians.
            print ("angle from rover to destination", angleToPoint)

            # Find the origin of the circle.
            directionToOrigin = self.getOrientation() + pi/2

            delta_theta = dist/r
            x = 0
            y = -1*r
            x_local = x * cos(delta_theta) - y * sin(delta_theta) + 0
            y_local = x * sin(delta_theta) + y * cos(delta_theta) + r

            delta_x_t = x_local * cos(self.getOrientation()) - y_local * sin(self.getOrientation())
            delta_y_t = x_local * sin(self.getOrientation()) + y_local * cos(self.getOrientation())

            x_t = self.getPosition()[0] + delta_x_t
            y_t = self.getPosition()[1] + delta_y_t
            self.setPosition(x_t, y_t)

            self.setOrientation(self.getOrientation() - delta_theta)

            if abs(self.getOrientation() / 6.78) >= 1:
                print 'reset theta'
                if self.getOrientation() > 0:
                    setOrientation(self.getOrientation() - 6.28)

    	print("moved to", self.getPosition()[0], self.getPosition()[1])
     	return True
