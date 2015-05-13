from src.nanoparticle import NanoParticle
from src.photon import Photon
from src.utils import read4file

#To parse the argument from comand line
import argparse

# Creation of argument parser
parser = argparse.ArgumentParser(description='TEN')
parser.add_argument('-c', '--config',dest='config', default='config.conf', help='path to configuration (initial parameters) file')
args = parser.parse_args()

init_param = read4file(args.config)

nano_particle = NanoParticle(init_param['r'], init_param['num_acceptors'], init_param['tau_D'], init_param['R_Forster'], init_param['L_D'], init_param['delta_t'])
nano_particle.deposit_volumetrically_acceptors()

simu = Photon(nano_particle, init_param['num_exc'])
simu.laser_generated()
simu.move()
simu.save_out('.')
