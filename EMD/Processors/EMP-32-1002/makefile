main.iso: main.c
	test -d build || mkdir build
	test -d dist || mkdir dist
	python compiler.py main.c -o main
	python asm.py main.asm -o main
	python linker.py main.o -o main
