import sys
sys.path.append("../")
import warnings
warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt
import math
import numpy as np

from SimUtils import mobility
from TaskAcceptanceRate import dcemto, randomAllocation, localExecution

if __name__ == "__main__":
    #array to store task completion% values in DCEMTO run 
    dcemto_ = []

    #array to store task completion% values in randomAllocation run 
    rand_alloc = []

    #array to store task completion% values in localExecution run 
    local_exec = []

    #input : task deadline constraint
    task_deadline = list(range(1,9))
    task_deadline = [x/10 for x in task_deadline]

    #initializing simulation settings
    users,servers = mobility.init(30)
        
    #DCEMTO run returns an array of no of tasks requests accepted for each given deadline 
    dcemto_ = [y/30 for y in dcemto.run(users,servers,task_deadline)]
    
    #randomAllocation run
    rand_alloc = [y/30 for y in randomAllocation.run(users,servers,task_deadline)]

    #localExecution run
    local_exec = [y/30 for y in localExecution.run(users,task_deadline)]

    #plotting
    plt.plot(task_deadline,dcemto_,label = 'DCEMTO',marker='^')
    plt.plot(task_deadline,rand_alloc,label = 'random',marker='+')
    plt.plot(task_deadline,local_exec,label = 'mobile-execution',marker='*')
    plt.xlabel('Task Deadline(sec)')
    plt.ylabel('Task Completion(%)')
    plt.legend()
    plt.grid()
    plt.show()