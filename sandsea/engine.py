import objects
import gui

# All measurements are in Standard Imperial system.
# # Density: kg / m^3
# # Volume: m^3
# # Area: m^2
# # Length: m
# # Energy: J

class PropertiesController:
	def __init__(self, gravity=objects.Vector(0, 0, 0), airDensity=0, precisionFactor=1e-16, gravitationEnabled=True, tickRate=1000):
		self.properties = {
			"gravity": gravity,
			"airDensity": airDensity,
			"precisionFactor": precisionFactor,
			"gravitationEnabled": gravitationEnabled,
			"tickRate": tickRate
		}
		self.gravity = gravity
		self.airDensity = airDensity
		self.precisionFactor = precisionFactor
		self.gravitationEnabled = gravitationEnabled
		self.tickRate = tickRate

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
		                             and tickRate.

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

	def __init__(self, *objects, **properties):
		self.simulationTime = 0
		self.objects = objects
		self.points = []
		[self.points.append(x) for x in [obj.__iter__() for obj in self.objects]]
		self.centerOfMass = objects.Point(sum([p.x for p in self.points]) / len(self.points), sum([p.y for p in self.points]) / len(self.points), sum([p.z for p in self.points]) / len(self.points))

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
		pass

	def runUntilTimestamp(self, futureTimestamp):
		while time.time() < futureTimestamp:
			self.tick()
		return self.objects

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
		for x in objects:
			self.objects.append(x)

	def remove(self, *indices):
		for x in indices:
			del self.objects[x]
