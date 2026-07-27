all: plot-const

plot-const:
	gcc plot-const.c svg.c -o plot-const -lm
clean:
	-rm -f ./plot-const.exe
	-rm -f ./plot-const
	-rm -f svg/*
	-rmdir svg
	-mkdir svg