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
		it = Interferometer()
		it.execute()
	else:
		print("Simulator not supported")


""" TODO
* constant supply of light
* Show interference pattern in screen
"""
