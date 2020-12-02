# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 12:04:39 2020

@author: Amin

Goal:
    Adding additional layer of environemtal extansions to the CVX SUT
    using any Environmental Extension.
    
    The idea is to have an environmental extension in the form of CVX SUT.
"""
# This parameter tells the model inf it should make a new proxy matrix or not
rewrite = False
Extension = 'EORA' # Must be the post-prefix name of the two files (one in Concordance and one in Extensions) of the chosen Environmental Extension
#%%
# Importing the needed libraries
import pandas as pd
import numpy as np
import os
#%%
"""
First step:
    the user has to build the a concordance matrix with the following structure:
        1. index: Extension Industries
        2. columns: CVX SUT Industries
    this matrix should be filled with 0 or 1 showing the concordance of the
    different sectors in the tables.
    There should not be any rows or sectors without at least one cell equal to 0,
    which means that at the end, two tables are representating the same economy 
    with differnet representation.
"""
# Reading the concordance matrix
Gi = pd.read_excel(r'Concordance/C_'+Extension+'.xlsx', index_col = [0], header = [0])

# Building the main lists
EE_sec = Gi.index.to_list()
CVX_sec  = Gi.columns.to_list()

# Checking the rows:
for i in range (len(EE_sec)):
    if Gi.loc[EE_sec[i]].sum() == 0 :
        raise ValueError("sector {} in Extension has no concordance sector in CVX SUT".format(EE_sec[i]))

# Cheking the columns:
for i in range(len(CVX_sec)):
    if Gi[CVX_sec[i]].sum() == 0 :
        raise ValueError("sector {} in SAM has no concordance sector in Extension".format(CVX_sec[i]))

#%%
"""
We may need to do both aggregation and disaggregation on Extension in order to reach
to the same structure of CVX SUT.
The structure of concordance matrix tells us if we need to aggregation or 
disaggregation.

HOW?

Looking at the structure of the excel file, it can be understood if the sum of
a row is greater than 1, it means that some sectors in Extension belong to 1 sector
in CVX SUT together and should be aggregated and vice versa.

Lets start with aggregation which is easier
"""
# Make the list of the sectors that needs to be aggregated with their corresponding sector
EE_agg = []
EE_to_CVX_ag = []
agg_list = []
for i in range(len(CVX_sec)):
    if Gi[CVX_sec[i]].sum() > 1 :

        for j in range(len(EE_sec)):
            if Gi.values[j,i] == 1:
                EE_agg.append(EE_sec[j])
                EE_to_CVX_ag.append(CVX_sec[i])
                
EE_dis = []
EE_to_CVX_dis = []
for i in range (len(EE_sec)):
    if Gi.loc[EE_sec[i]].sum() > 1 :
        for j in range(len(CVX_sec)):
            if Gi.values[i,j] == 1:
                EE_dis.append(EE_sec[i])
                EE_to_CVX_dis.append(CVX_sec[j])
                
#%%
# Reading Extension Datbase 
EE = pd.read_excel(r'Environmental Extension/EE_'+Extension+'.xlsx',index_col = [0,1,2] , columns = [0])
#%%

for i in range (len(EE_agg)):
    Gi = Gi.rename(index = {EE_agg[i]:EE_to_CVX_ag[i]})
    EE = EE.rename(columns = {EE_agg[i]:EE_to_CVX_ag[i]})
    
#%%
Gi = Gi.groupby(level = 0,sort = False, axis = 0).mean()
EE = EE.groupby(level = 0 , sort = False, axis = 1).sum()
#%%
EE_dis_single = list(dict.fromkeys(EE_dis))
#%%
# Find the position in data frame
number = []
for i in range(len(EE_dis_single)):
    counter = 0
    for j in range (len(EE_dis)):
        if EE_dis_single[i] == EE_dis [j]:
            counter += 1
    number.append(counter)
#%%
my_list = []
for i in range(len(EE_dis_single)):
    location = EE.columns.get_loc(EE_dis_single[i])
    my_list.append(EE_dis_single[i])
    for j in range(number[i]-1):
        EE.insert(location+j+1,EE_dis_single[i] + str(j+1),'0',True)
        my_list.append(EE_dis_single[i] + str(j+1))
                
#%%
if rewrite:
    proxy = pd.DataFrame(np.zeros((len(EE_dis_single),len(my_list))),index=EE_dis_single,columns = [EE_to_CVX_dis,my_list] )        
    with pd.ExcelWriter(r'proxy.xlsx') as writer:
        proxy.to_excel(writer)
    os.startfile(r'proxy.xlsx')
    
    input('Click on Enter to Continue:')      
#%% 
proxy = pd.read_excel(r'Proxy/P_'+Extension+'.xlsx', index_col = [0] , header = [0,1])
#%%
EE_calc = EE.copy()
#%%
for i in range (len(EE_dis_single)):
    for j in range(number[i]):
        if j ==0:
            ind = my_list.index(EE_dis_single[i])
            EE[EE_dis_single[i]] = EE_calc[EE_dis_single[i]].astype(float) \
                * proxy.loc[EE_dis_single[i],(EE_to_CVX_dis[ind],my_list[ind])].astype(float)
            print(proxy.loc[EE_dis_single[i],(EE_to_CVX_dis[ind],my_list[ind])])
        else :
            
            ind = my_list.index(EE_dis_single[i] + str(j))
            EE[EE_dis_single[i] + str(j)] = EE_calc[EE_dis_single[i]].astype(float) \
                * proxy.loc[EE_dis_single[i],(EE_to_CVX_dis[ind],my_list[ind])].astype(float)  
            print(proxy.loc[EE_dis_single[i],(EE_to_CVX_dis[ind],my_list[ind])])
    



#%%       
for i in range(len(my_list)):
    EE = EE.rename(columns = {my_list[i]:EE_to_CVX_dis[i]})            
        
#%%
# EE = EE[Gi.columns.to_list()]
#%%
with pd.ExcelWriter(r'check_dis_E_2013.xlsx') as writer:
    EE.to_excel(writer)