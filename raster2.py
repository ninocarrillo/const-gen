# Python3
# Nino Carrillo
# 7 Jun 26

import sys
import matplotlib.pyplot as plt
import numpy as np

def genQAM(size, step):
	constellation = np.zeros((2,size))
	# Make a constellation with radial symmetry
	# Work on one quadrant at a time
	x = step // 2
	y = step // 2
	count = 0
	while (count < size // 4) and (y < 32768):
		if (np.abs(x + (y * 1j))  < 32768):
			constellation[0][count] = x
			constellation[1][count] = y
			count += 1
		x += step
		if x > 32767:
			x = step // 2
			y += step
	# Now reflect the constellation quadrants to fill the circle
	# quadrant 2:
	offset = size // 4
	for i in range(size // 4):
		constellation[0][i+offset] = -constellation[0][i]
		constellation[1][i+offset] = constellation[1][i]
		count += 1
	# quadrant 3:
	offset += size // 4
	for i in range(size // 4):
		constellation[0][i+offset] = -constellation[0][i]
		constellation[1][i+offset] = -constellation[1][i]
		count += 1
	# quadrant 4:
	offset += size // 4
	for i in range(size // 4):
		constellation[0][i+offset] = constellation[0][i]
		constellation[1][i+offset] = -constellation[1][i]
		count += 1
	print(f'Count: {count}')
	if count == size:
		print("Good constellation")
	else:
		print("Bad constellation")
	# now sort the constellation into offsets in even and odd
	sorted_constellation = np.zeros((2,size))
	xmin = np.min(constellation[0])
	ymin = np.min(constellation[1])
	print(f'xmin: {xmin} ymin: {ymin}')
	j_even = 0
	j_odd = 1
	for i in range(size):
		# determine absolute row and column
		xrow = int(round((constellation[0][i] - xmin) / step))
		yrow = int(round((constellation[1][i] - ymin) / step))
		print(f'xrow: {xrow} yrow: {yrow}')
		if (xrow % 2) == (yrow % 2):
			# set A, put in even
			sorted_constellation[0][j_even] = constellation[0][i]
			sorted_constellation[1][j_even] = constellation[1][i]
			j_even += 2
		else:
			# set B, put in odd
			sorted_constellation[0][j_odd] = constellation[0][i]
			sorted_constellation[1][j_odd] = constellation[1][i]
			j_odd += 2
	print(f'A Count: {int(j_even/2)}, B Count: {int((j_odd - 1)/2)}')



	return sorted_constellation

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

	if len(sys.argv) < 2:
		print("Not enough arguments. Usage: python3 raster.py <const size> <interval>")
		sys.exit(1)

	const_size = int(sys.argv[1])
	const_intv = int(sys.argv[2])

	constellation = genQAM(const_size, const_intv)

	shift_bits = 10

	# create a decode map
	demap = genDemap(constellation, shift_bits)

	# create a circle
	n = 360
	circle = np.zeros((2,n))
	for i in range(n):
		circle[0][i] = np.cos(i * np.pi / 180) * 32768
		circle[1][i] = np.sin(i * np.pi / 180) * 32768


	even_constellation = [constellation[0][::2],constellation[1][::2]]
	odd_constellation = [constellation[0][1::2],constellation[1][1::2]]

	plt.figure()
	plt.scatter(even_constellation[0], even_constellation[1])
	plt.scatter(odd_constellation[0], odd_constellation[1])
	plt.scatter(circle[0], circle[1], s=1)
	plt.show()

	genConstTable(constellation)
	genDemapTable(demap, np.power(2,16-shift_bits))

	print('\r\nDone.\r\n')

if __name__ == "__main__":
	main()