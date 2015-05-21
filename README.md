# TEN
**Transferencia de Energía en NanoParticulas**

##Equipo de trabajo

*Directores:*  
* Chemical: **Dr. Rodrigo Palacio**  
* Cloud computing: [**Dr. Jose Luis Vazquez-Poletti**](http://www.dsa-research.org/doku.php?id=people:poletti)

*Students*:  
* PhD student **Rodrigo Ponsio**  
* Master student **Daniel Bellomo**  
* Undergraduate [**Franco Bellomo**](https://github.com/fnbellomo) [@fnbellomo](https://twitter.com/fnbellomo)  
* Undergraduate [**Lucas Bellomo**](https://github.com/lbellomo) [@ucaomo](https://twitter.com/ucaomo)

##Objetivo

Comprobar eficiencia de Quenching.

Mediante simulaciones de Monte Carlo, se quiere estudiar la eficiencia de Quenching para una nanopartícula (NP) determinada. Estas simulaciones van a ser contrastadas con las mediciones experimentales realizadas en el Laboratorio de Microscopia Optica Avanzada (LMOA) de la Universidad Nacional de Río Cuarto (UNRC).

En principio, son tres los experimentos en los que queremos corroborar la eficiencia de Quenching:  
1. En el caso de tener los aceptores distribuidos volumetricamente en la NP.  
2. Que los aceptores estén sobre la superficie de la NP.  
3. En los dos casos anteriores el fotón es generado mediante un laser. Se quiere estudiar que sucede en el caso de que sea generado mediante una electrólisis química.

Para el experimento 1, estamos trabajando basados un en paper, desarrollando nuestra herramienta computacional. Para los experimentos 2 y 3, se quiere verificar una hipótesis de trabajo, no existiendo trabajos de referencia.

##Instalación
###Requerimientos

*Core*:
* Python (2.x o 3.x)
* Numpy
* Scipy (Solo es para importar pi. Si no esta instalado, se usa un valor con menor precisión).
* MPI4py
* OpenMPI o MPICH

*Herramientas de post-procesamiento:*
* Matplotlib

###Instalación
TODO setup.py

##Funcionalidades

* Podemos generar aceptores:
    1. En toda la NP con el método: Nanoparticle.deposit_volumetrically_acceptors().
    2. En la superficie (Nanoparticle.deposit_superficial_acceptors()).

* Podemos generar exitones:
    1. En cualquier lugar de la NP (Exiton.laser_generated()), simulando que a la NP la bombardeamos con un laser.
    2. Entre dos radios (Exiton.electro_generate()), simulando que este es generado mediante una electrolisis.

En todos los casos, las generaciones son con distribución uniforme.

##Resumen de funcionamiento.

Basicamente, el código (escrito en python3) funciona de la siguiente forma:
* **Creamos un objeto NP** con sus propiedades como el radio, cantidad de aceptores, etc. Dichas propiedades se especifican en el archivo `experimento.conf`.
* **Generamos los aceptores** distribuidos uniformemente sobre la NP, usando alguno de los dos métodos explicados anteriormente.
* **Creamos el exiton** generandolo aleatoriamente sobre la NP, usando alguno de los dos métodos explicados anteriormente.
* **Movemos el exiton** calculando las probabilidades de decae, transferencia o de realizar un random walk. En caso de que el exiton se mueva, se realiza este ultima paso nuevamente.

Por la manera en la que esta modulizado el código, podemos bombardear a la misma NP con los mismo aceptores, la cantidad de veces que deseemos.

##Experimento.

En la *Fig. 1* se muestran los procesos que intervienen en el experimento, con el objeto de detallar los procesos secuenciales y paralelos (multicore/GPU/cluster/cloud).

###Existen tres niveles de paralelismo:

1. Bombardeo de fotones, el punto *3)* de la fig.  
   - Paralelizar en multicore/GPU/cluster.  
2. Cada una de las simulaciones (identificada por cada columna en la fig).  
   - Paralelizar en cluster/cloud.  
3. Cada experimento (identificado por la fig. completa).  
   - Paralelizar en la infraestructura cloud.

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

**Se podran ejecutar un nro arbitrario de experimentos distintos, *en simultáneo*, haciendo uso de la infraestructura cloud.**

##Primeros Output
El código de esta salida esta en el notebook `ten/examples/test.ipynb`

    TEN 2015-05-09 00:37:18.493444

    Linux-3.16.0-4-amd64-x86_64-with-debian-stretch-sid
    uname_result(system='Linux', node='antu', release='3.16.0-4-amd64', version='#1 SMP Debian 3.16.7-ckt9-3 (2015-04-23)', machine='x86_64', processor='')

	Input parameters:
	-----------------
	NP radius: 50.000
	Forster radius: 2.290
	Length of excition diffusion: 8.000
	Tau_D: 344.000
	Number of acceptors: 60
	Delta_t: 1.000
	Epsilon: 0.023
	Probability of decay: 0.003
	Number of exitations: 500

	Outputs:
	--------
	Amount of decays: 117
	Amount of transfers: 383
	Quenching efficiency: 0.766000

	Total time in seg: 43.010

##Plan de trabajo.
1. Entender el modelo teórico.
2. Realizar prototipo de la aplicación verificando la teória (dominio de la aplicación mínimo).
3. Optimizar performance del código.
4. Ampliar el dominio de estudio (números de NP y de los aceptores).
5. Portar a Cloud Computing.
6. Paralelizar el bombardeo de fotónes usando MPI / OpenCL.

##TODO.
- [x] hacer gráfico detallando procesos seriales y paralelos (detallando paralelismo en el cluster/multicore y procesos al cloud)
- [x] Usar [Sphinx](http://sphinx-doc.org/) para subir la documentación.
- [ ] Medir la performance del código serial.
- [ ] Gráficos de las eficiencias de cantidad de aceptores vs Quenching.
- [ ] Para una NP, queremos paralelizar el bombardeo de fotónes.
- [x] Generar el photon mediante una electrolisis química.
- [ ] El archivo de salida, hay que ponerle un nombre representativo. Por ej, dd-mm-aa-id que el id puede ser algo que ingrese el usuario o un random.
- [ ] Herramientas de post-procesamiento:
   - [ ] Leer un output especifico y que grafique los aceptores.
   - [ ] De un directorio, lea todos los output y grafique la eficiencia de quenching
- [ ] Usando MPI, paralelizar la cantidad de bombardeos p/ multicore/cluster.
- [ ] Usando OpenCL, paralelizar la cantidad de bombardeos p/ multicore/GPU
- [x] Hacer un interfaz simple de usar, que se le puedan pasar algunos parámetros por cli, o que levante un archivo de configuración y lo chequee.
- [ ] Cuando este funcionando la implementación de MPI, que en el output indique cuantos cpu usa, y el porcentaje (igual que LAMPS).
- [ ] Portar la aplicación a un entrono de Cloud Computing, con el objetivo de realizar simulaciones masivas.
- [ ] Dotar de volumen a los aceptores.

##Licencia.
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">TEN</span> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.  
Todo el código esta bajo licencia [MIT](https://github.com/pewen/ten/blob/master/LICENSE).
