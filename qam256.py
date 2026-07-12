# Python3
# Nino Carrillo
# 7 Jun 26

import sys
import matplotlib.pyplot as plt
import numpy as np

def genQAM():
	constellation = np.zeros((2,256))
	step = np.sqrt(2)/30
	# row 1
	y = step * 15
	x = -step * 15
	point = 0
	for j in range (16):
		for i in range(16):
			constellation[0][point] = x
			constellation[1][point] = y
			point += 1
			x += (step * 2)
		# row 2
		y -= 2*step
		x = -step * 15
	return constellation

def genDemap(constellation, shift):
	map_dim = np.power(2,16-shift)
	div = np.power(2,shift)
	const_count = len(constellation[0])
	demap = np.zeros(map_dim*map_dim)
	distances = np.zeros(const_count)
	ii = 0
	for y in range(-map_dim//2, map_dim//2):
		for x in range(-map_dim//2, map_dim//2):
			# determine the closest constellation point to this map point
			for i in range(const_count):
				x_c = constellation[0][i] / div
				y_c = constellation[1][i] / div
				distances[i] = np.sqrt(np.power(x-x_c,2) + np.power(y-y_c,2))
			demap[ii] = int(np.argmin(distances))
			ii += 1
	return demap

def genDemapTable(demap, row_size):
	print(f'\r\nconst int16_t Demap[{len(demap)}] = {{ \\')
	i = 0;
	for y in range(row_size):
		print(f'   /* {i:^5} */ ', end='')
		for x in range(row_size):
			print(f'{int(demap[i])}, ', end='')
			i += 1
		print(f' \\\r\n', end='')
	print(f'}};')
	return

def genConstTable(constellation):
	print(f'\r\nconst uint8_t Constellation[{len(constellation[0])*2}] = {{ \\')
	for i in range(len(constellation[0])):
		print(f'   /* {i:^5} */ ', end='')
		print(f'{int(constellation[0][i])},', end='')
		print(f'{int(constellation[1][i])}, \\\r\n', end='')
	print(f'}};')
	return

def main():
	# check correct version of Python
	if sys.version_info < (3, 0):
		print("Python version should be 3.x, exiting")
		sys.exit(1)

	constellation = genQAM()
	# scale constellation to int16_t
	constellation = constellation * 32768

	shift_bits = 10

	# create a decode map
	demap = genDemap(constellation, shift_bits)

	plt.figure()
	plt.scatter(constellation[0],constellation[1])
	plt.show()

	genConstTable(constellation)
	genDemapTable(demap, np.power(2,16-shift_bits))

	print('\r\nDone.\r\n')

if __name__ == "__main__":
	main()