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

    #array to store energy consumption values in localExecution run 
    energy_local_exec = []

    no_of_users = []
    no_of_users_1 = []
    for i in range(1,30):
        users,servers = mobility.init(i*5)
        no_of_users.append(i*5)
        print("------------------------------No of Users = ",i*5,end="------------------------------\n")

        #DCEMTO run
        energy,count = dcemto.run(users,servers)
        energy_dcemto.append(energy/count)
        print("Avg energy DCEMTO = ",energy/count,"\n")

        #randomAllocation run
        energy,count = randomAllocation.run(users,servers)
        energy_rand_alloc.append(energy/count)
        print("Avg energy random = ",energy/count,"\n")

        #localExecution run
        energy,count = localExecution.run(users)
        if count!=0:
            energy_local_exec.append(energy/count)
            print("Avg energy local  = ",energy/count,"\n")
            no_of_users_1.append(i*5)
        print("\n\n")

    #plotting
    plt.plot(no_of_users,energy_dcemto,label = 'DCEMTO',marker='^')
    plt.plot(no_of_users,energy_rand_alloc,label='Random-Allocation',marker='+')
    plt.plot(no_of_users_1,energy_local_exec,label = 'Local-Execution',marker='*')
    plt.xlabel('Number of Users')
    plt.ylabel('Avg Energy Consumption(Joules)')
    plt.legend()
    plt.grid()
    plt.show()