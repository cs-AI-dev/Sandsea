import objects
import gui

# All measurements are in Standard Imperial system.
# # Density: kg / m^3
# # Volume: m^3
# # Area: m^2
# # Length: m
# # Energy: J
# # Temperature: degrees K

# gravity=objects.Vector(0, 0, 0), airDensity=0, precisionFactor=1e-16, gravitationEnabled=True, tickRate=1000

class PropertiesController:
	def __init__(self, **properties):
		self.properties = {
			"gravity": properties["gravity"],
			"airDensity": properties["airDensity"],
			"precisionFactor": properties["precisionFactor"],
			"gravitationEnabled": properties["gravitationEnabled"],
			"tickRate": properties["tickRate"],
			"gravitationalConstant": properties["gravitationalConstant"]
		}
		self.gravity = properties["gravity"]
		self.airDensity = properties["airDensity"]
		self.precisionFactor = properties["precisionFactor"]
		self.gravitationEnabled = properties["gravitationEnabled"]
		self.tickRate = properties["tickRate"]
		self.gravitationalConstant

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

	def setTickRate(self, newValue):
		self.tickRate = newValue
		self.properties["tickRate"] = newValue

	def setProperty(self, name, value):
		if name == "gravity":
			self.setGravity(value)
		if name == "airDensity":
			self.setAirDensity(value)
		if name == "precisionFactor":
			self.setPrecisionFactor(value)
		if name == "gravitationEnabled":
			self.setGravitationEnabled(value)
		if name == "tickRate":
			self.setTickRate(value)

class Material:
	def __init__(self, density=1, electricalResistance=0, magnetic=True, reflectance=1, meltingPoint=1000, boilingPoint=2000):
		self.density = density
		self.electricalResistance = electricalResistance
		self.magnetic = magnetic
		self.reflectance = reflectance
		self.meltingPoint = meltingPoint
		self.boilingPoint = boilingPoint

	def stateOfMatter(self, temperatureK):
		if temperatureK <= meltingPoint:
			return 0
		elif temperatureK <= boilingPoint:
			return 1
		else:
			return 2

class Asset:
	def __init__(self, materialObject, *objects):
		self.objects = objects
		self.materialProperties = materialObject
		self.volume = sum([obj.volume for obj in self.objects if obj.isReal])
		self.mass = self.material.density * self.volume
		self.movement = objects.Vector(0, 0, 0)
		self.momentum = self.movement.length * self.mass
		self.centerOfMass = objects.Point(0, 0, 0)
		[self.centerOfMass.translate(obj.centerOfMass.x / len(self.objects), 0, 0) for obj in self.objects]
		[self.centerOfMass.translate(0, obj.centerOfMass.y / len(self.objects), 0) for obj in self.objects]
		[self.centerOfMass.translate(0, 0, obj.centerOfMass.z / len(self.objects)) for obj in self.objects]
		self.parentSimulation = None

	def __iter__(self):
		self.n = 0
		return self

	def __next__(self):
		if self.n < len(self.objects):
			out = self.objects[self.n]
			self.n += 1
		else:
			raise StopIteration
		return out
<<<<<<< Updated upstream
	
	def checkCollision(self, object):
		positiveObjects = []
		negativeObjects = []
		[negative.append(obj) if obj.isNegative else positiveObjects.append(obj) for obj in self.objects]
		collided = []
		[collided.append(positiveObject.checkCollision(object)) for positiveObject in positiveObjects]
		[collided.append(not negativeObject.checkCollision(object)) for negativeObject in negativeObjects]
		for collisionCheck in collided:
			if collisionCheck:
				return True
		return False
	
=======

>>>>>>> Stashed changes
	def setParentSimulation(self, parentSimulation):
		try:
			self.parentSimulation = parentSimulation
			return True
		except NameError:
			return False
		except Exception as e:
			return e

class Simulation:
	help = """HELP - Simulation
The Simulation class is a very useful Sandsea class
which allows you to add objects to a physics simulation
and run the physics simulation. The class has a few methods,
all of which require that it has objects to work with, and
a few initialization arguments to control its operation.

INITIALIZATION ARGUMENTS
	*objects                           - All of the objects in the simulation in order.
                                             For example, Simulation(o1, o2, o3 ... oN)
	**properties                       - Properties of the simulation. Include gravity,
	                                     airDensity, precisionFactor, gravitationEnabled,
		                             tickRate, and smth.

METHODS
	tick()                             - Runs a single tick of the simulation.
	runUntilTimestamp(futureTimestamp) - Runs ticks of the simulation until the timestamp.
	run(time, setting)                 - Runs ticks until the desired time. Time must be an
					     integer representing the timestamp to end at, and
					     setting must be rs, rm, rh, rd, rw, ss, sm, sh, sd,
					     or sw, for real seconds, real minutes, real hours, real
					     days, real weeks, and the simulated converse.
	add(*objects)			   - Adds all objects supplied in the *objects parameter.
	remove(*indices)		   - Removes all objects at indices listed under *indices
					     from the objects in the simulation.
"""

	def __init__(self, *assets, **properties):
		self.simulationTime = 0
		self.assets = assets
		self.objects = []
		[self.objects += asset.objects for asset in self.assets]
		self.points = []
		[self.points += [[x for x in iter(obj)] for obj in asset] for asset in self.assets]
		self.centroid = objects.Point(
			sum([p.x for p in self.points]) / len(self.points),
			sum([p.y for p in self.points]) / len(self.points),
			sum([p.z for p in self.points]) / len(self.points)
		)
		self.centerOfMass = objects.Point(
			sum([asset.centerOfMass.x for asset in self.assets]) / len(self.assets),
			sum([asset.centerOfMass.y for asset in self.assets]) / len(self.assets),
			sum([asset.centerOfMass.z for asset in self.assets]) / len(self.assets)
		)
		self.properties = PropertiesController(**properties)
<<<<<<< Updated upstream
		return self
		
=======

>>>>>>> Stashed changes
	def __iter__(self):
		self.n = 0
		return self

	def __next__(self):
		if self.n < len(self.objects):
			out = self.objects[self.n]
			self.n += 1
		else:
			raise StopIteration
		return out

	def tick(self):
<<<<<<< Updated upstream
		for asset in self.assets:
			
=======
		if self.properties.gravitationEnabled:
			for obj1 in self.assets:
				for obj2 in self.assets:
					forceValue = (gravitationalConstant * ((obj1.mass * obj2.mass) / obj1.centerOfMass.distance(obj2.centerOfMasss))) / self.properties.ticksPerSecond
>>>>>>> Stashed changes

	def runUntilTimestamp(self, futureTimestamp):
		while time.time() < futureTimestamp:
			self.tick()
		return self.__init__(*self.assets, **self.properties.properties)

	def run(self, time, setting):
		if setting in ["realSeconds", "rs"]:
			return runUntilTimestamp(time.time() + time)
		elif setting in ["realMinutes", "rm"]:
			return runUntilTimestamp(time.time() + (60 * time))
		elif setting in ["realHours", "rh"]:
			return runUntilTimestamp(time.time() + (3600 * time))
		elif setting in ["realDays", "rd"]:
			return runUntilTimestamp(time.time() + (86400 * time))
		elif setting in ["realWeeks", "rw"]:
			return runUntilTimestamp(time.time() + (604800 * time))
		elif setting in ["simulatedSeconds", "ss"]:
			for x in range(time * self.properties.tickRate)): self.tick()
			return self.objects
		elif setting in ["simulatedMinutes" "sm"]:
			for x in range(time * self.properties.tickRate * 60): self.tick()
			return self.objects
		elif setting in ["simulatedHours", "sh"]:
			for x in range(time * self.properties.tickRate * 3600): self.tick()
			return self.objects
		elif setting in ["simulatedDays", "sd"]:
			for x in range(time * self.properties.tickRate * 86400): self.tick()
			return self.objects
		elif setting in ["simulatedWeeks", "sw"]:
			for x in range(time * self.properties.tickRate * 604800): self.tick()
			return self.objects
		elif setting in ["ticks", "t"]:
			for x in range(time):
				self.tick()
		else:
			return False

	def add(self, *objects):
		self.__init__(*self.objects + objects, **self.properties.properties)

	def remove(self, *indices):
		self.__init__(*[self.objects[x] for x in range(len(self.objects)) if not x in indices], **self.properties.properties)
