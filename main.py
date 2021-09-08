import vpython as vp
from interferometer import *

# Alias a funciones
vc = vp.vector
cl = vp.color

# Establecer configuracion inicial
vp.scene.width = 1500
vp.scene.height = 750
vp.scene.autoscale = False
vp.scene.userspin = False
vp.scene.userpan = False
vp.scene.background = vc(.7, .7, .7)
vp.scene.camera.pos = vc(0, 0, 30)

# Parametros
t = 0 # Tiempo inicial
dt = 100 # Diferencial de tiempo (en milisegundos)
dv = vc(0.2, 0, 0) # Velocidad de movimiento de particulas de luz

# Objetos
vp.box(pos=vc(0, 0, -2), size=vc(50, 50, 1), color=vc(.9, .9, .9))
beam = laser(0, 0, 0, 8)

# Procesar mediante iterador
while t<10000:
	vp.rate(dt) # Pausar por dt
	t += dt # Incrementar dt a t

	# Compute
	move_beam(beam, dv)
	print(t)
