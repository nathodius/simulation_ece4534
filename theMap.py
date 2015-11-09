class theMap:
	"""Represents the physical map."""

	def __init__(self, mapFileName):
		"""Map initialization"""
		mapFile = open(mapFileName, 'r')
		self.array2d = [[coordinates for coordinates in row.split()] for row in mapFile]	

	def getArray2d(self):
		"""Return the array representation of the map."""
		return self.array2d
