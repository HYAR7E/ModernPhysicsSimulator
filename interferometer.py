""" MICHELSON AND MORLEY'S INTERFEROMETER """

import vpython as vp
import random as rand
import datetime as dt
from drawings import laserbeam, x_table,\
	x_laserengine, x_beamsplitter,\
	x_beamreceptor, x_mirror, indicator,\
	copy_particle

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
		self.to_delete = list()
		# Initialize objects
		self.init_objects()
		# Add event handlers
		self.set_event_handlers()

		# Interference pattern
		self.pattern = list( [0 for _ in range(0, self.settings.physics.number_of_particles)] )

	""" SETTINGS """
	def init(self):
		vp = self.vp
		# Set library configuration
		vp.scene.title = "Interferometro\n"
		vp.scene.width = 1200
		vp.scene.height = 650
		vp.scene.autoscale = False
		#vp.scene.userspin = False
		#vp.scene.userpan = False
		vp.scene.background = self.vc(.7, .7, .7)
		vp.scene.camera.pos = self.vc(0, 0, 40)

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
		settings.physics.t = 1
		# Ratio of execution per second
		settings.physics.rate = 200
		# light particle's movement speed
		""" dv
		* this value should be half the value of step in laserbeam function
		"""
		settings.physics.dv = self.vc(0.25, 0, 0)
		# angle of beamsplitter
		settings.physics.beamsplitter_angle = 135
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
			self.settings.physics.dv,
			self.wavelike and self.settings.physics.t)
		"""
		#indicator 
		objects.indicator = indicator(
			self.settings.objects.indicator.x,
			self.settings.objects.indicator.y,
			self.settings.objects.indicator.h,
			self.settings.objects.indicator.w, 2)
		GF=data(
			self.settings.objects.indicator.x,
			self.settings.objects.indicator.y,
			self.settings.objects.indicator.w,
			self.settings.objects.indicator.h,
			self.settings.objects.indicator.n)
		"""
		
	""" EVENT FUNCTIONS """
	def btnPlayPause(self, btn):
		# Func to set play or pause
		self.playing = not self.playing
		if self.playing: btn.text = "Detener"
		else: btn.text = "Continuar"
	def btnResetBeam(self, btn):
		for p in self.beam: p.visible = False
		del(self.beam) # Free memory
		self.beam = list()
	def sldDistanceToMirrorR(self, sld):
		self.objects.mirror_r.pos.x = round(sld.value, 0)
		self.widgets.x.text = "X: "+str(int(self.objects.mirror_r.pos.x))
	def sldDistanceToMirrorB(self, sld):
		self.objects.mirror_b.pos.y = round(sld.value*-1, 0)
		self.widgets.y.text = "Y: "+str(int(self.objects.mirror_b.pos.y*-1))
	def sldSpeed(self, sld):
		self.settings.physics.rate = round(sld.value, 0)
		self.widgets.dv.text = "Ejecuciones por segundo: "+str(int(self.settings.physics.rate))

	def set_event_handlers(self):
		vp = self.vp
		self.widgets = lambda: None

		""" Add Play/Pause/Reset button """
		self.playing = True
		vp.button(text="Detener", pos=vp.scene.title_anchor, bind=self.btnPlayPause)
		vp.button(text="Reiniciar", pos=vp.scene.title_anchor, bind=self.btnResetBeam)
		vp.scene.append_to_title("\n")

		""" Change Mirror R distance """
		vp.slider(
			value=self.objects.mirror_r.pos.x,
			min=10, max=40, length=300,
			pos=vp.scene.title_anchor,
			bind=self.sldDistanceToMirrorR)
		self.widgets.x = vp.wtext(
			text="X: "+str(int(self.objects.mirror_r.pos.x)),
			pos=vp.scene.title_anchor)
		vp.scene.append_to_title("\n")

		""" Change Mirror B distance """
		vp.slider(
			value=self.objects.mirror_b.pos.y*-1,
			min=10, max=40, length=300,
			pos=vp.scene.title_anchor,
			bind=self.sldDistanceToMirrorB)
		self.widgets.y = vp.wtext(
			text="Y: "+str(int(self.objects.mirror_b.pos.y*-1)),
			pos=vp.scene.title_anchor)
		vp.scene.append_to_title("\n")

		""" Change execution speed """
		vp.slider(
			value=self.settings.physics.rate,
			min=10, max=300, length=300,
			pos=vp.scene.title_anchor,
			bind=self.sldSpeed)
		self.widgets.dv = vp.wtext(
			text="Ejecuciones por segundo: "+str(int(self.settings.physics.rate)),
			pos=vp.scene.title_anchor)

	""" FUNCTIONS """
	def move_particle(self, p):
		""" Move particle by its own speed
		params:
			* p: light particles
		"""
		_x = round(p.pos.x + p.speed.x, 6)
		p.pos.x = _x
		_y = round(p.pos.y + p.speed.y, 6)
		p.pos.y = _y
		p.pos.z = round(p.pos.z + p.speed.z, 6)
		p.traveled = round(p.traveled + vp.sqrt(_x**2 + _y**2), 6)

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

			# Resultant particle
			if p.resultant: return

			# Split beam
			if p.speed.x >= 0 and p.speed.y >= 0 and not p.semiparticle:
				# Generate 2 particles with same id
				p1 = copy_particle(p, speed_x=p.speed.x, speed_y=p.speed.y)
				p2 = copy_particle(p, speed_x=p.speed.y, speed_y=-p.speed.x)
				self.beam.append(p1)
				self.beam.append(p2)
				self.delete_particle(p)
				return

			# Semiparticles collision
			if p.semiparticle and (p.speed.x < 0 or p.speed.y > 0):
				# Get semiparticles with same ID and same pos
				particles = [_p for _p in self.beam if _p.semiparticle and _p.pos == p.pos and _p.id == p.id and (_p.speed.x < 0 or _p.speed.y > 0)]

				# No collision
				if len(particles) < 2:
					# Set speed straight up
					p.speed.y = max(abs(p.speed.x), abs(p.speed.y))
					p.speed.x = 0
					p.color = self.cl.green
					p.resultant = True
				else:
					# Collision
					# and _p.pk != p.pk

					# Calc new _p id
					sum_id = p.yx
					sum_id = [sum_id+(_p.yx if _p.pk != p.pk else 0) for _p in particles][-1]

					# Create resultant particle
					pr = copy_particle(p, speed_x=0, speed_y=max(abs(p.speed.x), abs(p.speed.y)), result=True)
					pr.yx = sum_id
					self.beam.append(pr)

					# Delete semiparticles
					[self.delete_particle(_p) for _p in particles]
				return

			# Prevent instant collision when generated
			if p.semiparticle: return

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
			self.pattern[p.id] += p.yx

		# Delete particle when it heads towards light origen (no more compute needed)
		p.visible = False
		self.to_delete.append(p)

	def delete_particles(self):
		for _p in self.to_delete:
			try: self.beam.remove(_p) # Remove particle from beam
			except: pass
			del(_p) # Free memory
		self.to_delete = list()

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
			if not self.playing: continue

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
			#if self.settings.physics.t < 150:
			if len(self.beam) < 800:
				self.beam += laserbeam(
					self.settings.objects.laserengine.x\
					+self.settings.objects.laserengine.length,
					self.settings.objects.laserengine.y,
					self.settings.physics.number_of_particles,
					self.settings.physics.dv,
					self.wavelike and self.settings.physics.t)

			# Delete particles
			self.delete_particles()

			# Print pattern as 2D
			print("pattern: %s"%self.pattern)
			#self.print_2dpattern(self.pattern)
