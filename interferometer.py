""" MICHELSON INTERFEROMETER """

import vpython as vp
import random as rand
import datetime as dt
from drawings import table, laserbeam, laserengine, beamsplitter, mirror ,wood

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


""" FUNCTIONS """
def move_particle(p):
	""" Move particle by its own speed
	params:
		* p: light particles
	"""
	p.pos.x = round(p.pos.x + p.speed.x, 3)
	p.pos.y = round(p.pos.y + p.speed.y, 3)
	p.pos.z = round(p.pos.z + p.speed.z, 3)

def compute_collision(wall, p, walltype):
	""" compute_collision
	* check if given particle collision with given wall
	params:
		* wall: object to collision with (box object)
		* p: light particle (sphere object)
	"""
	# Check if there is collision
	#print("-------------")
	#print("x: %s"%p.pos.x)
	#print("y: %s"%p.pos.y)
	#print("calc y: %s"%wall.calc_y(p.pos.x))
	if wall.calc_y(p.pos.x) == p.pos.y:
		# If walltype is beamsplitter: odds of ignoring collision is 50%
		if walltype == "beamsplitter":
			if bool( rand.randint(0, 1) ): return

		# Update speed vector
		mag = vp.mag(p.speed) # Get magnitude (abs of vector)
		rad = beamsplitter_angle*vp.pi/180
		p.speed.x = round( mag*( vp.cos(rad)**2 - vp.sin(rad)**2 ) , 3)
		p.speed.y = round( 2*mag*vp.sin(rad)*vp.cos(rad) , 3)


""" DATA """
laserengine_x = -45
laserengine_y = 0
laserengine_length = 10
beamsplitter_x = 0
beamsplitter_y = 0
beamsplitter_length = 10
mirror1_x = 30
mirror1_y = -10
mirror1_length = 10
mirror2_x = 0
mirror2_y = -30
mirror2_length = 10
receptor_x = 0
receptor_y = 30
receptor_length = 10

# Physics Parameters
t = 0 # Init time
rate = 2000 # Ratio of execution per second
step = 1000/rate # Time differential (miliseconds)
dv = vc(0.25, 0, 0) # light particle's movement speed
""" dv
* this value should be half the value of step in laserbeam function
"""
beamsplitter_angle = 45
number_of_particles = 10


""" EXECUTE """
# Objects list
beam = list()

# Objects
table(100, 100, vc(.9, .9, .9))
engine = laserengine(laserengine_x, laserengine_y, laserengine_length, cl.black)
splitter = beamsplitter(beamsplitter_x, beamsplitter_y, beamsplitter_length, beamsplitter_angle)
beam += laserbeam(laserengine_x+laserengine_length, laserengine_y, number_of_particles, dv)
# Mirror 1 (right)
mirror1 = None
# Mirror 2 (bottom)
mirror2 = None
# Receptor (top)
receptor = None

mirror1= mirror(mirror1_x,mirror1_y,mirror1_l,mirror1_g)
mirror2= mirror(mirror2_x,mirror2_y,mirror2_l,mirror2_g)
madera1= wood(30.5,0,10,1)
madera2= wood(0,-30.5,1,10)


# Render loop
while True:
	vp.rate(rate) # Pause for time differential
	t += step

	# Compute from cods
	for p in beam:
		# Collision with BeamSplitter
		if True \
			and p.pos.x >= (beamsplitter_x-beamsplitter_length/2) \
			and p.pos.y >= (beamsplitter_y-beamsplitter_length/2) \
			and p.pos.x <= (beamsplitter_x+beamsplitter_length/2) \
			and p.pos.y <= (beamsplitter_y+beamsplitter_length/2) :
			compute_collision(splitter, p, "beamsplitter")
		# Collision with Mirror1 (right)
		if True \
			and p.pos.x == (mirror1_x) \
			and p.pos.y >= (mirror1_y-mirror1_length/2) \
			and p.pos.y <= (mirror1_y+mirror1_length/2) :
			#compute_collision(mirror1, p, "mirror")
			pass
		# Collision with Mirror2
		if True \
			and p.pos.y == (mirror2_y)\
			and p.pos.x >= (mirror2_x-mirror2_length/2) \
			and p.pos.x <= (mirror2_x+mirror2_length/2):
			#compute_collision(mirror2, p, "mirror")
			pass
		# Collision with Receptor
		if True \
			and p.pos.y == (receptor_y)\
			and p.pos.x >= (receptor_x-receptor_length/2) \
			and p.pos.x <= (receptor_x+receptor_length/2):
			compute_collision(receptor, p, "receptor")

		# Move particle
		move_particle(p)
		print(p.pos.x, p.pos.y)

	# Fire new laserbeam
	beam +=  laserbeam(laserengine_x+laserengine_length, laserengine_y, number_of_particles, dv)
	print(len(beam))
