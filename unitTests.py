import unittest
from time import sleep
import rover
import sensor
import control
import driver
from theMap import theMap
import time
from math import pi
import matplotlib.pyplot as plt

class TestInstantiationMethods(unittest.TestCase):
	"""Test class for system instantiation methods."""

	def test_instantiateRover(self):
		"""Test method for rover instantiation"""

		print("Testing instantiation of the rover.")

		r = driver.instantiateRover(["system=rover", "rotationSpeed=0", "forwardSpeed=1", "rotationSpeedError=2", "forwardSpeedError=3", "x=4", "y=5", "orientation=45", "port=/dev/tty.usbserial-A702ZKVY"])
		self.assertEqual(r.getRotationSpeed(), 0)
		self.assertEqual(r.getForwardSpeed(), 1)
		self.assertEqual(r.getRotationSpeedError(), 2)
		self.assertEqual(r.getForwardSpeedError(), 3)
		self.assertEqual(r.getPosition()[0], 4)
		self.assertEqual(r.getPosition()[1], 5)

	def test_instantiateSensor(self):
		"""Test method for sensor instantiation"""

		print("Testing instantiation of the sensor.")

		s = driver.instantiateSensor(["sampleRate=0", "sampleRateError=1", "rotationRate=2", "rotationRateError=3", "rangeOfMotion=4", "buff=5", "port=/dev/tty.usbserial-A702ZIQS"])
		self.assertEqual(s.getSampleRate(), 0)
		self.assertEqual(s.getSampleRateError(), 1)
		self.assertEqual(s.getRotationRate(), 2)
		self.assertEqual(s.getRotationRateError(), 3)
		self.assertEqual(s.getRangeOfMotion(), 4)
		self.assertEqual(s.getBuff(), 5)

	def test_instantiateSystems(self):
		"""Test method for systems instantiation"""

		print("Testing instantiation of the systems.")

		r1 = driver.instantiateRover(["system=rover", "rotationSpeed=0", "forwardSpeed=1", "rotationSpeedError=2", "forwardSpeedError=3", "x=4", "y=5", "orientation=45", "port=/dev/tty.usbserial-A702ZKVY"])
		s1 = driver.instantiateSensor(["sampleRate=0", "sampleRateError=1", "rotationRate=2", "rotationRateError=3", "rangeOfMotion=4", "buff=5", "port=/dev/tty.usbserial-A702ZIQS"])
		r2, s2, c2 = driver.instantiateSystems("config1.txt")

		self.assertEqual(r1.getRotationSpeed(), r2.getRotationSpeed())
		self.assertEqual(r1.getForwardSpeed(), r2.getForwardSpeed())
		self.assertEqual(r1.getRotationSpeedError(), r2.getRotationSpeedError())
		self.assertEqual(r1.getForwardSpeedError(), r2.getForwardSpeedError())
		self.assertEqual(r1.getPosition()[0], r2.getPosition()[0])
		self.assertEqual(r1.getPosition()[1], r2.getPosition()[1])
		
		self.assertEqual(s1.getSampleRate(), s2.getSampleRate())
		self.assertEqual(s1.getSampleRateError(), s2.getSampleRateError())
		self.assertEqual(s1.getRotationRate(), s2.getRotationRate())
		self.assertEqual(s1.getRotationRateError(), s2.getRotationRateError())
		self.assertEqual(s1.getRangeOfMotion(), s2.getRangeOfMotion())
		self.assertEqual(s1.getBuff(), s2.getBuff())

class TestMapMethods(unittest.TestCase):
	"""Test class for map building methods"""

	def test_buildMap(self):

		m = theMap("map1.txt")
		array2d = m.getArray2d()
		for row in array2d:
			columnIndex = 0
			for coordinates in row:
				if columnIndex == 4:
					self.assertEqual(int(coordinates), 1)
				else:
					self.assertEqual(int(coordinates), 0)
				columnIndex = columnIndex + 1

class TestSensorMethods(unittest.TestCase):
	"""Test class for sensor simulation"""

	def test_orientSensor(self):
		"""Test method for sensor orientation"""

		print("Testing orientation of the sensor.")

		s = driver.instantiateSensor(["sampleRate=500", "sampleRateError=0", "rotationRate=500", "rotationRateError=0", "rangeOfMotion=50", "buff=2", "port=/dev/tty.usbserial-A702ZIQS"])
		samplingPeriod = 1/s.getSampleRate()
		orientation = 0
		for i in range(s.getRangeOfMotion()): # Scan clockwise
			self.assertEqual(s.getOrientation(), i % s.getRangeOfMotion())
			s.orientSensor()
			sleep(samplingPeriod)
		for i in range(s.getRangeOfMotion()): # Scan counter clockwise
			self.assertEqual(s.getOrientation(), s.getRangeOfMotion() - (i % s.getRangeOfMotion()))
			s.orientSensor()
			sleep(samplingPeriod)

	def test_sample(self):
		"""Test method for sensor sampling"""

		print("Testing sensor sampling.")

		r = driver.instantiateRover(["system=rover", "rotationSpeed=0", "forwardSpeed=1", "rotationSpeedError=2", "forwardSpeedError=3", "x=25", "y=25", "orientation=45", "port=/dev/tty.usbserial-A702ZKVY"])
		s = driver.instantiateSensor(["sampleRate=500", "sampleRateError=0", "rotationRate=500", "rotationRateError=0", "rangeOfMotion=90", "buff=3", "port=/dev/tty.usbserial-A702ZIQS"])

		foundRover = False

		while(foundRover != True):
			foundRover = s.sample(r.getPosition())

		# Check that the sensor is aimed within a 2 cm margin of the center of the rover. 
		self.assertLessEqual(abs(s.getOrientation() - 45), 1) # 45 degrees is the correct orientation.

		r.setPosition(25, 50)
		foundRover = False
		while(foundRover != True):
			foundRover = s.sample(r.getPosition())

		# Check that the sensor is aimed within a 2 cm margin of the center of the rover. 
		self.assertLessEqual(abs(s.getOrientation() - 63.5), 1) # 63.5 degrees is the correct orientation. 

class TestRoverMethods(unittest.TestCase):
	"""Test class for rover simulation."""

	def test_move(self):
		print("Testing rover movement.")
		
		r = driver.instantiateRover(["system=rover", "rotationSpeed=1", "forwardSpeed=1", "rotationSpeedError=2", "forwardSpeedError=3", "x=24", "y=25", "orientation=0", "port=/dev/tty.usbserial-A702ZKVY"])

		self.assertEqual(r.move(0.5, 1), False) # Radius is too small.

		stop = False

		r.move(1000, 1) # Move straight.

		# Rover is now at (25,25).

		self.assertLessEqual(abs(r.getPosition()[0] - 25), 0.1)

		# r.move(10, 5*pi) #circum: 20*pi cm -> one revolution in 20*pi seconds

		# # Check position of the rover.
		# self.assertLessEqual(abs(r.getPosition()[0] - 35), 1)
		# self.assertLessEqual(abs(r.getPosition()[1] - 15), 1)

		# # Check orientation of the rover.
		# self.assertLessEqual(abs(r.getOrientation() - 90), 1)

		# r.move(-10, 5*pi)

		# # Check position of the rover.
		# self.assertLessEqual(abs(r.getPosition()[0] - 45), 1)
		# self.assertLessEqual(abs(r.getPosition()[1] - 45), 1)

		# # Check orientation of the rover.
		# self.assertLessEqual(abs(r.getOrientation() - 0), 1)

		# plt.plot(r.getYHist(), r.getXHist())
		# plt.ylabel('Rover Position')
		# plt.show()

		# print("Rover movement times", r.getMovementTimes())
		# print("Init time", r.getInitTime())

		r.setPosition(4, 5)
		r.setOrientation(0)
		# Execute same commands from different starting location.

		r.move(1000, 1) # Move straight.

		# Rover is now at (5,5).

		self.assertLessEqual(abs(r.getPosition()[0] - 5), 0.1)

		# r.move(10, 7*pi) #circum: 20*pi cm -> one revolution in 20*pi seconds

		# # Check position of the rover.
		# self.assertLessEqual(abs(r.getPosition()[0] - 15), 1)
		# self.assertLessEqual(abs(r.getPosition()[1] - 15), 1)

		# # Check orientation of the rover.
		# self.assertLessEqual(abs(r.getOrientation() - 90), 1)

		r.move(-10, 21*pi)

		# Check position of the rover.
		self.assertLessEqual(abs(r.getPosition()[0] - 25), 1)
		self.assertLessEqual(abs(r.getPosition()[1] - 25), 1)

		# Check orientation of the rover.
		self.assertLessEqual(abs(r.getOrientation() - 0), 1)

		#print ("Position history", r.getPositionHistory())
		#print ("Orientation history", r.getOrientationHistory())



if __name__ == '__main__':
    unittest.main()