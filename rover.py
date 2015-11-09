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
        pass # do

    def getMessagePeriod(self):
        return self.messagePeriod


    # def rotateRight(self, durration):
    # 	rotation = self.rotationSpeed * durration
    # 	self.orientation[0] = self.orientation[0] - rotation
    # 	if self.orientation[0] <= 0:
    # 		self.orientation[0] = 360 + self.orientation[0]

    # 	if self.orientation[0] == 360:
    # 		self.orientation[0] = 0

    # def rotateLeft(self, durration):
    # 	rotation = self.rotationSpeed * durration
    # 	self.orientation[0] = self.orientation[0] + rotation
    # 	if self.orientation[0] >= 360:
    # 		self.orientation[0] = self.orientation[0] - 360

    # 	if self.orientation[0] == 360:
    # 		self.orientation[0] = 0

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

    	elif (r < 0):

            print "turning left"

            # convert to positive radians

            r = abs(r)

            circum = 2*pi*r

            angleToPoint =  (dist/circum) * 2*pi # In radians.
            print ("angle from rover to destination", angleToPoint)

            # Find the origin of the circle.
            directionToOrigin = self.getOrientation() + pi/2


            yIncrease = r * sin(directionToOrigin)
            ("y from rover to origin", yIncrease)
            xIncrease = r * cos(directionToOrigin)
            ("x from rover to origin", xIncrease)
            origin = (self.getPosition()[0] + xIncrease, self.getPosition()[1] + yIncrease)
            print ("origin of the circle", origin)

            xToPoint = cos(pi/2 - angleToPoint)*r
            print ("x from origin to destination", xToPoint)
            yToPoint = sin(pi/2 - angleToPoint)*r
            print ("y from origin to destination", yToPoint)

            if self.getOrientation() > 1.5708:
                point = (origin[0] - xToPoint, origin[1] + yToPoint)
            else:
                point = (origin[0] + xToPoint, origin[1] - yToPoint)
            #   print("point we're going to", point)

            self.setPosition(point[0], point[1])

            angle = atan2(xToPoint, yToPoint)
            if angle < 0:
                angle = 2*pi + angle

			# Update the rover's orientation
            self.setOrientation(self.getOrientation() + angle)

            print("Rover orientation", self.getOrientation())

    	elif (r > 0): # Turn right.

            print("turning right")

            r = abs(r)

            #r = abs(r)
            circum = 2*pi*r
            print ("circumference", circum)

            angleToPoint =  (dist/circum) * 2*pi # In radians.
            print ("angle to point", angleToPoint)

            # Find the origin of the circle. 
            directionToOrigin = self.getOrientation() - pi/2
            print("direction to origin", directionToOrigin)

            #print ("direction to origin", directionToOrigin)
            xIncrease = r * cos(directionToOrigin)
            yIncrease = r * sin(directionToOrigin)
            origin = (self.getPosition()[0] + xIncrease, self.getPosition()[1] + yIncrease)
            print ("origin of the circle", origin)

            xToPoint = sin(angleToPoint)*r
            print ("x from origin to point", xToPoint)
            yToPoint = cos(angleToPoint)*r
            print ("y from origin to point", yToPoint)

            if self.getOrientation() > -1.5708:
                point = (origin[0] + xToPoint, origin[1] + yToPoint)
            else:
                point = (origin[0] - xToPoint, origin[1] - yToPoint)
            #print("point we're going to", point)

            self.setPosition(point[0], point[1])

            angle = atan2(xToPoint, yToPoint)
            if angle < 0:
                angle = 2*pi + angle

            angle = 0 - angle # right turn

			# Update the rover's orientation
            self.setOrientation(self.getOrientation() + angle)


    	if (self.position[0][0] > 150) or (self.position[0][0] < 0):
    	    print ("Rover moved out of X boundaries.")
			return False
     	if (self.position[0][1] > 75 + self.buff) or (self.position[0][0] < self.buff):
     		print ("Rover moved out of Y boundaries.")
			return False

    	print("moved to", self.getPosition()[0], self.getPosition()[1])
     	return True
