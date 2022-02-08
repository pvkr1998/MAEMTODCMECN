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

    no_of_users = []

    for i in range(1,10):
        users,servers = mobility.init(i*5)
        no_of_users.append(i*5)
        print("------------------------------No of Users = ",i*5,end="------------------------------\n")

        #DCEMTO run
        energy,count = dcemto.run(users,servers)
        energy_dcemto.append(energy)
        print("energy DCEMTO = ",energy,"\n")

        #randomAllocation run
        energy,count = randomAllocation.run(users,servers)
        energy_rand_alloc.append(energy)
        print("energy random = ",energy,"\n\n\n")


    #plotting
    plt.plot(no_of_users,energy_dcemto,label = 'DCEMTO',marker='^')
    plt.plot(no_of_users,energy_rand_alloc,label='Random-Allocation',marker='+')
    plt.xlabel('Number of Users')
    plt.ylabel('Energy Consumption(Joules)')
    plt.legend()
    plt.grid()
    plt.show()