#!/bin/bash
# This script is meant to be called by the "install" step defined in
# .travis.yml. See http://docs.travis-ci.com/ for more details.
# The behavior of the script is controlled by environment variabled defined
# in the .travis.yml in the top level folder of the project.

# License: 3-clause BSD

# This install in based in scikit-learn install[1] and conda tutorial[2]
# [ 1 ] https://github.com/scikit-learn/scikit-learn/blob/master/build_tools/travis/install.sh
# [ 2 ] http://conda.pydata.org/docs/travis.html

sudo apt-get update
sudo apt-get install gfortran

# We do this conditionally because it saves us some downloading if the
# version is the same.
if [[ "$TRAVIS_PYTHON_VERSION" == "2.7" ]]; then
    wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -O miniconda.sh;
else
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh;
fi

bash miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
hash -r

# Set yes as default in conda
conda config --set always_yes yes --set changeps1 no
conda update -q conda
# Useful for debugging any issues with conda
conda info -a

# Install the dependencies
conda create -q -n test-environment python=$TRAVIS_PYTHON_VERSION pip numpy pytest pytest-cov
#pip install python-coveralls coverage

# Install TEN
source activate test-environment
python setup.py install

# Compile fortran dependencies
cd ten/random
f2py -c generator.f90 -m generator

cd ../mechanisms
gfortran -c -fPIC -O3 ../random/generator.f90 -o generator.o
f2py -c --fcompiler=gfortran -I. generator.o -m forster_mecha forster_mecha.f90

cd ../..
