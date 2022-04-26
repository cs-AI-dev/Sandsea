from objects import *

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

class PointCTX:
	def __init__(self, x, y, z, toggle=True):
		self.point = Point(x, y, z)
		self.colist = [x, y, z]
		self.toggle = toggle
		
	def __enter__(self):
		if toggle:
			return self.point
		elif not toggle:
			return self.colist
		else:
			raise IndexError("Toggle must be a Boolean.")
		
	def __exit__(self, exc_type, exc_value, exc_tb):
		try:
		    raise exc_type(exc_value)
		except TypeError:
		    pass
		except Exception as e:
		    raise e
		
class AngleCTX:
	def __init__(self, center, endp1, endp2, toggle=True):
		self.angle = Angle(center, endp1, endp2)
		self.angleList = [endp1, center, endp2]
		self.toggle = toggle
		
	def __enter__(self):
		if self.toggle:
			return self.angle
		elif not self.toggle:
			return self.angleList
		else:
			raise IndexError("Toggle must be a Boolean.")
		
	def __exit__(self, exc_type, exc_value, exc_tb):
		try:
		    raise exc_type(exc_value)
		except TypeError:
		    pass
		except Exception as e:
		    raise e
		
class LineCTX:
	def __init__(self, point1, arg2, toggle=True):
		if type(arg2) == type(Vector(0, 0, 0)):
			self.point2 = Point(point.x + arg2.x, point.y + arg2.y, point.z + arg2.z)
			self.vector = arg2
		elif type(arg2) == type(Point(0, 0, 0)):
			self.point2 = arg2
			self.vector = Vector(deltax(point, arg2), deltay(point, arg2), deltaz(point, arg2))
		else:
			raise TypeError("Line arguments must be Point and Vector or Point and Point, not " + str(type(arg2)).split("\'")[1] + ".")
		self.line = Line(point1, point2)
		self.plist = [self.point1, self.point2, self.vector]
		self.toggle = toggle
		
	def __enter__(self):
		if self.toggle:
			return self.line
		elif not self.toggle:
			return self.plist
		else:
			raise IndexError("Toggle must be a Boolean.")
		
	def __exit__(self, exc_type, exc_value, exc_tb):
		try:
		    raise exc_type(exc_value)
		except TypeError:
		    pass
		except Exception as e:
		    raise e
		
class TriangleCTX:
	def __init__(self, p1, p2, p3, toggle=True):
		self.triangle = Triangle(p1, p2, p3)
		self.plist = [p1, p2, p3]
		self.toggle = toggle
		
	def __enter__(self):
		if self.toggle:
			return self.triangle
		elif not self.toggle:
			return self.plist
		else:
			raise IndexError("Toggle must be a Boolean.")
		
	def __exit__(self, exc_type, exc_value, exc_tb):
		try:
		    raise exc_type(exc_value)
		except TypeError:
		    pass
		except Exception as e:
		    raise e
		
class SphereCTX:
	def __init__(self, center, radius):
		self.sphere = Sphere(center, radius)
	
	def __enter__(self):
		return self.sphere
		
	def __exit__(self, exc_type, exc_value, exc_tb):
		try:
		    raise exc_type(exc_value)
		except TypeError:
		    pass
		except Exception as e:
		    raise e
		
class CuboidCTX:
	def __init__(corner1, arg2, toggle=True):
		self.cuboid = Cuboid(corner1, arg2)
		self.plist = self.cuboid.points
		self.toggle = toggle
		
	def __enter__(self):
		if self.toggle:
			return self.cuboid
		elif not self.toggle:
			return self.plist
		else:
			raise IndexError("Toggle must be a Boolean.")
		
	def __exit__(self, exc_type, exc_value, exc_tb):
		try:
		    raise exc_type(exc_value)
		except TypeError:
		    pass
		except Exception as e:
		    raise e
		
class BlockCTX:
	def __init__(self, corner1, arg2, toggle=True):
		self.block = Block(corner1, arg2)
		self.plist = block.points
		self.toggle = toggle
		
	def __enter__(self):
		if self.toggle:
			return self.block
		elif not self.toggle:
			return self.plist
		else:
			raise IndexError("Toggle must be a Boolean.")
		
	def __exit__(self, exc_type, exc_value, exc_tb):
		try:
		    raise exc_type(exc_value)
		except TypeError:
		    pass
		except Exception as e:
		    raise e
		
class TriangularPyramidCTX:
	def __init__(self, p1, p2, p3, v, toggle=True):
		self.pyramid = TriangularPyramid(p1, p2, p3, v)
		self.plist = [p1, p2, p3, v]
		self.toggle = toggle
		
	def __enter__(self):
		if self.toggle:
			return self.pyramid
		elif not self.toggle:
			return self.plist
		else:
			raise IndexError("Toggle must be a Boolean.")
		
	def __exit__(self, exc_type, exc_value, exc_tb):
		try:
		    raise exc_type(exc_value)
		except TypeError:
		    pass
		except Exception as e:
		    raise e
