import math
import numpy as np

setting = {"lowerCollisionThreshold": 1e-16}

def pointToVector(point):
	return Vector(point.x, point.y, point.z)

def vectorToPoint(vector):
	return Point(vector.x, vector.y, vector.z)

deltax = lambda a, b : b.x - a.x
deltay = lambda a, b : b.y - a.y
deltaz = lambda a, b : b.z - a.z

class Vector:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
		self.net = x + y + z
		self.length = sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def addVector(self, vector):
		self.x = self.x + vector.x
		self.y = self.y + vector.y
		self.z = self.z + vector.z
		self.net = self.net + vector.net
		self.length = sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def addx(self, x):
		self.x += x
		self.net = x + y + z
		self.length = sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def addy(self, y):
		self.y += y
		self.net = x + y + z
		self.length = sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def addz(self, z):
		self.z += z
		self.net = x + y + z
		self.length = sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def subtractVector(self, vector):
		self.x = self.x - vector.x
		self.y = self.y - vector.y
		self.z = self.z - vector.z
		self.net = self.net - vector.net
		self.length = sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def subx(self, x):
		self.x -= x
		self.net = self.x + self.y + self.z
		self.length = sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def suby(self, y):
		self.y -= y
		self.net = self.x + self.y + self.z
		self.length = sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def subz(self, z):
		self.z -= z
		self.net = self.x + self.y + self.z
		self.length = sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def multiplyVector(self, vector):
		self.x = self.x * vector.x
		self.y = self.y * vector.y
		self.z = self.z * vector.z
		self.net = self.net - vector.net
		self.length = sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def mulx(self, x):
		self.x *= x
		self.net = self.x + self.y + self.z
		self.length = sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def muly(self, y):
		self.y *= y
		self.net = self.x + self.y + self.z
		self.length = sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def mulz(self, z):
		self.z *= z
		self.net = self.x + self.y + self.z
		self.length = sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def divideVector(self, vector):
		self.x = self.x / vector.x
		self.y = self.y / vector.y
		self.z = self.z / vector.z
		self.net = self.net - vector.net
		self.length = sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def divx(self, x):
		self.x /= x
		self.net = self.x + self.y + self.z
		self.length = sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def divy(self, y):
		self.y /= y
		self.net = self.x + self.y + self.z
		self.length = sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def divz(self, z):
		self.z /= z
		self.net = self.x + self.y + self.z
		self.length = sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

class Point:
	def __init__(a1, y, z):
		if type(y) == type(1) and type(z) == type(1):
			if type(a1) == type(Vector(0, 0, 0)):
				self.x = a1.x
				self.y = a1.y
				self.z = a1.z
				self.coordinates = [self.x, self.y, self.z]
				self.vector = a1
			elif type(a1) == type(1):
				self.x = a1
				self.y = y
				self.z = z
				self.coordinates = [self.x, self.y, self.z]
				self.vector = Vector(a1, y, z)
			else:
				raise TypeError("Point arguments must be three integers or a Vector.")
		else:
			raise TypeError("Point arguments must be three integers or a Vector.")
			
	def __iter__(self):
		return [self.x, self.y, self.z]

	def translate(self, dx, dy, dz):
		self.x += dx
		self.y += dy
		self.z += dz
		self.coordinates = [self.x, self.y, self.z]
		self.vector = Vector(self.x, self.y, self.z)

		return self

	def rotate(self, dx, dy, dz, centerPoint=None:
		if centerPoint != None:
			centeredPoint = [centerPoint.x, centerPoint.y, centerPoint.z]
		else:
			centeredPoint = [0, 0, 0]

		cosa = math.cos(dx)
		sina = math.sin(dx)

		cosb = math.cos(dy)
		sinb = math.sin(dy)

		cosc = math.cos(dz)
		sinc = math.sin(dz)

		Axx = cosa * cosb
		Axy = (cosa * sinb * sinc) - (sina * cosc)
		Axz = (cosa * sinb * cosc) + (sina * sinc)

		Ayx = sina * cosb
		Ayy = (sina * sinb * sinc) + (cosa * cosc)
		Ayz = (sina * sinb * cosc) - (cosa * sinc)

		Azx = -sinb
		Azy = (cosb * sinc)
		Azz = (cosb * cosc)

		px = centeredPoint[0];
		py = centeredPoint[1];
		pz = centeredPoint[2];

		self.x = ((Axx * px) + (Axy * py) + (Axz * pz)) + centerPoint[0]
		self.y = ((Ayx * px) + (Ayy * py) + (Ayz * pz)) + centerPoint[1]
		self.z = ((Azx * px) + (Azy * py) + (Azz * pz)) + centerPoint[2]

		return self

	def distance(self, object):
		if type(object) == type(self):
			return math.sqrt(((object.x - self.x) ** 2) + ((object.y - self.y) ** 2) + ((object.z - self.z) ** 2)))
		else:
			vec3 d = (C - B) / C.distance(B)
			vec3 v = A - B
			double t = v.dot(d)
			vec3 P = B + t * d
			return P.distance(A)

class Angle:
	def __init__(self, center, endp1, endp2):
		self.center = center
		self.endpoint1 = endp1
		self.endpoint2 = endp2

		ep1 = endp1.translate(-center.x, -center.y, -center.z)
		ep2 = endp2.translate(-center.x, -center.y, -center.z)

		endp1.translate(center.x, center.y, center.z)
		endp2.translate(center.x, center.y, center.z)
		
		self.angle = math.acos((ep1.x * ep2.x + ep1.y * ep2.y + ep1.z * ep2.z) / (sqrt((ep1.x ** 2) + (ep1.y ** 2) + (ep1.z ** 2)) * sqrt((ep2.x ** 2) + (ep2.y ** 2) + (ep2.z ** 2))))

	def translate(self, dx, dy, dz):
		self.__init__(self.center.translate(dx, dy, dz), self.endpoint1.translate(dx, dy, dz), self.endpoint2.translate(dx, dy, dz))
		return self

	def rotate(self, dx, dy, dz, centerPoint=None):
		self.__init__(self.center.rotate(dx, dy, dz, centerPoint), self.endpoint1.rotate(dx, dy, dz, centerPoint), self.endpoint2.rotate(dx, dy, dz, centerPoint))
		return self

class Line:
	def __init__(self, point1, arg2):
		self.point1 = point
		if type(arg2) == type(Vector(0, 0, 0)):
			self.point2 = Point(point.x + arg2.x, point.y + arg2.y, point.z + arg2.z)
			self.vector = arg2
		elif type(arg2) == type(Point(0, 0, 0)):
			self.point2 = arg2
			self.vector = Vector(deltax(point, arg2), deltay(point, arg2), deltaz(point, arg2))
		else:
			raise TypeError("Line arguments must be Point and Vector or Point and Point, not " + str(type(arg2)).split("\'")[1] + ".")

		self.midpoint = Point(((self.point1.x + self.point2.x) / 2), ((self.point1.y + self.point2.y) / 2), ((self.point1.z + self.point2.z) / 2))

		self.slope_yx = (self.point2.y - self.point1.y) / (self.point2.x - self.point1.x)
		self.slope_xy = (self.point2.x - self.point1.x) / (self.point2.y - self.point1.y)
		self.slope_zy = (self.point2.z - self.point1.z) / (self.point2.y - self.point1.y)
		self.slope_yz = (self.point2.y - self.point1.y) / (self.point2.z - self.point1.z)
		self.slope_zx = (self.point2.z - self.point1.z) / (self.point2.x - self.point1.x)
		self.slope_xz = (self.point2.x - self.point1.x) / (self.point2.z - self.point1.z)
		self.slope = self.slope_yx + self.slope_zy + self.slope_zx

		self.directionalVector = Vector(point2.x - point1.x, point2.y - point1.y, point2.z - point1.z)

	def translate(self, dx, dy, dz):
		self.__init__(origin.translate(dx, dy, dz), self.pointOnRay.translate(dx, dy, dz))
		return self

	def rotate(self, dx, dy, dz, centerPoint=None):
		self.__init__(self.origin.rotate(dx, dy, dz, centerPoint), self.pointOnRay.rotate(dx, dy, dz, centerPoint))
		return self

	def checkCollision(self, object):
		if type(object) == type(Point(0, 0, 0)):
			return ((object.x - self.point1.x) / self.directionalVector.x) == ((object.y - self.point1.y) / self.directionalVector.y) == ((object.z - self.point1.z) / self.directionalVector.z)

        	if type(object) == type(self):
			resultSegmentPoint1 = Point(0, 0, 0)
			resultSegmentPoint2 = Point(0, 0, 0)

			p1 = pointToVector(self.point1);
			p2 = pointToVector(self.point2);
			p3 = pointToVector(object.point1);
			p4 = pointToVector(object.point2);
			p13 = p1
			p13.subtractVector(p3)
			p43 = p4
			p43.subtractVector(p3)

			if p43.length ** 2 < setting["lowerCollisionThreshold"]:
				return False

			p21 = p2
			p21.subtractVector(p1)
			if p21.length ** 2 < setting["lowerCollisionThreshold"]:
				return False

			d1343 = p13.x * p43.x + p13.y * p43.y + p13.z * p43.z
			d4321 = p43.x * p21.x + p43.y * p21.y + p43.z * p21.z
			d1321 = p13.x * p21.x + p13.y * p21.y + p13.z * p21.z
			d4343 = p43.x * p43.x + p43.y * p43.y + p43.z * p43.z
			d2121 = p21.x * p21.x + p21.y * p21.y + p21.z * p21.z

			denom = d2121 * d4343 - d4321 * d4321;
			if abs(denom) < setting["lowerCollisionThreshold"]:
				return False

			numer = d1343 * d4321 - d1321 * d4343

			mua = numer / denom
			mub = (d1343 + d4321 * mua) / d4343

			resultSegmentPoint1.addx(p1.x + mua * p21.x)
			resultSegmentPoint1.addy(p1.y + mua * p21.y)
			resultSegmentPoint1.addz(p1.z + mua * p21.z)
			resultSegmentPoint2.addx(p3.x + mub * p43.x)
			resultSegmentPoint2.addy(p3.y + mub * p43.y)
			resultSegmentPoint2.addz(p3.z + mub * p43.z)

			return resultSegmentPoint1.distance(resultSegmentPoint2) < setting["lowerCollisionThreshold"]

class Ray:
	def __init__(self, origin, arg):
		self.origin = origin

		if type(arg) == type(Vector(0, 0, 0)):
			self.pointOnRay = Point(self.origin.x + arg.x, self.origin.y + arg.y, self.origin.z + arg.z)
			self.vector = arg
		elif type(arg) == type(Point(0, 0, 0)):
			self.pointOnRay = arg
			self.vector = Vector(self.origin.x - self.pointOnRay.x, self.origin.y - self.pointOnRay.y, self.origin.z - self.pointOnRay.z)
		else:
			raise TypeError("Ray arguments must be Point and either a Point or a Vector.")

		self.slope_yx = (self.point2.y - self.point1.y) / (self.point2.x - self.point1.x)
		self.slope_xy = (self.point2.x - self.point1.x) / (self.point2.y - self.point1.y)
		self.slope_zy = (self.point2.z - self.point1.z) / (self.point2.y - self.point1.y)
		self.slope_yz = (self.point2.y - self.point1.y) / (self.point2.z - self.point1.z)
		self.slope_zx = (self.point2.z - self.point1.z) / (self.point2.x - self.point1.x)
		self.slope_xz = (self.point2.x - self.point1.x) / (self.point2.z - self.point1.z)
		self.slope = self.slope_yx + self.slope_zy + self.slope_zx

	def translate(self, dx, dy, dz):
		self.__init__(origin.translate(dx, dy, dz), self.pointOnRay.translate(dx, dy, dz))
		return self

	def rotate(self, dx, dy, dz, centerPoint=None):
		self.__init__(self.origin.rotate(dx, dy, dz, centerPoint), self.pointOnRay.rotate(dx, dy, dz, centerPoint))
		return self

	def checkCollision(self, object):
		pass

class Triangle:
	def __init__(self, point1, point2, point3):
		self.point1 = point1
		self.point2 = point2
		self.point3 = point3

		self.length_12 = point1.distance(point2)
		self.length_13 = point1.distance(point3)
		self.length_21 = point2.distance(point1)
		self.length_23 = point2.distance(point3)
		self.length_31 = point3.distance(point1)
		self.length_32 = point3.distance(point2)

		self.perimiter = self.length_12 + self.length_13 + self.length_23
		self.semiperimiter = perimiter / 2
		self.area = self.semiperimiter * (self.semiperimiter - self.length_12) * (self.semiperimiter - self.length_23) * (self.semiperimiter - self.length_13)
		self.centroid = Point((self.point1.x + self.point2.x + self.point3.x) / 3, (self.point1.y + self.point2.y + self.point3.y) / 3, (self.point1.z + self.point2.z + self.point3.z) / 3)

	def __iter__(self):
		return [self.point1, self.point2, self.point3]
	
	def translate(self, dx, dy, dz):
		self.__init__(self.point1.translate(dx, dy, dz), self.point2.translate(dx, dy, dz), self.point3.translate(dx, dy, dz))
		return self

	def rotate(self, dx, dy, dz, centerPoint=None):
		self.__init__(self.point1.rotate(dx, dy, dz, centerPoint), self.point2.rotate(dx, dy, dz, centerPoint), self.point3.rotate(dx, dy, dz, centerPoint))
		return self

	def checkCollision(self, object):
		if type(object) == type(point):
			angle_12 = Angle(object, self.point1, self.point2)
			angle_13 = Angle(object, self.point1, self.point3)
			angle_23 = Angle(object, self.point2, self.point3)

			alpha = Angle(object, self.point1, self.point2).angle / Triangle(object, self.point1, self.point2).area
			beta = Angle(object, self.point1, self.point3).angle / Triangle(object, self.point1, self.point3).area
			gamma = Angle(object, self.point2, self.point2).angle / Triangle(object, self.point2, self.point2).area

			return (alpha + beta + gamma == 1) and (0 < alpha < 1) and (0 < beta < 1) and (0 < gamma < 1)
			   
		elif type(object) == type(Line(Point(0, 0, 0), Point(0, 0, 1))):
			return False

		elif type(object) == type(self):
			if Line(self.point1, self.point2).checkCollision(Line(object.point1, object.point2)): 
				return True
			if Line(self.point1, self.point2).checkCollision(Line(object.point1, object.point3)): 
		   		return True
			if Line(self.point1, self.point2).checkCollision(Line(object.point2, object.point3)): 
		   		return True
			if Line(self.point1, self.point3).checkCollision(Line(object.point1, object.point2)): 
		   		return True
			if Line(self.point1, self.point3).checkCollision(Line(object.point1, object.point3)): 
		   		return True
			if Line(self.point1, self.point3).checkCollision(Line(object.point2, object.point3)): 
		   		return True
			if Line(self.point2, self.point3).checkCollision(Line(object.point1, object.point2)): 
		   		return True
			if Line(self.point2, self.point3).checkCollision(Line(object.point1, object.point3)): 
		   		return True
			if Line(self.point2, self.point3).checkCollision(Line(object.point2, object.point3)): 
		   		return True

			inTriangle = True
			inTriangle = inTriangle and self.checkCollision(object.point1)
			inTriangle = inTriangle and self.checkCollision(object.point2)
			inTriangle = inTriangle and self.checkCollision(object.point3)

			if inTriangle:
				return True

			inTriangle = True
			inTriangle = inTriangle and self.checkCollision(object.point1)
			inTriangle = inTriangle and self.checkCollision(object.point2)
			inTriangle = inTriangle and self.checkCollision(object.point3)

			if inTri:
				return True

			return False

class Sphere:
	def __init__(self, center, radius):
		self.center = center

		if type(radius) == type(1):
			self.radius = radius
			self.tangentPoint = self.center.translate(self.radius, 0, 0)
		elif type(radius) == type(Point(0, 0, 0)):
			self.radius = self.center.distance(radius)
			self.tangentPoint = radius

	def checkCollision(self, object):
		if type(object) == type(Point(0, 0, 0)):
			return self.center.distance(object) <= self.radius

		elif type(object) == type(Triangle(Point(0, 0, 0), Point(0, 0, 0), Point(0, 0, 0))):
			collided = False
			collided = collided or self.center.distance(object.point1) <= self.radius
		   	collided = collided or self.center.distance(object.point2) <= self.radius
		   	collided = collided or self.center.distance(object.point3) <= self.radius
		   	t12 = Triangle(self.center, object.point1, object.point2)
			t13 = Triangle(self.center, object.point1, object.point3)
		   	t23 = Triangle(self.center, object.point2, object.point3)
		   	collided = collided or (t12.area * 2) / object.point1.distance(object.point2) <= self.radius
		   	collided = collided or (t13.area * 2) / object.point1.distance(object.point3) <= self.radius
		   	collided = collided or (t22.area * 2) / object.point2.distance(object.point3) <= self.radius
		  	
		   	return collided
		   
class Cuboid:
	def __init__(self, corner1, arg2):
		if type(arg2) == type(Point(0, 0, 0)):
			# Close (1) / Far (2) - X
			# Bottom (1) / Top (2) - Y
			# Left (1) / Right (2) - Z
			self.close_bottom_left = Point(corner1.x, corner1.y, corner1.z)
			self.far_bottom_left = Point(arg2.x, corner1.y, corner1.z)
			self.close_top_left = Point(corner1.x, arg2.y, corner1.z)
			self.far_top_left = Point(arg2.x, arg2.y, corner1.z)
			self.close_bottom_right = Point(corner1.x, corner1.y, arg2.z)
			self.far_bottom_right = Point(arg2.x, corner1.y, arg2.z)
			self.close_top_right = Point(corner1.x, arg2.y, arg2.z)
			self.far_top_right = Point(arg2.x, arg2.y, arg2.z)
		elif type(arg2) == type(Vector(0, 0, 0)):
			self.close_bottom_left = Point(corner1.x, corner1.y, corner1.z)
			self.far_bottom_left = Point(corner1.x + arg2.x, corner1.y, corner1.z)
			self.close_top_left = Point(corner1.x, corner1.y + arg2.y, corner1.z)
			self.far_top_left = Point(corner1.x + arg2.x, corner1.y + arg2.y, corner1.z)
			self.close_bottom_right = Point(corner1.x, corner1.y, corner1.z + arg2.z)
			self.far_bottom_right = Point(corner1.x + arg2.x, corner1.y, corner1.z + arg2.z)
			self.close_top_right = Point(corner1.x, corner1.y + arg2.y, corner1.z + arg2.z)
			self.far_top_right = Point(corner1.x + arg2.x, corner1.y + arg2.y, corner1.z + arg2.z)
			
		self.volume = self.close_bottom_left.distance(self.close_bottom_right)
		self.volume *= self.close_bottom_left.distance(self.close_top_left)
		self.volume *= self.close_bottom_left.distance(self.far_bottom_left)
		
		self.rotation = Vector(0, 0, 0)
		
	def __iter__(self):
		return [
			self.close_bottom_left, 
			self.far_bottom_left,
		        self.close_top_left,
		       	self.far_top_left,
		        self.close_bottom_right,
		       	self.far_bottom_right,
		        self.close_top_right,
		       	self.far_top_right
		]
			
	def translate(self, dx, dy, dz):
		self.__init__(self.close_bottom_left.translate(dx, dy, dz), self.far_top_right.translate(dx, dy, dz))
		return self
	
	def rotate(self, dx, dy, dz, centerPoint=None):
		self.__init__(self.close_bottom_left.rotate(dx, dy, dz, centerPoint), self.far_top_right.rotate(dx, dy, dz, centerPoint))
		self.rotation.addVector(Vector(dx, dy, dz))
		return self
	
	def checkCollision(self, object):
		if type(object) == type(Point(0, 0, 0)):
			tp = object.rotate(-self.rotation.x, -self.rotation.y, -self.rotation.z, Point(0, 0, 0))
			collided = True
			collided = collided and (min([p.x for p in iter(self)] <= tp.x <= max([p.x for p in iter(self)])))
			collided = collided and (min([p.y for p in iter(self)] <= tp.y <= max([p.y for p in iter(self)])))
			collided = collided and (min([p.z for p in iter(self)] <= tp.z <= max([p.z for p in iter(self)])))
			return collided
		
		elif type(object) == type(Triangle(Point(0, 0, 0), Point(0, 0, 0), Point(0, 0, 0))):
			collided = False
			collided = collided or self.checkCollision(object.point1)
			collided = collided or self.checkCollision(object.point2)
			collided = collided or self.checkCollision(object.point3)
			return collided
