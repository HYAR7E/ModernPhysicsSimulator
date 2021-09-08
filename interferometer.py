import vpython as vp

# Alias a funciones
vc = vp.vector
cl = vp.color

# Funciones
def laser(x, y, z, n, s=.1):
	if n < 1: return
	step = .05
	odd = n%2!=0
	# Obtener coordenadas de inicio de impresion
	start = y
	if odd: start += -step*(n//2)
	else: start += (1-n)*step/2
	# Iterar cada punto de luz
	beam = list()
	for i in range(1, n+1):
		p = vp.sphere(pos=vc(x, start, z), radius=s, color=cl.red, make_trail=True)
		beam.append(p)
		start += step
	return beam

def move_beam(beam, dv):
	for b in beam: b.pos += dv