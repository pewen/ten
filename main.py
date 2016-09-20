import numpy as np

import ten
from ten.utils.utils import read4file
from ten.experiments.mechanisms import forster, boolean

init_param = read4file('experiment.conf')
if 'quenching' in init_param['experiments']:
    for intrinsic_aceptor in init_param['intrinsic_aceptors']:
        dopantes_propios = ten.Aceptor(number=intrinsic_aceptor,
                                       r_mechanisms=init_param['intrinsic_r_mechanisms'],
                                       way=init_param['intrinsic_way'])
        dopantes = ten.Aceptor(number=init_param['aceptors'],
                               r_mechanisms=init_param['r_mechanisms'],
                               way=init_param['way'])
        NP = ten.Nanoparticle([init_param['r_mean'], init_param['r_deviation']],
                              init_param['tau_D'], init_param['mean_path'], 
                              init_param['epsilon'], dopantes_propios)
        print(NP)

        NP.doped(dopantes)

        out = ten.experiments.quenching(NP, dopantes, ten.forster,
                                    init_param['exiton'])
        print("Eficiencia: {0}, Nº decaidos: {1},\
              Nº transferidos: {2}".format(out[0], out[1], out[3]-out[1]))
        print("Pasos promedio: {0:.2f} nm, \
              Tiempo total: {1:.2f} seg. \n".format(out[2], out[4]))

if 'single_count' in init_param['experiments']:
     for intrinsic_aceptor in init_param['intrinsic_aceptors']:
         dopantes_propios = ten.Aceptor(number=intrinsic_aceptor,
                                        r_mechanisms=init_param['intrinsic_r_mechanisms'],
                                        way=init_param['intrinsic_way'])
         dopantes = ten.Aceptor(number=init_param['aceptors'],
                                r_mechanisms=init_param['r_mechanisms'],
                                way=init_param['way'])
         NP = ten.Nanoparticle([init_param['r_mean'], init_param['r_deviation']],
                               init_param['tau_D'], init_param['mean_path'], 
                               init_param['epsilon'], dopantes_propios)
         out = ten.experiments.single_count(NP, dopantes, forster, 'laser', exitations=(int(init_param['excitations'])))
         print(out)
if 'difusion_length' in init_param['experiments']:
    for intrinsic_aceptor in init_param['intrinsic_aceptors']:
        dopantes_propios = ten.Aceptor(number=intrinsic_aceptor,
                                       r_mechanisms=init_param['intrinsic_r_mechanisms'],
                                       way=init_param['intrinsic_way'])
        NP = ten.Nanoparticle([init_param['r_mean'], init_param['r_deviation']],
                              init_param['tau_D'], init_param['mean_path'], 
                              init_param['epsilon'], dopantes_propios)
        
        out = ten.experiments.difusion_length(NP, forster, 'laser', exitations=(int(init_param['excitations'])))
        print("Exciton difusion length: {0:.2f} nm, Nº exitaciones: {1}".format(out[0], out[1]))
        print("Tiempo total: {0:.2f} seg.".format(out[2]))