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
            b = ''.join(a.split()).split('|')[1: -1]
            num_acceptors.append(int(b[0]))
            print(num_acceptors)
            quenching_eff.append(float(b[4]))

            if '-' in a:
                break
    if a == '':
        break

print('foo')        
f.close()

plt.plot(num_acceptors, quenching_eff)
    
plt.show()
    
'''plot(x1a, y1a, 'o--', x2, y2, 'o--')
xlabel('Number of Dye Molecules per particle')
xlim(0, 900)
ylabel('Quenching Efficiency')
title('PDHF nanoparticles doped with perylene')
legend(['Simulation', 'Experimental'], loc=0)
grid()
savefig('Fig_para_resumen_Giambiagi_v3')
show()'''