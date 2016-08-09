import sys
sys.path.append('../../')

from ten.nanoparticle import Nanoparticle
from ten.aceptor import Aceptor
import ten.experiments as experiments
from ten.mechanisms.mechanisms import forsterF90

# python3 -m cProfile -o prop4 test_time.py

num_aceptores = [10, 20, 30, 40, 50, 80, 100]
num_intrisic_aceptors = [0, 1, 5, 10]

for j in num_intrisic_aceptors:
    for i in num_aceptores:
        # Dopantes propios (intrisicos) de la NP
        dopantes_propios = Aceptor(number=i, r_mechanisms=1, way='vol')
        # Dopantes que le vamos a agregar a la NP
        dopantes = Aceptor(number=j, r_mechanisms=3.14, way='vol')
        # Nanoparticula
        NP = Nanoparticle(r_param=[15, 0], tau_d=0.333, mean_path=80,
                          epsilon=1, intrinsic_aceptors=dopantes_propios)

        # Experiment
        out = experiments.quenching(NP, dopantes, forsterF90, 'laser')
        print
        print("Eff: {0}, Nº decaidos: {1}, Nº transferidos: {2}".format(out[0],
                                                                        out[1],
                                                                        out[3]-out[1]))
        print("Pasos prom: {0:.2f} nm, Tiempo total: {1:.2f}".format(out[2],
                                                                     out[4]))