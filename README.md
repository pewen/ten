.. -*- mode: rst -*-

|Travis|_  |Coveralls|_ 

.. |Travis| image:: https://api.travis-ci.org/scikit-learn/scikit-learn.svg?branch=master
.. _Travis: https://travis-ci.org/scikit-learn/scikit-learn

.. |Coveralls| image:: https://coveralls.io/repos/github/pewen/ten/badge.svg?branch=master
.. _Coveralls: https://coveralls.io/github/pewen/ten?branch=master 



# TEN

Colección de algoritmos para simular, usando el método de Monte Carlo, los procesos de Transferencia de Energía en Nanoparticulas (TEN) de polímeros conjugados.
TEN esta diseñado para correr eficientemente en paralelo.

Las simulaciones son contrastadas con las mediciones experimentales realizadas en el Laboratorio de Microscopia Óptica Avanzada (LMOA) de la Universidad Nacional de Río Cuarto (UNRC).

Es desarrollado en por el LMOA, UNRC, Argentina. Es un proyecto open-source, distribuido gratuitamente bajo los términos de la licencia MIT.


## Equipo de trabajo

* Químico **Dr. Rodrigo Palacio**  
* Químico **Dr. Carlos Chesta**  
* Metodología de la investigación **Dra. Dolores Rexachs**  
* GPUs Computing **Manuel Ujaldon**
* Estudiante de Doctorado **Rodrigo Ponsio**  
* Estudiante de Maestría **Daniel Bellomo**  
* Estudiante de Grado (desarrolladores del código) [**Franco Bellomo**](https://github.com/fnbellomo) [@fnbellomo](https://twitter.com/fnbellomo)  
* Estudiante de Grado (desarrolladores del código )[**Lucas Bellomo**](https://github.com/lbellomo) [@ucaomo](https://twitter.com/ucaomo)


## Documentación

La documentación esta disponible en: https://ten.readthedocs.org. Todas las contribuciones son bien venidas.


## Funcionalidades

Existen 3 objetos principales: Nanoparticle, Aceptors y Exiton que nos permiten poder simular a una nanoparticula por completo. Además, TEN cuenta con una serie de experimentos y mecanismos de transferencia de energía implementados.

Experimentos:
* Quenching : calculo de la eficiencia de Quenching.
* Single photon counting : histograma de vida media del exitón.
* tau_d : calculo de la distancia media del exiton.

Mecanismos:
* Forster
* Boolean : El exitón solo se transfiere si esta a menos de cierta distancia de un aceptor.

TEN esta diseñado para aceptar mecanismos de transferencia generados por el usuario.



## Instalación
### Requerimientos

*Core*:
* Python (2.x o 3.x)
* Numpy
* MPI4py
* OpenMPI o MPICH

*Herramientas de post-procesamiento:*
* Matplotlib

### Instalación
TODO setup.py


## Experimento

En la *Fig. 1* se muestran los procesos que intervienen en el experimento, con el objeto de detallar los procesos secuenciales y paralelos (multicore/cluster/GPU).

### Existen dos niveles de paralelismo:

1. Bombardeo de fotones, el punto *3)* de la fig.  
   - Paralelizar en multicore/cluster/GPU.  
2. Cada una de las simulaciones (identificada por cada columna en la fig).  
   - Paralelizar en cluster.  
3. Cada experimento (identificado por la fig. completa).  
   - Paralelizar en cluster.

######Fig. 1
![](doc/pictures/experimento.png)

1. Los parámetros que definen un determinado experimento están dados en el archivo de configuración `experimento.conf`.
   - Definir la NP. Es la misma NP en todo el experimento (`experimento.conf`).
   - Definir cantidad de simulaciones para la NP dada. En el ej. de la fig, son tres simulaciones (las columnas).
2. Dopar la NP: generar aceptores, distribuirlos homogeneamente, etc. (serial).
   - La cantidad de dopamientos es distinta de cada simulación (es definida en el archivo de configuración).
   - Simulación 1: 4 dopamientos
   - Simulación 2: 7 dopamientos
   - Simulación 3: 10 dopamientos
3. Bombardear la NP: la cantidad de bombardeos es distinta en cada simulación (es definida en el archivo de configuración).
   - Simulación 1: 4 bombardeos
   - Simulación 2: 3 bombardeos
   - Simulación 3: 6 bombardeos
   - El bombardeo se debe hacer en paralelo (multicore/GPU/Cluster). Cada bombardeo (indicado por cada flecha en la Fig) tiene un ID único y obtiene un único resultado. Todos los bombardeos de una simulación escriben su resultado en una variable (array) compartida accediendo mediante su ID al subindice correspondiente.
   - Simulación1.Bombardeos[resultado-bombardeo1, resultado-bombardeo2, ...]
   - Simulación2.Bombardeos[resultado-bombardeo1, resultado-bombardeo2, ...]
   - Simulación3.Bombardeos[resultado-bombardeo1, resultado-bombardeo2, ...]
4. Se calcula la eficiencia en función del nro de aceptores (cálculo serial).
   - Eficiencia1 = CalcularEficiencia(Simulación1.Bombardeos)
   - Eficiencia2 = CalcularEficiencia(Simulación2.Bombardeos)
   - Eficiencia3 = CalcularEficiencia(Simulación3.Bombardeos)
5. Join de los resultados de cada una de las simulaciones para su post-procesamiento (gráfico).
   - CalcularEficienciaTotalExperimento(Eficiencia1, Eficiencia2, Eficiencia3)

## TODO.

### Física del problema:
- [x] Generar el photon mediante una electrolisis química.
- [x] Calcular L_D
- [x] R variable usando una distribución normal. Se pasa en el config los dos parámetros de la normal. Si solo se pasa un parámtro, se toma R como constante.
- [ ] Dotar de volumen a los aceptores.

### Optimización y paralelismo:
- [x] hacer gráfico detallando procesos seriales y paralelos.
- [x] Medir la performance del código serial.
- [ ] Medir speed-up.
- [x] Para una NP, queremos paralelizar el bombardeo de fotónes.
- [ ] Usando Cuda, paralelizar la cantidad de bombardeos para GPU.
- [ ] Cuando este funcionando la implementación de MPI, que en el output indique cuantos cpu usa, el porcentaje de cada uno y la memoria por proceso (igual que LAMPS).

### Herramientas de post procesamiento:
- [ ] De un directorio, lea todos los output y grafique la eficiencia de Quenching.
- [ ] Histográmas de la distribución de los aceptores.

### Input, output, log y código:
- [x] Usar [Sphinx](http://sphinx-doc.org/) para la documentación.
- [x] Agregar al config:
  * Elección del método de depositado de dopantes.
  * Elección del método de genaración del exiton.
- [x] Cambiar en el input que se ingrese el \epsilon en lugar del \Delata t.
- [x] Respetar PEP8
- [ ] Agregar al output:
  * la forma en que se genero los acceptores
  * la forma en la que se genero el exiton
- [ ] Nombre representativo del output. Puede ser similar a los archivos del Landsat.
- [ ] Agregar función de log.
- [ ] En el main.py, ir informando del avance.
- [ ] Actualizar la documentación.
- [ ] Calculo automático de la convergencia.
- [ ] Hacer el requeriments.txt  


##Licencia.
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">TEN</span> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.  
Todo el código esta bajo licencia [MIT](https://github.com/pewen/ten/blob/master/LICENSE).
