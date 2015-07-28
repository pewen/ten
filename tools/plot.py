# Borrador del plot
import matplotlib.pyplot as plt
from sys import argv

script, file_path = argv

f = open(file_path, 'r')

num_acceptors = []
quenching_eff = []

while True:
    a = f.readline()
    if '| Number of acceptors' in a:
        f.readline()
        while True:
            a = f.readline()
            if '-' in a:
                break
                
            b = ''.join(a.split()).split('|')[1: -1]
            num_acceptors.append(int(b[0]))
            quenching_eff.append(float(b[4]))

    if a == '':
        break
       
f.close()
plt.plot(num_acceptors, quenching_eff, 'o--')
plt.xlabel('Number of acceptors')
plt.ylabel('Quenching Efficiency')
plt.grid()
plt.savefig(file_path[:-4] + '.svg')
plt.show()

