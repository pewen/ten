#!/bin/bash

cd ten/random
f2py3 -c generator.f90 -m generator

cd ../mechanisms
gfortran -c -fPIC -O3 ../random/generator.f90 -o generator.o
f2py3 -c --fcompiler=gfortran -I. generator.o -m forster_mecha forster_mecha.f90
