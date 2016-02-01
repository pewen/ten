=======
Install
=======

Instructions for install TEN

.. contents:: Contents
   :local:

Requirements
============

You need to have the following software properly installed in order to
run **TEN**:

* Python 2.7, 3.2 or above.
* `Pip`_
* A working MPI implementation, preferably supporting MPI-3 and built with shared/dynamic libraries (ex. `OpenMPI`_)

.. $ apt-get install openmpi-bin openmpi-common openmpi-doc libopenmpi-dev autoconf

The other depence (Numpy, MPI4Py and Matplotlib) are going to install via pip.

.. _Pip: https://pypi.python.org/pypi/pip/
.. _OpenMPI: https://www.open-mpi.org/

Install TEN
===========

The easiest way to install TEN is using pip:
::
   
    pip install -U ten

But also, you can get the last version from the sourcce code repo:

::

    cd ~
    git clon https://github.com/pewen/ten.git
    cd ten
    python setup.py install
