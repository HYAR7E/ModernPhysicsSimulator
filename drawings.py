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
		p.pk = order
		p.yx = vp.ceil(i-n/2)
		p.traveled = 0
		p.semiparticle = False
		p.resultant = False
		p.speed = vc(speed.x, speed.y, speed.z)
		beam.append(p) # Add sphere to beam list
	# Return beam (list of light particles)
	return beam

def copy_particle(_p, speed_x=0, speed_y=0, speed_z=0, result=False):
	_color = cl.red if result else cl.blue
	#_color = [cl.blue, cl.green, cl.black, cl.purple, cl.white][_p.id]
	p = vp.sphere(pos=vc(_p.pos.x, _p.pos.y, _p.pos.z), radius=0.5/2, color=_color) # semi particle color
	p.id = _p.id
	p.pk = _p.pk
	p.yx = _p.yx
	p.traveled = _p.traveled
	p.semiparticle = True
	p.resultant = result
	p.speed = vc(speed_x, speed_y, speed_z)
	return p

def indicator(x,y,r):
	A = [1,1,0,0,1,1]
	n=len(A)
	R=0#--
	for i in range(0,n):
		colors=cl.black
		if A[i]==1:
			colors=cl.white
		splitter = vp.box(
			pos=vc(x+i, y, 50),
			size=vc(1, 1, 1),
			color=colors)#,opacity=0.8)
		R=x+i
		#d/2:radio=R+r
	#r:distancia de de la ultima caja al centro de la circunferencia
	a=[]
	for i in range(2,n+2):
		angle = 0
		shape = .02 #0.9:pentagon
		eje_x=R+(2*r)+i-2
		base = vp.cylinder(
			pos=vc(R+r,y,50), 
			axis=vc(i+r-2,0,0), 
			radius=.02, 
			color=vp.color.white, 
			visible=False)
		girth = vp.curve(
			color=vp.color.orange, 
			radius= .02)
		girth.append(vc(eje_x,y,50))
		a.append(i)
		if A[n-i+1]==1:
			while angle < 2*vp.pi:
				vp.rate(1000)
				base.rotate(
					angle=shape, 
					axis=vc(0,0,1), 
					origin=base.pos) 
				girth.append(base.pos+base.axis)
				angle += shape
				a.insert(i-2,girth)
	vp.sleep(1) # sleep for 1 second
	for g in range(0,n):
		h=a[g]
		#h.clear()
