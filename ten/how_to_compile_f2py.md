# Como compilar

Para todas las compilaciones, vamos a suponer que estamos parados en la raíz del repositorio.


Compilando el modulo random

	$ cd ten/random
	$ f2py3 -c generator.f90 -m generator


Compilando los mecanismos de transferencia

	$ cd ten/mechanisms
	# crear un objeto de la subrutina de random
	$ gfortran -c -fPIC -O3 ../random/generator.f90 -o generator.o
	# linkeo y creo el objeto para llamar desde python
	$ f2py -c --fcompiler=gfortran -I. generator.o -m forster_mecha forster_mecha.f90
