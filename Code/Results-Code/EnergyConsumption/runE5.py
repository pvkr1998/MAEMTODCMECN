import sys
sys.path.append("../")
import warnings
warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt
import math
import numpy as np

import mobility
from EnergyConsumption import dcemto, randomAllocation, localExecution


if __name__ == "__main__":
    n_groups = 3
    #array to store energy consumption values in DCEMTO run 
    energy_dcemto = []

    #array to store energy consumption values in randomAllocation run 
    energy_rand_alloc = []

    for i in range(2,5):
        users,servers = mobility.init(30)
        servers['cap'] = [i*5*1e9]*servers.shape[0]
        print("-----------------------------Server Capacity(MHz) = ",i*5,"---------------------------------\n")
        #DCEMTO run
        energy,count = dcemto.run(users,servers)
        energy_dcemto.append(energy/count)
        print("Avg energy DCEMTO = ",energy/count,"\n")

        #randomAllocation run
        energy,count = randomAllocation.run(users,servers)
        energy_rand_alloc.append(energy/count)
        print("Avg energy random = ",energy/count,"\n\n\n")

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.15
    opacity = 0.6

    rects1 = plt.bar(index, energy_dcemto, bar_width,
    alpha=opacity,
    color='g',
    label='DCEMTO')

    rects2 = plt.bar(index + bar_width, energy_rand_alloc, bar_width,
    alpha=opacity,
    color='b',
    label='Random-Allocation')

    plt.xlabel('Server Computation Capacity(GHz)')
    plt.ylabel('Avg Energy Consumption(Joules)')
    plt.xticks(index + bar_width, ('10', '15', '20'))
    plt.legend()

    plt.tight_layout()
    plt.show()