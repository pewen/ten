TODO
====

- [ ] Hacer gráfico detallando procesos seriales y paralelos (detallando paralelismo en el cluster/multicore y procesos al cloud)
- [x] Usar Sphinx para la documentación.
- [ ] Medir la performance del código serial.
- [ ] Gráficos de las eficiencias de cantidad de aceptores vs Quenching.
- [ ] Para una NP, queremos paralelizar el bombardeo de fotónes.
- [ ] Generar el photon mediante una electrolisis química.
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
