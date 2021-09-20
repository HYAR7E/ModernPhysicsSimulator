""" MICHELSON AND MORLEY'S INTERFEROMETER """

import vpython as vp
import random as rand
import datetime as dt
from drawings import laserbeam, x_table, x_laserengine, x_beamsplitter, x_beamreceptor, x_mirror, indicator

""" Fake empty object
obj = lambda: None
* properties and methods can be setted by using dot operator
* eg: obj.title = "Hello World"
"""

class Interferometer():
	def __init__(self, beamtype="regular"):
		self.vp = vp

		# Custom behaviour
		self.wavelike = beamtype == "wave"

		# Set alias to ease usability
		self.vc = vp.vector
		self.cl = vp.color
		self.settings = lambda: None
		self.objects = lambda: None

		# Set initial settings
		self.init()
		self.set_settings()
		self.set_physics_settings()

		# Beam (Objects list)
		self.beam = list()
		# Initialize objects
		self.init_objects()

		# Interference pattern
		self.pattern = list( [0 for _ in range(0, self.settings.physics.number_of_particles)] )

	""" SETTINGS """
	def init(self):
		vp = self.vp
		# Set library configuration
		vp.scene.width = 1500
		vp.scene.height = 750
		vp.scene.autoscale = False
		#vp.scene.userspin = False
		#vp.scene.userpan = False
		vp.scene.background = self.vc(.7, .7, .7)
		vp.scene.camera.pos = self.vc(0, 0, 70)

	def set_settings(self):
		# Regular Settings
		settings = self.settings
		settings.objects = lambda: None
		settings.objects.laserengine = lambda: None
		settings.objects.beamsplitter = lambda: None
		settings.objects.mirror_r = lambda: None
		settings.objects.mirror_b = lambda: None
		settings.objects.receptor = lambda: None
		settings.objects.indicator = lambda: None

		""" DATA """
		# Laser Engine
		settings.objects.laserengine.x = -45
		settings.objects.laserengine.y = 0
		settings.objects.laserengine.length = 10
		# Beam Splitter
		settings.objects.beamsplitter.x = 0
		settings.objects.beamsplitter.y = 0
		settings.objects.beamsplitter.length = 10
		# Mirror R (right side)
		settings.objects.mirror_r.x = 30
		settings.objects.mirror_r.y = 0
		settings.objects.mirror_r.length = 10
		settings.objects.mirror_r.angle = 90
		# Mirror B (bottom side)
		settings.objects.mirror_b.x = 0
		settings.objects.mirror_b.y = -30
		settings.objects.mirror_b.length = 10
		settings.objects.mirror_b.angle = 0
		# Receptor
		settings.objects.receptor.x = 0
		settings.objects.receptor.y = 30
		settings.objects.receptor.length = 10
		settings.objects.receptor.angle = 0  
		#indicator
		settings.objects.indicator.x=10
		settings.objects.indicator.y=-10
		settings.objects.indicator.r=.5
	def set_physics_settings(self):
		# Physics Settings
		settings = self.settings
		settings.physics = lambda: None

		# Init time (miliseconds)
		settings.physics.t = 0
		# Ratio of execution per second
		settings.physics.rate = 200
		# Time differential (miliseconds)
		settings.physics.step = 1000/settings.physics.rate
		# light particle's movement speed
		""" dv
		* this value should be half the value of step in laserbeam function
		"""
		settings.physics.dv = self.vc(0.25, 0, 0)
		# angle of beamsplitter
		settings.physics.beamsplitter_angle = 45
		# number of particles per beam
		settings.physics.number_of_particles = 5

	def init_objects(self):
		# Initialize Objects
		objects = self.objects

		# Table background
		objects.table = x_table(100, 100, self.vc(.9, .9, .9))
		# Laser engine
		objects.laserengine = x_laserengine(
			self.settings.objects.laserengine.x,
			self.settings.objects.laserengine.y,
			self.settings.objects.laserengine.length,
			self.cl.black)
		# Beamsplitter
		objects.beamsplitter = x_beamsplitter(
			self.settings.objects.beamsplitter.x,
			self.settings.objects.beamsplitter.y,
			self.settings.objects.beamsplitter.length,
			self.settings.physics.beamsplitter_angle)
		# Mirror R (right)
		objects.mirror_r = x_mirror(
			self.settings.objects.mirror_r.x,
			self.settings.objects.mirror_r.y,
			self.settings.objects.mirror_r.length,
			self.settings.objects.mirror_r.angle)
		# Mirror B (bottom)
		objects.mirror_b = x_mirror(
			self.settings.objects.mirror_b.x,
			self.settings.objects.mirror_b.y,
			self.settings.objects.mirror_b.length,
			self.settings.objects.mirror_b.angle)
		# Receptor (top)
		objects.receptor = x_beamreceptor(
			self.settings.objects.receptor.x,
			self.settings.objects.receptor.y,
			self.settings.objects.receptor.length,
			self.settings.objects.receptor.angle)

		# Indicator
		objects.indicator = indicator(
			self.settings.objects.indicator.x,
			self.settings.objects.indicator.y,
			self.settings.objects.indicator.r)
		
		# Beam
		self.beam += laserbeam(
			self.settings.objects.laserengine.x\
			+self.settings.objects.laserengine.length,
			self.settings.objects.laserengine.y,
			self.settings.physics.number_of_particles,
			self.settings.physics.dv)
		
	""" FUNCTIONS """
	def move_particle(self, p):
		""" Move particle by its own speed
		params:
			* p: light particles
		"""
		p.pos.x = round(p.pos.x + p.speed.x, 3)
		p.pos.y = round(p.pos.y + p.speed.y, 3)
		p.pos.z = round(p.pos.z + p.speed.z, 3)

	def beamsplitter_collision(self, bs, p):
		""" compute_collision
		* check if given particle collision with beamsplitter
		params:
			* bs: beamsplitter (box object)
			* p: light particle (sphere object)
		"""
		vp = self.vp

		# Check if there is collision
		if bs.calc_y(p.pos.x) == p.pos.y:
			if bool( rand.randint(0, 1) ):
				if p.speed.x < 0 and p.speed.y == 0:
					self.delete_particle(p)
				return

			# Update speed vector
			rad = bs.angle
			mag = vp.mag(p.speed) # Get magnitude (abs of vector)

			# Calculate new speed
			_x = round( mag*( vp.cos(rad)**2 - vp.sin(rad)**2 ) , 3)
			_y = round( 2*mag*vp.sin(rad)*vp.cos(rad) , 3)
			# Calc change in direction of velocity from diff_angle between wall and point
			deg = round( vp.degrees( vp.diff_angle(bs.up, p.speed) ) , 3)
			if deg > 90:
				_x *= -1
				_y *= -1
			if abs(p.speed.y) > abs(p.speed.x):
				_tmp = _x
				_x = _y
				_y = _tmp
			p.speed.x = _x
			p.speed.y = _y

	def compute_collision(self, p, wall, walltype):
		""" compute_collision
		* check if given particle collision with given wall
		params:
			* wall: object to collision with (box object)
			* p: light particle (sphere object)
		"""
		vp = self.vp

		# Check if there is collision
		if not wall.calc_y or wall.calc_y(p.pos.x) == p.pos.y:
			# If walltype is receptor: remove point
			if walltype == "receptor":
				self.delete_particle(p, receptor=True)
				return

			# Update speed vector
			rad = wall.angle
			mag = vp.mag(p.speed) # Get magnitude (abs of vector)

			# Horizontal bounces
			if walltype == "mirror_b" or walltype == "receptor":
				rad += vp.pi/2

			# Calculate new speed
			_x = round( mag*( vp.cos(rad)**2 - vp.sin(rad)**2 ) , 3)
			_y = round( 2*mag*vp.sin(rad)*vp.cos(rad) , 3)

			# Horizontal bounce (exchange x and y)
			if wall.angle == 0:
				_tmp = _x
				_x = _y
				_y = _tmp
			if p.speed.x < 0: _x *= -1
			if p.speed.y < 0: _y *= -1

			p.speed.x = _x
			p.speed.y = _y

	def delete_particle(self, p, receptor=False):
		if receptor:
			self.pattern[p.id] = 1

		# Delete particle when it heads towards light origen (no more compute needed)
		p.visible = False
		self.beam.remove(p) # Remove particle from beam
		del(p) # Free memory

	def print_2dpattern(self, pattern):
		ar = pattern.copy()
		ar.reverse()
		r = list()
		for x in range(0, len(ar)):
			l = list()
			for y in range(0, len(ar)):
				v = "-"
				for i in range(0, len(ar)):
					if x == i or y == i: v = "0" if ar[i] else "-"
				l.append(v)
				_l = l[::-1]
				_l.pop()
			r.append(_l+l)
		_r = r[::-1]
		_r.pop()
		res = _r+r
		print("".join(["*" for _ in range(0, len(ar)*2-1)]))
		for r in res: print("".join(r))

	""" EXECUTE """
	def execute(self):
		vp = self.vp
		# Render loop (animation)
		while True:
			if self.wavelike: vp.rate(self.settings.physics.rate/2) # Pause
			else: vp.rate(self.settings.physics.rate) # Pause
			self.settings.physics.t += 1

			# Reset pattern
			self.pattern = list( [0 for _ in range(0, self.settings.physics.number_of_particles)] )

			# Compute from cords
			for p in self.beam:
				# Collision with BeamSplitter
				if True \
					and p.pos.x >= (self.objects.beamsplitter.pos.x-self.settings.objects.beamsplitter.length/2) \
					and p.pos.y >= (self.objects.beamsplitter.pos.y-self.settings.objects.beamsplitter.length/2) \
					and p.pos.x <= (self.objects.beamsplitter.pos.x+self.settings.objects.beamsplitter.length/2) \
					and p.pos.y <= (self.objects.beamsplitter.pos.y+self.settings.objects.beamsplitter.length/2) :
					self.beamsplitter_collision(self.objects.beamsplitter, p)

				# Collision with Mirror R (right)
				if True \
					and p.pos.x == (self.objects.mirror_r.pos.x) \
					and p.pos.y >= (self.objects.mirror_r.pos.y-self.settings.objects.mirror_r.length/2) \
					and p.pos.y <= (self.objects.mirror_r.pos.y+self.settings.objects.mirror_r.length/2) :
					self.compute_collision(p, self.objects.mirror_r, "mirror_r")

				# Collision with Mirror B (bottom)
				if True \
					and p.pos.y == (self.objects.mirror_b.pos.y) \
					and p.pos.x >= (self.objects.mirror_b.pos.x-self.settings.objects.mirror_b.length/2) \
					and p.pos.x <= (self.objects.mirror_b.pos.x+self.settings.objects.mirror_b.length/2) :
					self.compute_collision(p, self.objects.mirror_b, "mirror_b")

				# Collision with Receptor
				if True \
					and p.pos.y >= (self.objects.receptor.pos.y) \
					and p.pos.x >= (self.objects.receptor.pos.x-self.settings.objects.receptor.length/2) \
					and p.pos.x <= (self.objects.receptor.pos.x+self.settings.objects.receptor.length/2) :
					self.compute_collision(p, self.objects.receptor, "receptor")

				# Out of field
				if False \
					or p.pos.x > self.objects.mirror_r.pos.x \
					or p.pos.x < (self.objects.laserengine.pos.x+self.settings.objects.laserengine.length) \
					or p.pos.y < self.objects.mirror_b.pos.y \
					or p.pos.y > self.objects.receptor.pos.y :
					self.delete_particle(p)
					continue

				# Move particle
				self.move_particle(p)

			# Fire new laserbeam
			#if len(self.beam) < 3300:
			if len(self.beam) < 2500:
				self.beam += laserbeam(
					self.settings.objects.laserengine.x\
					+self.settings.objects.laserengine.length,
					self.settings.objects.laserengine.y,
					self.settings.physics.number_of_particles,
					self.settings.physics.dv,
					self.wavelike and self.settings.physics.t)

			# Print pattern as 2D
			self.print_2dpattern(self.pattern)
