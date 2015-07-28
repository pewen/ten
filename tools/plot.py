# Borrador del plot
import matplotlib.pyplot as plt

file_path = '../tets.txt'

f = open(file_path, 'r')

num_acceptors = []
quenching_eff = []

while True:
    a = f.readline()
    if 'Number of acceptors' in a:
        list_a = [int(number) for number in a[26:-2].split(sep=',')]
        num_acceptors.append(list_a)
        
    if 'Quenching efficiency' in a:
        list_a = [float(number) for number in a[24:-2].split(sep=',')]
        quenching_eff.append(list_a)
        
    if a == '':
        break

        
f.close()

print(num_acceptors, quenching_eff)
for plot in range(len(num_acceptors)):
    plt.plot(num_acceptors[plot], quenching_eff[plot])
    
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