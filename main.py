from src.nanoparticle import NanoParticle
from src.exciton import Exciton
from src.utils import read4file

#To parse the argument from comand line
import argparse

# Creation of argument parser
parser = argparse.ArgumentParser(description='TEN')
parser.add_argument('-c', '--config',dest='config', default='experiment.conf', help='path to configuration (initial parameters) file')
args = parser.parse_args()

#Read the configuration from file.
init_param = read4file(args.config)

#Initialice the nanopartile object,
#depending the way to generate acceptors.
if init_param['acceptors'] == 'sup':
    nano_particle = NanoParticle(init_param['r'], init_param['num_acceptors'], init_param['tau_D'], init_param['R_Forster'], init_param['L_D'], init_param['delta_t'], 'sup')
    #nano_particle.deposit_superficial_acceptors()
else:
    nano_particle = NanoParticle(init_param['r'], init_param['num_acceptors'], init_param['tau_D'], init_param['R_Forster'], init_param['L_D'], init_param['delta_t'], 'vol')
    #nano_particle.deposit_volumetrically_acceptors()

#Initialece the exiton,
#depending the way to generate it's.
if init_param['exiton'] == 'elec':
    simu = Exciton(nano_particle, init_param['num_exc'], 'elec')
    #simu.electro_generated()
else:
    simu = Exciton(nano_particle, init_param['num_exc'], 'laser')
    #simu.laser_generated()

#Calculate
simu.move()
simu.save_out('.')
