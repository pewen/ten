============
Introduction
============

This section provides an overview of what TEN can do.

.. contents:: Contents
   :local:

What is TEN?
============

Collection of algorithms to simulate, using Monte Carlo method, the quantum process of Energy Transfer in Nanoparticles (TEN for its acronym in Spanish) in conjugated polymers written in Python. With TEN we can calcule values like Quenching efficiency, plot the efficiency vs number of acceptors and much more.

TEN runs efficiently on single-processor machines, but is designed for parallel computers. It will run on any parallel machine that have Python and supports the MPI message-passing library.

TEN is a freely-available open-source code, distributed under the terms of the `MIT Licence`_.

It was developed at Laboratory of Advanced Optical Microscopy, Universidad Nacional de Río Cuarto, Argentina. It is an open-source code, distributed freely under the terms of the MIT License.

.. _MIT Licence: http://opensource.org/licenses/MIT

TEN features
============

Basic features

General features
----------------

* Runs on a single processor or in parallel
* Distributed-memory message-passing parallelism (MPI)
* open-source distribution
* All the code is written in Python
* Easy to extend with new features and functionality
* Runs on the cli from an input script
* Build as library, you can :code:`import TEN`

Nanoparticle model
------------------

* Nanoparticle object easy to import :code:`from TEN import NanoParticle`
* Can deposit acceptors superficial
* Or can deposit acceptors volumetrically

Exiton model
------------
* Easy to import
* Can be generate from a laser
* Or can be generate from a chemical electrolysis
* The ranmdom walk does not have a preferred direction, it moves on the surface of a sphere of radius equal to the step

Simulation
----------
* Calculation of quenching
* Calculation of the exciton difusion length (with or without exciton)
* Calculation of :math:`\tau_{D}`

Output
------
* Input parameters
* By number of acceptors, the amount of naturally fallen and transferred

  
Acknowledgments
===============
