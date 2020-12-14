

"""
Created on Tue Jul  14 10:39:16 2020

@author: stevo
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

idx = pd.IndexSlice


#%% DEMAND 


demand_GHANA = pd.read_csv('results/results_carrier_con.csv', index_col=[0,1,2,3]).loc[idx[:,:,'demand_power',:],:].groupby(level=['timesteps'],axis=0,sort=False).sum()

demand_UE = pd.read_csv('results/results_carrier_con.csv', index_col=[0,1,2,3]).loc[idx[:,'UE','demand_power',:],:].groupby(level=['timesteps'],axis=0,sort=False).sum()
demand_UW = pd.read_csv('results/results_carrier_con.csv', index_col=[0,1,2,3]).loc[idx[:,'UW','demand_power',:],:].groupby(level=['timesteps'],axis=0,sort=False).sum()
demand_NP = pd.read_csv('results/results_carrier_con.csv', index_col=[0,1,2,3]).loc[idx[:,'NP','demand_power',:],:].groupby(level=['timesteps'],axis=0,sort=False).sum()
demand_BA = pd.read_csv('results/results_carrier_con.csv', index_col=[0,1,2,3]).loc[idx[:,'BA','demand_power',:],:].groupby(level=['timesteps'],axis=0,sort=False).sum()
demand_AH = pd.read_csv('results/results_carrier_con.csv', index_col=[0,1,2,3]).loc[idx[:,'AH','demand_power',:],:].groupby(level=['timesteps'],axis=0,sort=False).sum()
demand_CP = pd.read_csv('results/results_carrier_con.csv', index_col=[0,1,2,3]).loc[idx[:,'CP','demand_power',:],:].groupby(level=['timesteps'],axis=0,sort=False).sum()
demand_AA = pd.read_csv('results/results_carrier_con.csv', index_col=[0,1,2,3]).loc[idx[:,'AA','demand_power',:],:].groupby(level=['timesteps'],axis=0,sort=False).sum()
demand_EP = pd.read_csv('results/results_carrier_con.csv', index_col=[0,1,2,3]).loc[idx[:,'EP','demand_power',:],:].groupby(level=['timesteps'],axis=0,sort=False).sum()
demand_WP = pd.read_csv('results/results_carrier_con.csv', index_col=[0,1,2,3]).loc[idx[:,'WP','demand_power',:],:].groupby(level=['timesteps'],axis=0,sort=False).sum()
demand_TV = pd.read_csv('results/results_carrier_con.csv', index_col=[0,1,2,3]).loc[idx[:,'TV','demand_power',:],:].groupby(level=['timesteps'],axis=0,sort=False).sum()


#%% INDEX DATETIME

### BASE ###

demand_GHANA.index = pd.to_datetime(demand_GHANA.index)



#%% RESAMPLING

### BASE ###

demand_GHANA = -demand_GHANA.resample('W').mean()


#%% ## PREPROCESSING ## 


day = '2019-01-01 00:00:00'
end = '2019-12-31 23:00:00'


#%%  ### PLOTTING SAPP ###

## ENTIRE SAPP ##

demand_GHANA_cum = demand_GHANA/1000000

fig, (ax) = plt.subplots(1, figsize=(16,8))

# positive side #
ax.plot(demand_GHANA_cum[day:end].index,demand_GHANA_cum[day:end].values,'#000000')
plt.ylim(1.5,2.6)


ax.set_ylabel('Power (GW)',labelpad = 11, size = 20)
ax.axes.tick_params(labelsize = 15)

ax.margins(x=0)
ax.margins(y=0)

# Fill #

ax.set_title('Ghana Power Demand 2019', size=30)


