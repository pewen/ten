# Borrador del plot
import matplotlib.pyplot as plt
from sys import argv

script, file_path = argv

f = open(file_path, 'r')

num_acceptors = []
quenching_eff = []

while True:
    a = f.readline()
    if '| Nº acceptors' in a:
        f.readline()
        while True:
            a = f.readline()
            if '-' in a:
                break
                
            b = ''.join(a.split()).split('|')[1: -1]
            num_acceptors.append(int(b[0]))
            quenching_eff.append(float(b[3]))

    if 'NP radius mean' in a:
        np_radius = a.split(': ')[1].split()[0]

    if 'Foster radius' in a:
        foster_radius = a.split(': ')[1].split()[0]

    if 'Tau_D' in a:
        tau_d = a.split(': ')[1].split()[0]

    if 'Epsilon' in a:
        epsilon = a.split(': ')[1].split()[0]

    if 'L_D' in a:
        l_d = a.split('= ')[1]
        
    if a == '':
        break
       
f.close()
plt.plot(num_acceptors, quenching_eff, 'o--')
plt.xlabel('Number of acceptors')
plt.xlim(xmin=-10)
plt.ylim(-0.1, 1.1)
plt.ylabel('Quenching Efficiency')
plt.text(200, 0.5, r'$NP\;radius = %.1f \;nm$' %(float(np_radius)), fontsize=14)
plt.text(200, 0.45, r'$Foster\;radius = %.4f \;nm$' %(float(foster_radius)), fontsize=14)
plt.text(200, 0.4, r'$\tau_{D}\;  = %.4f \;ns$' %(float(tau_d)), fontsize=14)
plt.text(200, 0.35, r'$\epsilon\; = %.4f \;nm$' %(float(epsilon)), fontsize=14)
plt.text(200, 0.3, r'$L_{D} = %.4f \;nm$' %(float(l_d)), fontsize=14)
plt.grid()
plt.savefig(file_path[:-4] + '.svg')
plt.show()

