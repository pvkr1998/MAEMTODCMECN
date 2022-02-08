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
    #array to store energy consumption values in DCEMTO run 
    energy_dcemto = []

    #array to store energy consumption values in randomAllocation run 
    energy_rand_alloc = []

    task_ip_size = []

    for i in range(1,17):
        users,servers = mobility.init(30)
        task_ip_size.append(i/2)
        print("-----------------------------------Task size(MB) = ",i/2,"-----------------------------------\n")
        
        users['i_data_size'] = [(i/2)*32e5]*30
        users['o_data_size'] = [(0)*32e5]*30 

        #DCEMTO run
        energy,count = dcemto.run(users,servers)
        energy_dcemto.append(energy/count)
        print("Avg energy DCEMTO = ",energy/count,"\n")

        #randomAllocation run
        energy,count = randomAllocation.run(users,servers)
        energy_rand_alloc.append(energy/count)
        print("Avg energy random = ",energy/count,"\n\n\n")

    plt.plot(task_ip_size,energy_dcemto,label = 'DCEMTO',marker='^')
    plt.plot(task_ip_size,energy_rand_alloc,label='Random-Allocation',marker='+')
    plt.xlabel('Task Input size(MB)')
    plt.ylabel('Avg Energy Consumption(Joules)')
    plt.legend()
    plt.grid()
    plt.show()