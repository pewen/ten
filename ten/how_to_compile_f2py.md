# Como compilar

Compilando el modulo random

	$ cd utils
	$ f2py3 -c random.f90 -m random


Compilando los mecanismos de transferencia

	# desde la raíz de TEN
	$ cd ten/experiments
	# crear un objeto de la subrutina de random
	$ gfortran -c -fPIC -O3 ../utils/random.f90 -o random.o
	# linkeo y creo el objeto para llamar desde python
	$ f2py -c --fcompiler=gfortran -I. random.o -m forster_mecha forster_mecha.f90
