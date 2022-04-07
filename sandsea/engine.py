import objects
import gui

# All measurements are in Standard Imperial system.
# # Density: kg / m^3
# # Volume: m^3
# # Area: m^2
# # Length: m
# # Energy: J

class PropertiesController:
	def __init__(self, gravity=objects.Vector(0, 0, 0), airDensity=0, precisionFactor=1e-16, gravitationEnabled=True):
		self.properties = {
			"gravity": gravity,
			"airDensity": airDensity,
			"precisionFactor": precisionFactor,
			"gravitationEnabled": gravitationEnabled
		}
		self.gravity = gravity
		self.airDensity = airDensity
		self.precisionFactor = precisionFactor
		self.gravitationEnabled = gravitationEnabled

	def setGravity(self, newValue):
		self.gravity = newValue
		self.properties["gravity"] = newValue

	def setAirDensity(self, newValue):
		self.airDensity = newValue
		self.properties["airDensity"] = newValue

	def setPrecisionFactor(self, newValue):
		self.setPrecisionFactor = newValue
		self.properties["setPrecisionFactor"] = newValue

	def setGravitationEnabled(self, newValue):
		self.gravitationEnabled = newValue
		self.properties["gravitationEnabled"] = newValue

	def toggleGravitation(self):
		if self.gravitationEnabled:
			self.gravitationEnabled = False
			self.properties["gravitationEnabled"] = False
		else:
			self.gravitationEnabled = True
			self.properties["gravitationEnabled"] = True

	def setProperty(self, name, value):
		if name == "gravity":
			self.setGravity(value)
		if name == "airDensity":
			self.setAirDensity(value)
		if name == "precisionFactor":
			self.setPrecisionFactor(value)
		if name == "gravitationEnabled":
			self.setGravitationEnabled(value)

class Asset:
	def __init__(self, *objects):
		self.objects = objects
		self.points = []
		[self.points.append(x) for x in [obj.__iter__() for obj in self.objects]]
		self.centerOfMass = objects.Point(sum([p.x for p in self.points]) / len(self.points), sum([p.y for p in self.points]) / len(self.points), sum([p.z for p in self.points]) / len(self.points))

	def __iter__(self):
		return self.objects

class Simulation:
	def __init__(self, *assets, **properties):
		self.objects = assets
		if "gravity" in properties.keys():
			gv = properties["gravity"]
		else:
			gv = objects.Vector(0, 0, 0)
		if "gravity" in properties.keys():
			ad = properties["airDensity"]
		else:
			ad = 0
		if "gravity" in properties.keys():
			pf = properties["precisionFactor"]
		else:
			pf = 1e-16
		if "gravity" in properties.keys():
			ge = properties["gravitationEnabled"]
		else:
			ge = True
		self.properties = PropertiesController(gravity=gv, airDensity=ad, precisionFactor=pf, gravitationEnabled=ge)

	def __iter__(self):
		return self.objects

	def tick(self):
		pass

	def run(self, time, setting):
		if setting == "s":
			pass
		elif setting == "t":
			for x in range(time):
				self.tick()
		else:
			return False
