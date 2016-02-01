================
Input Parameters
================

This section describes the parameters of the input file used to define a TEN simulation

.. contents:: Contents
   :local:

TEN input file
==============

When you run TEN from the command-line, the first thing is to read and parsing the entire input file. So, no matter the order of the parameters in the file.


Parsing rules
=============

Each non-blank line in the input file is treated as a parameter. TEN parameters are case sensitive. The input file must have only one parameter per line.

All characters from the  *#* character to the end of the line are treated as comment and discarded. Also, all the lines between *"""* and other *"""* are a block of comment.

NP Parameters
=============

::
       
    r_mean : float

Mean of the normal distribution nanoparticle radius. [r] = nm

::
   
    r_deviation float, optional

Standard deviation of the normal distribution nanoparticle radius. if not, the radius is considered constant. [r] = nm
    
::

    R_Forster : float

Forster radius. [R_Forster] = nm

::

    mean_path : float

Mean free path. [mean_path] = nm

::

    tau_D : float

Lifetime of donor. [tau_D] = ns

::
   
    epsilon : float

Size of the random walk [epsilon] = nm

::
   
    acceptors : str

Way to create the acceptors. Can be 'vol' (volumetrically) for uniform distribution inside of nanoparticle or 'sup' (superficialy) for uniform distributions on the surface of the nanoparticle.

Experiment Parameters
=====================

::
   
    exiton : str
    
Way to create the exiton. Can be 'laser' to generate uniformily in the nanoparticle or 'elec' (electrolysis) to generate between the radius R of the nanoparticle and a r (R > r).
    
::
   
    r_electro : float, optional

In a chemical electrolysis, the exiton position is generated between the radius R of the nanoparticle and a radius r (r<R), where r depends electrolysis.


Simulation Parameters
=====================
::
   
    num_acceptors_min : int, optional

Minimum number of acceptores to simulate. Default value = 1
    
::
   
    num_acceptors_max : int
   
Maximum number of acceptores to simulate.
    
::
   
    acceptors_step : int

Step number of acceptores.

::

    num_exc : int

Numbers of exitation of the same nanoparticle.
