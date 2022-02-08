import math
import numpy as np
import random

from SimUtils import params

"""
This function returns Energy Consumption and Task Acceptance number 
"""

def run(users,servers):
    energy = 0
    count = 0
    """
    for each user
    """
    for u in users.index:
        #time taken for transmission and execution
        prev_node = -2
        i = 0
        tot_trans_en = 0
        tot_time = 0
        min_ = []
        """
        for each step of user u
        """
        for step in users['servers_set'][u]:
            if(step[0]==-1):    #no servers at this step
                continue
            #execution
            if prev_node==-2:   #no previous => uplink + exec + downlink
                m = []
                for s in step:
                    if(s==-1):      #end of servers
                        break
                    #uplink
                    x1,y1 = users['step_co'][u][i][0],users['step_co'][u][i][1]
                    [x2,y2] = servers['co-ordx'][s],servers['co-ordy'][s]
                    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
                    datarate = params.BANDWIDTH*np.log2(1 + users['transPow'][u]/(params.NOISE*pow(distance,params.ALPHA)))
                    time_u = users['i_data_size'][u]/datarate
                    energy_u = time_u*users['transPow'][u]
                     #exec
                    time_ex = users['cycles_req'][u]/servers['cap'][s]
                    energy_ex = time_ex*servers['compPow'][s]
                   

                    ener = energy_u + energy_ex 
                    time = time_u + time_ex 

                    if(time <= users['deadline'][u]):
                        m.append(ener)

                if(len(m)>0):
                    ind = random.randint(0,len(m)-1)
                    min_.append(m[ind])
            else:
                for s in step:
                    if(s==-1):      #end of servers
                        break
                    elif(s==prev_node):
                        continue
                    #trans
                    [x1,y1] = servers['co-ordx'][prev_node],servers['co-ordy'][prev_node]
                    x2,y2 = servers['co-ordx'][s],servers['co-ordy'][s]
                    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
                    datarate = params.BANDWIDTH*np.log2(1 + servers['transPow'][prev_node]/(params.NOISE*pow(distance,params.ALPHA)))
                    time_t = users['i_data_size'][u]/datarate
                    energy_t = servers['transPow'][prev_node]*time_t
                     #exec
                    time_ex = users['cycles_req'][u]/servers['cap'][s]
                    energy_ex = time_ex*servers['compPow'][s]
                   

                    ener = energy_t + energy_ex  + tot_trans_en
                    time = time_t + time_ex  + tot_time

                    if(time <= users['deadline'][u]):
                        m.append(ener)

                if(len(m)>0):
                    ind = random.randint(0,len(m)-1)
                    min_.append(m[ind])

            if(i<len(users['servers_set'][u])-1):
                min_trans = math.inf
                x1,y1 = users['step_co'][u][i+1][0],users['step_co'][u][i+1][1]
                arg_min = -1
                for s in step:
                    if(s==-1):
                        break
                    x2,y2 = servers['co-ordx'][s],servers['co-ordy'][s]
                    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
                    datarate = params.BANDWIDTH*np.log2(1 + servers['transPow'][s]/(params.NOISE*pow(distance,params.ALPHA)))
                    trans_en = servers['transPow'][s]*users['i_data_size'][u]/datarate
                    if(min_trans>trans_en):
                        min_trans = trans_en 
                        arg_min = s
                if prev_node == -2 and arg_min!=-1:
                    x1,y1 = users['step_co'][u][i][0],users['step_co'][u][i][1]
                    [x2,y2] = servers['co-ordx'][arg_min],servers['co-ordy'][arg_min]
                    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
                    datarate = params.BANDWIDTH*np.log2(1 + users['transPow'][u]/(params.NOISE*pow(distance,params.ALPHA)))
                    time_u = users['i_data_size'][u]/datarate
                    energy_u = time_u*users['transPow'][u]
                    tot_time = tot_time + time_u
                    tot_trans_en = tot_trans_en + energy_u 
                elif prev_node!=arg_min and arg_min!=-1:
                    [x1,y1] = servers['co-ordx'][prev_node],servers['co-ordy'][prev_node]
                    x2,y2 = servers['co-ordx'][arg_min],servers['co-ordy'][arg_min]
                    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
                    datarate = params.BANDWIDTH*np.log2(1 + servers['transPow'][prev_node]/(params.NOISE*pow(distance,params.ALPHA)))
                    trans_time = users['i_data_size'][u]/datarate
                    trans_en = servers['transPow'][prev_node]*trans_time
                    tot_time = tot_time + trans_time
                    tot_trans_en = tot_trans_en + trans_en 
                            
                prev_node = arg_min
            i = i + 1
        if(len(min_)>0):
            ind = random.randint(0,len(min_)-1)
            energy = energy + min_[ind]
            count = count + 1
       
    return energy,count