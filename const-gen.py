# Python3
# Nino Carrillo
# 7 Jun 26

import sys
import matplotlib.pyplot as plt
import numpy as np

def genQAM32():
	constellation = np.zeros((2,32))
	step = np.sqrt(2)/10
	# row 1
	y = step * 5
	x = -step * 3
	point = 0
	for i in range(4):
		constellation[0][point] = x
		constellation[1][point] = y
		point += 1
		x += (step * 2)
	# row 2
	y = step * 3
	x = -step * 5
	for i in range(6):
		constellation[0][point] = x
		constellation[1][point] = y
		point += 1
		x += (step * 2)
	# row 3
	y = step
	x = -step * 5
	for i in range(6):
		constellation[0][point] = x
		constellation[1][point] = y
		point += 1
		x += (step * 2)
	# row 4
	y = -step
	x = -step * 5
	for i in range(6):
		constellation[0][point] = x
		constellation[1][point] = y
		point += 1
		x += (step * 2)
	# row 5
	y = -step * 3
	x = -step * 5
	for i in range(6):
		constellation[0][point] = x
		constellation[1][point] = y
		point += 1
		x += (step * 2)
	# row 6
	y = -step * 5
	x = -step * 3
	for i in range(4):
		constellation[0][point] = x
		constellation[1][point] = y
		point += 1
		x += (step * 2)
	return constellation

def genDemap(constellation, map_dim, shift):
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
	print(f'\r\nconst int16_t Constellation[{len(constellation[0])*2}] = {{ \\')
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

	constellation = genQAM32()
	# scale constellation to int16_t
	constellation = constellation * 32768

	# create a decode map
	demap = genDemap(constellation, 32, 11)
	for y in range(32):
		print(f'\r\n', end='')
		for x in range(32):
			i = int(x + (y * 32))
			print(f'{int(demap[i]):>3}', end='')

	plt.figure()
	plt.scatter(constellation[0],constellation[1])
	plt.grid(True)
	plt.show()

	genConstTable(constellation)
	genDemapTable(demap, 32)
	
	# Compute the average energy of this constellation:
	energy = 0;
	for i in range(len(constellation[0])):
		energy += np.sqrt(np.power(constellation[0][i]/32768, 2) + np.power(constellation[1][i]/32768, 2))
	energy = energy / 32
	print(f'Constellation energy: {energy}\r\n');
	correction = 1/energy
	print(f'Constellation time domain int16_t gain correction: {int(correction * 32768)}\r\n');
	constellation*= correction
	energy = 0;
	for i in range(len(constellation[0])):
		energy += np.sqrt(np.power(constellation[0][i]/32768, 2) + np.power(constellation[1][i]/32768, 2))
	energy = energy / 32
	print(f'Corrected Constellation energy: {energy}\r\n');
	
	print('\r\nDone.\r\n')

if __name__ == "__main__":
	main()