class SpaceObject:
	def __init__(self, space, dx, dy, dz):
		self.space = space
		self.dimensionX = dx
		self.dimensionY = dy
		self.dimensionZ = dz
		
	def set(self, x, y, z, val):
		self.space[x][y][z] = val
		return self.space
	
	def translate(self, ox, oy, oz, dx, dy, dz):
		val = self.space[ox][oy][oz]
		self.space[ox][oy][oz] = None
		self.space[ox + dx][oy + dy][oz + dz] = val
		return self.space
	
	def rotate(self, ox, oy, oz, dx, dy, dz, centerPoint):
		return self.space

class Space:
	def __init__(self, dimensionx, dimensiony=None, dimensionz=None):
		if dimensiony == dimensionz == None:
			self.dimensionX = dimensionx
			self.dimensionY = dimensionx
			self.dimensionZ = dimensionx
		elif type(dimensionx) == type(dimensiony) == type(dimensionz) == type(1):
			self.dimensionX = dimensionx
			self.dimensionY = dimensiony
			self.dimensionZ = dimensionz
		else:
			raise TypeError("Dimensions of spacial context must be integers.")
		self.space = [[[None for x in range(self.dimensionX)] for x in range(self.dimensionY)] for x in range(self.dimensionZ)]
		
	def __enter__(self):
		return SpaceObject(self.space, self.dimensionX, self.dimensionY, self.dimensionZ)
	
	def __exit__(self, exc_type, exc_value, exc_tb):
		try:
		    raise exc_type(exc_value)
		except TypeError:
		    pass
		except Exception as e:
		    raise e
