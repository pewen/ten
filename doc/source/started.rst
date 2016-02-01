===============
Getting Started
===============

.. contents:: Contents
   :local:

TEN in Command-line
===================

Typically you should put the input parameters of the simulations in an input file and call TEN from the comand line interface (cli):

::
    
    ten --config experiment.conf

This section describes how input parameters are structured and what commands they contain.

You can test TEN on any of the sample inputs provided in the examples directory. Input scripts are named *.conf
Here is how you might run a example on a Linux, using mpirun to launch a parallel job:

.. and sample outputs are named log.*.name.P where name is a machine and P is the number of processors it was run on.

::
   
    cd ~
    git clone https://github.com/pewen/ten.git
    cd ten/examples
    mpirun -np 4 ten --config example.conf

Command-line options
====================

TEN recognizes several optional command-line switches which may be used in any order. Either the full word or a one letter abbreviation can be used:

* -h, --help            
* -c CONFIG, --config
* -o
* -v
* -q

Here are the details on the options:

::
   
    -h, --help

Print a brief help summary. TEN will print the info and immediately exit if this switch is used.

::
   
    -c, --config

Path to the file with the initials parameters. If it is not specified, TEN use the *experiment.conf* only if this file exist in your current directory.

::
   
    -o

Path where save the output of the simulation. By default, TEN save the output file in the directory where you are.

::
   
    -v

Verborse
    
::
   
    -q

Only print the errors in the console.

TEN as library
==============

Also, you can use TEN as a library. You only need open a python interpreter and make an import:

::

    import ten

And now you can make test or simulations directly in a python console.
