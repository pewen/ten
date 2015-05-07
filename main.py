from src.nanoparticle import NanoParticle
from src.photon import Photon
from config import *

np = NanoParticle(r, num_acceptores, tau_D, R_Forster, L_D, delta_t)
np.deposit_volumetrically_acceptors()

simu = Photon(np, num_exc)

