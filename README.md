# TEN
**Transfer of energy in nanoparticles**

##Autores

*Chemical director:* **Dr. Palacio Roberto**  
*Cloud computing director:* **Dr **   
*Students*:  
* PhD student **Ponsio Rodrigo**
* Master student **Daniel Bellomo**
* Undergraduate **Franco Bellomo** @fnbellomo
* Undergraduate **Lucas Bellomo** @ucaomo

##Idea general

Mediante simulaciones de Monte Carlo, se quiere estudiar la eficiencia de Quenching para una nanopartícula (NP) determinada. Estas simulaiones van a ser contastadas con las mediciones experimentales realizadas en el Laboratorio de Microscopia Optica Avanzada (LMOA) de la Universidad Nacional de Río Cuarto (UNRC).

Basicamente, el código (escrito en python3) funciona de la siguiente forma:
* **Creamos un objeto NP** con sus propiedades como el radio, cantidad de aceptors, etc. Dichas propiedades se especifican en el archivo config.py.
* **Generamos los aceptores** distribuidos uniformemente sobre la NP. Estos aceptores pueden estar distribuidos sobre la superficie o dentro de la NP.
* **Creamos el obtejo Photon** generandolo aleatoriamente sobre la NP.
* **Movemos el fotón** y si vemos si decae o si se transfiere a un fotón.

Por la manera en la que esta modulizado el código, podemos bombardear a la misma NP con los mismo aceptores, la cantidad de veces que deseemos.

##TODO
* Tenemos las clases y sus métodos documentados. Ahora queremos ponerlos online usando [Sphinx](http://sphinx-doc.org/).
* Medir la performance del código serial.
* Para una NP, queremos paralelizar el bombardeo de fotónes.
* Usando Cloud Computing, poder simular muchas NP distintas.

##Licencia
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">TEN</span> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.  
Todo el código esta bajo licencia [MIT](https://github.com/pewen/ten/blob/master/LICENSE).