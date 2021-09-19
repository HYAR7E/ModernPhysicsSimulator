import sys
from interferometer import Interferometer


if __name__ == '__main__':
	""" This will execute only when called by CLI """

	if len(sys.argv) < 2:
		# print menu and select simulator
		call_to = "interferometer"
	elif len(sys.argv):
		call_to = sys.argv[1]

	# Execute simulator
	if call_to == "interferometer":
		if len(sys.argv) > 2:
			it = Interferometer(beamtype=sys.argv[2])
		else:
			it = Interferometer()
		it.execute()
	else:
		print("Simulator not supported")

	""" Egs:
	* python3 main.py interferometer
	* python3 main.py interferometer wave
	"""


""" TODO
* Particle's traveled distance
* Wave behaviour calcs (wave sum by traveled distance)
* Show interference pattern in screen
* Move mirror (L1 ^ L2)
"""
