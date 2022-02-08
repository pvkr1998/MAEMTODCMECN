import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
import math
import utm

from pymobility.models.mobility import random_waypoint
from SimUtils.params import *

"""
Method to transform latitude x and longitude y by applying shift and rotate operations  
"""
def transform(x,y):
    x = x - x[np.argmin(y)]
    y = y - min(y)

    x1,y1 = x[np.argmin(y)], min(y)
    x2,y2 = max(x),y[np.argmax(x)]
    
    d = math.sqrt((x2-x1)**2+(y2-y1)**2)
    
    x = x * (x2/d) - y * (-y2/d)
    y = x * (-y2/d) + y* (x2/d)
   
    x = x + 10
    y = y + 50

    return x,y

"""
Method to initialize simulation settings
"""
def init(n_users):
    #reading CSV file from Melbourne CBD Dataset
    servers_df = pd.read_csv(r"../data/site-optus-melbCBD.csv",encoding = "ISO-8859-1", engine='python')

    #server dataframe 
    servers = pd.DataFrame(columns=['co-ordx','co-ordy','cov-rad','transPow','compPow','cap'])
    
    #base station coordinates (latitude, longitude)
    coords = np.empty((2,servers_df.shape[0]))
    for i in servers_df.index:
        coords[0][i], coords[1][i],_,_ = utm.from_latlon(servers_df['LATITUDE'][i],servers_df['LONGITUDE'][i])
    coords[0],coords[1] = transform(coords[0],coords[1])
    servers['co-ordx'] = coords[0]
    servers['co-ordy'] = coords[1]

    #MEC coverage radius (metres)
    servers['cov-rad'] = np.random.uniform(COVERAGE_RADIUS_MIN,COVERAGE_RADIUS_MAX,size=servers_df.shape[0]) 
    
    #MEC transmission power (watts)
    servers['transPow'] = np.random.uniform(SERVER_TRANS_POW_MIN,SERVER_TRANS_POW_MAX,size=servers_df.shape[0])  

    #MEC compuation power (watts)    
    servers['compPow'] = np.random.uniform(3, 5,size=servers_df.shape[0]) 

    #MEC computation capacity (Hz)
    servers['cap']= np.random.uniform(7,20, size=servers_df.shape[0])*1e9   
    
    #user dataframe 
    users = pd.DataFrame(columns = ['steps','servers_set','i_data_size','cycles_req','ind','step_co'])

    #Task Input data size (bits)
    users['i_data_size'] = np.random.uniform(1, 6, size=n_users)*32e5  

    #Task Computation Requirement (cycles)
    users['cycles_req'] = np.random.uniform(1, 10, size=n_users)*1e9  

    #User Mobile device computation capacity (Hz)
    users['cap']= np.random.uniform(low=1, high=10, size=n_users)*1e9  

    #User Mobile device computation power (watts)
    users['compPow'] = np.random.uniform(7, 10,size=n_users)

    #Deadline for Tasks
    users['deadline'] = np.random.uniform(0.1,1,size=n_users)
    
    #No of timsteps in user's mobility
    users['steps'] = np.random.random_integers(5,10,size=n_users)

    #Coordinates of User's no of timesteps
    users['step_co'] = np.empty((n_users,users['steps'].max(),2)).tolist()

    #Available servers at each timestep
    users['servers_set'] = np.zeros((n_users,users['steps'].max(),20)).tolist()

    #index of each user
    users['ind'] = [0 for i in range(n_users)]

    #User Mobile device Transmission power (watts)
    users['transPow'] = np.random.uniform(7,15,size=n_users)

    #generating timesteps using Random Way Point Mobility Model
    rw = random_waypoint(n_users, dimensions=(servers['co-ordx'].max(), servers['co-ordy'].max()), velocity=(100, 150), wt_max=1.0)    
    
    for i in range(users['steps'].max()):
        x = next(rw)
        for j in users.index:
            if(i<users['steps'][j]):
                ind = users['ind'][j] 
                users['step_co'][j][ind][0] = x[j][0]
                users['step_co'][j][ind][1] = x[j][1]
                users['ind'][j] = ind + 1
                q=0
                for k in servers_df.index:
                    if(distance.euclidean((x[j][0],x[j][1]),(servers['co-ordx'][k],servers['co-ordy'][k]))<servers['cov-rad'][k]):
                         users['servers_set'][j][ind][q] = k
                         q = q + 1
                users['servers_set'][j][ind][q] = -1
            else:
                ind = users['ind'][j] 
                users['servers_set'][j][ind][0] = -1
                users['ind'][j] = ind + 1

    return users,servers