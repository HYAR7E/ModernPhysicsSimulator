import vpython as vp

# Set alias to ease usability
vc = vp.vector
cl = vp.color

def x_table(x, y, c):
	return vp.box(pos=vc(0, 0, -2), size=vc(x, y, 1), color=c)

def x_laserengine(x, y, l, c):
	""" Print laser engine
	params:
		* x: X axis
		* y: Y axis
		* c: color
	"""
	vl_length = l
	vl_l1_length = vl_length*.9
	vl_l2_length = vl_length*.1
	laserengine = vp.cylinder(
		pos=vc(x, y, 0),
		axis=vc(vl_l1_length, 0, 0),
		radius=2,
		color=cl.black)
	vp.cylinder(
		pos=vc(x+vl_l1_length, y, 0),
		axis=vc(vl_l2_length, 0, 0),
		radius=1,
		texture=vp.textures.metal)
	return laserengine

def x_beamsplitter(x, y, l, angle):
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

def x_beamreceptor(x, y, l, angle):
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

def x_mirror(x, y, l, angle):
	rad = angle*vp.pi/180
	mirror =  vp.box(
		pos=vc(x, y, 0),
		size=vc(1, l, 0),
		up=vc(vp.cos(rad), vp.sin(rad), 0),
		color=cl.cyan)
	mirror.calc_y = None
	mirror.angle = rad
	return mirror

def laserbeam(x, y, n, speed, order=False):
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
	start = round(start - step, 3)
	# Iterate in n range
	beam = list() # list to contain light particles
	for i in range(0, n):
		start = round(start + step, 3) # Iterate start (y axis) with step

		# Wave like behaviour
		if order is not False:
			if order//n%2 == 1:
				if i != (n-1) - order%n: continue
			elif i != order%n: continue

		# Generate sphere (light particle)
		p = vp.sphere(pos=vc(x, start, 0), radius=step/2, color=cl.red)
		p.id = i
		p.speed = vc(speed.x, speed.y, speed.z)
		beam.append(p) # Add sphere to beam list
	# Return beam (list of light particles)
	return beam

def indicator(x, y, h, w, n):
	bar = vp.shapes.rectangle(width=w, height=h, thickness=0.05, roundness=0.1)
	GH = vp.extrusion(path=[vp.vec(0,0,0), vp.vec(0,0,-0.1)], color=vp.color.red, pos=vp.vector(x, y, 2), shape=bar)
	for i in range(-3, round(w/2),round(w/3) ):
		column = vp.shapes.rectangle(width=0.5, height=h-2, roundness=0.1) 
		vp.extrusion(path=[vp.vec(0,0,0), vp.vec(0,0,-0.1)], color=vp.color.black, pos=vp.vector(x+i, y,2), shape=column)
	#vp.text(pos=GH.pos-vp.vector(w/3,0,0), text='∆x', align='center', height=2, depth=0, color=vp.color.blue)
	vp.text(pos=vp.vec(x-(w/3),y+(h/3)-3,5), text='∆x', align='center', height=2, depth=0, color=vp.color.blue)
	vp.text(pos=vp.vec(x,y+(h/3)-3,5), text='N', align='center', height=2, depth=0, color=vp.color.blue)
	vp.text(pos=vp.vec(x+(w/3),y+(h/3)-3,5), text='λ', align='center', height=2, depth=0, color=vp.color.blue)

def data(x,y,w,h,n):
	for i in range(2,n*2+3,2):
		number=str(round(i/2))
		vp.text(pos=vp.vec(x,y+(h/3)-i-2,2), text=number, align='center', height=1.5, depth=0, color=vp.color.black)
