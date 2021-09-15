""" MICHELSON INTERFEROMETER """

import vpython as vp
import random as rand
import datetime as dt
from drawings import table, laserbeam, laserengine, beamsplitter, beamreceptorengine, mirror

# Set alias to ease usability
vc = vp.vector
cl = vp.color

# Set library configuration
vp.scene.width = 1500
vp.scene.height = 750
vp.scene.autoscale = False
#vp.scene.userspin = False
#vp.scene.userpan = False
vp.scene.background = vc(.7, .7, .7)
vp.scene.camera.pos = vc(0, 0, 70)


""" DATA """
laserengine_x = -45
laserengine_y = 0
laserengine_length = 10
beamsplitter_x = 0
beamsplitter_y = 0
beamsplitter_length = 10
mirror1_x = 30
mirror1_y = 0
mirror2_x = 0
mirror2_y = -30
mirror_length = 10
receptor_x = 0
receptor_y = 30
receptor_length = 10

# Physics Parameters
t = 0 # Init time (miliseconds)
rate = 200 # Ratio of execution per second
step = 1000/rate # Time differential (miliseconds)
dv = vc(0.25, 0, 0) # light particle's movement speed
""" dv
* this value should be half the value of step in laserbeam function
"""
beamsplitter_angle = 45
number_of_particles = 10


""" FUNCTIONS """
def move_particle(p):
	""" Move particle by its own speed
	params:
		* p: light particles
	"""
	p.pos.x = round(p.pos.x + p.speed.x, 3)
	p.pos.y = round(p.pos.y + p.speed.y, 3)
	p.pos.z = round(p.pos.z + p.speed.z, 3)

def beamsplitter_collision(bs, p):
	""" compute_collision
	* check if given particle collision with beamsplitter
	params:
		* bs: beamsplitter (box object)
		* p: light particle (sphere object)
	"""
	# Check if there is collision
	if bs.calc_y(p.pos.x) == p.pos.y:
		if bool( rand.randint(0, 1) ): return

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

def compute_collision(wall, p, walltype):
	""" compute_collision
	* check if given particle collision with given wall
	params:
		* wall: object to collision with (box object)
		* p: light particle (sphere object)
	"""
	# Check if there is collision
	if not wall.calc_y or wall.calc_y(p.pos.x) == p.pos.y:
		# If walltype is receptor: remove point
		if walltype == "receptor":
			p.visible = False
			beam.remove(p) # Remove particle from beam
			del(p) # Free memory
			return

		# Update speed vector
		rad = wall.angle
		mag = vp.mag(p.speed) # Get magnitude (abs of vector)

		# Horizontal bounces
		if walltype == "mirror2" or walltype == "receptor":
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


""" INITIALIZE VARS """
# Objects list
beam = list()

# Objects
table(100, 100, vc(.9, .9, .9))
engine = laserengine(laserengine_x, laserengine_y, laserengine_length, cl.black)
splitter = beamsplitter(beamsplitter_x, beamsplitter_y, beamsplitter_length, beamsplitter_angle)
beam += laserbeam(laserengine_x+laserengine_length, laserengine_y, number_of_particles, dv)
# Mirror 1 (right)
mirror1 = mirror(mirror1_x, mirror1_y, mirror_length, 90)
# Mirror 2 (bottom)
mirror2 = mirror(mirror2_x, mirror2_y, mirror_length, 0)
# Receptor (top)
receptor = beamreceptorengine(receptor_x, receptor_y, receptor_length, 0)


""" EXECUTE """
# Render loop
while True:
	vp.rate(rate) # Pause
	t += 1

	# Compute from cods
	for p in beam:
		# Collision with BeamSplitter
		if True \
			and p.pos.x >= (beamsplitter_x-beamsplitter_length/2) \
			and p.pos.y >= (beamsplitter_y-beamsplitter_length/2) \
			and p.pos.x <= (beamsplitter_x+beamsplitter_length/2) \
			and p.pos.y <= (beamsplitter_y+beamsplitter_length/2) :
			beamsplitter_collision(splitter, p)

		# Collision with Mirror1 (right)
		if True \
			and p.pos.x == (mirror1_x) \
			and p.pos.y >= (mirror1_y-mirror_length/2) \
			and p.pos.y <= (mirror1_y+mirror_length/2) :
			compute_collision(mirror1, p, "mirror1")

		# Collision with Mirror2
		if True \
			and p.pos.y == (mirror2_y) \
			and p.pos.x >= (mirror2_x-mirror_length/2) \
			and p.pos.x <= (mirror2_x+mirror_length/2) :
			compute_collision(mirror2, p, "mirror2")

		# Collision with Receptor
		if True \
			and p.pos.y >= (receptor_y) \
			and p.pos.x >= (receptor_x-receptor_length/2) \
			and p.pos.x <= (receptor_x+receptor_length/2) :
			compute_collision(receptor, p, "receptor")

		# Out of field
		if False \
			or p.pos.x > mirror1_x \
			or p.pos.x < (laserengine_x+laserengine_length) \
			or p.pos.y < mirror2_y \
			or p.pos.y > receptor_y :
			p.visible = False
			beam.remove(p) # Remove particle from beam
			del(p) # Free memory
			continue

		# Move particle
		move_particle(p)

	# Fire new laserbeam
	if t < 40:
		beam += laserbeam(laserengine_x+laserengine_length, laserengine_y, number_of_particles, dv)
	print(len(beam))
