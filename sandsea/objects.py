import math
import numpy as np
import scipy
from scipy import spatial
import pandas as pd
import numpy as np
import descartes
from descartes import PolygonPatch
import matplotlib.pyplot as plt
import alphashape
import inspect
from inspect import signature

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
		self.length = math.sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def __iter__(self):
		return [self.x, self.y, self.z]

	def addVector(self, vector):
		self.x = self.x + vector.x
		self.y = self.y + vector.y
		self.z = self.z + vector.z
		self.net = self.net + vector.net
		self.length = math.sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def addx(self, x):
		self.x += x
		self.net = x + y + z
		self.length = math.sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def addy(self, y):
		self.y += y
		self.net = x + y + z
		self.length = math.sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def addz(self, z):
		self.z += z
		self.net = x + y + z
		self.length = math.sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def subtractVector(self, vector):
		self.x = self.x - vector.x
		self.y = self.y - vector.y
		self.z = self.z - vector.z
		self.net = self.net - vector.net
		self.length = math.sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def subx(self, x):
		self.x -= x
		self.net = self.x + self.y + self.z
		self.length = math.sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def suby(self, y):
		self.y -= y
		self.net = self.x + self.y + self.z
		self.length = math.sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def subz(self, z):
		self.z -= z
		self.net = self.x + self.y + self.z
		self.length = math.sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def multiplyVector(self, vector):
		self.x = self.x * vector.x
		self.y = self.y * vector.y
		self.z = self.z * vector.z
		self.net = self.net - vector.net
		self.length = math.sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def mulx(self, x):
		self.x *= x
		self.net = self.x + self.y + self.z
		self.length = math.sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def muly(self, y):
		self.y *= y
		self.net = self.x + self.y + self.z
		self.length = math.sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def mulz(self, z):
		self.z *= z
		self.net = self.x + self.y + self.z
		self.length = math.sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def divideVector(self, vector):
		self.x = self.x / vector.x
		self.y = self.y / vector.y
		self.z = self.z / vector.z
		self.net = self.net - vector.net
		self.length = math.sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def divx(self, x):
		self.x /= x
		self.net = self.x + self.y + self.z
		self.length = math.sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def divy(self, y):
		self.y /= y
		self.net = self.x + self.y + self.z
		self.length = math.sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

	def divz(self, z):
		self.z /= z
		self.net = self.x + self.y + self.z
		self.length = math.sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

class Point:
	def __init__(self, a1, y, z):
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

	def translateVector(self, vector):
		self.translate(vector.x, vector.y, vector.z)

	def rotate(self, dx, dy, dz, centerPoint=None):
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

	def rotateVector(self, vector, centerPoint=None):
		self.rotate(vector.x, vector.y, vector.z, centerPoint)

	def distance(self, object):
		if type(object) == type(self):
			return math.sqrt(((object.x - self.x) ** 2) + ((object.y - self.y) ** 2) + ((object.z - self.z) ** 2))
		else:
			# vec3 d = (C - B) / C.distance(B)
			# vec3 v = A - B
			# double t = v.dot(d)
			# vec3 P = B + t * d
			# return P.distance(A)
			pass

class Angle:
	def __init__(self, center, endp1, endp2):
		self.center = center
		self.endpoint1 = endp1
		self.endpoint2 = endp2

		ep1 = endp1.translate(-center.x, -center.y, -center.z)
		ep2 = endp2.translate(-center.x, -center.y, -center.z)

		endp1.translate(center.x, center.y, center.z)
		endp2.translate(center.x, center.y, center.z)

		self.angle = math.acos((ep1.x * ep2.x + ep1.y * ep2.y + ep1.z * ep2.z) / (sqrt((ep1.x ** 2) + (ep1.y ** 2) + (ep1.z ** 2)) * math.sqrt((ep2.x ** 2) + (ep2.y ** 2) + (ep2.z ** 2))))

	def translate(self, dx, dy, dz):
		self.__init__(self.center.translate(dx, dy, dz), self.endpoint1.translate(dx, dy, dz), self.endpoint2.translate(dx, dy, dz))
		return self

	def translateVector(self, vector):
		self.translate(vector.x, vector.y, vector.z)

	def rotate(self, dx, dy, dz, centerPoint=None):
		self.__init__(self.center.rotate(dx, dy, dz, centerPoint), self.endpoint1.rotate(dx, dy, dz, centerPoint), self.endpoint2.rotate(dx, dy, dz, centerPoint))
		return self

	def rotateVector(self, vector, centerPoint=None):
		self.rotate(vector.x, vector.y, vector.z, centerPoint)

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

	def translateVector(self, vector):
		self.translate(vector.x, vector.y, vector.z)

	def rotate(self, dx, dy, dz, centerPoint=None):
		self.__init__(self.origin.rotate(dx, dy, dz, centerPoint), self.pointOnRay.rotate(dx, dy, dz, centerPoint))
		return self

	def rotateVector(self, vector, centerPoint=None):
		self.rotate(vector.x, vector.y, vector.z, centerPoint)

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

def raycastCollision(point, *triangles):
	collisionLine = Line(object, Point(object.x + 1, object.y, object.z))
	hits = 0
	for tri in triangles:
		if tri.checkCollision(collisionLine) and tri.point1.x < object.x and tri.point2.x < object.x and tri.point3.x < object.x:
			hits += 1
	return hits % 2 == 1

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

	def translateVector(self, vector):
		self.translate(vector.x, vector.y, vector.z)

	def rotate(self, dx, dy, dz, centerPoint=None):
		self.__init__(self.origin.rotate(dx, dy, dz, centerPoint), self.pointOnRay.rotate(dx, dy, dz, centerPoint))
		return self

	def rotateVector(self, vector, centerPoint=None):
		self.rotate(vector.x, vector.y, vector.z, centerPoint)

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

	def translateVector(self, vector):
		self.translate(vector.x, vector.y, vector.z)

	def rotate(self, dx, dy, dz, centerPoint=None):
		self.__init__(self.point1.rotate(dx, dy, dz, centerPoint), self.point2.rotate(dx, dy, dz, centerPoint), self.point3.rotate(dx, dy, dz, centerPoint))
		return self

	def rotateVector(self, vector, centerPoint=None):
		self.rotate(vector.x, vector.y, vector.z, centerPoint)

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

	def translate(self, dx, dy, dz):
		self.center.translate(dx, dy, dz)
		self.tangentPoint.translate(dx, dy, dz)
		return self

	def translateVector(self, vector):
		self.translate(vector.x, vector.y, vector.z)

	def rotate(self, dx, dy, dz, centerPoint):
		self.center.rotate(dx, dy, dz, centerPoint)
		self.tangentPoint.rotate(dx, dy, dz, centerPoint)
		return self

	def rotateVector(self, vector, centerPoint=None):
		self.rotate(vector.x, vector.y, vector.z, centerPoint)

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

	def translateVector(self, vector):
		self.translate(vector.x, vector.y, vector.z)

	def rotate(self, dx, dy, dz, centerPoint=None):
		self.__init__(self.close_bottom_left.rotate(dx, dy, dz, centerPoint), self.far_top_right.rotate(dx, dy, dz, centerPoint))
		self.rotation.addVector(Vector(dx, dy, dz))
		return self

	def rotateVector(self, vector, centerPoint=None):
		self.rotate(vector.x, vector.y, vector.z, centerPoint)

	def checkCollision(self, object):
		if type(object) == type(Point(0, 0, 0)):
			tp = object.rotate(self.rotation.x, self.rotation.y, self.rotation.z, Point(0, 0, 0))
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

class Block:
	def __init__(self, corner1, arg2, material, isNegative):
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

		self.points = [self.close_bottom_left,
			       self.far_bottom_left,
			       self.close_top_left,
			       self.far_top_left,
			       self.close_bottom_right,
			       self.far_bottom_right,
			       self.close_top_right,
			       self.far_top_right
			      ]
		self.point1, self.point2, self.point3, self.point4, self.point5, self.point6, self.point7, self.point8 = self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.p8 = \
		self.close_bottom_left,self.far_bottom_left, self.close_top_left,self.far_top_left, self.close_bottom_right, self.far_bottom_right, self.close_top_right, self.far_top_right

		self.volume = self.close_bottom_left.distance(self.close_bottom_right)
		self.volume *= self.close_bottom_left.distance(self.close_top_left)
		self.volume *= self.close_bottom_left.distance(self.far_bottom_left)
		self.material = material
		self.mass = self.volume * self.material.density
		self.linearMovement = Vector(0, 0, 0)
		self.angularMovement = Vector(0, 0, 0)
		self.centerOfMass = Point(
			sum([p.x for p in self.points]) / len(self.points),
			sum([p.y for p in self.points]) / len(self.points),
			sum([p.z for p in self.points]) / len(self.points)
		)

		self.rotation = Vector(0, 0, 0)
		self.isNegative = isNegative

		self.links = []

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

	def recalculate(self, corner1, corner2):
		self.close_bottom_left = Point(corner1.x, corner1.y, corner1.z)
		self.far_bottom_left = Point(arg2.x, corner1.y, corner1.z)
		self.close_top_left = Point(corner1.x, arg2.y, corner1.z)
		self.far_top_left = Point(arg2.x, arg2.y, corner1.z)
		self.close_bottom_right = Point(corner1.x, corner1.y, arg2.z)
		self.far_bottom_right = Point(arg2.x, corner1.y, arg2.z)
		self.close_top_right = Point(corner1.x, arg2.y, arg2.z)
		self.far_top_right = Point(arg2.x, arg2.y, arg2.z)

		self.points = [self.close_bottom_left,
			       self.far_bottom_left,
			       self.close_top_left,
			       self.far_top_left,
			       self.close_bottom_right,
			       self.far_bottom_right,
			       self.close_top_right,
			       self.far_top_right
			      ]

	def translate(self, dx, dy, dz):
		self.recalculate(self.close_bottom_left.translate(dx, dy, dz), self.far_top_right.translate(dx, dy, dz))
		[link.propagateEffect(self, 0, dx, dy, dz) for link in self.links]
		return self

	def translateVector(self, vector):
		return self.translate(vector.x, vector.y, vector.z)

	def rotate(self, dx, dy, dz, centerPoint=None):
		self.__init__(self.close_bottom_left.rotate(dx, dy, dz, centerPoint), self.far_top_right.rotate(dx, dy, dz, centerPoint))
		self.rotation.addVector(Vector(dx, dy, dz))
		[link.propagateEffect(self, 1, dx, dy, dz, centerPoint) for link in self.links]
		return self

	def rotateVector(self, vector, centerPoint=None):
		return self.rotate(vector.x, vector.y, vector.z, centerPoint)

	def applyForce(self, force):
		self.movement.addVector(force)

	def checkCollision(self, object):
		if type(object) == type(Point(0, 0, 0)):
			tp = object.rotate(self.rotation.x, self.rotation.y, self.rotation.z, Point(0, 0, 0))
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

	def applyLinearForce(self, fx, fy, fz):
		self.linearMovement.addx(fx)
		self.linearMovement.addy(fy)
		self.linearMovement.addz(fz)
		[link.propagateEffect(self, 2, fx, fy, fz) for link in self.links]
		return self

	def applyLinearForceVector(self, force):
		self.linearMovement.addVector(force)
		[link.propagateEffect(self, 2, force.x, force.y, force.z) for link in self.links]
		return self

	def applyAngularForce(self, fx, fy, fz):
		self.angularMovement.addx(fx)
		self.angularMovement.addy(fy)
		self.angularMovement.addz(fz)
		[link.propagateEffect(self, 3, fx, fy, fz) for link in self.links]
		return self

	def applyAngularForceVector(self, force):
		self.angularMovement.addVector(force)
		[link.propagateEffect(self, 3, force.x, force.y, force.z) for link in self.links]
		return self

	def applyForce(self, linearForce, angularForce):
		self.linearMovement.addVector(linearForce)
		self.angularMovement.addVector(angularForce)
		[link.propagateEffect(self, 2, linearForce.x, linearForce.y, linearForce.z) for link in self.links]
		[link.propagateEffect(self, 3, angularForce.x, angularForce.y, angularForce.z) for link in self.links]
		return self

class Ball:
	def __init__(self, center, radius, material, isNegative):
		self.center = center

		if type(radius) == type(1):
			self.radius = radius
			self.tangentPoint = self.center.translate(self.radius, 0, 0)
		elif type(radius) == type(Point(0, 0, 0)):
			self.radius = self.center.distance(radius)
			self.tangentPoint = radius
			self.isNegative = isNegative

		self.material = material
		self.volume = (4/3) * math.pi * (self.radius ^ 3)
		self.mass = self.volume * self.material.density
		self.linearMovement = Vector(0, 0, 0)
		self.angularMovement = Vector(0, 0, 0)
		self.centerOfMass = self.center

		self.links = []

	def translate(self, dx, dy, dz):
		self.center.translate(dx, dy, dz)
		self.tangentPoint.translate(dx, dy, dz)
		[link.propagateEffect(self, 0, dx, dy, dz) for link in self.links]
		return self

	def translateVector(self, vector):
		return self.translate(vector.x, vector.y, vector.z)

	def rotate(self, dx, dy, dz, centerPoint):
		self.center.rotate(dx, dy, dz, centerPoint)
		self.tangentPoint.rotate(dx, dy, dz, centerPoint)
		[link.propagateEffect(self, 1, dx, dy, dz, centerPoint) for link in self.links]
		return self

	def rotateVector(self, vector, centerPoint=None):
		return self.rotate(vector.x, vector.y, vector.z, centerPoint)

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

	def applyLinearForce(self, fx, fy, fz):
		self.linearMovement.addx(fx)
		self.linearMovement.addy(fy)
		self.linearMovement.addz(fz)
		[link.propagateEffect(self, 2, fx, fy, fz) for link in self.links]
		return self

	def applyLinearForceVector(self, force):
		self.linearMovement.addVector(force)
		[link.propagateEffect(self, 2, force.x, force.y, force.z) for link in self.links]
		return self

	def applyAngularForce(self, fx, fy, fz):
		self.angularMovement.addx(fx)
		self.angularMovement.addy(fy)
		self.angularMovement.addz(fz)
		[link.propagateEffect(self, 3, fx, fy, fz) for link in self.links]
		return self

	def applyAngularForceVector(self, force):
		self.angularMovement.addVector(force)
		[link.propagateEffect(self, 3, force.x, force.y, force.z) for link in self.links]
		return self

	def applyForce(self, linearForce, angularForce):
		self.linearMovement.addVector(linearForce)
		self.angularMovement.addVector(angularForce)
		[link.propagateEffect(self, 2, linearForce.x, linearForce.y, linearForce.z) for link in self.links]
		[link.propagateEffect(self, 3, angularForce.x, angularForce.y, angularForce.z) for link in self.links]
		return self

class Cylinder:
	def __init__(self, centerPoint, radius, height, material, isNegative):
		self.centerPoint = centerPoint
		self.radius = radius
		self.height = height
		self.material = material
		self.volume = math.pi * (self.radius ^ 2) * self.height
		self.mass = self.volume * self.material.density
		self.movement = Vector(0, 0, 0)
		self.isNegative = isNegative
		self.linearMovement = Vector(0, 0, 0)
		self.angularMovement = Vector(0, 0, 0)

		self.rotationVector = Vector(0, 0, 0)

		self.links = []

	def translate(self, dx, dy, dz):
		self.center.translate(dx, dy, dz)
		[link.propagateEffect(self, 0, dx, dy, dz) for link in self.links]
		return self

	def translateVector(self, vector):
		return self.translate(vector.x, vector.y, vector.z)

	def rotate(self, dx, dy, dz, centerPoint):
		self.center.rotate(dx, dy, dz, centerPoint)
		self.rotationVector.addVector(dx, dy, dz)
		[link.propagateEffect(self, 1, dx, dy, dz, centerPoint) for link in self.links]
		return self

	def rotateVector(self, vector, centerPoint=None):
		return self.rotate(vector.x, vector.y, vector.z, centerPoint)

	def checkCollision(self, object):
		rv = self.rotationVector
		self.rotate(-self.rotationVector.x, -self.rotationVector.y, -self.rotationVector.z)
		if type(object) == type(Point(0, 0, 0)):
			return self.centerPoint.distance(object) <= self.radius and self.center.z <= object.z <= self.center.z + self.height
		elif type(object) == type(Triangle(0, 0, 0)):
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

			zrange = False
			zrange = zrange or self.center.z <= object.point1.z <= self.center.z + self.height
			zrange = zrange or self.center.z <= object.point2.z <= self.center.z + self.height
			zrange = zrange or self.center.z <= object.point3.z <= self.center.z + self.height

			return collided and zrange
		self.rotate(rv.x, rv.y, rv.z)

	def applyLinearForce(self, fx, fy, fz):
		self.linearMovement.addx(fx)
		self.linearMovement.addy(fy)
		self.linearMovement.addz(fz)
		[link.propagateEffect(self, 2, fx, fy, fz) for link in self.links]
		return self

	def applyLinearForceVector(self, force):
		self.linearMovement.addVector(force)
		[link.propagateEffect(self, 2, force.x, force.y, force.z) for link in self.links]
		return self

	def applyAngularForce(self, fx, fy, fz):
		self.angularMovement.addx(fx)
		self.angularMovement.addy(fy)
		self.angularMovement.addz(fz)
		[link.propagateEffect(self, 3, fx, fy, fz) for link in self.links]
		return self

	def applyAngularForceVector(self, force):
		self.angularMovement.addVector(force)
		[link.propagateEffect(self, 3, force.x, force.y, force.z) for link in self.links]
		return self

	def applyForce(self, linearForce, angularForce):
		self.linearMovement.addVector(linearForce)
		self.angularMovement.addVector(angularForce)
		[link.propagateEffect(self, 2, linearForce.x, linearForce.y, linearForce.z) for link in self.links]
		[link.propagateEffect(self, 3, angularForce.x, angularForce.y, angularForce.z) for link in self.links]
		return self

class TriangularPyramid:
	def __init__(self, pb1, pb2, pb3, pv, material):
		self.point_base1 = pb1 # point 1
		self.point1 = self.point_base1
		self.point_base2 = pb2 # point 2
		self.point2 = self.point_base2
		self.point_base3 = pb3 # point 3
		self.point3 = self.point_base3
		self.point_vertex = pv # point 4
		self.point4 = self.point_vertex
		self.base = Triangle(self.point_base1, self.point_base2, self.point_base3)
		self.face_123 = self.base
		self.face_124 = Triangle(self.point1, self.point2, self.point3)
		self.face_134 = Triangle(self.point1, self.point3, self.point4)
		self.face_234 = Triangle(self.point2, self.point3, self.point4)
		self.surface_area = self.face_123.area + self.face_124.area + self.face_134.area + self.face_234.area
		self.material = material
		self.volume = self.face_123.area

		self.movement = Vector(0, 0, 0)
		self.links = []

	def __iter__(self):
		pass

	def __next__(self):
		pass

	def translate(self, dx, dy, dz):
		self.__init__(self.point_base1.translate(dx, dy, dz), self.point_base2.translate(dx, dy, dz), self.point_base3.translate(dx, dy, dz), self.point_vertex.translate(dx, dy, dz), self.material)
		[link.propagateEffect(self, 0, dx, dy, dz) for link in self.links]
		return self

	def translateVector(self, vector):
		return self.translate(vector.x, vector.y, vector.z)

	def rotate(self, dx, dy, dz, centerPoint=None):
		self.__init__(self.point_base1.rotate(dx, dy, dz, centerPoint), self.point_base2.rotate(dx, dy, dz, centerPoint), self.point_base3.rotate(dx, dy, dz, centerPoint), self.point_vertex.rotate(dx, dy, dz, centerPoint), self.material)
		[link.propagateEffect(self, 1, dx, dy, dz, centerPoint) for link in self.links]
		return self

	def rotateVector(self, vector, centerPoint=None):
		return self.rotate(vector.x, vector.y, vector.z, centerPoint)

	def checkCollision(object):
		if type(object) == type(Point(0, 0, 0)):
			collisionLine = Line(object, Point(object.x + 1, object.y, object.z))
			hits = 0
			for tri in [self.face_123, self.face_]:
				if tri.checkCollision(collisionLine) \
				and tri.point1.x < object.x \
				and tri.point2.x < object.x \
				and tri.point3.x < object.x:
					hits += 1
			return hits % 2 == 1

	def applyLinearForce(self, fx, fy, fz):
		self.linearMovement.addx(fx)
		self.linearMovement.addy(fy)
		self.linearMovement.addz(fz)
		[link.propagateEffect(self, 2, fx, fy, fz) for link in self.links]
		return self

	def applyLinearForceVector(self, force):
		self.linearMovement.addVector(force)
		[link.propagateEffect(self, 2, force.x, force.y, force.z) for link in self.links]
		return self

	def applyAngularForce(self, fx, fy, fz):
		self.angularMovement.addx(fx)
		self.angularMovement.addy(fy)
		self.angularMovement.addz(fz)
		[link.propagateEffect(self, 3, fx, fy, fz) for link in self.links]
		return self

	def applyAngularForceVector(self, force):
		self.angularMovement.addVector(force)
		[link.propagateEffect(self, 3, force.x, force.y, force.z) for link in self.links]
		return self

	def applyForce(self, linearForce, angularForce):
		self.linearMovement.addVector(linearForce)
		self.angularMovement.addVector(angularForce)
		[link.propagateEffect(self, 2, linearForce.x, linearForce.y, linearForce.z) for link in self.links]
		[link.propagateEffect(self, 3, angularForce.x, angularForce.y, angularForce.z) for link in self.links]
		return self

class ConvexLowpoly:
	def __init__(self, material, *triangles):
		self.triangles = triangles
		self.points = []
		for tri in self.triangles:
			self.points.append(tri.point1)
			self.points.append(tri.point2)
			self.points.append(tri.point3)
		self.surfaceArea = sum([tri.area for tri in self.triangles])
		try:
			self.volume = spatial.ConvexHull(self.points).volume
		except scipy.spatial._qhull.QhullError:
			return False
		except Exception as e:
			raise e
		self.material = material
		self.mass = self.volume * self.material.density
		self.isNegative = isNegative

		self.linearMovement = Vector(0, 0, 0)
		self.angularMovement = Vector(0, 0, 0)

		self.links = []

	def translate(self, dx, dy, dz):
		[tri.translate(dx, dy, dz) for tri in self.triangles]
		[link.propagateEffect(self, 0, dx, dy, dz) for link in self.links]
		return self

	def translateVector(self, vector):
		return self.translate(vector.x, vector.y, vector.z)

	def rotate(self, dx, dy, dz, centerPoint):
		[tri.rotate(dx, dy, dz, centerPoint) for tri in self.triangles]
		[link.propagateEffect(self, 1, dx, dy, dz, centerPoint) for link in self.links]
		return self

	def rotateVector(self, vector, centerPoint=None):
		return self.rotate(vector.x, vector.y, vector.z, centerPoint)

	def checkCollision(self, object):
		if type(object) == type(Point(0, 0, 0)):
			return raycastCollision(object, self.triangles)

	def applyLinearForce(self, fx, fy, fz):
		self.linearMovement.addx(fx)
		self.linearMovement.addy(fy)
		self.linearMovement.addz(fz)
		[link.propagateEffect(self, 2, fx, fy, fz) for link in self.links]
		return self

	def applyLinearForceVector(self, force):
		self.linearMovement.addVector(force)
		[link.propagateEffect(self, 2, force.x, force.y, force.z) for link in self.links]
		return self

	def applyAngularForce(self, fx, fy, fz):
		self.angularMovement.addx(fx)
		self.angularMovement.addy(fy)
		self.angularMovement.addz(fz)
		[link.propagateEffect(self, 3, fx, fy, fz) for link in self.links]
		return self

	def applyAngularForceVector(self, force):
		self.angularMovement.addVector(force)
		[link.propagateEffect(self, 3, force.x, force.y, force.z) for link in self.links]
		return self

	def applyForce(self, linearForce, angularForce):
		self.linearMovement.addVector(linearForce)
		self.angularMovement.addVector(angularForce)
		[link.propagateEffect(self, 2, linearForce.x, linearForce.y, linearForce.z) for link in self.links]
		[link.propagateEffect(self, 3, angularForce.x, angularForce.y, angularForce.z) for link in self.links]
		return self

class ConcaveLowpoly:
	def __init__(self, material, alpha=0.4, *triangles):
		self.triangles = triangles
		self.points = []
		for tri in self.triangles:
			self.points.append(tri.point1)
			self.points.append(tri.point2)
			self.points.append(tri.point3)
		self.surfaceArea = sum([tri.area for tri in self.triangles])
		self.alphashape = alphashape.alphashape([(p.x, p.y, p.z) for p in self.points], alpha)
		self.volume = self.alphashape.volume
		self.material = material
		self.mass = self.volume * self.material.density
		self.linearMovement = Vector(0, 0, 0)
		self.angularMovement = Vector(0, 0, 0)

		self.links = []

	def translate(self, dx, dy, dz):
		[tri.translate(dx, dy, dz) for tri in self.triangles]
		[point.translate(dx, dy, dz) for point in self.points]
		[link.propagateEffect(self, 0, dx, dy, dz) for link in self.links]
		return self

	def translateVector(self, vector):
		return self.translate(vector.x, vector.y, vector.z)

	def rotate(self, dx, dy, dz, centerPoint=None):
		[tri.rotate(dx, dy, dz, centerPoint) for tri in self.triangles]
		[point.rotate(dx, dy, dz, centerPoint) for point in self.points]
		[link.propagateEffect(self, 1, dx, dy, dz, centerPoint) for link in self.links]
		return self

	def rotateVector(self, vector, centerPoint=None):
		return self.rotate(vector.x, vector.y, vector.z, centerPoint)

	def checkCollision(self, object):
		if type(object) == type(Point(0, 0, 0)):
			return raycastCollision(object, self.triangles)

	def applyLinearForce(self, fx, fy, fz):
		self.linearMovement.addx(fx)
		self.linearMovement.addy(fy)
		self.linearMovement.addz(fz)
		[link.propagateEffect(self, 2, fx, fy, fz) for link in self.links]
		return self

	def applyLinearForceVector(self, force):
		self.linearMovement.addVector(force)
		[link.propagateEffect(self, 2, force.x, force.y, force.z) for link in self.links]
		return self

	def applyAngularForce(self, fx, fy, fz):
		self.angularMovement.addx(fx)
		self.angularMovement.addy(fy)
		self.angularMovement.addz(fz)
		[link.propagateEffect(self, 3, fx, fy, fz) for link in self.links]
		return self

	def applyAngularForceVector(self, force):
		self.angularMovement.addVector(force)
		[link.propagateEffect(self, 3, force.x, force.y, force.z) for link in self.links]
		return self

	def applyForce(self, linearForce, angularForce):
		self.linearMovement.addVector(linearForce)
		self.angularMovement.addVector(angularForce)
		[link.propagateEffect(self, 2, linearForce.x, linearForce.y, linearForce.z) for link in self.links]
		[link.propagateEffect(self, 3, angularForce.x, angularForce.y, angularForce.z) for link in self.links]
		return self

Lowpoly = ConvexLowpoly

class Custom:
	def __init__(self, material, volume, collisionFunction, position):
		if type(position) == type(Point(0, 0, 0)):
			self.coordinates = position
		elif type(position) == type(Vector(0, 0, 0)):
			self.coordinates = Point(position.x, position.y, position.z)
		elif type(position) in [type([]), type((False, False))]:
			if len(position) == 3 and type(position[0]) in [type(0), type(0.5)] \
			and type(position[0]) in [type(0), type(0.5)] \
			and type(position[0]) in [type(0), type(0.5)]:
				self.coordinates = Point(position[0], position[1], position[2])
			else:
				raise IndexError("Tuples or Lists for positional arguments must contain exactly three numbers")
		else:
			raise TypeError("Position must be a Point, Vector, List, or Triple.")
		self.position = self.coordinates
		self.material = material
		self.volume = volume
		self.mass = self.volume * self.material.density

		self.collisionFunction = collisionFunction

		self.linearMovement = Vector(0, 0, 0)
		self.angularMovement = Vector(0, 0, 0)

		self.rotation = Vector(0, 0, 0)

		self.links = []

	def translate(self, dx, dy, dz):
		self.coordinates.translate(dx, dy, dz)
		self.position = self.coordinates
		[link.propagateEffect(self, 0, dx, dy, dz) for link in self.links]
		return self

	def translateVector(self, vector):
		return self.translate(vector.x, vector.y, vector.z)

	def rotate(self, dx, dy, dz, centerPoint=None):
		self.coordinates.rotate(dx, dy, dz, centerPoint)
		self.position = self.coordinates
		self.rotation.addVector(Vector(dx, dy, dz))
		[link.propagateEffect(self, 1, dx, dy, dz, centerPoint) for link in self.links]
		return self

	def rotateVector(self, vector, centerPoint=None):
		return self.rotate(vector.x, vector.y, vector.z, centerPoint)

	def checkCollision(self, object):
		crv = self.rotation
		self.rotate(-self.rotation.x, -self.rotation.y, -self.rotation.z)
		rotation_reversed = self
		self.rotate(crv.x, crv.y, crv.z)
		del crv
		pos = self.position
		self.translate(-self.position.x, -self.position.y, -self.position.z)
		at_0 = self
		self.translate(pos.x, pos.y, pos.z)
		del pos
		return self.collisionFunction(**{
			"object": object,
			"self_current": self,
			"self_rotation_reversed": rotation_reversed,
			"self_at_0": at_0
		})

	def applyLinearForce(self, fx, fy, fz):
		self.linearMovement.addx(fx)
		self.linearMovement.addy(fy)
		self.linearMovement.addz(fz)
		[link.propagateEffect(self, 2, fx, fy, fz) for link in self.links]
		return self

	def applyLinearForceVector(self, force):
		self.linearMovement.addVector(force)
		[link.propagateEffect(self, 2, force.x, force.y, force.z) for link in self.links]
		return self

	def applyAngularForce(self, fx, fy, fz):
		self.angularMovement.addx(fx)
		self.angularMovement.addy(fy)
		self.angularMovement.addz(fz)
		[link.propagateEffect(self, 3, fx, fy, fz) for link in self.links]
		return self

	def applyAngularForceVector(self, force):
		self.angularMovement.addVector(force)
		[link.propagateEffect(self, 3, force.x, force.y, force.z) for link in self.links]
		return self

	def applyForce(self, linearForce, angularForce):
		self.linearMovement.addVector(linearForce)
		self.angularMovement.addVector(angularForce)
		[link.propagateEffect(self, 2, linearForce.x, linearForce.y, linearForce.z) for link in self.links]
		[link.propagateEffect(self, 3, angularForce.x, angularForce.y, angularForce.z) for link in self.links]
		return self

class Link:
	def __init__(self, translation=True, rotation=True, linearForce=True, angularForce=True, *objects):
		self.objects = objects
		for obj in objects:
			obj.links.append(self)
		self.translationEnabled = translation
		self.rotationEnabled = rotation
		self.linearForceEnabled = linearForce
		self.angularForceEnabled = angularForce

	def propagateEffect(self, affectedObject, effectType, dx, dy, dz, centerPoint):
		try:
			for obj in self.objects:
				if obj == affectedObject:
					pass
				else:
					if effectType == 0:
						obj.translate(dx, dy, dz)
					if effectType == 1:
						obj.rotate(dx, dy, dz, centerPoint)
					if effectType == 2:
						obj.applyLinearForce(dx, dy, dz)
					if effectType == 3:
						obj.applyAngularForce(dx, dy, dz)
		except Exception as e:
			raise e
		finally:
			return True

class ContactTrigger:
	def __init__(self, callback, *objects, **callbackarggenerators):
		self.callback = callback
		self.callbackarguments = callbackarggenerators
		self.objects = objects

	def add(self, object):
		self.objects.append(object)
		return self

	def remove(self, object):
		self.objects = [x for x in self.objects if x != object]
		return self

	def checkCollision(self, object):
		collided = False
		for x in objects:
			collided = collided or object.checkCollision(object)
		if collided:
			self.callback(**self.callbackarguments)
		return collided

	def translate(self, dx, dy, dz):
		[obj.translate(dx, dy, dz) for obj in self.objects]
		return self

	def translateVector(self, vector):
		return self.translate(vector.x, vector.y, vector.z)

	def rotate(self, dx, dy, dz, centerPoint=None):
		[obj.rotate(dx, dy, dz, centerPoint) for obj in self.objects]
		return self

	def rotateVector(self, vector, centerPoint=None):
		return self.rotate(vector.x, vector.y, vector.z, centerPoint=None)

	def applyLinearForce(self, dx, dy, dz):
		[obj.applyLinearForce(dx, dy, dz) for obj in self.objects]
		return self

	def applyLinearForceVector(self, vector):
		[obj.applyLinearForce(vector.x, vector.y, vector.z) for obj in self.objects]
		return self

	def applyAngularForce(self, dx, dy, dz):
		[obj.applyAngularForce(dx, dy, dz) for obj in self.objects]
		return self

	def applyAngularForceVector(self, vector):
		[obj.applyAngularForce(vector.x, vector.y, vector.z) for obj in self.objects]
		return self

	def applyForce(self, linear, angular):
		self.applyLinearForceVector(linear)
		self.applyAngularForceVector(angular)
		return self

	def call(self):
		return self.callback(**self.callbackarguments)
