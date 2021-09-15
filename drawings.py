import vpython as vp

# Set alias to ease usability
vc = vp.vector
cl = vp.color

def table(x, y, c):
	vp.box(pos=vc(0, 0, -2), size=vc(x, y, 1), color=c)

def laserbeam(x, y, n, speed):
	""" Print a laserbeam iteration
		* print a "group" of light particles piled up onto the Y axis
	params:
		* x: X axis
		* y: Y axis
		* n: number of light particles to be generated into the beam
	"""
	# Validate n have to be at least 2
	if n < 1: return

	# Define step longitude
	step = 0.5
	odd = n%2!=0 # n is odd?
	# Set start coordinate as Y (Y axis)
	start = y
	# Update start coordinate according to n and if n is odd or not
	if odd: start += -step*(n//2)
	else: start += (1-n)*step/2
	start = round(start, 3)
	# Iterate in n range
	beam = list() # list to contain light particles
	for i in range(1, n+1):
		# Generate sphere (light particle)
		p = vp.sphere(pos=vc(x, start, 0), radius=step/2, color=cl.red)
		p.id = i
		p.speed = vc(speed.x, speed.y, speed.z)
		beam.append(p) # Add sphere to beam list
		start = round(start + step, 3) # Iterate start (y axis) with step
	# Return beam (list of light particles)
	return beam

def laserengine(x, y, l, c):
	""" Print laser engine
	params:
		* x: X axis
		* y: Y axis
		* c: color
	"""
	vl_length = l
	vl_l1_length = vl_length*.9
	vl_l2_length = vl_length*.1
	vp.cylinder(
		pos=vc(x, y, 0),
		axis=vc(vl_l1_length, 0, 0),
		radius=2,
		color=cl.black)
	vp.cylinder(
		pos=vc(x+vl_l1_length, y, 0),
		axis=vc(vl_l2_length, 0, 0),
		radius=1,
		texture=vp.textures.metal)

def beamsplitter(x, y, l, angle):
	""" Print beam splitter
	params:
		* x: X axis
		* y: Y axis
		* angle: inclination angle (from +X axis) (360)
	"""
	rad = angle*vp.pi/180
	splitter = vp.box(
		pos=vc(x, y, 0),
		size=vc(1, l, 1),
		up=vc(vp.cos(rad), vp.sin(rad), 0),
		color=cl.white)
	splitter.calc_y = lambda _x: round((_x - x)*vp.tan(rad) + y, 3)
	splitter.angle = rad
	return splitter

def beamreceptorengine(x, y, l, angle):
	""" Print beam receptor
	params:
		* x: X axis
		* y: Y axis
		* w: width
	"""
	rad = angle*vp.pi/180
	beamreceptor = vp.box(
		pos=vc(x, y, 0),
		size=vc(2, l, 0),
		up=vc(vp.cos(rad), vp.sin(rad), 0),
		texture="https://i.imgur.com/Ijy9Yqs.png")
	beamreceptor.calc_y = None
	beamreceptor.angle = rad
	return beamreceptor

def mirror(x, y, l, angle):
	rad = angle*vp.pi/180
	mirror =  vp.box(
		pos=vc(x, y, 0),
		size=vc(1, l, 0),
		up=vc(vp.cos(rad), vp.sin(rad), 0),
		color=cl.white)
	mirror.calc_y = None
	mirror.angle = rad
	return mirror
